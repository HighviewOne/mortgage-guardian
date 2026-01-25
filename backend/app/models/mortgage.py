from datetime import datetime, date
from sqlalchemy import Column, Integer, Float, String, Date, DateTime
from app.database import Base


class Mortgage(Base):
    __tablename__ = "mortgages"

    id = Column(Integer, primary_key=True, index=True)

    # Loan details
    loan_amount = Column(Float, nullable=False)
    current_balance = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    loan_term_months = Column(Integer, nullable=False)
    remaining_months = Column(Integer, nullable=False)
    monthly_payment = Column(Float, nullable=False)

    # Dates
    loan_start_date = Column(Date, nullable=False)
    last_payment_date = Column(Date, nullable=True)

    # Payment status
    missed_payments = Column(Integer, default=0)

    # Financial info
    monthly_income = Column(Float, nullable=True)
    monthly_expenses = Column(Float, default=0)
    property_value = Column(Float, nullable=True)

    # Location
    state = Column(String(2), nullable=False)
    property_address = Column(String(500), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
