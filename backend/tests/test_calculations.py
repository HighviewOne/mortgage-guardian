import pytest
from app.services.calculations import CalculationService
from app.schemas.mortgage import RiskLevel


class TestCalculationService:
    """Tests for CalculationService."""

    def test_calculate_monthly_payment(self):
        """Test standard amortization calculation."""
        # $300,000 loan at 6% for 30 years
        payment = CalculationService.calculate_monthly_payment(300000, 6.0, 360)
        assert round(payment, 2) == 1798.65

    def test_calculate_monthly_payment_zero_rate(self):
        """Test payment calculation with zero interest."""
        payment = CalculationService.calculate_monthly_payment(120000, 0, 360)
        assert round(payment, 2) == 333.33

    def test_calculate_monthly_payment_short_term(self):
        """Test payment calculation for short-term loan."""
        # $50,000 loan at 5% for 5 years
        payment = CalculationService.calculate_monthly_payment(50000, 5.0, 60)
        assert round(payment, 2) == 943.56

    def test_calculate_total_interest(self):
        """Test total interest calculation."""
        total = CalculationService.calculate_total_interest(300000, 1798.65, 360)
        assert round(total, 2) == 347514.00

    def test_calculate_dti_ratio(self):
        """Test debt-to-income ratio calculation."""
        dti = CalculationService.calculate_dti_ratio(2000, 1500, 7000)
        assert round(dti, 1) == 50.0

    def test_calculate_dti_ratio_zero_income(self):
        """Test DTI with zero income returns 100%."""
        dti = CalculationService.calculate_dti_ratio(2000, 1500, 0)
        assert dti == 100.0

    def test_calculate_ltv_ratio(self):
        """Test loan-to-value ratio calculation."""
        ltv = CalculationService.calculate_ltv_ratio(275000, 350000)
        assert round(ltv, 1) == 78.6

    def test_calculate_ltv_ratio_underwater(self):
        """Test LTV when underwater."""
        ltv = CalculationService.calculate_ltv_ratio(400000, 350000)
        assert round(ltv, 1) == 114.3

    def test_risk_level_low(self):
        """Test LOW risk level calculation."""
        risk = CalculationService.calculate_risk_level(0, 30)
        assert risk == RiskLevel.LOW

    def test_risk_level_medium_payments(self):
        """Test MEDIUM risk level from missed payments."""
        risk = CalculationService.calculate_risk_level(1, 30)
        assert risk == RiskLevel.MEDIUM

    def test_risk_level_medium_dti(self):
        """Test MEDIUM risk level from high DTI."""
        risk = CalculationService.calculate_risk_level(0, 40)
        assert risk == RiskLevel.MEDIUM

    def test_risk_level_high_payments(self):
        """Test HIGH risk level from missed payments."""
        risk = CalculationService.calculate_risk_level(3, 30)
        assert risk == RiskLevel.HIGH

    def test_risk_level_high_dti(self):
        """Test HIGH risk level from high DTI."""
        risk = CalculationService.calculate_risk_level(0, 45)
        assert risk == RiskLevel.HIGH

    def test_risk_level_critical_payments(self):
        """Test CRITICAL risk level from missed payments."""
        risk = CalculationService.calculate_risk_level(6, 30)
        assert risk == RiskLevel.CRITICAL

    def test_risk_level_critical_dti(self):
        """Test CRITICAL risk level from high DTI."""
        risk = CalculationService.calculate_risk_level(0, 55)
        assert risk == RiskLevel.CRITICAL

    def test_calculate_arrears(self):
        """Test arrears calculation."""
        arrears = CalculationService.calculate_arrears(1896.20, 2)
        assert round(arrears, 2) == 3792.40

    def test_calculate_late_fees(self):
        """Test late fees estimation."""
        fees = CalculationService.calculate_late_fees(1896.20, 2)
        # 5% per missed payment
        assert round(fees, 2) == 189.62


class TestPaymentCalculationEndpoint:
    """Tests for payment calculation API endpoint."""

    def test_calculate_payment_endpoint(self, client):
        """Test the calculate payment endpoint."""
        response = client.post(
            "/api/v1/calculate/payment",
            json={
                "principal": 275000,
                "annual_rate": 6.5,
                "term_months": 324,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "monthly_payment" in data
        assert "total_interest" in data
        assert "total_cost" in data
        assert data["monthly_payment"] > 0

    def test_calculate_payment_validation_error(self, client):
        """Test validation error for invalid input."""
        response = client.post(
            "/api/v1/calculate/payment",
            json={
                "principal": -1000,
                "annual_rate": 6.5,
                "term_months": 324,
            },
        )
        assert response.status_code == 422
