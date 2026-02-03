# Tasks: Todo Organization & Usability Features

**Input**: Design documents from `/specs/002-todo-organization-features/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/openapi.yaml, contracts/schemas.ts
**Constitution**: TDD required (70% coverage) - test tasks included

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)
- Paths: `backend/src/` for FastAPI, `frontend/src/` for Next.js

---

## Phase 1: Setup

**Purpose**: Extend existing project with Phase 2 infrastructure

- [X] T001 Create database migration script for priority column and tag tables in backend/migrations/002_add_priority_and_tags.sql
- [X] T002 [P] Create Priority enum in backend/src/models/priority.py per data-model.md
- [X] T003 [P] Copy Zod schemas from contracts/schemas.ts to frontend/src/lib/validations/task.ts
- [X] T004 [P] Create priority constants with colors in frontend/src/lib/constants/priorities.ts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story

**CRITICAL**: Backend models and schemas must be ready before user story implementation

### Backend Foundation

- [X] T005 Extend Task model with priority field in backend/src/models/task.py (add Priority import, field with default, index)
- [X] T006 [P] Create Tag model in backend/src/models/tag.py (id, user_id, name, created_at, unique constraint)
- [X] T007 [P] Create TaskTag junction model in backend/src/models/tag.py (task_id, tag_id PKs with cascade delete)
- [X] T008 Add tags relationship to Task model in backend/src/models/task.py (Relationship with link_model)
- [X] T009 Extend TaskCreate schema with priority and tags in backend/src/schemas/task.py
- [X] T010 Extend TaskUpdate schema with priority and tags in backend/src/schemas/task.py
- [X] T011 Extend TaskRead schema with priority and tags in backend/src/schemas/task.py
- [X] T012 [P] Create TaskListResponse schema in backend/src/schemas/task.py (tasks, total, filtered)
- [X] T013 [P] Create TagRead and TagListResponse schemas in backend/src/schemas/task.py
- [X] T014 [P] Create filter/sort enums (StatusFilter, PriorityFilter, SortField, SortOrder) in backend/src/schemas/task.py
- [X] T015 Run database migration to add priority column and create tag tables

### Frontend Foundation

- [X] T016 [P] Extend Task interface with priority and tags in frontend/src/types/task.ts (completed via T003)
- [X] T017 [P] Add Priority type and Tag interface in frontend/src/types/task.ts (completed via T003)
- [X] T018 [P] Add TaskListResponse interface in frontend/src/types/task.ts (completed via T003)
- [X] T019 [P] Add TaskFilters, SortField, SortOrder types in frontend/src/types/task.ts (completed via T003)
- [X] T020 [P] Extend TaskCreateInput and TaskUpdateInput with priority and tags in frontend/src/types/task.ts (completed via T003)
- [X] T021 Extend taskCreateSchema with priority and tags validation in frontend/src/lib/validations/task.ts (completed via T003)
- [X] T022 Extend taskUpdateSchema with priority and tags validation in frontend/src/lib/validations/task.ts (completed via T003)

**Checkpoint**: Foundation ready - user story implementation can begin

---

## Phase 3: User Story 1 - Prioritize Tasks for Focus (Priority: P1)

**Goal**: Users can assign priority levels (High/Medium/Low/None) to tasks and see them sorted by priority

**Independent Test**: Create tasks with different priorities, verify visual indicators and priority-based sorting

### Backend Tests for US1

- [X] T023 [P] [US1] Unit test for create_task with priority in backend/tests/unit/test_task_crud_priority.py
- [X] T024 [P] [US1] Unit test for update_task priority in backend/tests/unit/test_task_crud_priority.py
- [X] T025 [P] [US1] Unit test for list_tasks sorted by priority in backend/tests/unit/test_task_crud_priority.py
- [X] T026 [P] [US1] Integration test for POST /api/todos with priority in backend/tests/integration/test_tasks_api_priority.py
- [X] T027 [P] [US1] Integration test for GET /api/todos default sort in backend/tests/integration/test_tasks_api_priority.py

### Backend Implementation for US1

- [X] T028 [US1] Update create_task in backend/src/crud/task.py to handle priority field
- [X] T029 [US1] Update update_task in backend/src/crud/task.py to handle priority field
- [X] T030 [US1] Update list_tasks in backend/src/crud/task.py with priority-based sorting (High->Medium->Low->None)
- [X] T031 [US1] Update POST /api/todos in backend/src/routers/tasks.py to accept priority
- [X] T032 [US1] Update PATCH /api/todos/{id} in backend/src/routers/tasks.py to accept priority
- [X] T033 [US1] Update GET /api/todos in backend/src/routers/tasks.py to return priority-sorted tasks

### Frontend Tests for US1

- [X] T034 [P] [US1] Component test for PriorityBadge in frontend/src/components/tasks/PriorityBadge.test.tsx
- [X] T035 [P] [US1] Component test for priority selector in TaskForm in frontend/src/components/tasks/TaskForm.test.tsx

### Frontend Implementation for US1

- [X] T036 [P] [US1] Create PriorityBadge component in frontend/src/components/tasks/PriorityBadge.tsx
- [X] T037 [US1] Add priority selector to TaskForm in frontend/src/components/tasks/TaskForm.tsx
- [X] T038 [US1] Display PriorityBadge in TaskItem in frontend/src/components/tasks/TaskItem.tsx
- [X] T039 [US1] Update useTasks hook to include priority in create/update in frontend/src/hooks/useTasks.ts (types already support it)

**Checkpoint**: Priority feature complete - tasks can be created/edited with priorities and display sorted

---

## Phase 4: User Story 2 - Organize Tasks with Tags (Priority: P1)

**Goal**: Users can add multiple tags to tasks, see tag suggestions, and filter by clicking tags

**Independent Test**: Create tasks with tags, verify tag display as chips, click tag to filter list

### Backend Tests for US2

- [X] T040 [P] [US2] Unit test for tag CRUD operations in backend/tests/unit/test_tag_crud.py
- [X] T041 [P] [US2] Unit test for create_task with tags in backend/tests/unit/test_task_crud_tags.py
- [X] T042 [P] [US2] Unit test for tag case-insensitive merge in backend/tests/unit/test_tag_crud.py
- [X] T043 [P] [US2] Integration test for POST /api/todos with tags in backend/tests/integration/test_tasks_api_tags.py
- [X] T044 [P] [US2] Integration test for GET /api/tags in backend/tests/integration/test_tags_api.py

### Backend Implementation for US2

- [X] T045 [P] [US2] Create tag CRUD functions in backend/src/crud/tag.py (get_or_create_tag, list_tags, get_tags_for_task)
- [X] T046 [US2] Update create_task in backend/src/crud/task.py to handle tags (create if not exist, link to task)
- [X] T047 [US2] Update update_task in backend/src/crud/task.py to handle tags (replace existing tags)
- [X] T048 [US2] Update list_tasks in backend/src/crud/task.py to include tags in response
- [X] T049 [US2] Update get_task in backend/src/crud/task.py to include tags in response
- [X] T050 [P] [US2] Create tags router in backend/src/routers/tags.py with GET /api/tags endpoint
- [X] T051 [US2] Register tags router in backend/src/main.py

### Frontend Tests for US2

- [X] T052 [P] [US2] Component test for TagChip in frontend/src/components/tasks/TagChip.test.tsx
- [X] T053 [P] [US2] Component test for TagInput in frontend/src/components/tasks/TagInput.test.tsx
- [X] T053b [P] [US2] Test TagInput shows "Tags must be single words" error when space entered in frontend/src/components/tasks/TagInput.test.tsx

### Frontend Implementation for US2

- [X] T054 [P] [US2] Create TagChip component in frontend/src/components/tasks/TagChip.tsx (display, remove, click-to-filter)
- [X] T055 [P] [US2] Create useTags hook in frontend/src/hooks/useTags.ts (fetch user's tags for suggestions)
- [X] T056 [US2] Create TagInput component in frontend/src/components/tasks/TagInput.tsx (autocomplete, validation)
- [X] T057 [US2] Add TagInput to TaskForm in frontend/src/components/tasks/TaskForm.tsx
- [X] T058 [US2] Display TagChips in TaskItem in frontend/src/components/tasks/TaskItem.tsx
- [X] T059 [US2] Update useTasks hook to include tags in create/update in frontend/src/hooks/useTasks.ts (already handled by type definitions)

**Checkpoint**: Tag feature complete - tasks can have tags, suggestions work, clicking tag filters

---

## Phase 5: User Story 3 - Search Tasks by Keyword (Priority: P2)

**Goal**: Users can search tasks by typing keywords that match title or description

**Independent Test**: Create tasks with various titles/descriptions, search for partial keywords

### Backend Tests for US3

- [X] T060 [P] [US3] Unit test for list_tasks with search parameter in backend/tests/unit/test_task_crud_search.py
- [X] T061 [P] [US3] Integration test for GET /api/todos?search= in backend/tests/integration/test_tasks_api_search.py

### Backend Implementation for US3

- [X] T062 [US3] Add search parameter to list_tasks in backend/src/crud/task.py (ILIKE on title and description)
- [X] T063 [US3] Add search query parameter to GET /api/todos in backend/src/routers/tasks.py

### Frontend Tests for US3

- [X] T064 [P] [US3] Component test for SearchBar in frontend/src/components/tasks/SearchBar.test.tsx
- [X] T065 [P] [US3] Hook test for useDebounce in frontend/src/hooks/useDebounce.test.ts

### Frontend Implementation for US3

- [X] T066 [P] [US3] Create useDebounce hook in frontend/src/hooks/useDebounce.ts (300ms debounce)
- [X] T067 [US3] Create SearchBar component in frontend/src/components/tasks/SearchBar.tsx (input, clear button, debounced)
- [X] T068 [US3] Update useTasks.fetchTasks to accept search parameter in frontend/src/hooks/useTasks.ts
- [X] T069 [US3] Integrate SearchBar in dashboard page in frontend/src/app/dashboard/page.tsx

**Checkpoint**: Search feature complete - users can search tasks by keyword

---

## Phase 6: User Story 4 - Filter Tasks by Criteria (Priority: P2)

**Goal**: Users can filter by status, priority, and tags with combined AND logic

**Independent Test**: Create varied tasks, apply filters individually and combined, verify counts

### Backend Tests for US4

- [X] T070 [P] [US4] Unit test for list_tasks with status filter in backend/tests/unit/test_task_crud_filter.py
- [X] T071 [P] [US4] Unit test for list_tasks with priority filter in backend/tests/unit/test_task_crud_filter.py
- [X] T072 [P] [US4] Unit test for list_tasks with tags filter in backend/tests/unit/test_task_crud_filter.py
- [X] T073 [P] [US4] Unit test for list_tasks with no_tags filter in backend/tests/unit/test_task_crud_filter.py
- [X] T074 [P] [US4] Unit test for list_tasks with combined filters (AND logic) in backend/tests/unit/test_task_crud_filter.py
- [X] T075 [P] [US4] Integration test for GET /api/todos with filter params in backend/tests/integration/test_tasks_api_filter.py

### Backend Implementation for US4

- [X] T076 [US4] Add status filter to list_tasks in backend/src/crud/task.py (all/pending/completed)
- [X] T077 [US4] Add priority filter to list_tasks in backend/src/crud/task.py
- [X] T078 [US4] Add tags filter to list_tasks in backend/src/crud/task.py (OR logic within tags)
- [X] T079 [US4] Add no_tags filter to list_tasks in backend/src/crud/task.py
- [X] T080 [US4] Implement combined filter logic (AND) in list_tasks in backend/src/crud/task.py
- [X] T081 [US4] Return total and filtered counts from list_tasks in backend/src/crud/task.py
- [X] T082 [US4] Add all filter query parameters to GET /api/todos in backend/src/routers/tasks.py
- [X] T083 [US4] Update GET /api/todos response to include total and filtered in backend/src/routers/tasks.py

### Frontend Tests for US4

- [X] T084 [P] [US4] Component test for FilterPanel in frontend/src/components/tasks/FilterPanel.test.tsx
- [X] T085 [P] [US4] Hook test for useTaskFilters in frontend/src/hooks/useTaskFilters.test.ts

### Frontend Implementation for US4

- [X] T086 [P] [US4] Create useTaskFilters hook in frontend/src/hooks/useTaskFilters.ts (filter state management)
- [X] T087 [US4] Create FilterPanel component in frontend/src/components/tasks/FilterPanel.tsx (status, priority, tags selectors)
- [X] T088 [US4] Add "Clear All Filters" button to FilterPanel in frontend/src/components/tasks/FilterPanel.tsx
- [X] T089 [US4] Update useTasks.fetchTasks to accept filter parameters in frontend/src/hooks/useTasks.ts
- [X] T090 [US4] Add total/filtered state to useTasks in frontend/src/hooks/useTasks.ts
- [X] T091 [US4] Display "Showing X of Y tasks" count in TaskList in frontend/src/components/tasks/TaskList.tsx
- [X] T092 [US4] Create EmptyFilterState component in frontend/src/components/tasks/EmptyFilterState.tsx
- [X] T093 [US4] Integrate FilterPanel in dashboard page in frontend/src/app/dashboard/page.tsx

**Checkpoint**: Filter feature complete - users can filter by multiple criteria with counts

---

## Phase 7: User Story 5 - Sort Tasks by Different Criteria (Priority: P3)

**Goal**: Users can sort tasks by priority, title, or creation date with persisted preference

**Independent Test**: Create varied tasks, switch sort options, verify order and persistence

### Backend Tests for US5

- [X] T094 [P] [US5] Unit test for list_tasks with title sort in backend/tests/unit/test_task_crud_sort.py
- [X] T095 [P] [US5] Unit test for list_tasks with created_at sort in backend/tests/unit/test_task_crud_sort.py
- [X] T096 [P] [US5] Integration test for GET /api/todos?sort=title&order=asc in backend/tests/integration/test_tasks_api_sort.py

### Backend Implementation for US5

- [X] T097 [US5] Add sort and order parameters to list_tasks in backend/src/crud/task.py
- [X] T098 [US5] Implement title sorting (A-Z, Z-A) in list_tasks in backend/src/crud/task.py
- [X] T099 [US5] Implement created_at sorting in list_tasks in backend/src/crud/task.py
- [X] T100 [US5] Add sort and order query parameters to GET /api/todos in backend/src/routers/tasks.py

### Frontend Tests for US5

- [X] T101 [P] [US5] Component test for SortSelector in frontend/src/components/tasks/SortSelector.test.tsx

### Frontend Implementation for US5

- [X] T102 [US5] Create SortSelector component in frontend/src/components/tasks/SortSelector.tsx
- [X] T103 [US5] Add localStorage persistence for sort preference in useTaskFilters in frontend/src/hooks/useTaskFilters.ts
- [X] T104 [US5] Update useTasks.fetchTasks to accept sort parameters in frontend/src/hooks/useTasks.ts
- [X] T105 [US5] Integrate SortSelector in dashboard page in frontend/src/app/dashboard/page.tsx

**Checkpoint**: Sort feature complete - users can sort tasks with preference persistence

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements affecting multiple user stories

- [X] T106 [P] Add responsive styles for mobile (320px+) to FilterPanel in frontend/src/components/tasks/FilterPanel.tsx
- [X] T107 [P] Add responsive styles for mobile to SearchBar in frontend/src/components/tasks/SearchBar.tsx
- [X] T108 [P] Handle edge case: empty search results in frontend/src/components/tasks/TaskList.tsx
- [X] T109 [P] Handle edge case: rapid typing debounce in SearchBar in frontend/src/components/tasks/SearchBar.tsx
- [X] T110 [P] Handle edge case: many tags (50+) with scrollable dropdown in TagInput in frontend/src/components/tasks/TagInput.tsx
- [X] T111 [P] Add loading states to filter/search operations in frontend/src/app/dashboard/page.tsx
- [X] T112 Cleanup orphan tags (tags with no tasks) - add function in backend/src/crud/tag.py
- [X] T113 Run backend test coverage check (>=70%) in backend/
- [X] T114 Run frontend test coverage check (>=70%) in frontend/
- [X] T115 End-to-end validation using acceptance scenarios from spec.md
- [X] T115b End-to-end regression test for Phase 1 CRUD: create task, edit task, delete task, toggle completion
- [X] T116 [P] Handle edge case: special characters in search without errors in backend/src/crud/task.py
- [X] T117 [P] Hide/disable filters when user has no tasks in frontend/src/app/dashboard/page.tsx

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 - BLOCKS all user stories
- **Phases 3-7 (User Stories)**: All depend on Phase 2 completion
  - US1 and US2 are both P1 - can run in parallel
  - US3 and US4 are both P2 - can run in parallel after P1 stories
  - US5 is P3 - can run after P2 stories
- **Phase 8 (Polish)**: Depends on all user stories

### User Story Dependencies

| Story | Priority | Backend Dependency | Frontend Dependency |
|-------|----------|-------------------|---------------------|
| US1 - Priority | P1 | Phase 2 only | Phase 2 + US1 backend |
| US2 - Tags | P1 | Phase 2 only | Phase 2 + US2 backend |
| US3 - Search | P2 | Phase 2 only | Phase 2 + US3 backend |
| US4 - Filter | P2 | Phase 2 + US1/US2 backend (uses priority/tags) | Phase 2 + US4 backend |
| US5 - Sort | P3 | Phase 2 only | Phase 2 + US5 backend |

### Parallel Opportunities

**Within Setup (Phase 1):**
```
T002 Priority enum || T003 Zod schemas || T004 Priority constants
```

**Within Foundational (Phase 2):**
```
Backend: T006 Tag model || T007 TaskTag model || T012 TaskListResponse || T013 TagRead || T014 Enums
Frontend: T016-T020 all types can run in parallel
```

**User Stories P1 in Parallel:**
```
US1 Backend || US2 Backend (different files)
Then: US1 Frontend || US2 Frontend
```

**User Stories P2 in Parallel (after US1+US2):**
```
US3 Backend || US4 Backend (note: US4 uses priority/tags from US1/US2)
Then: US3 Frontend || US4 Frontend
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Priority)
4. **STOP and VALIDATE**: Tasks show priorities, sort by priority works
5. Can demo/deploy after US1

