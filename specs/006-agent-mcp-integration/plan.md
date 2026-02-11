# Implementation Plan: AI Agent MCP Integration

**Branch**: `006-agent-mcp-integration` | **Date**: 2026-02-11 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/006-agent-mcp-integration/spec.md`

---

## Summary

Add a stateless `POST /api/{user_id}/chat` endpoint to the FastAPI backend. The endpoint receives a natural language message, runs an OpenAI Agents SDK agent equipped with 5 function tools wrapping the existing `TodoMCPServer`, persists the conversation to PostgreSQL, and returns the agent's response. Two new database models (`Conversation`, `Message`) store conversation state so the server holds zero in-memory state between requests.

---

## Technical Context

**Language/Version**: Python 3.11+ (existing backend)
**Primary Dependencies**: FastAPI, SQLModel, OpenAI Agents SDK (`openai-agents`), `openai` (for AsyncOpenAI client)
**Storage**: Neon Serverless PostgreSQL (existing engine, sync SQLModel Session)
**Testing**: pytest + pytest-asyncio, httpx TestClient (existing pattern)
**Target Platform**: Linux server (Vercel/backend deployment)
**Project Type**: Web application — monorepo backend (`backend/`)
**Performance Goals**: Agent response < 5s (constitutional requirement XIV)
**Constraints**: Stateless endpoint (constitution IX); agent MUST NOT directly access DB (constitution XII); MCP server is the only interface to task logic (constitution XII)
**Scale/Scope**: 10 concurrent users (spec SC-004)

---

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| I. TDD | ✅ PASS | Tests written before implementation (red-green-refactor) |
| II. No Manual Coding | ✅ PASS | All code generated via Claude Code per spec |
| III. Code Quality | ✅ PASS | Type hints, Pydantic validation, 70% coverage target |
| VIII. Persistent Storage | ✅ PASS | Conversation + Message persisted to PostgreSQL |
| IX. Stateless Chat | ✅ PASS | History fetched from DB per request, no in-memory state |
| X. User Isolation | ✅ PASS | `user_id` filters all DB queries; conversation ownership enforced |
| XI. Authentication | ✅ PASS | Existing JWT dependency reused on chat endpoint |
| XII. AI Architecture | ✅ PASS | Agent uses MCP tools; no direct DB access from agent |
| XIII. MCP Governance | ✅ PASS | Each tool is atomic, validated, stateless, user-isolated |
| XIV. Performance | ✅ PASS | SC-001 targets < 5s (matches constitutional limit) |

**Gate**: All checks pass. Proceeding to Phase 1 design.

---

## Project Structure

### Documentation (this feature)

```text
specs/006-agent-mcp-integration/
├── plan.md              ✅ This file
├── research.md          ✅ Phase 0 complete
├── data-model.md        ✅ Phase 1 complete
├── quickstart.md        ✅ Phase 1 complete
├── contracts/
│   └── chat-endpoint.md ✅ Phase 1 complete
└── tasks.md             ⏳ Phase 2 — /sp.tasks command
```

### Source Code Changes

```text
backend/
├── src/
│   ├── models/
│   │   ├── conversation.py        NEW  — Conversation SQLModel table
│   │   └── message.py             NEW  — Message SQLModel table
│   ├── schemas/
│   │   └── chat.py                NEW  — ChatRequest, ChatResponse Pydantic schemas
│   ├── crud/
│   │   └── chat.py                NEW  — Conversation and Message CRUD functions
│   ├── agents/
│   │   └── todo_agent.py          NEW  — TodoAgent with 5 MCP-backed function tools
│   └── routers/
│       └── chat.py                NEW  — POST /api/{user_id}/chat router
├── src/db/database.py             MODIFY — import new models for auto table creation
├── src/main.py                    MODIFY — register chat router
└── tests/
    ├── unit/
    │   └── test_chat_crud.py      NEW  — unit tests for conversation/message CRUD
    └── integration/
        └── test_chat_api.py       NEW  — integration tests for chat endpoint
