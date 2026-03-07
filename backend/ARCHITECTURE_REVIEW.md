# Backend Architecture Review & Improvement Plan

> Compared against: `.claude/skills/fastapi-builder/` best practices
> Date: 2026-03-07
> Branch: `enhance-code-architecture`

---

## Current Structure vs Skill-Recommended Structure

### Current Layout

```
src/
├── main.py
├── config.py
├── auth/
│   ├── jwt_handler.py
│   └── dependencies.py
├── db/
│   └── database.py
├── models/          (SQLModel table models)
├── schemas/         (Pydantic API models)
├── crud/            (business logic mixed with data access)
├── routers/         (API endpoints)
├── middleware/
├── exceptions/
├── agents/          (AI - out of scope)
└── chatkit/         (AI - out of scope)
```

### Skill-Recommended Layout (Medium-to-Large)

```
src/
├── main.py
├── core/
│   ├── config.py          (Settings with ConfigDict)
│   ├── security.py        (JWT, password hashing)
│   ├── database.py        (engine, session)
│   └── logging.py         (structlog JSON/console)
├── models/                (table=True with sa_column)
├── schemas/               (API models with Field constraints)
├── api/
│   └── v1/
│       ├── endpoints/     (routers per resource)
│       └── api.py         (router aggregation)
├── services/              (business logic layer)
├── repositories/          (data access layer)
├── utils/
│   ├── rate_limit.py      (slowapi setup)
│   └── validators.py
├── middleware/
├── exceptions/
├── agents/                (AI - untouched)
└── chatkit/               (AI - untouched)
```

---

## Violations & Gaps (Skill vs Current Code)

### CRITICAL - Must Fix

| # | Issue | Skill Says | Current Code | File |
|---|-------|-----------|-------------|------|
| C1 | **Missing `sa_column=Column(String(N))`** on table model string fields | "MANDATORY: Use `sa_column=Column(String(N))` on ALL string fields in table models" | `title: str = Field(max_length=200)` — `max_length` on Field is Pydantic-only, does NOT create DB constraint | `models/task.py:43`, `models/tag.py:52`, `models/user.py:20-21` |
| C2 | **`class Config` instead of `model_config = ConfigDict`** | "Use ConfigDict not class-based Config" with `extra="ignore"` | Uses old `class Config:` pattern in Settings and User model | `config.py:55-57`, `models/user.py:26-29` |
| C3 | **Hardcoded secret in config default** | "Never hardcode secrets; use env vars" | `better_auth_secret: str = "your-secret-key-change-in-production"` | `config.py:16` |
| C4 | **No `server_default` on columns with defaults** | "Always set `server_default` on columns with defaults" | `completed: bool = Field(default=False)` has no `server_default` | `models/task.py:47` |
| C5 | **Duplicate `utc_now()` and `generate_uuid()`** | Implies shared utilities | Defined separately in `models/task.py:16`, `models/tag.py:11`, `models/user.py:9` | 3 files |

### HIGH - Should Fix

| # | Issue | Skill Says | Current Code | File |
|---|-------|-----------|-------------|------|
| H1 | **No service layer** | "Services: Business logic, orchestration" separate from data access | CRUD layer mixes business logic + DB queries in one layer | `crud/task.py`, `crud/tag.py` |
| H2 | **No rate limiting** | "Rate limiting on auth endpoints (5/min login, 10/hr signup)" with `slowapi` in `utils/rate_limit.py` | No rate limiting at all | Missing |
| H3 | **No `nullable=False`** on required DB columns | "Always set `nullable=False`" on required columns | `title`, `user_id`, `name` — none have explicit `nullable=False` in sa_column | `models/task.py`, `models/tag.py` |
| H4 | **Logging uses basic logger, not structlog properly** | "Structured via structlog (JSON prod, console dev) with RequestLoggingMiddleware" | `middleware/logging.py` uses `print()` or basic logger, not structlog's JSON/console dual mode | `middleware/logging.py` |
| H5 | **No health check for database** | "GET /health/db → session.exec(text('SELECT 1'))" | Only basic `/health` returning static JSON | `routers/health.py` |
| H6 | **No API versioning** | "api/v1/endpoints/ for versioned APIs" | Routes directly under `/api/todos`, no versioning | `routers/tasks.py` |
| H7 | **`psycopg2` + `psycopg[binary]` both present** | "ALWAYS include psycopg[binary], use `postgresql+psycopg://`" | Both `psycopg2>=2.9.11` AND `psycopg[binary]>=3.3.2` — redundant, psycopg2 is legacy | `pyproject.toml` |

