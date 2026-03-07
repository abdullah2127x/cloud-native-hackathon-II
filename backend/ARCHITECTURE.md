# Backend Architecture

> Branch: `enhance-code-architecture`
> Last updated: 2026-03-07

---

## Current Structure

```
src/
├── main.py                      App entry — lifespan, middleware, routers
├── core/                        Foundation layer (CANONICAL locations)
│   ├── config.py                Settings via pydantic-settings + ConfigDict
│   ├── database.py              Engine, session factory, create_db_and_tables
│   └── security.py              JWT verification via JWKS (Better Auth), get_current_user
├── api/
│   └── deps.py                  Annotated DI aliases: CurrentUser, DbSession
├── models/                      SQLModel table models (sa_column for DB constraints)
│   ├── task.py                  Task model — title, description, completed, priority
│   ├── tag.py                   Tag + TaskTag (many-to-many junction)
│   ├── user.py                  User model (read-only, managed by Better Auth)
│   ├── priority.py              Priority enum (high, medium, low, none)
│   ├── conversation.py          Conversation model (chat — NOT YET MIGRATED)
│   └── message.py               Message model (chat — NOT YET MIGRATED)
├── schemas/
│   ├── task.py                  TaskCreate, TaskUpdate, TaskRead, TaskListResponse, enums
│   └── chat.py                  Chat schemas (NOT YET MIGRATED)
├── repositories/                Pure data access — SQL queries only, no business logic
│   ├── task_repo.py             TaskRepository class + task_repo instance
│   └── tag_repo.py              TagRepository class + tag_repo instance
├── services/                    Business logic — orchestrates repos, enforces rules
│   ├── task_service.py          TaskService class + task_service instance
│   └── tag_service.py           TagService class + tag_service instance
├── routers/                     HTTP layer — thin, delegates to services
│   ├── tasks.py                 /api/todos/* — imports task_service directly
│   ├── tags.py                  /api/tags/*  — imports tag_service directly
│   ├── health.py                /health + /health/db
│   ├── chat.py                  Chat endpoints (NOT YET MIGRATED)
│   └── chatkit.py               ChatKit SSE endpoint (NOT YET MIGRATED)
├── middleware/
│   ├── cors.py                  CORS from settings.cors_origins
│   ├── logging.py               Request logging + X-Process-Time header
│   ├── error_handler.py         Catches unhandled exceptions → clean 500 JSON
│   └── rate_limit.py            slowapi limiter (60/min default per IP)
├── exceptions/
│   ├── base.py                  TaskNotFoundError, TagNotFoundError, UnauthorizedError, etc.
│   └── handlers.py              Maps exceptions → HTTP responses (404, 401, 422)
├── utils/
│   └── helpers.py               Shared utc_now(), generate_uuid()
├── crud/                        ONLY contains chat (task/tag crud deleted)
│   └── chat.py                  Chat CRUD functions (NOT YET MIGRATED)
├── agents/                      AI layer (NOT YET MIGRATED)
│   ├── todo_agent.py            OpenAI Agents SDK — calls MCP tools
│   └── math_teacher.py          Example agent
└── chatkit/                     ChatKit server (NOT YET MIGRATED)
    ├── server.py                ChatKitServer with agent integration
    └── store.py                 TodoPostgresStore for chat persistence
```

### Backward-Compatible Re-export Shims

These files exist ONLY because untouched code (chat, agents, chatkit, mcpserver, tests/conftest) still imports from old paths. They re-export from canonical locations:

| Shim File | Canonical Location | Who Still Imports It |
|-----------|-------------------|---------------------|
| `src/config.py` | `src/core/config.py` | chatkit/store.py |
| `src/db/database.py` | `src/core/database.py` | tests/conftest.py, chatkit/store.py |
| `src/auth/dependencies.py` | `src/core/security.py` | tests/conftest.py |
| `src/auth/jwt_handler.py` | `src/core/security.py` | mcpserver/ |

**When migrating a feature that imports from these shims**, update its imports to the canonical `src.core.*` path. Once no code imports from a shim, delete it.

---

## What Was Done (This Branch)

### Commit History

| Commit | What Changed |
|--------|-------------|
| `019960b` | Added fastapi-builder and openai-agents-sdk skills |
| `35029d0` | **Phase 1** — Fixed critical violations: `sa_column` on all models, `ConfigDict`, `server_default`, shared helpers, `Annotated` deps, removed redundant psycopg2 |
| `a981447` | **Phase 2** — Restructured to layered architecture: `core/`, `repositories/`, `services/`, `api/deps.py`, backward-compatible re-export shims |
| `2472565` | **Phase 3** — Production hardening: rate limiting, GZip, pagination, health/db, X-Process-Time |
| `d06060e` | Removed dead deps: `passlib[bcrypt]`, `python-jose[cryptography]` |
| `310f813` | Converted repos/services to class-based, deleted crud/task.py and crud/tag.py shims |
| `ff2ca02` | Replaced deprecated `on_event` with `lifespan` context manager |

