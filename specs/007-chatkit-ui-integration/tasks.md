# Tasks: ChatKit UI Integration

**Feature**: 007-chatkit-ui-integration | **Branch**: `007-chatkit-ui-integration`
**Input**: specs/007-chatkit-ui-integration/{plan.md, spec.md, data-model.md, contracts/, research.md}
**Date**: 2026-02-11

---

## Format: `- [ ] [ID] [P?] [Story?] Description — file path`

- **[P]**: Parallelizable (different files, no blocking dependency)
- **[US1/US2/US3/US4]**: User Story scope (matches spec.md priorities)
- **Setup/Foundational tasks**: no story label

---

## Phase 1: Setup

**Purpose**: Install dependencies and verify prerequisites before writing any code.

- [ ] T001 Install backend dependencies `openai-chatkit` and `psycopg[binary]` via `uv add openai-chatkit "psycopg[binary]"` in `backend/` and confirm both appear in `backend/pyproject.toml` dependencies
- [ ] T002 [P] Install frontend dependency `@openai/chatkit` via `npm install @openai/chatkit` in `frontend/` and confirm it appears in `frontend/package.json` dependencies

**Checkpoint**: Both packages installed — proceed to Phase 2

---

## Phase 2: Foundational (Data Layer)

**Purpose**: Create the ChatKit PostgreSQL store with user-isolated thread persistence. All user stories depend on this.

**⚠️ CRITICAL**: T003–T007 must complete before Phase 3

- [ ] T003 Create `backend/src/chatkit/__init__.py` (empty file) to make `chatkit` a Python package — `backend/src/chatkit/__init__.py`
- [ ] T004 [P] Create `ChatKitRequestContext` dataclass (fields: `user_id: str`, `session: Session`) and `TodoPostgresStore(Store[ChatKitRequestContext])` using psycopg3 with `_init_schema()` that creates `chatkit_threads` and `chatkit_items` tables; implement all required Store methods (`load_thread`, `save_thread`, `load_thread_items`, `add_thread_item`, `save_item`, `load_item`, `delete_thread`, `delete_thread_item`); all queries MUST filter by `context.user_id`; use `settings.database_url` for connection — `backend/src/chatkit/store.py`
- [ ] T005 [P] Write unit tests for `TodoPostgresStore`: `save_thread` + `load_thread` round-trip returns correct ThreadMetadata; `add_thread_item` + `load_thread_items(order="asc")` returns items oldest-first; `load_thread` with wrong `user_id` raises `NotFoundError`; `load_thread_items` with wrong `user_id` returns empty page; `delete_thread` cascades to items — `backend/tests/unit/test_chatkit_store.py`
- [ ] T006 [P] Create `backend/.env.example` entry or verify `DATABASE_URL` already present; confirm `settings.database_url` is accessible in `backend/src/config.py` — `backend/src/config.py`

**Checkpoint**: Run `uv run pytest tests/unit/test_chatkit_store.py -v` — all store tests pass before Phase 3

---

## Phase 3: User Story 1 — Real-Time Streaming Chat (Priority: P1) 🎯 MVP

**Goal**: A logged-in user sends a message to `POST /chatkit` and receives a real-time streaming SSE reply from the todo agent. First token appears within 2 seconds.

**Independent Test**: `POST /chatkit` with valid JWT + message "show my tasks" → `text/event-stream` response with streamed tokens.

**Acceptance Scenarios covered**: US1 scenarios 1, 2, 3 (streaming reply, first token timing, auth rejection)

