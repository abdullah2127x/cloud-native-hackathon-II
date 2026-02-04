# Backend - Todo Web App

FastAPI + SQLModel REST API with JWT authentication and PostgreSQL database.

## Quick Start

### Prerequisites
- Python 3.12+
- UV package manager

### Setup
```bash
# Install dependencies
uv sync

# Copy environment template
cp .env.example .env

# Run development server
uv run uvicorn src.main:app --reload --port 8000
```

Access API at http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Environment Variables
```env
DATABASE_URL=postgresql://user:password@host/database
BETTER_AUTH_URL=http://localhost:3000
CORS_ORIGINS=["http://localhost:3000"]
```

## Available Commands

```bash
uv sync                  # Install dependencies
uv run pytest            # Run tests
uv run pytest --cov=src  # Run tests with coverage
uv run uvicorn src.main:app --reload  # Dev server
```

## Features

- JWT authentication via Better Auth JWKS
- User-isolated task management (CRUD)
- Search, filter, and sort tasks
- Tag management
- Comprehensive error handling
- CORS support for multiple origins

## Project Structure

```
src/
├── main.py           # FastAPI app entry
├── config.py         # Environment configuration
├── auth/             # JWT verification
├── crud/             # Database operations
├── db/               # Database connection
├── models/           # SQLModel entities
├── routers/          # API endpoints
├── schemas/          # Request/response models
├── middleware/       # CORS, logging, error handling
└── exceptions/       # Custom exceptions
```

## API Endpoints

All endpoints require JWT authentication via `Authorization: Bearer <token>` header.

### Tasks
- `POST /api/todos` - Create task
- `GET /api/todos` - List user's tasks
- `GET /api/todos/{id}` - Get specific task
- `PATCH /api/todos/{id}` - Update task
- `DELETE /api/todos/{id}` - Delete task
- `POST /api/todos/{id}/toggle` - Toggle completion

### Health
- `GET /health` - Health check
- `GET /` - Root endpoint

Full API documentation: http://localhost:8000/docs

## Technology

- **Framework**: FastAPI
- **Language**: Python 3.12+
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Database**: PostgreSQL
- **Auth**: JWT verification via JWKS
- **Testing**: pytest + TestClient

## Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run specific test
uv run pytest tests/unit/test_task_crud.py
```

Target: 70%+ code coverage

## Deployment

For deployment instructions, see `DEPLOYMENT.md`

## Support

- See `CLAUDE.md` for development standards
- See root `README.md` for full project overview
- Frontend README: `../frontend/README.md`
