# Todo Web Application

A full-stack task management web app with user authentication, task CRUD operations, filtering, and search built with Next.js (frontend) and FastAPI (backend).

## Features

- **User Authentication**: Secure signup/signin with Better Auth using JWT tokens
- **Task Management**: Complete CRUD operations for tasks
  - Create tasks with title and description
  - View all your tasks in a clean interface
  - Edit task details
  - Mark tasks as complete/incomplete
  - Delete tasks with confirmation
- **User Isolation**: Each user sees only their own tasks (enforced at database level)
- **Responsive UI**: Mobile-friendly interface built with Tailwind CSS
- **Type Safety**: Full TypeScript support with runtime validation
- **Comprehensive Testing**: 70%+ test coverage with unit and integration tests

## Technology Stack

### Frontend
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Forms**: React Hook Form + Zod validation
- **Authentication**: Better Auth client
- **HTTP Client**: Axios with interceptors
- **Testing**: Jest + React Testing Library + MSW

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.13+
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Database**: PostgreSQL (Neon Serverless)
- **Authentication**: JWT verification via JWKS
- **Testing**: pytest + TestClient

## Prerequisites

- **Node.js**: 18+ (for frontend)
- **Python**: 3.13+ (for backend)
- **UV**: Python package manager ([Install UV](https://github.com/astral-sh/uv))
- **PostgreSQL**: Database (or use Neon Serverless)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd todo-in-memory-console-app
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies with UV
uv sync

# Create .env file
cp .env.example .env
```

Configure `backend/.env`:
```env
DATABASE_URL=postgresql://user:password@host:port/database
BETTER_AUTH_URL=http://localhost:3000
CORS_ORIGINS=["http://localhost:3000"]
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local
```

Configure `frontend/.env.local`:
```env
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000

# Database for Better Auth
DATABASE_URL=postgresql://user:password@host:port/database

# Better Auth secret (generate with: openssl rand -base64 32)
BETTER_AUTH_SECRET=your-secret-key-here
```

## Running the Application

### Start Backend Server

```bash
cd backend
uv run uvicorn src.main:app --reload --port 8000
```

Backend will be available at: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### Start Frontend Server

```bash
cd frontend
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## Usage Guide

### 1. Create an Account

1. Navigate to `http://localhost:3000`
2. Click "Sign Up" or go to `/sign-up`
3. Enter your name, email, and password
4. Submit the form

### 2. Sign In

1. Go to `/sign-in`
2. Enter your email and password
3. You'll be redirected to the dashboard

### 3. Create Tasks

1. On the dashboard, find the "Create New Task" form
2. Enter a task title (required, max 200 characters)
3. Optionally add a description (max 2000 characters)
4. Click "Create Task"
5. The task appears in your task list immediately

### 4. View Tasks

- All your tasks are displayed in the "Tasks" section
- Completed tasks show with a strikethrough and gray color
- Each task shows:
  - Title and description
  - Completion status (checkbox)
  - Created date (and updated date if modified)
  - Edit and Delete buttons

### 5. Edit Tasks

1. Click the "Edit" button on any task
2. A modal opens with the task details
3. Modify the title and/or description
4. Click "Save Changes" or "Cancel"

### 6. Toggle Completion

- Click the checkbox next to any task to toggle its completion status
- Visual feedback shows completed vs pending tasks

### 7. Delete Tasks

1. Click the "Delete" button on any task
2. Confirm the deletion in the browser dialog
3. Task is removed immediately

### 8. Sign Out

- Click "Sign Out" button in the navigation
- You'll be redirected to the sign-in page

## API Endpoints

### Authentication
- Handled by Better Auth at `/api/auth/*`

### Tasks
All endpoints require JWT authentication via `Authorization: Bearer <token>` header.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/todos` | Create a new task |
| GET | `/api/todos` | List all user's tasks |
| GET | `/api/todos/{id}` | Get specific task |
| PATCH | `/api/todos/{id}` | Update task |
| DELETE | `/api/todos/{id}` | Delete task |
| POST | `/api/todos/{id}/toggle` | Toggle completion status |

### Example Request

```bash
# Create a task
curl -X POST http://localhost:8000/api/todos \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
  }'
```

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run specific test file
uv run pytest tests/unit/test_task_model.py
```

### Frontend Tests

```bash
cd frontend

# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch
```

## Project Structure

```
.
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── auth/           # JWT verification, dependencies
│   │   ├── crud/           # Database CRUD operations
│   │   ├── db/             # Database connection
│   │   ├── exceptions/     # Custom exceptions & handlers
│   │   ├── middleware/     # CORS, logging, error handling
│   │   ├── models/         # SQLModel database models
│   │   ├── routers/        # API endpoints
│   │   ├── schemas/        # Pydantic request/response schemas
│   │   ├── config.py       # Environment configuration
│   │   └── main.py         # FastAPI app entry point
│   ├── tests/
│   │   ├── unit/           # Unit tests
│   │   └── integration/    # Integration tests
│   └── pyproject.toml      # Python dependencies
│
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # Next.js pages & API routes
│   │   ├── components/    # React components
│   │   │   ├── auth/     # Authentication components
│   │   │   ├── tasks/    # Task management components
│   │   │   └── ui/       # Reusable UI components
│   │   ├── hooks/        # Custom React hooks
│   │   ├── lib/          # Utilities & validation schemas
│   │   ├── middleware/   # API interceptor
│   │   ├── providers/    # React context providers
│   │   ├── types/        # TypeScript type definitions
│   │   └── tests/        # Test setup & mocks
│   └── package.json      # Node dependencies
│
├── specs/                 # Feature specifications
├── history/              # PHR & ADR records
├── .specify/             # Spec-Kit configuration
├── CLAUDE.md             # Development guidelines
└── README.md             # This file
```

## Development Workflow

This project follows **Spec-Driven Development (SDD)** methodology:

1. **Specify**: Define requirements in `specs/` using `/sp.specify`
2. **Plan**: Create implementation plan using `/sp.plan`
3. **Tasks**: Break down into atomic tasks using `/sp.tasks`
4. **Implement**: Execute tasks following TDD principles

### Key Guidelines

- **Test-Driven Development**: Write tests before implementation (70% minimum coverage)
- **User Isolation**: All database queries MUST filter by `user_id`
- **Type Safety**: Use TypeScript (frontend) and type hints (backend)
- **No Manual Coding**: All code generated via Claude Code
- **Validation**: Zod (frontend) + Pydantic (backend) for input validation

See `CLAUDE.md` for complete development standards.

## Security Features

- **Authentication**: JWT tokens with Better Auth
- **Authorization**: All endpoints require valid JWT
- **User Isolation**: Database-level filtering ensures users only access their own data
- **Input Validation**: All user input validated on client and server
- **SQL Injection Prevention**: SQLModel uses parameterized queries
- **XSS Prevention**: React escapes output automatically
- **HTTPS**: Required in production (HTTP OK for localhost development)

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://...        # PostgreSQL connection string
BETTER_AUTH_URL=http://localhost:3000  # Better Auth server URL
CORS_ORIGINS=["http://localhost:3000"] # Allowed CORS origins
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_APP_URL=http://localhost:3000    # Frontend URL
NEXT_PUBLIC_API_URL=http://localhost:8000    # Backend API URL
DATABASE_URL=postgresql://...                # Database for Better Auth
BETTER_AUTH_SECRET=...                       # Auth secret key
```

## Constitutional Compliance

This project adheres to strict development principles:

- ✅ Test-Driven Development (TDD) with 70%+ coverage
- ✅ No manual coding (all via Claude Code)
- ✅ Code quality standards (type safety, validation)
- ✅ Workflow: Specify → Plan → Tasks → Implement
- ✅ Governance via constitution (`.specify/memory/constitution.md`)

## Contributing

1. Read `CLAUDE.md` for development guidelines
2. Follow TDD workflow (write tests first)
3. Ensure 70%+ test coverage
4. Run linters before committing
5. Create Prompt History Records (PHR) for significant work

## License

[Your License Here]

## Support

For issues or questions:
- Check API documentation at `http://localhost:8000/docs`
- Review frontend guide at `frontend/CLAUDE.md`
- Review backend guide at `backend/CLAUDE.md`
- See project constitution at `.specify/memory/constitution.md`