- [ ] T007 [US1] Write unit tests for `TodoChatKitServer.respond()`: mock `TodoPostgresStore.load_thread_items` returns 2 items; mock `chatkit.agents.Runner.run_streamed`; assert `simple_to_agent_input` called with thread items; assert `stream_agent_response` events are yielded; assert agent has 5 tools registered — `backend/tests/unit/test_chatkit_server.py`
- [ ] T008 [US1] Create `TodoChatKitServer(ChatKitServer[ChatKitRequestContext])` with: module-level `TodoPostgresStore` instance and `AsyncOpenAI` OpenRouter client; `respond()` method that loads last 20 thread items via `self.store.load_thread_items(thread.id, after=None, limit=20, order="asc", context=context)`, converts via `simple_to_agent_input()`, creates agent with 5 adapted tools + system prompt, runs `Runner.run_streamed()`, yields events via `stream_agent_response()`; 5 adapter functions that bridge `RunContextWrapper[AgentContext]` → `mcp_server.call_tool()` via `context.request_context` — `backend/src/chatkit/server.py`
- [ ] T009 [US1] Write integration tests for `POST /chatkit`: 200 + `text/event-stream` response with valid JWT and mocked `TodoChatKitServer.respond`; 401 on missing `Authorization` header; 401 on invalid JWT — `backend/tests/integration/test_chatkit_api.py`
- [ ] T010 [US1] Create `POST /chatkit` FastAPI router: `APIRouter()` with no prefix; endpoint takes `request: Request`, `user_id: str = Depends(get_current_user)`, `session: Session = Depends(get_session)`; builds `ChatKitRequestContext(user_id, session)`; calls `chatkit_server.process(await request.body(), context)`; returns `StreamingResponse(result, media_type="text/event-stream")` or `Response(content=result.json, media_type="application/json")` based on `isinstance(result, StreamingResult)` — `backend/src/routers/chatkit.py`
- [ ] T011 [US1] Register `chatkit_router` in FastAPI app with `app.include_router(chatkit_router)` — `backend/src/main.py`
- [ ] T012 [P] [US1] Write frontend chat page tests: renders without crashing when authenticated; redirects to sign-in when unauthenticated; `<ChatKit>` component receives `Authorization: Bearer <token>` header — `frontend/src/app/dashboard/chat/__tests__/page.test.tsx`
- [ ] T013 [US1] Create `/dashboard/chat` page: server component checks `auth.api.getSession()` and redirects to `/sign-in` if not authenticated; client component with `"use client"` directive renders `<ChatKit api={{ url: \`${process.env.NEXT_PUBLIC_BACKEND_URL}/chatkit\`, headers: { Authorization: \`Bearer ${getJwtToken()}\` } }} />` — `frontend/src/app/dashboard/chat/page.tsx`

**Checkpoint**: Backend running + frontend running → open `/dashboard/chat` → type "show my tasks" → verify streaming reply appears

---

## Phase 4: User Story 2 — All Five Task Operations (Priority: P2)

**Goal**: All 5 MCP tool operations (add, list, complete, update, delete) are accessible via the chat interface through natural language.

**Independent Test**: In one chat session, send 5 messages exercising each operation and verify each one produces a correct DB change + streaming confirmation reply.

**Acceptance Scenarios covered**: US2 scenarios 1–5 (all 5 task operations)

- [ ] T014 [US2] Extend integration tests with tool operation coverage: `POST /chatkit` with mocked `respond` returning `add_task` tool name → verify streaming reply contains "Created task"; `list_tasks` tool → verify reply contains task list; `complete_task` → verify completion text; `update_task` → verify update text; `delete_task` → verify deletion text — `backend/tests/integration/test_chatkit_api.py`

**Checkpoint**: All 5 tool verbs reachable via chat — verified manually with real OpenRouter call

---

## Phase 5: User Story 3 — Conversation Context (Priority: P3)

**Goal**: The chat maintains context within a thread. A follow-up message in the same thread receives prior history as context. A new thread starts with no history.

**Independent Test**: Send "add groceries" then "also add milk" with the same thread ID → two tasks created, second reply shows awareness of first.

**Acceptance Scenarios covered**: US3 scenarios 1, 2

- [ ] T015 [US3] Extend integration tests with multi-turn coverage: send 2 messages with same thread_id → assert `load_thread_items` is called with correct thread_id; send without thread_id → assert new thread created; second message in new thread has no prior history — `backend/tests/integration/test_chatkit_api.py`

**Checkpoint**: Run `uv run pytest tests/integration/test_chatkit_api.py -k "us3" -v` — all US3 tests pass

---

## Phase 6: User Story 4 — Graceful Error Handling (Priority: P4)

**Goal**: Provider down → friendly error in chat. Off-topic message → scope explanation. Session expired → redirect to login.

**Independent Test**: Mock OpenRouter to raise `ConnectionError` → verify 503 with user-friendly message, no blank screen.

**Acceptance Scenarios covered**: US4 scenarios 1, 2, 3

