# Implementation Plan: ChatKit UI Integration

**Branch**: `007-chatkit-ui-integration` | **Date**: 2026-02-11 | **Spec**: specs/007-chatkit-ui-integration/spec.md
**Input**: Feature specification from `/specs/007-chatkit-ui-integration/spec.md`

---

## Summary

Add a real-time streaming chat interface to the todo web application. A logged-in user types natural language task commands and sees the assistant's reply stream word-by-word via the OpenAI ChatKit UI component. The backend adds a `POST /chatkit` SSE endpoint built on the `openai-chatkit` Python SDK, wrapping the existing TodoAgent tools (from feature 006) with streaming capability. The frontend adds a `/dashboard/chat` page using the ChatKit UI component pointed at the new endpoint.

**Two endpoints coexist**: `POST /api/{user_id}/chat` (stateless JSON, feature 006) and `POST /chatkit` (streaming SSE, this feature). Both call the same underlying todo tools via the same MCP server.

---

## Technical Context

**Backend Language/Version**: Python 3.11+ | FastAPI | uv package manager
**Frontend Language/Version**: TypeScript | Next.js 16 App Router
**New Backend Dependencies**: `openai-chatkit`, `psycopg[binary]`
**New Frontend Dependencies**: `@openai/chatkit` (npm package)
**Database**: Neon Serverless PostgreSQL — 2 new tables (`chatkit_threads`, `chatkit_items`)
**Auth**: Existing `get_current_user` FastAPI dependency (Better Auth JWT JWKS)
**AI Provider**: OpenRouter via existing `settings.openrouter_api_key` + `settings.llm_model`
**Existing reuse**: `_add_task_tool`, `_list_tasks_tool`, `_complete_task_tool`, `_update_task_tool`, `_delete_task_tool` from `backend/src/agents/todo_agent.py`

---

## Constitution Check

| Principle | Gate | Status |
|-----------|------|--------|
| I. TDD | Tests must be written before implementation | ✅ Plan enforces TDD — tests before implementation tasks |
| II. No Manual Coding | All code via Claude Code | ✅ |
| III. Code Quality (70% coverage) | `--cov-fail-under=70` | ✅ New code must maintain ≥70% |
| VIII. Persistent Storage | DB storage required, no in-memory | ✅ PostgresStore with 2 new DB tables |
| IX. API Stateless | Every request fetches state from DB | ✅ PostgresStore loads thread per request |
| X. User Isolation | All queries filter by user_id | ✅ PostgresStore enforces user_id on all queries |
| XI. JWT Auth | Bearer JWT required | ✅ Existing `get_current_user` dependency reused |
| XII. MCP Architecture | AI agent via MCP only | ✅ Same tools as feature 006, MCP unchanged |
| XIV. Performance | First token < 5s | ✅ Streaming SSE, first token typically < 2s |

**Gate result**: PASS — no violations.

---

## Architecture

```
Browser (Next.js)
    └── /dashboard/chat (new page)
            └── <ChatKit> component
                    │  POST /chatkit  (SSE streaming)
                    │  Authorization: Bearer <jwt>
                    ▼
            FastAPI app (existing)
                    └── POST /chatkit router (new)
                            │  Depends(get_current_user) → user_id
                            │  Depends(get_session) → session
                            ▼
                    TodoChatKitServer.respond()
                            │  load thread from PostgresStore
                            │  convert items → agent input
                            ▼
                    chatkit.agents.Runner.run_streamed(agent, input_items)
                            │  agent has same 5 tools from todo_agent.py
                            │  tools call mcp_server.call_tool()
                            ▼
                    stream_agent_response() → SSE events → browser
                            │
                    PostgresStore saves items to chatkit_threads + chatkit_items
```

---

## File Structure

### New Backend Files

```
backend/src/
├── chatkit/
│   ├── __init__.py
│   ├── store.py          ← PostgresStore (psycopg3 implementation)
│   └── server.py         ← TodoChatKitServer + ChatKitRequestContext
└── routers/
    └── chatkit.py        ← POST /chatkit endpoint

backend/tests/
├── unit/
│   └── test_chatkit_server.py   ← Unit tests for server.respond()
└── integration/
    └── test_chatkit_api.py      ← Integration tests for POST /chatkit
```

