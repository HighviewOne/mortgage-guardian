import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db


# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db():
    """Create test database tables for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create test client with database override."""
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture
def sample_mortgage_data():
    """Sample mortgage data for testing."""
    return {
        "loan_amount": 300000,
        "current_balance": 275000,
        "interest_rate": 6.5,
        "loan_term_months": 360,
        "remaining_months": 324,
        "monthly_payment": 1896.20,
        "loan_start_date": str(date.today() - timedelta(days=1080)),  # 3 years ago
        "last_payment_date": str(date.today() - timedelta(days=45)),
        "missed_payments": 2,
        "monthly_income": 6500,
        "monthly_expenses": 2000,
        "property_value": 350000,
        "state": "CA",
        "property_address": "123 Main St, Los Angeles, CA 90001",
    }


@pytest.fixture
def sample_mortgage_current():
    """Sample mortgage data for a current (non-delinquent) account."""
    return {
        "loan_amount": 250000,
        "current_balance": 240000,
        "interest_rate": 5.5,
        "loan_term_months": 360,
        "remaining_months": 348,
        "monthly_payment": 1419.47,
        "loan_start_date": str(date.today() - timedelta(days=365)),
        "last_payment_date": str(date.today() - timedelta(days=5)),
        "missed_payments": 0,
        "monthly_income": 9000,
        "monthly_expenses": 1000,
        "property_value": 300000,
        "state": "TX",
    }


@pytest.fixture
def sample_mortgage_critical():
    """Sample mortgage data for a critical situation."""
    return {
        "loan_amount": 400000,
        "current_balance": 380000,
        "interest_rate": 7.0,
        "loan_term_months": 360,
        "remaining_months": 300,
        "monthly_payment": 2661.21,
        "loan_start_date": str(date.today() - timedelta(days=1825)),
        "last_payment_date": str(date.today() - timedelta(days=180)),
        "missed_payments": 6,
        "monthly_income": 5000,
        "monthly_expenses": 2500,
        "property_value": 350000,
        "state": "FL",
    }
