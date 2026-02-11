# Tasks: AI Agent MCP Integration

**Feature**: 006-agent-mcp-integration | **Branch**: `006-agent-mcp-integration`
**Input**: specs/006-agent-mcp-integration/{plan.md, spec.md, data-model.md, contracts/, research.md}
**Date**: 2026-02-11

---

## Format: `- [ ] [ID] [P?] [Story?] Description — file path`

- **[P]**: Parallelizable (different files, no blocking dependency)
- **[US1/US2/US3]**: User Story scope (matches spec.md priorities)
- **Setup/Foundational tasks**: no story label

---

## Phase 1: Setup

**Purpose**: Verify the existing project has everything needed before writing new code.

- [X] T001 Verify `openai-agents>=0.2.0` is listed in `backend/pyproject.toml` dependencies and confirm `src/agents/`, `src/schemas/`, `src/crud/`, `tests/unit/`, `tests/integration/` directories all exist

**Checkpoint**: Environment confirmed — proceed to Phase 2

---

## Phase 2: Foundational (Data Layer)

**Purpose**: New DB models, schemas, and CRUD functions that ALL user stories depend on. No user story work can begin until this phase is complete.

**⚠️ CRITICAL**: T002–T007 must be completed before Phase 3

- [X] T002 [P] Create Conversation SQLModel table model (fields: id, user_id, created_at, updated_at; FK to user.id, index on user_id, Relationship to Message) — `backend/src/models/conversation.py`
- [X] T003 [P] Create Message SQLModel table model (fields: id, conversation_id, user_id, role, content, created_at; FK constraints, indexes on conversation_id and user_id, Relationship back to Conversation) — `backend/src/models/message.py`
- [X] T004 Update database.py to import Conversation and Message so SQLModel.metadata.create_all() creates both tables automatically — `backend/src/db/database.py`
- [X] T005 [P] Create ChatRequest (message: str 1–5000 chars, conversation_id: int | None) and ChatResponse (conversation_id: int, response: str, tool_calls: list[str]) Pydantic schemas — `backend/src/schemas/chat.py`
- [X] T006 Create CRUD functions: `create_conversation(user_id, session)`, `get_conversation(conversation_id, user_id, session)` (returns None if not found or wrong owner), `add_message(conversation_id, user_id, role, content, session)`, `get_messages(conversation_id, user_id, limit, session)` (last 50 ordered by created_at ASC) — `backend/src/crud/chat.py`
- [X] T007 Write unit tests covering: create_conversation returns Conversation with correct user_id; get_conversation returns None for wrong user_id (isolation enforced); add_message persists role and content; get_messages returns max 50 ordered correctly; get_messages with wrong user_id returns empty list — `backend/tests/unit/test_chat_crud.py`
- [X] T007a [P] Verify `backend/pyproject.toml` pytest configuration includes `--cov=src --cov-fail-under=70`; add it to the `[tool.pytest.ini_options]` `addopts` entry if absent (constitution III: 70% minimum coverage) — `backend/pyproject.toml`

**Checkpoint**: Run `uv run pytest tests/unit/test_chat_crud.py -v` — all tests must pass before Phase 3

---

## Phase 3: User Story 1 — Natural Language Task Management (Priority: P1) 🎯 MVP

**Goal**: A logged-in user sends a natural language message and the agent invokes the correct MCP tool, returns a confirmation, and all 5 task operations are accessible conversationally.

**Independent Test**: `POST /api/{user_id}/chat` with "Add a task to buy groceries" → task created in DB, response contains confirmation text.

**Acceptance Scenarios covered**: All 5 from US1 (add, list, complete, delete, update via natural language)

- [X] T007b [US1] Write unit tests for all 5 agent tool functions with a mocked `TodoMCPServer.call_tool`: add_task returns "Created task: X (ID: N)"; list_tasks returns formatted task list string; complete_task returns completion confirmation; delete_task returns deletion confirmation; update_task returns update confirmation; on `isError=True` each tool returns the error text (constitution I: TDD — tests before T008 implementation) — `backend/tests/unit/test_todo_agent.py`
- [X] T008 [US1] Create `TodoContext` dataclass (user_id: str, session: Session), instantiate TodoMCPServer at module level, implement 5 `@function_tool` functions each using `RunContextWrapper[TodoContext]` as first param and calling `mcp_server.call_tool(...)` with context injection; each tool must have a descriptive docstring; extract clean string from `structuredContent` (not raw MCP dict); on `isError` return the error text — `backend/src/agents/todo_agent.py`
- [X] T009 [US1] Implement `run_todo_agent(messages, user_id, session) -> tuple[str, list[str]]` that builds TodoContext, constructs OpenRouter AsyncOpenAI client + OpenAIChatCompletionsModel + RunConfig(tracing_disabled=True), creates Agent with system prompt + 5 tools, calls `await Runner.run(agent, messages, context=ctx, max_turns=10, run_config=run_config)`, returns `(result.final_output, [item.tool_name for item in result.new_items if hasattr(item, "tool_name")])` — `backend/src/agents/todo_agent.py`
- [X] T010 [US1] Create `POST /api/{user_id}/chat` router: use `response_model=ChatResponse`; inject `SessionDep = Annotated[Session, Depends(get_session)]` and existing JWT auth dependency; implement stateless flow in this EXACT order: (1) resolve/create Conversation, (2) persist and COMMIT user Message (user message must survive provider failures — do NOT defer commit), (3) load last 50 Messages, (4) build input list (role/content dicts), (5) `await run_todo_agent(...)`, (6) persist assistant Message + update conversation.updated_at + commit; on provider exception at step 5: raise HTTPException(503, detail="AI provider unavailable") WITHOUT rollback (user message already committed); on conversation not found: HTTPException(404, detail="Conversation not found") — `backend/src/routers/chat.py`
- [X] T011 [US1] Register `chat_router` with prefix `/api/{user_id}` in the FastAPI app — `backend/src/main.py`
- [X] T012 [P] [US1] Write integration tests for US1: new conversation creation (no conversation_id → 200 OK with new conversation_id in response body); add_task via natural language (task appears in DB); list_tasks via "show my tasks"; complete_task via "mark task N as done"; delete_task via "delete task N"; update_task via "change task N to X"; 401 on missing/invalid auth token; provider failure (mocked) → 503 AND user message still persisted in DB — `backend/tests/integration/test_chat_api.py`