### MEDIUM - Nice to Have

| # | Issue | Skill Says | Current Code | File |
|---|-------|-----------|-------------|------|
| M1 | **No `EmailStr` on User email** | "EmailStr on all email fields (never plain str)" | `email: str` — no EmailStr validation | `models/user.py:20` |
| M2 | **No `Literal` types for enum-like strings** | "Literal types on enum-like strings (role, status, grade, category)" | `llm_provider: str = "openrouter"` — should be `Literal["openrouter", "openai", "gemini"]` | `config.py:33` |
| M3 | **No GZip middleware** | "GZipMiddleware(minimum_size=1000)" for response compression | Not configured | `main.py` |
| M4 | **No pagination limit enforcement** | "Always add offset/limit" with max limit enforced | `list_tasks()` returns all matching tasks, no offset/limit | `crud/task.py`, `routers/tasks.py` |
| M5 | **No `Annotated` type alias for dependencies** | "Use Annotated with Depends() pattern" | Repeats `user_id: str = Depends(get_current_user)` in every route | `routers/tasks.py` |
| M6 | **No process-time header** | "Add X-Process-Time header" via timing middleware | Logging middleware tracks time but doesn't return it in header | `middleware/logging.py` |
| M7 | **CRUD commits inside functions** | Backend CLAUDE.md says "Don't commit inside CRUD functions" but CRUD does commit | `session.commit()` called inside CRUD, not in router layer | `crud/task.py` |

---

## Proposed Restructure

### Phase 1: Core Fixes (no structure change)

These can be done in-place without moving files:

1. **Fix `sa_column` on all table model string fields** (C1)
   - `Task.title` → `sa_column=Column(String(200), nullable=False)`
   - `Task.description` → `sa_column=Column(String(2000), nullable=True)`
   - `Tag.name` → `sa_column=Column(String(50), nullable=False, index=True)`
   - `User.email` → `sa_column=Column(String(255), unique=True, index=True, nullable=False)`
   - `User.name` → `sa_column=Column(String(100), nullable=False)`

2. **Switch to `model_config = ConfigDict`** (C2)
   - Settings: `model_config = ConfigDict(env_file=".env", case_sensitive=False, extra="ignore")`
   - User: Remove old `class Config`

3. **Remove hardcoded secret default** (C3)
   - `better_auth_secret: str = ""` or make it Optional with validation

4. **Add `server_default`** on columns with defaults (C4)
   - `completed` → `sa_column=Column(Boolean, server_default="false")`

5. **Extract shared utilities** (C5)
   - Create `src/utils/helpers.py` with `utc_now()` and `generate_uuid()`
   - Import from single source in all models

6. **Add `nullable=False`** on required columns (H3)

7. **Use `Literal` types** for config enums (M2)

8. **Use `Annotated` dependency aliases** (M5)

### Phase 2: Structure Enhancement

Move to layered architecture:

```
src/
├── main.py                     (app factory, middleware, router registration)
├── core/                       (was: config.py + db/ + auth/)
│   ├── config.py              (Settings with ConfigDict)
│   ├── database.py            (engine, session, create_tables)
│   ├── security.py            (JWT handler + auth dependencies merged)
│   └── logging.py             (structlog dual-mode: JSON prod, console dev)
├── models/                     (unchanged - table models)
│   ├── __init__.py            (re-exports all models)
│   ├── user.py
│   ├── task.py
│   ├── tag.py
│   └── priority.py
├── schemas/                    (unchanged - API models)
│   ├── __init__.py
│   └── task.py
├── api/                        (was: routers/)
│   ├── deps.py                (shared dependencies: CurrentUser, DbSession)
│   └── v1/
│       ├── __init__.py
│       ├── router.py          (aggregates all v1 endpoints)
│       ├── tasks.py
│       ├── tags.py
│       └── health.py
├── services/                   (NEW: business logic extracted from crud/)
│   ├── __init__.py
│   ├── task_service.py        (orchestration, validation, business rules)
│   └── tag_service.py
├── repositories/               (was: crud/ — now pure data access)
│   ├── __init__.py
│   ├── task_repo.py           (SQL queries only, no business logic)
│   └── tag_repo.py
├── utils/                      (NEW)
│   ├── helpers.py             (utc_now, generate_uuid)
│   ├── rate_limit.py          (slowapi setup + constants)
│   └── constants.py
├── middleware/                  (enhanced)
│   ├── cors.py
│   ├── error_handler.py
│   └── request_logging.py     (structlog + X-Process-Time header)
├── exceptions/                 (unchanged)
│   ├── base.py
│   └── handlers.py
├── agents/                     (untouched)
└── chatkit/                    (untouched)
```

