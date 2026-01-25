from datetime import date, timedelta
from typing import List
from app.models.mortgage import Mortgage
from app.schemas.mortgage import (
    GuidanceResponse,
    GuidanceStep,
    Resource,
    Warning,
    DeadlineInfo,
    Milestone,
    RiskLevel,
    WarningType,
    WarningSeverity,
    Priority,
    ResourceType,
    ForeclosureStage,
    MilestoneStatus,
)
from app.services.calculations import CalculationService
from app.services.states import StateService


class GuidanceService:
    """Service for generating foreclosure prevention guidance."""

    @classmethod
    def get_warnings(cls, mortgage: Mortgage) -> List[Warning]:
        """Generate warnings based on mortgage status."""
        warnings = []
        dashboard = CalculationService.get_payment_dashboard(mortgage)

        # Payment due warning
        next_due = CalculationService.get_next_payment_due(mortgage.last_payment_date)
        days_until_due = (next_due - date.today()).days
        if 0 < days_until_due <= 7:
            warnings.append(
                Warning(
                    type=WarningType.PAYMENT_DUE,
                    severity=WarningSeverity.INFO,
                    title="Payment Due Soon",
                    message=f"Your next payment of ${mortgage.monthly_payment:,.2f} is due in {days_until_due} days.",
                    action_required=True,
                    deadline=next_due,
                )
            )

        # Late notice (15+ days)
        if 15 <= dashboard.days_past_due < 30:
            warnings.append(
                Warning(
                    type=WarningType.LATE_NOTICE,
                    severity=WarningSeverity.WARNING,
                    title="Payment is Late",
                    message=(
                        f"Your payment is {dashboard.days_past_due} days late. "
                        "Late fees are accruing. Contact your lender to make arrangements."
                    ),
                    action_required=True,
                )
            )

        # Default warning (30+ days)
        if 30 <= dashboard.days_past_due < 90:
            warnings.append(
                Warning(
                    type=WarningType.DEFAULT_WARNING,
                    severity=WarningSeverity.URGENT,
                    title="Default Warning",
                    message=(
                        f"You are {dashboard.days_past_due} days past due. "
                        "Your loan may be reported to credit bureaus. "
                        "Contact your lender immediately to discuss options."
                    ),
                    action_required=True,
                )
            )

        # Pre-foreclosure (90+ days)
        if 90 <= dashboard.days_past_due < 120:
            warnings.append(
                Warning(
                    type=WarningType.PRE_FORECLOSURE,
                    severity=WarningSeverity.CRITICAL,
                    title="Pre-Foreclosure Stage",
                    message=(
                        "You are in the pre-foreclosure stage. Your lender may file "
                        "a Notice of Default. Time is critical - contact a HUD-approved "
                        "housing counselor immediately."
                    ),
                    action_required=True,
                )
            )

        # Foreclosure notice (120+ days)
        if dashboard.days_past_due >= 120:
            warnings.append(
                Warning(
                    type=WarningType.FORECLOSURE_NOTICE,
                    severity=WarningSeverity.CRITICAL,
                    title="Foreclosure Process May Begin",
                    message=(
                        "Your lender may initiate formal foreclosure proceedings. "
                        "Seek legal assistance immediately. You may still have options "
                        "including loan modification, short sale, or deed in lieu."
                    ),
                    action_required=True,
                )
            )

        # High DTI warning
        if dashboard.dti_ratio > 43:
            warnings.append(
                Warning(
                    type=WarningType.HIGH_DTI,
                    severity=WarningSeverity.WARNING,
                    title="High Debt-to-Income Ratio",
                    message=(
                        f"Your debt-to-income ratio is {dashboard.dti_ratio:.1f}%. "
                        "This exceeds the recommended 43% maximum. Consider ways to "
                        "reduce expenses or increase income."
                    ),
                    action_required=False,
                )
            )

        # Underwater warning (LTV > 100%)
        if dashboard.ltv_ratio and dashboard.ltv_ratio > 100:
            warnings.append(
                Warning(
                    type=WarningType.UNDERWATER,
                    severity=WarningSeverity.WARNING,
                    title="Underwater Mortgage",
                    message=(
                        f"Your loan-to-value ratio is {dashboard.ltv_ratio:.1f}%. "
                        "You owe more than your home is worth. This may affect your "
                        "refinancing options but does not prevent loan modification."
                    ),
                    action_required=False,
                )
            )

        return warnings

    @classmethod
    def get_deadline_info(cls, mortgage: Mortgage) -> DeadlineInfo:
        """Get foreclosure timeline and deadlines."""
        state_info = StateService.get_state(mortgage.state)
        if not state_info:
            # Default to judicial if state not found
            state_info = StateService.get_state("NY")

        # Determine current stage
        days_past_due = CalculationService.calculate_days_past_due(
            mortgage.last_payment_date, mortgage.missed_payments
        )

        if days_past_due == 0:
            current_stage = ForeclosureStage.CURRENT
        elif days_past_due <= 15:
            current_stage = ForeclosureStage.GRACE_PERIOD
        elif days_past_due <= 30:
            current_stage = ForeclosureStage.LATE
        elif days_past_due <= 90:
            current_stage = ForeclosureStage.DEFAULT
        elif days_past_due <= 120:
            current_stage = ForeclosureStage.PRE_FORECLOSURE
        elif days_past_due <= state_info.timeline_days_max:
            current_stage = ForeclosureStage.FORECLOSURE
        else:
            current_stage = ForeclosureStage.AUCTION

        # Calculate first missed payment date
        if mortgage.last_payment_date:
            first_missed = mortgage.last_payment_date + timedelta(days=30)
        else:
            first_missed = date.today() - timedelta(days=days_past_due)

        # Build milestones
        milestones = [
            Milestone(
                stage="Grace Period Ends",
                days_from_first_missed=15,
                estimated_date=first_missed + timedelta(days=15),
                description="Late fees begin to accrue",
                status=cls._get_milestone_status(days_past_due, 15),
            ),
            Milestone(
                stage="Reported to Credit Bureau",
                days_from_first_missed=30,
                estimated_date=first_missed + timedelta(days=30),
                description="Delinquency reported, credit score impact",
                status=cls._get_milestone_status(days_past_due, 30),
            ),
            Milestone(
                stage="Notice of Default",
                days_from_first_missed=90,
                estimated_date=first_missed + timedelta(days=90),
                description="Formal notice filed by lender",
                status=cls._get_milestone_status(days_past_due, 90),
            ),
            Milestone(
                stage="Notice of Sale",
                days_from_first_missed=state_info.timeline_days_min,
                estimated_date=first_missed + timedelta(days=state_info.timeline_days_min),
                description="Property scheduled for foreclosure sale",
                status=cls._get_milestone_status(days_past_due, state_info.timeline_days_min),
            ),
            Milestone(
                stage="Foreclosure Sale",
                days_from_first_missed=state_info.timeline_days_max,
                estimated_date=first_missed + timedelta(days=state_info.timeline_days_max),
                description="Property sold at auction",
                status=cls._get_milestone_status(days_past_due, state_info.timeline_days_max),
            ),
        ]

        # Calculate days until next stage
        stage_thresholds = [15, 30, 90, state_info.timeline_days_min, state_info.timeline_days_max]
        days_until_next = None
        for threshold in stage_thresholds:
            if days_past_due < threshold:
                days_until_next = threshold - days_past_due
                break

        return DeadlineInfo(
            state=state_info.code,
            state_name=state_info.name,
            foreclosure_type=state_info.foreclosure_type,
            timeline_days_min=state_info.timeline_days_min,
            timeline_days_max=state_info.timeline_days_max,
            current_stage=current_stage,
            days_until_next_stage=days_until_next,
            milestones=milestones,
        )

    @staticmethod
    def _get_milestone_status(days_past_due: int, milestone_days: int) -> MilestoneStatus:
        """Determine milestone status based on days past due."""
        if days_past_due > milestone_days:
            return MilestoneStatus.PASSED
        elif days_past_due >= milestone_days - 7:
            return MilestoneStatus.CURRENT
        else:
            return MilestoneStatus.UPCOMING

    @classmethod
    def get_guidance(cls, mortgage: Mortgage) -> GuidanceResponse:
        """Generate personalized guidance based on mortgage status."""
        dashboard = CalculationService.get_payment_dashboard(mortgage)
        risk_level = dashboard.risk_level

        # Generate summary
        summary = cls._get_summary(risk_level, dashboard.days_past_due)

        # Generate steps based on risk level
        steps = cls._get_steps(risk_level, mortgage)

        # Get resources
        resources = cls._get_resources(mortgage.state)

        # Generate lender script
        lender_script = cls._get_lender_script(mortgage, dashboard)

        return GuidanceResponse(
            risk_level=risk_level,
            summary=summary,
            immediate_steps=steps,
            resources=resources,
            lender_script=lender_script,
        )

    @staticmethod
    def _get_summary(risk_level: RiskLevel, days_past_due: int) -> str:
        """Generate summary based on risk level."""
        summaries = {
            RiskLevel.LOW: (
                "Your mortgage is in good standing. Continue making payments on time "
                "to maintain your excellent status."
            ),
            RiskLevel.MEDIUM: (
                "Your mortgage requires attention. You may be falling behind on payments "
                "or have a high debt-to-income ratio. Take action now to prevent escalation."
            ),
            RiskLevel.HIGH: (
                f"Your mortgage is at significant risk. You are {days_past_due} days "
                "behind on payments. Immediate action is required to avoid foreclosure "
                "proceedings."
            ),
            RiskLevel.CRITICAL: (
                f"URGENT: Your mortgage is in critical condition. At {days_past_due} days "
                "past due, foreclosure proceedings may begin soon. Contact your lender "
                "and a housing counselor immediately."
            ),
        }
        return summaries.get(risk_level, summaries[RiskLevel.MEDIUM])

    @classmethod
    def _get_steps(cls, risk_level: RiskLevel, mortgage: Mortgage) -> List[GuidanceStep]:
        """Generate action steps based on risk level."""
        steps = []
        step_num = 1

        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            steps.append(
                GuidanceStep(
                    step_number=step_num,
                    title="Contact Your Lender Immediately",
                    description=(
                        "Call your lender's loss mitigation department. Explain your "
                        "situation and ask about forbearance, loan modification, or "
                        "repayment plan options. Document the date, time, and name of "
                        "who you speak with."
                    ),
                    priority=Priority.IMMEDIATE,
                    deadline_days=1,
                )
            )
            step_num += 1

            steps.append(
                GuidanceStep(
                    step_number=step_num,
                    title="Contact a HUD-Approved Housing Counselor",
                    description=(
                        "Get free professional help from a HUD-approved housing "
                        "counseling agency. They can review your situation, help you "
                        "understand your options, and even negotiate with your lender "
                        "on your behalf."
                    ),
                    priority=Priority.IMMEDIATE,
                    deadline_days=3,
                    phone_number="1-800-569-4287",
                    url="https://www.hud.gov/counseling",
                )
            )
            step_num += 1

        if risk_level == RiskLevel.CRITICAL:
            steps.append(
                GuidanceStep(
                    step_number=step_num,
                    title="Seek Legal Assistance",
                    description=(
                        "Consult with a foreclosure prevention attorney. Many offer "
                        "free consultations. Legal aid organizations may provide free "
                        "representation if you qualify."
                    ),
                    priority=Priority.IMMEDIATE,
                    deadline_days=7,
                    url="https://www.lawhelp.org",
                )
            )
            step_num += 1

        steps.append(
            GuidanceStep(
                step_number=step_num,
                title="Gather Financial Documents",
                description=(
                    "Collect: recent pay stubs, tax returns (2 years), bank statements "
                    "(2-3 months), monthly expense list, hardship letter explaining your "
                    "situation. These are needed for loss mitigation applications."
                ),
                priority=Priority.HIGH if risk_level != RiskLevel.LOW else Priority.MEDIUM,
                deadline_days=7,
            )
        )
        step_num += 1

        steps.append(
            GuidanceStep(
                step_number=step_num,
                title="Submit Loss Mitigation Application",
                description=(
                    "Complete and submit your lender's loss mitigation application. "
                    "Include all required documents. Send via certified mail and keep "
                    "copies of everything. Follow up to confirm receipt."
                ),
                priority=Priority.HIGH if risk_level != RiskLevel.LOW else Priority.MEDIUM,
                deadline_days=14,
            )
        )
        step_num += 1

        if risk_level in [RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL]:
            steps.append(
                GuidanceStep(
                    step_number=step_num,
                    title="Explore Income Options",
                    description=(
                        "Consider ways to increase income: overtime, second job, "
                        "renting a room, selling unused items. Even temporary income "
                        "increases can help you catch up on payments."
                    ),
                    priority=Priority.MEDIUM,
                )
            )
            step_num += 1

            steps.append(
                GuidanceStep(
                    step_number=step_num,
                    title="Review and Reduce Expenses",
                    description=(
                        "Create a detailed budget. Identify non-essential expenses "
                        "that can be temporarily reduced or eliminated. Prioritize "
                        "your mortgage payment above unsecured debts."
                    ),
                    priority=Priority.MEDIUM,
                )
            )
            step_num += 1

        steps.append(
            GuidanceStep(
                step_number=step_num,
                title="Check State Assistance Programs",
                description=(
                    f"Research assistance programs in {mortgage.state}. Many states "
                    "have Homeowner Assistance Funds from the American Rescue Plan "
                    "that can help with past-due mortgage payments."
                ),
                priority=Priority.HIGH,
                url="https://www.ncsha.org/homeowner-assistance-fund/",
            )
        )

        return steps

    @staticmethod
    def _get_resources(state: str) -> List[Resource]:
        """Get relevant resources for homeowner."""
        resources = [
            Resource(
                name="HUD Housing Counseling",
                type=ResourceType.GOVERNMENT,
                description="Free counseling from HUD-approved agencies",
                phone="1-800-569-4287",
                url="https://www.hud.gov/counseling",
                state_specific=False,
            ),
            Resource(
                name="Consumer Financial Protection Bureau",
                type=ResourceType.GOVERNMENT,
                description="Federal resources and complaint filing",
                phone="1-855-411-2372",
                url="https://www.consumerfinance.gov/housing/",
                state_specific=False,
            ),
            Resource(
                name="Homeowner Assistance Fund",
                type=ResourceType.GOVERNMENT,
                description="State programs funded by American Rescue Plan",
                url="https://www.ncsha.org/homeowner-assistance-fund/",
                state_specific=True,
            ),
            Resource(
                name="LawHelp.org",
                type=ResourceType.LEGAL,
                description="Find free legal aid in your area",
                url="https://www.lawhelp.org",
                state_specific=True,
            ),
            Resource(
                name="National Foundation for Credit Counseling",
                type=ResourceType.NONPROFIT,
                description="Non-profit credit and housing counseling",
                phone="1-800-388-2227",
                url="https://www.nfcc.org",
                state_specific=False,
            ),
            Resource(
                name="Making Home Affordable",
                type=ResourceType.GOVERNMENT,
                description="Information about federal mortgage assistance programs",
                url="https://www.makinghomeaffordable.gov",
                state_specific=False,
            ),
        ]
        return resources

    @staticmethod
    def _get_lender_script(mortgage: Mortgage, dashboard) -> str:
        """Generate a script for calling the lender."""
        return f"""SCRIPT FOR CALLING YOUR LENDER

Hello, my name is [YOUR NAME] and I'm calling about my mortgage account.

My account number is [ACCOUNT NUMBER].
The property address is {mortgage.property_address or '[YOUR ADDRESS]'}.

I'm experiencing financial hardship and I'm currently {dashboard.days_past_due} days behind on my payments. I'd like to speak with someone in your loss mitigation department about my options.

QUESTIONS TO ASK:
1. What loss mitigation options are available to me?
2. Can I qualify for a forbearance or repayment plan?
3. What documents do I need to submit for a loan modification?
4. Is there a deadline to submit my application?
5. Will you stop foreclosure proceedings while my application is reviewed?
6. Can I get this information in writing?

REMEMBER:
- Get the name and direct number of who you speak with
- Take detailed notes with date and time
- Ask for everything in writing
- Follow up in writing via certified mail
- Keep copies of all correspondence"""