### Recommended Order

1. **Setup + Foundational** (T001-T022) - ~22 tasks
2. **US1 Priority** (T023-T039) - ~17 tasks - MVP!
3. **US2 Tags** (T040-T059) - ~20 tasks - Core feature
4. **US3 Search** (T060-T069) - ~10 tasks - Quick win
5. **US4 Filter** (T070-T093) - ~24 tasks - Complex but valuable
6. **US5 Sort** (T094-T105) - ~12 tasks - Nice to have
7. **Polish** (T106-T115) - ~10 tasks - Final touches

### Task Counts

| Phase | Tasks | Cumulative |
|-------|-------|------------|
| Setup | 4 | 4 |
| Foundational | 18 | 22 |
| US1 Priority | 17 | 39 |
| US2 Tags | 20 | 59 |
| US3 Search | 10 | 69 |
| US4 Filter | 24 | 93 |
| US5 Sort | 12 | 105 |
| Polish | 10 | 115 |

**Total: 115 tasks**

---

## Notes

- [P] tasks = different files, no dependencies, can parallelize
- [Story] label maps task to user story for traceability
- Backend tests use pytest, frontend tests use Jest + RTL
- All CRUD functions MUST filter by user_id (security requirement)
- Constitution requires TDD - write tests first, verify they fail
- Commit after each task or logical group

---

**Generated**: 2026-01-23
**Spec Version**: Draft
**Plan Version**: 1.0.0
