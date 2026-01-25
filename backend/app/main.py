from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routers.mortgages import router as mortgages_router
from app.routers.calculations import router as calculations_router
from app.schemas.mortgage import HealthResponse

app = FastAPI(
    title="Mortgage Guardian API",
    description="API for tracking mortgage deadlines, calculating modified payments, and providing guidance on avoiding foreclosure.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://mortgage-guardian-mocha.vercel.app",
        "https://mortgage-guardian-o2o3.onrender.com",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(mortgages_router)
app.include_router(calculations_router)


@app.on_event("startup")
def on_startup():
    """Initialize database on startup."""
    init_db()


@app.get("/health", response_model=HealthResponse, tags=["health"])
def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0",
    )


@app.get("/", tags=["health"])
def root():
    """Root endpoint redirects to docs."""
    return {
        "message": "Mortgage Guardian API",
        "docs": "/docs",
        "health": "/health",
    }
