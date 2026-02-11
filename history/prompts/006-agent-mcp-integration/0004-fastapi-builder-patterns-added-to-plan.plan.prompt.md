---
id: "0004"
title: FastAPI Builder Patterns Added to Plan
stage: plan
date: 2026-02-11
surface: project
model: claude-haiku-4-5-20251001
feature: 006-agent-mcp-integration
branch: 006-agent-mcp-integration
user: AbdullahQureshi
command: manual (continued from context)
labels: [plan, fastapi-builder, anti-patterns, phase-c]
links:
  spec: specs/006-agent-mcp-integration/spec.md
  ticket: ""
  adr: ""
  pr: ""
files:
  - specs/006-agent-mcp-integration/plan.md
tests:
  - N/A (planning phase)
---

## Prompt

does the plan setteted the fastapi-builder skill

## Response snapshot

Invoked fastapi-builder skill. Read `references/anti-patterns.md` and `references/database.md`. Identified 3 gaps in plan.md that the fastapi-builder skill prescribes:

1. **`Annotated[Session, Depends(get_session)]` pattern** — anti-patterns.md explicitly flags `session: Session = Depends(get_session)` as BAD (fails Python 3.10+). Plan updated to require `SessionDep = Annotated[Session, Depends(get_session)]`.

2. **`response_model=ChatResponse` on decorator** — anti-patterns.md warns that returning objects without `response_model` can leak sensitive fields. Plan updated to require `response_model=ChatResponse` on the `POST /api/{user_id}/chat` decorator.

3. **`session.rollback()` on exceptions** — anti-patterns.md shows the pattern: on DB/provider failure, call `session.rollback()` before raising HTTPException. Plan updated Phase C to require rollback before 503 raise.

4. **Descriptive HTTPException details** — anti-patterns.md: use descriptive `detail` strings. Added to Phase C.

5. **Sync DB in async endpoint acknowledged** — anti-patterns.md flags `async def` + sync `Session` as technically BAD. Added to Key Design Decisions table as explicit acknowledged tradeoff (existing codebase is sync; migration out of scope; DB calls <5ms). Already documented in research.md Decision 5.

Updated `plan.md` Phase C step 8 and added 3 rows to Key Design Decisions table. Committed.

## Outcome

- ✅ Impact: plan.md now fully reflects both fastapi-builder and openai-agents-sdk skill requirements — all 5 missing patterns identified and addressed
- 🧪 Tests: N/A (planning phase)
- 📁 Files: specs/006-agent-mcp-integration/plan.md
- 🔁 Next prompts: `/sp.tasks` to generate atomic, dependency-ordered task list
- 🧠 Reflection: Key insight — always consult ALL relevant skills before finalizing a plan; fastapi-builder and openai-agents-sdk both contributed critical implementation constraints

## Evaluation notes (flywheel)

- Failure modes observed: Plan written without consulting fastapi-builder skill — missing Annotated pattern, response_model, rollback
- Graders run and results (PASS/FAIL): All gaps resolved — PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add a plan checklist that verifies all active skills have been consulted
