from typing import List
from fastapi import APIRouter

from app.schemas.mortgage import (
    PaymentCalculationRequest,
    PaymentCalculationResponse,
    StateInfo,
)
from app.services.calculations import CalculationService
from app.services.states import StateService

router = APIRouter(prefix="/api/v1", tags=["calculations"])


@router.post("/calculate/payment", response_model=PaymentCalculationResponse)
def calculate_payment(request: PaymentCalculationRequest):
    """Calculate monthly payment for given loan parameters."""
    monthly_payment = CalculationService.calculate_monthly_payment(
        request.principal, request.annual_rate, request.term_months
    )
    total_interest = CalculationService.calculate_total_interest(
        request.principal, monthly_payment, request.term_months
    )

    return PaymentCalculationResponse(
        monthly_payment=round(monthly_payment, 2),
        total_interest=round(total_interest, 2),
        total_cost=round(request.principal + total_interest, 2),
    )


@router.get("/states", response_model=List[StateInfo])
def list_states():
    """List all states with foreclosure information."""
    return StateService.get_all_states()
