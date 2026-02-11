---
id: "0008"
title: chatkit-server-skill-analysis
stage: general
date: 2026-02-11
surface: backend
model: claude-haiku-4-5-20251001
feature: none
branch: feat/overhaul-openai-agents-sdk-skill
user: AbdullahQureshi
command: manual
labels: [general, chatkit, skill-analysis, phase3]
links:
  spec: ""
  ticket: ""
  adr: ""
  pr: ""
files:
  - .claude/skills/chatkit-server/SKILL.md
tests:
  - N/A (analysis only)
---

## Prompt

analyze the skill 'chatkit-server' and tell me what it does? Your task is to create a detailed summary of what the skill does, how it works, and how it can be used to wire the ChatKit UI frontend to the existing backend chat endpoint.

## Response snapshot

**Skill**: `chatkit-server` — Builder + Guide for `openai-chatkit` (Python) + FastAPI backends.

**Three build levels**:
- Level 1: Hello World — minimal ChatKitServer subclass, InMemoryStore, hardcoded response
- Level 2 (default): Agent integration — OpenAI Agents SDK wired in, thread history, streaming via `stream_agent_response()`
- Level 3: Production — Better Auth JWT RequestContext, PostgreSQL Store, server tools, widgets, CORS

**Architecture**: Frontend ChatKit UI → `POST /chatkit` → `ChatKitServer.process()` → `respond()` → `Runner.run_streamed()` → SSE streaming back

**Key relevance**: This skill generates the ChatKit-protocol endpoint required for Phase III. Our existing `POST /api/{user_id}/chat` is stateless/JSON; ChatKit UI requires a streaming SSE endpoint via `ChatKitServer`. The skill would wrap `run_todo_agent()` in a `ChatKitServer.respond()` method and register a `/chatkit` router with JWT auth from Better Auth.

## Outcome

- ✅ Impact: Identified the exact skill needed for Phase III ChatKit frontend integration
- 🧪 Tests: N/A (analysis only)
- 📁 Files: .claude/skills/chatkit-server/SKILL.md (read only)
- 🔁 Next prompts: Invoke chatkit-server skill at Level 3 to build `/chatkit` endpoint wrapping `run_todo_agent()`
- 🧠 Reflection: ChatKit requires a distinct SSE streaming endpoint — not compatible with the stateless JSON `/api/{user_id}/chat` pattern. Two coexist: stateless for programmatic use, ChatKit endpoint for the UI

## Evaluation notes (flywheel)

- Failure modes observed: None — pure read/analysis
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment: Invoke /chatkit-server skill at Level 3, wire to existing run_todo_agent() and Better Auth JWT