**Checkpoint**: Run `uv run pytest tests/integration/test_chat_api.py -k "us1" -v` — all US1 tests pass

---

## Phase 4: User Story 2 — Persistent Conversation Context (Priority: P2)

**Goal**: Multi-turn conversations work correctly. History is loaded from DB per request. Server restart does not lose context. New conversation_id is returned on first message.

**Independent Test**: Send two consecutive messages — first creating a task, then referencing "it" in follow-up — agent resolves the reference using loaded history.

**Acceptance Scenarios covered**: All 3 from US2 (multi-turn context; new session returns ID; restart persistence)

- [X] T013 [US2] Extend integration test file with US2 tests: continuation with conversation_id loads prior history correctly; "also add milk" follow-up after "add groceries" creates second task (agent uses context); new session (no conversation_id) returns fresh conversation_id with no prior history; same conversation_id after mock server restart still loads history from DB — `backend/tests/integration/test_chat_api.py`

**Checkpoint**: Run `uv run pytest tests/integration/test_chat_api.py -k "us2" -v` — all US2 tests pass

---

## Phase 5: User Story 3 — Graceful Error Handling (Priority: P3)

**Goal**: All error paths return human-readable messages. No raw exceptions exposed. Off-topic messages handled gracefully. Provider failure returns 503.

**Independent Test**: Ask agent to complete task 999 (non-existent) → agent returns friendly message, no 500 error.

**Acceptance Scenarios covered**: All 3 from US3 (task not found; off-topic; DB error)

- [X] T014 [US3] Extend integration test file with US3 tests: task-not-found returns 200 with friendly agent message (not 500); off-topic message ("what's the weather?") returns 200 with helpful scope explanation; 503 returned when OpenRouter client is mocked to raise an exception; 404 returned when conversation_id belongs to a different user; empty message body returns 400 (Pydantic validation); message > 5000 chars returns 400 (Pydantic validation) — `backend/tests/integration/test_chat_api.py`

**Checkpoint**: Run `uv run pytest tests/integration/test_chat_api.py -k "us3" -v` — all US3 tests pass

---

## Phase 6: Polish & Environment

**Purpose**: Documentation and environment variable completeness.

- [X] T015 [P] Add `OPENROUTER_API_KEY`, `LLM_MODEL`, and `LLM_PROVIDER` entries with example values and comments to the backend environment example file — `backend/.env.example`
- [X] T016 [P] Verify `backend/src/agents/todo_agent.py` reads `openrouter_api_key` and `llm_model` from `settings` (Pydantic Settings) — not hardcoded; confirm `backend/src/config.py` already exposes these fields (no change needed if already present)

---

## Dependency Graph

```
T001
  ├── T002 [P] ──┐
  ├── T003 [P] ──┴── T004
  ├── T005 [P] ────── (independent of T004)
  └── T007a [P] ───── (independent, coverage gate)
                       T004
                         └── T006
                               └── T007
                                     └── T007b [US1] (agent unit tests — TDD gate for T008)
                                           └── T008
                                                 └── T009
                                                       └── T010
                                                             └── T011
                                                                   └── T012 [P] (US1 integration tests)
                                                                         └── T013 (US2 tests)
                                                                               └── T014 (US3 tests)

T015 [P] ── independent
T016 [P] ── independent
```

---

## Parallel Execution Opportunities

**Within Phase 2** (after T001):
- T002, T003, T005 can run simultaneously (different files)
- T004, T006 can start after T002 + T003 complete
- T007 can start immediately after T006

**Within Phase 3** (after T007 passes):
- T008 + T009 must be sequential (same file, dependent)
- T012 integration tests can be started alongside T010/T011 as stubs

**Within Phase 6** (any point):
- T015 and T016 are fully independent of all other phases

---

## Implementation Strategy

**Deliver US1 first (MVP)**. US1 covers all 5 MCP tools and the core stateless flow — T001 through T012. This is a complete, demonstrable chatbot endpoint.

**US2 is tested by T013 only** — the implementation is already built into the stateless router (history loading in T010). T013 adds the multi-turn test coverage.

**US3 is tested by T014 only** — graceful agent responses and HTTP error codes are part of T010's error handling. T014 adds targeted error scenario tests.

---

## Full Test Run

```bash
cd backend

# Phase 2 gate
uv run pytest tests/unit/test_chat_crud.py -v

# Full integration suite
uv run pytest tests/integration/test_chat_api.py -v

# All tests
uv run pytest tests/ -v --tb=short
```

---

## Task Summary

| Phase | Tasks | Parallelizable | Story |
|-------|-------|---------------|-------|
| Phase 1: Setup | T001 | — | — |
| Phase 2: Foundational | T002–T007, T007a | T002, T003, T005, T007a | — |
| Phase 3: US1 (MVP) | T007b, T008–T012 | T012 | US1 |
| Phase 4: US2 | T013 | — | US2 |
| Phase 5: US3 | T014 | — | US3 |
| Phase 6: Polish | T015–T016 | T015, T016 | — |
| **Total** | **19 tasks** | **7 parallelizable** | |
