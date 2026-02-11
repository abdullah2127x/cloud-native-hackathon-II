---
id: "0004"
title: Fix 4 remaining failing tests
stage: green
date: 2026-02-11T00:00:00Z
surface: project
model: claude-sonnet-4-5-20250929
feature: 005-mcp-todo-tools
branch: main
user: AbdullahQureshi
command: continue session
labels: [tests, bug-fix, tag-filter, auth-mock]
links:
  spec: specs/005-mcp-todo-tools/spec.md
  ticket: ""
  adr: ""
  pr: ""
files:
  - backend/src/routers/tasks.py
  - backend/tests/integration/test_tags_api.py
tests:
  - tests/integration/test_tags_api.py::test_api_get_tags_different_users_isolated
  - tests/integration/test_tasks_api_filter.py::test_api_filter_by_tags
  - tests/integration/test_tasks_api_filter.py::test_api_combined_filters
  - tests/integration/test_tasks_api_sort.py::test_api_sort_with_filters
---

## Prompt

Fix the 4 remaining failing tests (continued from previous session).

## Response snapshot

Fixed two root causes:

1. **Tag filter bug in router** (`src/routers/tasks.py`): `tags: list[str] = None` was not using `Query()`, so FastAPI did not parse `?tags=work` as a list query parameter — it remained `None`. Fixed by importing `Query` and changing to `tags: Optional[List[str]] = Query(default=None)`.

2. **User isolation test** (`tests/integration/test_tags_api.py::test_api_get_tags_different_users_isolated`): Test called `mock_auth.return_value = {"sub": "other-user-id"}` but the `mock_auth` fixture now yields `None` (it's a dependency override, not a Mock object). Rewrote the test to manipulate `app.dependency_overrides[get_current_user]` directly within the test body.

## Outcome

- ✅ Impact: 228 tests passing, 0 failing. Coverage 80.96% (above 70% threshold).
- 🧪 Tests: 228 passed, 5405 warnings
- 📁 Files: 2 files modified (router + test)
- 🔁 Next prompts: commit and push to remote
- 🧠 Reflection: FastAPI list query params require `Query()` annotation — without it, `list[str]` parameters are not parsed from the URL query string.

## Evaluation notes (flywheel)

- Failure modes observed: Missing `Query()` on list param; stale test using Mock API on a dependency override fixture
- Graders run and results (PASS/FAIL): pytest 228/228 PASS
- Prompt variant (if applicable): N/A
- Next experiment: N/A
