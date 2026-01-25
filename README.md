# Mortgage Guardian

A tool that helps homeowners track mortgage deadlines, calculate modified payments, and get step-by-step guidance on avoiding foreclosure.

## Problem Description

Millions of homeowners face foreclosure each year, often due to temporary financial hardships. Many don't understand their options or miss critical deadlines that could save their homes. This tool provides:

1. **Payment Tracking** - Monitor mortgage status, missed payments, and arrears
2. **Risk Assessment** - Calculate foreclosure risk based on payment history and debt-to-income ratio
3. **Modified Payment Scenarios** - Model different loan modification options (rate reduction, term extension, forbearance)
4. **Deadline Alerts** - State-specific foreclosure timeline warnings
5. **Step-by-Step Guidance** - Actionable steps to avoid foreclosure with resources

## AI-Assisted Development

This project was built using AI coding assistants as part of the AI Dev Tools Zoomcamp 2025.

### Tools Used
- **Claude Code** - Primary coding assistant for architecture, implementation, and testing
- **MCP Integration** - [Document MCP usage here]

### Development Workflow
1. Requirements gathering and specification with AI assistance
2. API contract (OpenAPI) designed with AI
3. Backend implementation with AI pair programming
4. Frontend development with AI assistance
5. Test generation and debugging with AI support

## Technologies & Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│    Frontend     │────▶│    Backend      │────▶│    Database     │
│    (React)      │     │    (FastAPI)    │     │ (SQLite/Postgres)│
│                 │◀────│                 │◀────│                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        └───────────────────────┴───────────────────────┘
                    Docker Compose
```

### Stack
- **Frontend**: React 18 + Vite + TypeScript
- **Backend**: Python 3.11 + FastAPI
- **Database**: SQLite (development) / PostgreSQL (production)
- **Containerization**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Deployment**: Render.com

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Run with Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd ProjectAttempt2

# Start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Local Development

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Testing

### Backend Tests
```bash
cd backend
pytest --cov=app tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Integration Tests
```bash
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## API Documentation

The OpenAPI specification is available at:
- **Interactive Docs**: http://localhost:8000/docs (Swagger UI)
- **OpenAPI JSON**: http://localhost:8000/openapi.json
- **Specification File**: [docs/openapi.yaml](docs/openapi.yaml)

## Deployment

The application is deployed on Render.com:
- **Live URL**: [To be added after deployment]

### Deploy Your Own
1. Fork this repository
2. Create a Render.com account
3. Connect your GitHub repository
4. Deploy using the `render.yaml` blueprint

## Project Structure

```
ProjectAttempt2/
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API client (centralized)
│   │   ├── hooks/         # Custom React hooks
│   │   └── types/         # TypeScript types
│   ├── public/
│   └── package.json
├── backend/               # FastAPI backend application
│   ├── app/
│   │   ├── main.py       # FastAPI application
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── routers/      # API routes
│   │   ├── services/     # Business logic
│   │   └── database.py   # Database configuration
│   ├── tests/
│   └── requirements.txt
├── docs/
│   └── openapi.yaml      # API specification
├── .github/
│   └── workflows/        # CI/CD pipelines
├── docker-compose.yml
├── Dockerfile.frontend
├── Dockerfile.backend
└── README.md
```

## License

MIT License - See [LICENSE](LICENSE) for details.