### Phase 3: Production Hardening

1. **Add rate limiting** (H2) — `utils/rate_limit.py` with slowapi
2. **Add DB health check** (H5) — `GET /health/db`
3. **Add GZip middleware** (M3)
4. **Add pagination** (M4) — `offset`/`limit` with max limit enforcement
5. **Structured logging** (H4) — structlog with JSON in prod, console in dev
6. **Process-time header** (M6)

---

## Import Hierarchy (Prevents Circular Imports)

```
core/config → core/database → models → schemas → repositories → services → api/deps → api/v1/* → main
```

This is the skill's recommended hierarchy. Current code roughly follows it but some cross-imports exist between models.

---

## Service vs Repository Split (H1)

### Current (crud/task.py mixes both):
```python
def create_task(session, task_data, user_id):
    # Business logic: validate, transform
    task = Task(user_id=user_id, title=task_data.title, ...)
    # Data access: SQL operations
    session.add(task)
    session.flush()
    # More business logic: handle tags
    for tag_name in task_data.tags:
        tag = _get_or_create_tag(session, tag_name, user_id)
        session.add(TaskTag(task_id=task.id, tag_id=tag.id))
    session.commit()
```

### Proposed (separated):
```python
# repositories/task_repo.py — pure data access
def insert_task(session, task: Task) -> Task:
    session.add(task)
    session.flush()
    return task

def link_task_tag(session, task_id: str, tag_id: str):
    session.add(TaskTag(task_id=task_id, tag_id=tag_id))

# services/task_service.py — business logic
def create_task(session, task_data, user_id) -> Task:
    task = Task(user_id=user_id, title=task_data.title, ...)
    task = task_repo.insert_task(session, task)
    for tag_name in task_data.tags:
        tag = tag_service.get_or_create(session, tag_name, user_id)
        task_repo.link_task_tag(session, task.id, tag.id)
    session.commit()
    return task
```

---

## Dependency Pattern Fix (M5)

### Current (repeated everywhere):
```python
@router.post("/")
async def create(task_data: TaskCreate,
                 user_id: str = Depends(get_current_user),
                 session: Session = Depends(get_session)):
```

### Proposed (Annotated aliases in api/deps.py):
```python
# api/deps.py
from typing import Annotated
CurrentUser = Annotated[str, Depends(get_current_user)]
DbSession = Annotated[Session, Depends(get_session)]

# api/v1/tasks.py
@router.post("/")
async def create(task_data: TaskCreate, user_id: CurrentUser, session: DbSession):
```

---

## Files That Need NO Changes (Out of Scope)

- `src/agents/` — AI agent code
- `src/chatkit/` — ChatKit SSE streaming
- `src/routers/chat.py` — Chat endpoint
- `src/routers/chatkit.py` — ChatKit endpoint
- `src/crud/chat.py` — Chat CRUD
- `src/schemas/chat.py` — Chat schemas
- `src/models/conversation.py` — Conversation model
- `src/models/message.py` — Message model
- `mcpserver/` — MCP tools

These exist in the codebase but are NOT touched during this enhancement.

---

## Priority Order

1. **Phase 1** — Fix critical violations (C1-C5, H3, M2, M5) — same file locations
2. **Phase 2** — Restructure to layered architecture — move files, update imports
3. **Phase 3** — Production hardening (rate limiting, health/db, GZip, pagination, structlog)

Each phase is independently shippable and testable.
