from datetime import date, datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ForeclosureType(str, Enum):
    JUDICIAL = "JUDICIAL"
    NON_JUDICIAL = "NON_JUDICIAL"
    HYBRID = "HYBRID"


class ForeclosureStage(str, Enum):
    CURRENT = "CURRENT"
    GRACE_PERIOD = "GRACE_PERIOD"
    LATE = "LATE"
    DEFAULT = "DEFAULT"
    PRE_FORECLOSURE = "PRE_FORECLOSURE"
    FORECLOSURE = "FORECLOSURE"
    AUCTION = "AUCTION"


class MilestoneStatus(str, Enum):
    PASSED = "PASSED"
    CURRENT = "CURRENT"
    UPCOMING = "UPCOMING"


class WarningType(str, Enum):
    PAYMENT_DUE = "PAYMENT_DUE"
    LATE_NOTICE = "LATE_NOTICE"
    DEFAULT_WARNING = "DEFAULT_WARNING"
    PRE_FORECLOSURE = "PRE_FORECLOSURE"
    FORECLOSURE_NOTICE = "FORECLOSURE_NOTICE"
    AUCTION_IMMINENT = "AUCTION_IMMINENT"
    HIGH_DTI = "HIGH_DTI"
    UNDERWATER = "UNDERWATER"


class WarningSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    URGENT = "URGENT"
    CRITICAL = "CRITICAL"


class ScenarioType(str, Enum):
    RATE_REDUCTION_1 = "RATE_REDUCTION_1"
    RATE_REDUCTION_2 = "RATE_REDUCTION_2"
    TERM_EXTENSION_10 = "TERM_EXTENSION_10"
    TERM_EXTENSION_20 = "TERM_EXTENSION_20"
    PRINCIPAL_FORBEARANCE = "PRINCIPAL_FORBEARANCE"
    COMBINATION = "COMBINATION"


class Priority(str, Enum):
    IMMEDIATE = "IMMEDIATE"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ResourceType(str, Enum):
    GOVERNMENT = "GOVERNMENT"
    NONPROFIT = "NONPROFIT"
    LEGAL = "LEGAL"
    FINANCIAL = "FINANCIAL"


# Request/Response Schemas
class MortgageCreate(BaseModel):
    loan_amount: float = Field(..., gt=0, le=10000000)
    current_balance: float = Field(..., gt=0)
    interest_rate: float = Field(..., ge=0.1, le=25)
    loan_term_months: int = Field(..., ge=12, le=480)
    remaining_months: int = Field(..., ge=1)
    monthly_payment: float = Field(..., gt=0)
    loan_start_date: date
    last_payment_date: Optional[date] = None
    missed_payments: int = Field(default=0, ge=0)
    monthly_income: Optional[float] = Field(default=None, ge=0)
    monthly_expenses: float = Field(default=0, ge=0)
    property_value: Optional[float] = Field(default=None, ge=0)
    state: str = Field(..., min_length=2, max_length=2)
    property_address: Optional[str] = None

    @field_validator("state")
    @classmethod
    def validate_state(cls, v: str) -> str:
        return v.upper()

    @field_validator("current_balance")
    @classmethod
    def validate_current_balance(cls, v: float, info) -> float:
        if "loan_amount" in info.data and v > info.data["loan_amount"]:
            raise ValueError("current_balance cannot exceed loan_amount")
        return v


class MortgageUpdate(BaseModel):
    current_balance: Optional[float] = Field(default=None, gt=0)
    interest_rate: Optional[float] = Field(default=None, ge=0.1, le=25)
    remaining_months: Optional[int] = Field(default=None, ge=1)
    monthly_payment: Optional[float] = Field(default=None, gt=0)
    last_payment_date: Optional[date] = None
    missed_payments: Optional[int] = Field(default=None, ge=0)
    monthly_income: Optional[float] = Field(default=None, ge=0)
    monthly_expenses: Optional[float] = Field(default=None, ge=0)
    property_value: Optional[float] = Field(default=None, ge=0)
    property_address: Optional[str] = None


class MortgageResponse(MortgageCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PaymentDashboard(BaseModel):
    mortgage_id: int
    current_monthly_payment: float
    days_past_due: int
    total_arrears: float
    late_fees_estimate: float
    risk_level: RiskLevel
    dti_ratio: float
    next_payment_due: Optional[date] = None
    ltv_ratio: Optional[float] = None


class ModificationScenario(BaseModel):
    scenario_type: ScenarioType
    description: str
    new_interest_rate: Optional[float] = None
    new_monthly_payment: float
    payment_change: float
    new_term_months: int
    term_change_months: int = 0
    total_interest: float
    total_cost: float
    meets_affordability: bool


class Milestone(BaseModel):
    stage: str
    days_from_first_missed: int
    estimated_date: Optional[date] = None
    description: str
    status: MilestoneStatus


class DeadlineInfo(BaseModel):
    state: str
    state_name: str
    foreclosure_type: ForeclosureType
    timeline_days_min: int
    timeline_days_max: int
    current_stage: ForeclosureStage
    days_until_next_stage: Optional[int] = None
    milestones: List[Milestone]


class Warning(BaseModel):
    type: WarningType
    severity: WarningSeverity
    title: str
    message: str
    action_required: bool = False
    deadline: Optional[date] = None


class GuidanceStep(BaseModel):
    step_number: int
    title: str
    description: str
    priority: Priority
    deadline_days: Optional[int] = None
    phone_number: Optional[str] = None
    url: Optional[str] = None


class Resource(BaseModel):
    name: str
    type: ResourceType
    description: str
    phone: Optional[str] = None
    url: Optional[str] = None
    state_specific: bool = False


class GuidanceResponse(BaseModel):
    risk_level: RiskLevel
    summary: str
    immediate_steps: List[GuidanceStep]
    resources: List[Resource]
    lender_script: Optional[str] = None


class PaymentCalculationRequest(BaseModel):
    principal: float = Field(..., gt=0)
    annual_rate: float = Field(..., ge=0.1, le=25)
    term_months: int = Field(..., ge=1)


class PaymentCalculationResponse(BaseModel):
    monthly_payment: float
    total_interest: float
    total_cost: float


class StateInfo(BaseModel):
    code: str
    name: str
    foreclosure_type: ForeclosureType
    timeline_days_min: int
    timeline_days_max: int
    notes: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str = "1.0.0"
