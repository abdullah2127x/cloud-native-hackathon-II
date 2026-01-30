---
id: {{ID}}
title: {{TITLE}}
stage: {{STAGE}}
date: {{DATE_ISO}}
surface: {{SURFACE}}
model: {{MODEL}}
feature: {{FEATURE}}
branch: {{BRANCH}}
user: {{USER}}
command: {{COMMAND}}
labels: [{{LABELS}}]
links:
  spec: {{LINKS_SPEC}}
  ticket: {{LINKS_TICKET}}
  adr: {{LINKS_ADR}}
  pr: {{LINKS_PR}}
files:
{{FILES_YAML}}
tests:
{{TESTS_YAML}}
---

## Prompt

Implement the following plan: [003-modern-ui-dashboard plan.md - Comprehensive Modern UI Dashboard Transformation plan with 7 user stories, zero backend changes, fully researched and designed]

Generate tasks.md with 95 atomic, dependency-ordered implementation tasks organized by user story (P1-P3 priorities) for frontend-only Next.js + shadcn/ui transformation of todo application.

## Response snapshot

Generated `specs/003-modern-ui-dashboard/tasks.md` (95 tasks):
- Phase 1: Setup & Routing (4 tasks)
- Phase 2: Foundational Components (9 tasks) [BLOCKING]
- Phase 3: Landing Page / US1 (9 tasks)
- Phase 4: Authentication / US2 (9 tasks)
- Phase 5: Dashboard Navigation / US3 (11 tasks)
- Phase 6: Overview Statistics / US4 (9 tasks)
- Phase 7: Todos Management / US5 (18 tasks) [CORE]
- Phase 8: Priority Organization / US6 (7 tasks)
- Phase 9: Tags Organization / US7 (9 tasks)
- Phase 10: Polish & Cross-Cutting (10 tasks)

All tasks marked with [P] for parallelization, [US#] for user story traceability, exact file paths.

## Outcome

- ✅ Impact: Transformed plan → executable task list; teams can now implement in parallel or serial; MVP-scoped incremental delivery enabled
- 🧪 Tests: No tests required per spec (testing work deferred); tasks structured for TDD-ready implementation
- 📁 Files: 95 tasks across 10 phases, 18 new React components, 5 page modifications, zero backend changes
- 🔁 Next prompts: `/sp.implement` to start Phase 1 Setup, or use TaskUpdate to begin tracking task progress
- 🧠 Reflection: Task generation complete - specification fully decomposed into atomic, independently testable user story phases. Clear MVP boundary at Phase 7 (Todos) completion.

## Evaluation notes (flywheel)

- Failure modes observed: None - specification was sufficiently detailed, research questions resolved, no architectural unknowns remaining
- Graders run and results (PASS/FAIL): ✅ PASS - all 88 FRs addressable by 95 tasks; all 7 user stories have independent test criteria; constitutional compliance verified
- Prompt variant (if applicable): N/A - single direct implementation from finalized plan
- Next experiment (smallest change to try): Begin T001 (directory structure) as first implementation step; verify Phase 1 setup before proceeding to Phase 2
