from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.mortgage import Mortgage
from app.schemas.mortgage import (
    MortgageCreate,
    MortgageUpdate,
    MortgageResponse,
    PaymentDashboard,
    ModificationScenario,
    DeadlineInfo,
    Warning,
    GuidanceResponse,
)
from app.services.calculations import CalculationService
from app.services.guidance import GuidanceService

router = APIRouter(prefix="/api/v1/mortgages", tags=["mortgages"])


def get_mortgage_or_404(mortgage_id: int, db: Session) -> Mortgage:
    """Helper to get mortgage or raise 404."""
    mortgage = db.query(Mortgage).filter(Mortgage.id == mortgage_id).first()
    if not mortgage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mortgage not found",
        )
    return mortgage


@router.get("", response_model=List[MortgageResponse])
def list_mortgages(db: Session = Depends(get_db)):
    """List all mortgages."""
    return db.query(Mortgage).all()


@router.post("", response_model=MortgageResponse, status_code=status.HTTP_201_CREATED)
def create_mortgage(mortgage: MortgageCreate, db: Session = Depends(get_db)):
    """Create a new mortgage to track."""
    db_mortgage = Mortgage(**mortgage.model_dump())
    db.add(db_mortgage)
    db.commit()
    db.refresh(db_mortgage)
    return db_mortgage


@router.get("/{mortgage_id}", response_model=MortgageResponse)
def get_mortgage(mortgage_id: int, db: Session = Depends(get_db)):
    """Get mortgage details."""
    return get_mortgage_or_404(mortgage_id, db)


@router.put("/{mortgage_id}", response_model=MortgageResponse)
def update_mortgage(
    mortgage_id: int, mortgage_update: MortgageUpdate, db: Session = Depends(get_db)
):
    """Update an existing mortgage."""
    db_mortgage = get_mortgage_or_404(mortgage_id, db)

    update_data = mortgage_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_mortgage, field, value)

    db.commit()
    db.refresh(db_mortgage)
    return db_mortgage


@router.delete("/{mortgage_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mortgage(mortgage_id: int, db: Session = Depends(get_db)):
    """Delete a mortgage."""
    db_mortgage = get_mortgage_or_404(mortgage_id, db)
    db.delete(db_mortgage)
    db.commit()
    return None


@router.get("/{mortgage_id}/dashboard", response_model=PaymentDashboard)
def get_payment_dashboard(mortgage_id: int, db: Session = Depends(get_db)):
    """Get payment dashboard for a mortgage."""
    mortgage = get_mortgage_or_404(mortgage_id, db)
    return CalculationService.get_payment_dashboard(mortgage)


@router.get("/{mortgage_id}/scenarios", response_model=List[ModificationScenario])
def get_modification_scenarios(mortgage_id: int, db: Session = Depends(get_db)):
    """Get loan modification scenarios."""
    mortgage = get_mortgage_or_404(mortgage_id, db)
    return CalculationService.get_modification_scenarios(mortgage)


@router.get("/{mortgage_id}/deadlines", response_model=DeadlineInfo)
def get_deadlines(mortgage_id: int, db: Session = Depends(get_db)):
    """Get foreclosure deadlines and timeline."""
    mortgage = get_mortgage_or_404(mortgage_id, db)
    return GuidanceService.get_deadline_info(mortgage)


@router.get("/{mortgage_id}/warnings", response_model=List[Warning])
def get_warnings(mortgage_id: int, db: Session = Depends(get_db)):
    """Get active warnings for a mortgage."""
    mortgage = get_mortgage_or_404(mortgage_id, db)
    return GuidanceService.get_warnings(mortgage)


@router.get("/{mortgage_id}/guidance", response_model=GuidanceResponse)
def get_guidance(mortgage_id: int, db: Session = Depends(get_db)):
    """Get step-by-step guidance for avoiding foreclosure."""
    mortgage = get_mortgage_or_404(mortgage_id, db)
    return GuidanceService.get_guidance(mortgage)