### Modified Backend Files

```
backend/pyproject.toml            ← Add openai-chatkit, psycopg[binary] deps
backend/src/main.py               ← Register chatkit_router
```

### New Frontend Files

```
frontend/src/app/dashboard/
└── chat/
    └── page.tsx                  ← Chat page with ChatKit UI component
```

### Modified Frontend Files

```
frontend/package.json             ← Add @openai/chatkit dep
frontend/src/app/dashboard/components/Sidebar.tsx  ← Add Chat nav item
```

---

## Phase 0: Dependencies

Install required packages before writing any code.

**Backend** (`backend/`):
```bash
uv add openai-chatkit psycopg[binary]
```

**Frontend** (`frontend/`):
```bash
npm install @openai/chatkit
```

---

## Phase 1: Backend — Store (TDD)

### 1a. Write store tests first (RED)
File: `backend/tests/unit/test_chatkit_store.py`
- Test `save_thread` + `load_thread` round-trip
- Test `add_thread_item` + `load_thread_items` ordering
- Test user isolation: `load_thread` with wrong user_id raises `NotFoundError`
- Test thread deletion cascades to items

### 1b. Implement PostgresStore (GREEN)
File: `backend/src/chatkit/store.py`
- `ChatKitRequestContext` dataclass: `user_id: str, session: Session`
- `TodoPostgresStore(Store[ChatKitRequestContext])` using psycopg3
- Tables created via `_init_schema()` on startup
- All queries filter by `context.user_id`
- Use `settings.database_url` for connection

---

## Phase 2: Backend — ChatKit Server (TDD)

### 2a. Write server tests first (RED)
File: `backend/tests/unit/test_chatkit_server.py`
- Mock `TodoPostgresStore` and `chatkit.agents.Runner`
- Test `respond()` calls `load_thread_items` with correct args
- Test streaming events emitted
- Test 5 tools are present on the agent

### 2b. Implement TodoChatKitServer (GREEN)
File: `backend/src/chatkit/server.py`

```python
from chatkit.server import ChatKitServer, ThreadMetadata, UserMessageItem, ThreadStreamEvent
from chatkit.agents import Agent, AgentContext, Runner, simple_to_agent_input, stream_agent_response
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from agents.run import RunConfig
from openai import AsyncOpenAI
from src.config import settings
from src.agents.todo_agent import (
    _add_task_tool, _list_tasks_tool, _complete_task_tool,
    _update_task_tool, _delete_task_tool, TodoContext, mcp_server
)
```

Key implementation:
- Agent has same system prompt + same 5 tools as `run_todo_agent`
- Agent uses `OpenAIChatCompletionsModel` with OpenRouter (same as feature 006)
- `respond()` loads last 20 thread items, converts to agent input, streams response
- Tools receive `RunContextWrapper[AgentContext]` — extract `user_id` and `session` from `context.request_context`

**CRITICAL tool adaptation**: The 5 existing tools use `RunContextWrapper[TodoContext]`. For ChatKit, we wrap each tool to extract `TodoContext` from `AgentContext.request_context`. Create 5 thin wrappers that bridge `AgentContext` → `TodoContext`.

---

## Phase 3: Backend — Router (TDD)

### 3a. Write router tests first (RED)
File: `backend/tests/integration/test_chatkit_api.py`
- Test 200 streaming response on `POST /chatkit` with valid auth
- Test 401 on missing/invalid JWT
- Test 404 when thread belongs to another user
- Test 503 on OpenRouter failure
- Test off-topic message returns 200 with scope explanation

### 3b. Implement POST /chatkit router (GREEN)
File: `backend/src/routers/chatkit.py`

