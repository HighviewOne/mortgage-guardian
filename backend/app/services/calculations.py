from datetime import date, timedelta
from typing import List, Optional
from app.models.mortgage import Mortgage
from app.schemas.mortgage import (
    PaymentDashboard,
    ModificationScenario,
    RiskLevel,
    ScenarioType,
)


class CalculationService:
    """Service for mortgage payment and risk calculations."""

    LATE_FEE_PERCENTAGE = 0.05  # 5% of monthly payment

    @staticmethod
    def calculate_monthly_payment(
        principal: float, annual_rate: float, term_months: int
    ) -> float:
        """
        Calculate monthly payment using standard amortization formula.
        M = P × [r(1+r)^n] / [(1+r)^n - 1]
        """
        if annual_rate == 0:
            return principal / term_months

        monthly_rate = annual_rate / 100 / 12
        numerator = monthly_rate * ((1 + monthly_rate) ** term_months)
        denominator = ((1 + monthly_rate) ** term_months) - 1
        return principal * (numerator / denominator)

    @staticmethod
    def calculate_total_interest(
        principal: float, monthly_payment: float, term_months: int
    ) -> float:
        """Calculate total interest over the life of the loan."""
        total_paid = monthly_payment * term_months
        return total_paid - principal

    @staticmethod
    def calculate_dti_ratio(
        monthly_payment: float, monthly_expenses: float, monthly_income: float
    ) -> float:
        """Calculate debt-to-income ratio."""
        if monthly_income <= 0:
            return 100.0
        return ((monthly_payment + monthly_expenses) / monthly_income) * 100

    @staticmethod
    def calculate_ltv_ratio(current_balance: float, property_value: float) -> float:
        """Calculate loan-to-value ratio."""
        if property_value <= 0:
            return 100.0
        return (current_balance / property_value) * 100

    @classmethod
    def calculate_risk_level(
        cls, missed_payments: int, dti_ratio: float
    ) -> RiskLevel:
        """
        Calculate foreclosure risk level.
        LOW:      0 missed payments, DTI < 36%
        MEDIUM:   1-2 missed payments OR DTI 36-43%
        HIGH:     3-5 missed payments OR DTI 43-50%
        CRITICAL: 6+ missed payments OR DTI > 50%
        """
        if missed_payments >= 6 or dti_ratio > 50:
            return RiskLevel.CRITICAL
        if missed_payments >= 3 or dti_ratio > 43:
            return RiskLevel.HIGH
        if missed_payments >= 1 or dti_ratio >= 36:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    @classmethod
    def calculate_days_past_due(
        cls, last_payment_date: Optional[date], missed_payments: int
    ) -> int:
        """Calculate days past due based on last payment and missed payments."""
        if missed_payments == 0:
            return 0

        if last_payment_date:
            # Assume monthly payments, so each missed payment is ~30 days
            days_since_last = (date.today() - last_payment_date).days
            return max(0, days_since_last - 30)  # Subtract grace period
        else:
            # No payment date, estimate based on missed payments
            return missed_payments * 30

    @classmethod
    def calculate_arrears(cls, monthly_payment: float, missed_payments: int) -> float:
        """Calculate total amount in arrears."""
        return monthly_payment * missed_payments

    @classmethod
    def calculate_late_fees(
        cls, monthly_payment: float, missed_payments: int
    ) -> float:
        """Estimate late fees accrued."""
        return monthly_payment * cls.LATE_FEE_PERCENTAGE * missed_payments

    @classmethod
    def get_next_payment_due(cls, last_payment_date: Optional[date]) -> date:
        """Calculate next payment due date."""
        if last_payment_date:
            # Assume monthly payments on the same day
            next_due = last_payment_date + timedelta(days=30)
            while next_due < date.today():
                next_due += timedelta(days=30)
            return next_due
        else:
            # No payment history, assume due on 1st of next month
            today = date.today()
            if today.day == 1:
                return today
            if today.month == 12:
                return date(today.year + 1, 1, 1)
            return date(today.year, today.month + 1, 1)

    @classmethod
    def get_payment_dashboard(cls, mortgage: Mortgage) -> PaymentDashboard:
        """Generate complete payment dashboard for a mortgage."""
        dti_ratio = cls.calculate_dti_ratio(
            mortgage.monthly_payment,
            mortgage.monthly_expenses or 0,
            mortgage.monthly_income or 0,
        )

        ltv_ratio = None
        if mortgage.property_value and mortgage.property_value > 0:
            ltv_ratio = cls.calculate_ltv_ratio(
                mortgage.current_balance, mortgage.property_value
            )

        return PaymentDashboard(
            mortgage_id=mortgage.id,
            current_monthly_payment=round(mortgage.monthly_payment, 2),
            days_past_due=cls.calculate_days_past_due(
                mortgage.last_payment_date, mortgage.missed_payments
            ),
            total_arrears=round(
                cls.calculate_arrears(mortgage.monthly_payment, mortgage.missed_payments),
                2,
            ),
            late_fees_estimate=round(
                cls.calculate_late_fees(
                    mortgage.monthly_payment, mortgage.missed_payments
                ),
                2,
            ),
            risk_level=cls.calculate_risk_level(mortgage.missed_payments, dti_ratio),
            dti_ratio=round(dti_ratio, 1),
            next_payment_due=cls.get_next_payment_due(mortgage.last_payment_date),
            ltv_ratio=round(ltv_ratio, 1) if ltv_ratio else None,
        )

    @classmethod
    def get_modification_scenarios(
        cls, mortgage: Mortgage
    ) -> List[ModificationScenario]:
        """Generate loan modification scenarios."""
        scenarios = []
        monthly_income = mortgage.monthly_income or mortgage.monthly_payment * 4

        # Target: payment should be <= 31% of income for affordability
        target_payment = monthly_income * 0.31

        # Scenario 1: 1% Rate Reduction
        new_rate_1 = max(0.1, mortgage.interest_rate - 1)
        new_payment_1 = cls.calculate_monthly_payment(
            mortgage.current_balance, new_rate_1, mortgage.remaining_months
        )
        total_interest_1 = cls.calculate_total_interest(
            mortgage.current_balance, new_payment_1, mortgage.remaining_months
        )
        scenarios.append(
            ModificationScenario(
                scenario_type=ScenarioType.RATE_REDUCTION_1,
                description="1% Interest Rate Reduction",
                new_interest_rate=round(new_rate_1, 2),
                new_monthly_payment=round(new_payment_1, 2),
                payment_change=round(new_payment_1 - mortgage.monthly_payment, 2),
                new_term_months=mortgage.remaining_months,
                term_change_months=0,
                total_interest=round(total_interest_1, 2),
                total_cost=round(mortgage.current_balance + total_interest_1, 2),
                meets_affordability=new_payment_1 <= target_payment,
            )
        )

        # Scenario 2: 2% Rate Reduction
        new_rate_2 = max(0.1, mortgage.interest_rate - 2)
        new_payment_2 = cls.calculate_monthly_payment(
            mortgage.current_balance, new_rate_2, mortgage.remaining_months
        )
        total_interest_2 = cls.calculate_total_interest(
            mortgage.current_balance, new_payment_2, mortgage.remaining_months
        )
        scenarios.append(
            ModificationScenario(
                scenario_type=ScenarioType.RATE_REDUCTION_2,
                description="2% Interest Rate Reduction",
                new_interest_rate=round(new_rate_2, 2),
                new_monthly_payment=round(new_payment_2, 2),
                payment_change=round(new_payment_2 - mortgage.monthly_payment, 2),
                new_term_months=mortgage.remaining_months,
                term_change_months=0,
                total_interest=round(total_interest_2, 2),
                total_cost=round(mortgage.current_balance + total_interest_2, 2),
                meets_affordability=new_payment_2 <= target_payment,
            )
        )

        # Scenario 3: 10-Year Term Extension
        new_term_10 = mortgage.remaining_months + 120
        new_payment_10 = cls.calculate_monthly_payment(
            mortgage.current_balance, mortgage.interest_rate, new_term_10
        )
        total_interest_10 = cls.calculate_total_interest(
            mortgage.current_balance, new_payment_10, new_term_10
        )
        scenarios.append(
            ModificationScenario(
                scenario_type=ScenarioType.TERM_EXTENSION_10,
                description="10-Year Term Extension",
                new_interest_rate=mortgage.interest_rate,
                new_monthly_payment=round(new_payment_10, 2),
                payment_change=round(new_payment_10 - mortgage.monthly_payment, 2),
                new_term_months=new_term_10,
                term_change_months=120,
                total_interest=round(total_interest_10, 2),
                total_cost=round(mortgage.current_balance + total_interest_10, 2),
                meets_affordability=new_payment_10 <= target_payment,
            )
        )

        # Scenario 4: 20-Year Term Extension
        new_term_20 = mortgage.remaining_months + 240
        new_payment_20 = cls.calculate_monthly_payment(
            mortgage.current_balance, mortgage.interest_rate, new_term_20
        )
        total_interest_20 = cls.calculate_total_interest(
            mortgage.current_balance, new_payment_20, new_term_20
        )
        scenarios.append(
            ModificationScenario(
                scenario_type=ScenarioType.TERM_EXTENSION_20,
                description="20-Year Term Extension",
                new_interest_rate=mortgage.interest_rate,
                new_monthly_payment=round(new_payment_20, 2),
                payment_change=round(new_payment_20 - mortgage.monthly_payment, 2),
                new_term_months=new_term_20,
                term_change_months=240,
                total_interest=round(total_interest_20, 2),
                total_cost=round(mortgage.current_balance + total_interest_20, 2),
                meets_affordability=new_payment_20 <= target_payment,
            )
        )

        # Scenario 5: Principal Forbearance (10% deferred)
        forbearance_amount = mortgage.current_balance * 0.10
        reduced_principal = mortgage.current_balance - forbearance_amount
        new_payment_forb = cls.calculate_monthly_payment(
            reduced_principal, mortgage.interest_rate, mortgage.remaining_months
        )
        total_interest_forb = cls.calculate_total_interest(
            reduced_principal, new_payment_forb, mortgage.remaining_months
        )
        scenarios.append(
            ModificationScenario(
                scenario_type=ScenarioType.PRINCIPAL_FORBEARANCE,
                description="10% Principal Forbearance (balloon at end)",
                new_interest_rate=mortgage.interest_rate,
                new_monthly_payment=round(new_payment_forb, 2),
                payment_change=round(new_payment_forb - mortgage.monthly_payment, 2),
                new_term_months=mortgage.remaining_months,
                term_change_months=0,
                total_interest=round(total_interest_forb, 2),
                total_cost=round(
                    reduced_principal + total_interest_forb + forbearance_amount, 2
                ),
                meets_affordability=new_payment_forb <= target_payment,
            )
        )

        return scenarios
