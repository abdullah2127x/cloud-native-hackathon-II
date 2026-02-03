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

User invoked `/sp.analyze` to validate artifacts before implementation. Command analyzed:
1. spec.md (88 FRs, 14 SCs, 7 user stories)
2. plan.md (5 phases, architecture, tech stack)
3. tasks.md (95 tasks, 10 phases, user story mapping)
4. data-model.md (zero DB changes, UI-only)
5. constitution.md (13 principles - compliance verification)

## Response snapshot

Generated comprehensive analysis report:
- **Coverage**: 102/102 requirements mapped (100%)
- **Quality**: 0 critical issues, 0 constitution violations
- **Tasks**: 95 atomic tasks across 10 phases
- **Findings**: 3 ambiguities (all resolved), 1 medium-priority clarification (not blocker)
- **Verdict**: ✅ READY FOR IMPLEMENTATION

Key findings:
1. All requirements mapped to supporting tasks
2. All 13 constitutional principles verified (PASS)
3. Parallelizable tasks identified (38/95 = 40%)
4. MVP boundary clear at Phase 7 completion
5. Edge cases enumerated and addressed
6. Non-functional requirements covered

Minor items (non-blocking):
- Tag input scope clarification recommended (single vs multi-tag)
- Dark mode deferral confirmed and acceptable
- Performance validation tools recommendation (Lighthouse suggested)

## Outcome

- ✅ Impact: Artifacts validated as production-ready; 0 blockers identified; 102/102 requirements covered by 95 executable tasks
- 🧪 Tests: Testing deferred per spec (out of scope); artifact quality validated through cross-reference analysis
- 📁 Files: ANALYSIS_REPORT.md generated (~600 lines) with detailed findings, severity matrix, and recommendations
- 🔁 Next prompts: `/sp.implement` to start Phase 1, or `/sp.clarify` if user wants clarifications before starting
- 🧠 Reflection: Artifact quality excellent across all four documents (spec, plan, tasks, data-model). Feature is well-scoped, architecture sound, and execution path clear. Ready for immediate implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None - all artifacts show high quality and internal consistency
- Graders run and results (PASS/FAIL): ✅ PASS - All requirements mapped, no constitution violations, no critical blockers
- Prompt variant (if applicable): N/A - standard /sp.analyze workflow applied
- Next experiment (smallest change to try): Proceed directly to Phase 1 Setup (T001-T004). If issues arise, return to analysis for specific artifact refinement.