### Patterns Established

**Class-based repos/services with module-level instances:**
```python
class TaskRepository:
    def find_by_id(self, session, task_id, user_id): ...

task_repo = TaskRepository()
```

```python
class TaskService:
    def __init__(self, task_repo, tag_repo, tag_service):
        self._task_repo = task_repo
        ...

task_service = TaskService(task_repo, tag_repo, tag_service)
```

**Routers import service instances directly:**
```python
from src.services.task_service import task_service as task_crud
```

**Session is per-request, never stored on class.** Passed as first arg to every method.

**Every query filters by user_id** — user isolation is enforced at the repository level.

---

## What Needs To Be Done (Future Features)

### Features NOT YET MIGRATED to the new architecture

These features exist in the codebase but still use the old patterns. When you work on them, follow the migration steps below.

#### 1. Chat (conversations + messages)

**Current state:**
- `src/crud/chat.py` — functional style, mixes business logic + SQL (old pattern)
- `src/routers/chat.py` — imports from `src.crud.chat`
- `src/schemas/chat.py` — schemas exist
- `src/models/conversation.py` + `src/models/message.py` — models exist
- `tests/unit/test_chat_crud.py` — tests import from `src.crud.chat`
- `tests/integration/test_chat_api.py` — integration tests

**Migration steps:**
1. Create `src/repositories/chat_repo.py` — `ChatRepository` class, extract pure SQL from `crud/chat.py`
2. Create `src/services/chat_service.py` — `ChatService` class, business logic
3. Update `src/routers/chat.py` — import from `chat_service` instead of `crud.chat`
4. Update tests to import from `src.services.chat_service`
5. Delete `src/crud/chat.py`
6. Update `src/models/conversation.py` — add `sa_column` constraints if missing
7. Update `src/models/message.py` — add `sa_column` constraints if missing
8. Once `crud/chat.py` is deleted and nothing imports from `src/crud/`, delete `src/crud/` entirely

#### 2. ChatKit Server

**Current state:**
- `src/chatkit/server.py` — ChatKitServer class
- `src/chatkit/store.py` — TodoPostgresStore, imports from `src.config` (shim)
- `src/routers/chatkit.py` — SSE endpoint

**Migration steps:**
1. Update `store.py` to import from `src.core.config` instead of `src.config`
2. Once done, check if `src/config.py` shim is still needed — if nothing else imports it, delete it

#### 3. Agents

**Current state:**
- `src/agents/todo_agent.py` — uses MCP tools, does NOT import from crud/services/repos
- `src/agents/math_teacher.py` — standalone example

**No migration needed** — agents talk through MCP server, they don't import app layers.

#### 4. MCP Server

**Current state:**
- `mcpserver/tools/*.py` — each tool has its own direct SQL queries (bypasses services/repos)
- `mcpserver/mcp_server.py` — imports from `src.auth.jwt_handler` (shim)

**Migration steps (when ready):**
1. Update MCP tools to use service instances instead of direct SQL
2. Update `mcp_server.py` to import from `src.core.security` instead of `src.auth.jwt_handler`
3. Once done, check if `src/auth/jwt_handler.py` and `src/auth/dependencies.py` shims are still needed — delete if not

#### 5. Re-export Shim Cleanup

After all features are migrated, these files should be deleted:
- `src/config.py`
- `src/db/database.py` + `src/db/__init__.py`
- `src/auth/jwt_handler.py` + `src/auth/dependencies.py` + `src/auth/__init__.py`
- `src/crud/__init__.py` (once `crud/chat.py` is migrated out)

### Other Cleanup

- `backend/migrations/` — dead SQL files, never executed. SQLModel handles schema via `create_all()`. Safe to delete.
- `backend/htmlcov/` — pytest-cov build artifact, regenerates every test run. Already in `.gitignore`. Not tracked in git.

---

## Import Hierarchy (Prevents Circular Imports)

```
core/config → core/database → models → schemas → repositories → services → api/deps → routers → main
```

Never import backwards in this chain (e.g., a repo should never import from a service).

---

## Testing

```bash
cd backend && uv run pytest              # all tests with coverage
cd backend && uv run pytest --no-cov -q  # fast run without coverage
```

- **285 tests pass** (156 unit+integration, rest are mcpserver/chat)
- **6 pre-existing failures** in `tests/mcpserver/test_auth.py` (JWT key encoding issue, unrelated to architecture)
- **Coverage: 77%** (minimum required: 70%)