- [ ] T016 [US4] Extend integration tests with error scenario coverage: OpenRouter raises `ConnectionError` → 503 response; off-topic message with mocked agent reply → 200 with scope explanation text; missing JWT → 401 — `backend/tests/integration/test_chatkit_api.py`

**Checkpoint**: Run `uv run pytest tests/integration/test_chatkit_api.py -k "us4" -v` — all US4 tests pass

---

## Phase 7: Polish & Navigation

**Purpose**: Complete the UI integration — add Chat to the sidebar nav and environment variable documentation.

- [ ] T017 [P] Add "Chat" navigation item to the dashboard sidebar linking to `/dashboard/chat`; use the existing nav item component and styling pattern — `frontend/src/app/dashboard/components/Sidebar.tsx`
- [ ] T018 [P] Add `NEXT_PUBLIC_BACKEND_URL=http://localhost:8000` to `frontend/.env.example` if not already present; add comment explaining it points to the FastAPI backend — `frontend/.env.example`
- [ ] T019 [P] Verify `backend/src/chatkit/store.py` calls `_init_schema()` at module level so `chatkit_threads` and `chatkit_items` tables are auto-created on startup — `backend/src/chatkit/store.py`

---

## Dependency Graph

```
T001 (backend deps)
T002 [P] (frontend deps)
  │
  ├── T003 (__init__.py)
  │       └── T004 [P] (store impl) ─┐
  │       └── T005 [P] (store tests)─┴── T006 [P] (config verify)
  │                                        │
  │                                   T007 (server unit tests)
  │                                        └── T008 (server impl)
  │                                               └── T009 (router integration tests)
  │                                                     └── T010 (router impl)
  │                                                           └── T011 (register in main.py)
  │
  └── T002 (npm install) ─────────────────────────────────────────
            └── T012 [P] (frontend page tests)
                  └── T013 (chat page impl)
                        └── T017 (sidebar nav)

T014 (US2 integration tests) — after T011
T015 (US3 integration tests) — after T011
T016 (US4 integration tests) — after T011
T018 [P] (env example) — independent
T019 [P] (schema init verify) — after T004
```

---

## Parallel Execution Opportunities

**Phase 1** (T001 + T002): Backend and frontend deps install in parallel.

**Phase 2** (T004 + T005 + T006): Store implementation, store tests, and config verify are all different files — can run in parallel after T003.

**Phase 3** (T012 + T007): Frontend page tests and backend server unit tests are independent — can run in parallel.

**Phase 7** (T017 + T018 + T019): Sidebar, env file, schema verify are fully independent.

---

## Implementation Strategy

**Deliver US1 first (MVP)**. US1 requires T001–T013 complete — this is a full working streaming chat from browser to agent. Demonstrable and testable independently.

**US2 is covered by T014** — the 5 tools already exist in the server. T014 adds integration test coverage for each operation. No new code needed if the adapter tools work correctly.

**US3 is covered by T015** — thread history loading is built into the store + server. T015 adds the multi-turn test coverage.

**US4 is covered by T016** — error paths are part of T010's router implementation. T016 adds targeted error scenario tests.

---

## Full Test Run

```bash
# Backend unit tests
cd backend
uv run pytest tests/unit/test_chatkit_store.py -v
uv run pytest tests/unit/test_chatkit_server.py -v

# Backend integration tests
uv run pytest tests/integration/test_chatkit_api.py -v

# All backend tests
uv run pytest tests/ -v --tb=short

# Frontend tests
cd frontend
npm test -- --testPathPattern=dashboard/chat
```

---

## Task Summary

| Phase | Tasks | Parallelizable | Story |
|-------|-------|---------------|-------|
| Phase 1: Setup | T001–T002 | T002 | — |
| Phase 2: Foundational | T003–T006 | T004, T005, T006 | — |
| Phase 3: US1 (MVP) | T007–T013 | T012 | US1 |
| Phase 4: US2 | T014 | — | US2 |
| Phase 5: US3 | T015 | — | US3 |
| Phase 6: US4 | T016 | — | US4 |
| Phase 7: Polish | T017–T019 | T017, T018, T019 | — |
| **Total** | **19 tasks** | **9 parallelizable** | |
