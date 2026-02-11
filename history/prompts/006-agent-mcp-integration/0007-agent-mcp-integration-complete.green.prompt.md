---
id: "0007"
title: agent-mcp-integration-complete
stage: green
date: 2026-02-11
surface: backend
model: claude-haiku-4-5-20251001
feature: 006-agent-mcp-integration
branch: feat/overhaul-openai-agents-sdk-skill
user: AbdullahQureshi
command: /sp.implement
labels: [green, backend, agents, mcp, fastapi, tdd]
links:
  spec: specs/006-agent-mcp-integration/spec.md
  ticket: ""
  adr: ""
  pr: ""
files:
  - backend/src/agents/todo_agent.py
  - backend/src/routers/chat.py
  - backend/src/main.py
  - backend/tests/unit/test_todo_agent.py
  - backend/tests/integration/test_chat_api.py
  - backend/tests/conftest.py
tests:
  - tests/unit/test_todo_agent.py (10 pass)
  - tests/unit/test_chat_crud.py (11 pass)
  - tests/integration/test_chat_api.py (17 pass)
  - Full suite: 266 pass, 80.29% coverage
---

## Prompt

Continue /sp.implement for feature 006-agent-mcp-integration. All Phase 2 tasks (T001-T007a) were complete. T007b (agent unit tests) had been written and were failing with `TypeError: 'FunctionTool' object is not callable`. Debugging and completing T007b through T016.

## Response snapshot

**Root cause of T007b failure**: `@function_tool` decorator wraps async functions into `FunctionTool` objects, which are not directly callable. Tests called `await add_task(...)` expecting a coroutine.

**Fix**: Separated raw async implementations from `FunctionTool` wrappers. Raw async functions (`add_task`, `list_tasks`, etc.) remain directly testable. `FunctionTool` wrappers created via `function_tool(add_task)` and named `_add_task_tool` etc. Agent uses the tool wrappers; tests call the raw functions.

**Tasks completed**:
- T007b ✅ — 10 unit tests for 5 tool functions all pass
- T008/T009 ✅ — `todo_agent.py` with `TodoContext`, 5 tools, `run_todo_agent()`
- T010 ✅ — `POST /api/{user_id}/chat` stateless endpoint with correct commit ordering
- T011 ✅ — `chat_router` registered in `main.py`
- T012/T013/T014 ✅ — 17 integration tests (US1/US2/US3) all pass
- T015/T016 ✅ — env vars and config already present, verified

## Outcome

- ✅ Impact: Complete AI agent MCP integration — stateless chat endpoint wires OpenAI Agents SDK + in-process MCP server via JWT-authenticated FastAPI endpoint
- 🧪 Tests: 266 pass, 80.29% coverage (exceeds 70% constitution requirement)
- 📁 Files: todo_agent.py, chat.py router, conftest.py updated, test_todo_agent.py, test_chat_api.py
- 🔁 Next prompts: Frontend ChatKit integration, E2E testing with real OpenRouter key
- 🧠 Reflection: `@function_tool` creates `FunctionTool` objects not directly callable — keep raw async functions separate from tool wrappers for testability

## Evaluation notes (flywheel)

- Failure modes observed: `@function_tool` decorator incompatibility with direct async call in tests
- Graders run and results (PASS/FAIL): uv run pytest — 266 passed, 80.29% coverage PASS
- Prompt variant (if applicable): N/A
- Next experiment: Consider using `function_tool` with `strict_mode=False` for optional params in future
