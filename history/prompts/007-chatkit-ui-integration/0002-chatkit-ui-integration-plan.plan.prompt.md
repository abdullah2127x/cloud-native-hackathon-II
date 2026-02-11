---
id: "0002"
title: chatkit-ui-integration-plan
stage: plan
date: 2026-02-11
surface: fullstack
model: claude-haiku-4-5-20251001
feature: 007-chatkit-ui-integration
branch: 007-chatkit-ui-integration
user: AbdullahQureshi
command: /sp.plan
labels: [plan, chatkit, streaming, sse, postgres-store, fullstack, phase3]
links:
  spec: specs/007-chatkit-ui-integration/spec.md
  ticket: ""
  adr: ""
  pr: ""
files:
  - specs/007-chatkit-ui-integration/plan.md
  - specs/007-chatkit-ui-integration/research.md
  - specs/007-chatkit-ui-integration/data-model.md
  - specs/007-chatkit-ui-integration/contracts/chatkit-endpoint.md
tests:
  - N/A (plan stage)
---

## Prompt

/sp.plan (for feature 007-chatkit-ui-integration — ChatKit streaming UI integration)

## Response snapshot

**Plan**: `specs/007-chatkit-ui-integration/plan.md`

**Architecture**: Browser → ChatKit UI → POST /chatkit (SSE) → TodoChatKitServer → chatkit.agents.Runner.run_streamed() → 5 adapted tools → mcp_server → DB

**Key decisions**:
1. PostgresStore with 2 new tables (chatkit_threads, chatkit_items) — not bridging to feature 006 tables
2. chatkit.agents.Runner.run_streamed() + stream_agent_response() for SSE — not calling run_todo_agent() directly
3. Tool adapter pattern: 5 thin wrappers bridging AgentContext → TodoContext → mcp_server
4. Existing get_current_user dependency reused for JWT auth
5. New route /dashboard/chat in Next.js dashboard

**5 Phases**: P0 deps, P1 store TDD, P2 server TDD, P3 router TDD, P4 frontend TDD, P5 polish

**New files**: backend/src/chatkit/{store,server}.py, backend/src/routers/chatkit.py, frontend/src/app/dashboard/chat/page.tsx

**Constitution check**: PASS (all 9 relevant principles satisfied)

## Outcome

- ✅ Impact: Complete implementation plan for Phase III ChatKit streaming UI integration
- 🧪 Tests: N/A (plan stage)
- 📁 Files: plan.md, research.md, data-model.md, contracts/chatkit-endpoint.md
- 🔁 Next prompts: /sp.tasks to generate atomic task list
- 🧠 Reflection: Tool adaptation (AgentContext → TodoContext) is the critical design decision — adapter wrapper pattern is cleaner than modifying existing tools

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution check — PASS
- Prompt variant (if applicable): N/A
- Next experiment: /sp.tasks for 007 — verify parallel opportunities (store vs frontend are independent)