```

**Structure Decision**: Web application (Option 2). Backend-only changes. No frontend changes in this feature.

---

## Architecture

```
POST /api/{user_id}/chat
        │
        ▼
┌──────────────────────────────────┐
│   chat.py router (FastAPI)       │
│                                  │
│  1. Validate JWT (existing dep)  │
│  2. Resolve/create Conversation  │
│  3. Persist user Message (DB)    │
│  4. Load last 50 Messages (DB)   │
│  5. Build agent input            │
│  6. await Runner.run(agent, ...) │
│  7. Persist assistant Message    │
│  8. Return ChatResponse          │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│   todo_agent.py                  │
│   Agent + 5 function tools       │
│   (OpenAI Agents SDK)            │
│   Provider: OpenRouter           │
└──────────┬───────────────────────┘
           │ calls
           ▼
┌──────────────────────────────────┐
│   TodoMCPServer.call_tool()      │
│   (existing, unchanged)          │
│   add_task / list_tasks /        │
│   complete_task / update_task /  │
│   delete_task                    │
└──────────┬───────────────────────┘
           │ reads/writes
           ▼
┌──────────────────────────────────┐
│   Neon PostgreSQL                │
│   (tasks, conversations,         │
│    messages tables)              │
└──────────────────────────────────┘
```

---

## Implementation Phases

### Phase A: Data Layer (models + CRUD)

1. Create `src/models/conversation.py` — `Conversation` SQLModel
2. Create `src/models/message.py` — `Message` SQLModel
3. Update `src/db/database.py` — import new models
4. Create `src/schemas/chat.py` — `ChatRequest`, `ChatResponse` Pydantic models
5. Create `src/crud/chat.py` — CRUD: create_conversation, get_conversation, add_message, get_messages
6. Write `tests/unit/test_chat_crud.py` — unit tests for CRUD functions

### Phase B: Agent Layer

7. Create `src/agents/todo_agent.py`:
   - Instantiate `TodoMCPServer`
   - Define 5 `@function_tool` wrappers (one per MCP tool), each passing `user_id` and DB `session`
   - Create `Agent` with OpenRouter model + tools + system prompt
   - Expose `run_agent(messages, user_id, session) -> (response_text, tool_calls)`

### Phase C: API Layer

8. Create `src/routers/chat.py`:
   - `POST /api/{user_id}/chat` handler
   - Stateless flow: resolve conversation → persist user message → load history → run agent → persist response → return
   - 503 on AI provider failure; 404 on unknown conversation_id; 401 on auth failure
9. Update `src/main.py` — register chat router

### Phase D: Integration Tests

10. Write `tests/integration/test_chat_api.py`:
    - Test new conversation creation (returns conversation_id)
    - Test continuation with conversation_id
    - Test each MCP tool via natural language
    - Test 401 on missing auth
    - Test 404 on unknown conversation_id
    - Test 503 on mocked provider failure

---

## Key Design Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| MCP integration pattern | Function tool wrappers | In-process server, no subprocess needed |
| Agent state | Stateless, created per request | Satisfies constitution IX |
| DB session in agent tools | Passed via closure from router | Session lifetime matches request |
| Conversation history cap | Last 50 messages | From spec clarification (Q1) |
| Provider failure | 503 immediately, no retry | From spec clarification (Q2) |
| Concurrent requests | Process independently | From spec clarification (Q3) |
| Stored roles | user + assistant only | From spec clarification (Q4) |
| LLM provider | OpenRouter via `OpenAIChatCompletionsModel` | Already in settings; verified against skill template |
| `RunConfig` | `RunConfig(model=model, model_provider=client, tracing_disabled=True)` | **Required** for non-OpenAI providers — tracing_disabled prevents SDK errors |

---

## Complexity Tracking

No constitutional violations. No complexity justification needed.