```python
@router.post("/chatkit")
async def chatkit_endpoint(
    request: Request,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    context = ChatKitRequestContext(user_id=user_id, session=session)
    result = await chatkit_server.process(await request.body(), context)
    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")
    return Response(content=result.json, media_type="application/json")
```

### 3c. Register in main.py (GREEN)
- Add `from src.routers.chatkit import router as chatkit_router`
- Add `app.include_router(chatkit_router)`

---

## Phase 4: Frontend — Chat Page (TDD)

### 4a. Write frontend tests first (RED)
File: `frontend/src/app/dashboard/chat/__tests__/page.test.tsx`
- Test chat page renders ChatKit component
- Test unauthenticated user is redirected to login
- Test auth header is set from `getJwtToken()`

### 4b. Implement chat page (GREEN)
File: `frontend/src/app/dashboard/chat/page.tsx`
- Server component checks auth session, redirects if not logged in
- Client component renders `<ChatKit>` with backend URL + auth header
- Use `NEXT_PUBLIC_BACKEND_URL` env var for API URL

### 4c. Add Chat nav item to Sidebar (GREEN)
File: `frontend/src/app/dashboard/components/Sidebar.tsx`
- Add "Chat" link pointing to `/dashboard/chat`
- Use existing nav item styling

---

## Phase 5: Polish & Environment

- Add `NEXT_PUBLIC_BACKEND_URL` to `frontend/.env.example` if not already present
- Add OpenAI domain allowlist note to README (manual step — register frontend domain in OpenAI dashboard)
- Verify backend `.env.example` already has `DATABASE_URL` (yes, from feature 005)

---

## Design Decisions

### Tool Adaptation Pattern

The 5 existing tools expect `RunContextWrapper[TodoContext]`. With ChatKit, the context is `AgentContext` which carries `request_context: ChatKitRequestContext`. We create adapter tools:

```python
# In server.py — adapter wrapper
async def _chatkit_add_task(wrapper: RunContextWrapper[AgentContext], title: str, description: Optional[str] = None) -> str:
    ctx = wrapper.context.request_context  # ChatKitRequestContext
    todo_ctx = TodoContext(user_id=ctx.user_id, session=ctx.session)
    # Delegate to mcp_server directly (same logic as existing add_task)
    response = await mcp_server.call_tool("add_task", {...}, session=ctx.session)
    ...
```

This keeps MCP calls identical to feature 006 without importing or duplicating the raw async functions.

### Store Initialization

`TodoPostgresStore._init_schema()` is called once at module level (when the store instance is created). This creates the two tables if they don't exist. No Alembic migration needed — matches the existing `SQLModel.metadata.create_all()` pattern.

---

## Quickstart Test Scenarios

After implementation, validate manually:

1. Sign in → navigate to `/dashboard/chat`
2. Type "add buy milk" → see streaming reply confirming task created
3. Type "show my tasks" → see task list in reply
4. Type "mark task 1 as done" → see completion confirmation
5. Type "what is the weather?" → see scope explanation reply
6. Open new tab `/dashboard/chat` → fresh conversation, no prior history
7. Close backend → send message → see friendly error message

---

## Dependencies Graph

```
Phase 0: Install deps
    ├── Phase 1: Store (tests → implementation)
    │       └── Phase 2: ChatKit Server (tests → implementation)
    │               └── Phase 3: Router (tests → implementation → register)
    └── Phase 4: Frontend Chat Page (tests → implementation → sidebar)
                                   ↑
                               (independent of Phase 1-3 for structure,
                                but requires working backend for E2E)
    Phase 5: Polish (independent)
```

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| `@openai/chatkit` npm package name differs | Verify at `npm install` time; fall back to checking OpenAI GitHub |
| OpenAI domain allowlist required | Note in README; not needed for localhost dev |
| Tool context mismatch (TodoContext vs AgentContext) | Adapter wrapper pattern in server.py resolves cleanly |
| psycopg3 vs psycopg2 conflict | Use `psycopg[binary]` (psycopg3) — new, no conflict with existing setup |
| ChatKit store vs feature 006 store coexistence | Separate tables, no coupling |
