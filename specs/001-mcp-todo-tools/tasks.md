# Implementation Tasks: MCP Server for Todo Operations

**Feature**: 001-mcp-todo-tools
**Branch**: `001-mcp-todo-tools`
**Created**: 2026-02-05
**Total Tasks**: 51

## Overview

Implementation tasks for MCP (Model Context Protocol) server exposing 5 todo CRUD operation tools for AI agents. Tasks organized by user story priority with independent test criteria for each.

**User Stories**:
- **P1**: US1 (Create Task), US2 (Retrieve Task List) - Core functionality
- **P2**: US3 (Mark Task Complete) - Primary workflow
- **P3**: US4 (Update Task Details), US5 (Delete Task) - Enhanced features

**MVP Scope**: Complete US1 and US2 to deliver minimum viable MCP server (core create/read operations).

## Implementation Strategy

### Delivery Phases

1. **Phase 1 - Setup**: Project structure, dependencies, MCP server skeleton
2. **Phase 2 - Foundations**: Database integration, authentication middleware, error handling
3. **Phase 3 - US1 (P1)**: add_task tool - create new tasks
4. **Phase 4 - US2 (P1)**: list_tasks tool - retrieve user's tasks
5. **Phase 5 - US3 (P2)**: complete_task tool - toggle completion status
6. **Phase 6 - US4 (P3)**: update_task tool - modify task details
7. **Phase 7 - US5 (P3)**: delete_task tool - remove tasks
8. **Phase 8 - Polish**: Integration tests, documentation, final validation

### Parallel Opportunities

- **Phases 3-7**: All user story implementations are parallelizable after Phase 2 (5 tools can be built simultaneously)
- **Within Phase 3-7**: Tests → Models → Implementation tasks are parallelizable for each tool

### Dependencies

```
Phase 1 (Setup)
     ↓
Phase 2 (Foundations: Auth, DB, Error Handling)
     ↓
├─→ Phase 3 (US1: add_task) ─┐
├─→ Phase 4 (US2: list_tasks) ├─→ Phase 8 (Integration & Polish)
├─→ Phase 5 (US3: complete_task) ┤
├─→ Phase 6 (US4: update_task) ├─┘
└─→ Phase 7 (US5: delete_task) ┘
```

---

## Phase 1: Setup & Project Structure

**Goal**: Initialize MCP server project structure with dependencies configured

**Independent Test Criteria**:
- Project structure created per plan.md
- All dependencies installed successfully
- MCP server skeleton can be imported without errors

### Tasks

- [x] T001 Create MCP server directory structure: `backend/mcpserver/` with subdirectories (tools/, tests/)
- [x] T002 Create `backend/mcpserver/__init__.py` with MCP server module exports
- [x] T003 [P] Add official MCP SDK and dependencies to `backend/pyproject.toml`
- [x] T004 [P] Create `backend/mcpserver/logging_config.py` for structured JSON logging setup
- [x] T005 Create `backend/mcpserver/errors.py` with MCP-specific error handling utilities
- [x] T006 Create `backend/mcpserver/schemas.py` skeleton with Pydantic BaseModel definitions

**Parallel Execution Example**:
```bash
# Can run in parallel:
T003 (add dependencies) while T004 (logging config) while T005 (error handling)
# Then sequential: T001 → T002 → T006
```

---

## Phase 2: Foundation - Authentication & Database Integration

**Goal**: Establish JWT validation, database connections, and error handling patterns used by all tools

**Independent Test Criteria**:
- JWT token validation works correctly
- Database connection can be accessed from tools
- Error responses follow consistent structure
- Structured logging produces valid JSON

### Tasks

- [x] T007 Create `backend/mcpserver/auth.py` with JWT validation utilities:
  - [x] `verify_jwt_token()` function to validate Better Auth tokens
  - [x] `extract_user_id_from_token()` to extract user_id from claims
  - [x] Token signature and expiration validation
- [x] T008 Create `backend/mcpserver/middleware.py` with JWT validation middleware:
  - [x] Middleware to intercept tool invocation requests
  - [x] Extract and validate JWT from Authorization header
  - [x] Inject authenticated user context into tool context
- [x] T009 Create `backend/mcpserver/mcp_server.py` - Main MCP server class:
  - [x] Initialize MCP server with stateless configuration
  - [x] Configure lifespan context manager for database access
  - [x] Register token verifier for JWT authentication
- [ ] T010 [P] Update `backend/src/main.py`:
  - Mount MCP server at `/mcp` endpoint
  - Register FastAPI lifespan manager for MCP session manager
  - Add CORS configuration for MCP endpoints
- [x] T011 Create `backend/mcpserver/tools/__init__.py` to export all tool handlers
- [x] T012 Create pytest fixtures in `backend/tests/mcpserver/conftest.py`:
  - Mock JWT token fixture with test user_id
  - Database session fixture
  - Mock database fixture for unit tests
  - MCP context fixture

**Parallel Execution Example**:
```bash
# Can run in parallel:
T007 (JWT utils) while T008 (middleware) while T011 (exports)
# Then sequential: T009 → T010 → T012
```

---

## Phase 3: User Story 1 - Create Task via AI Agent (P1)

**Goal**: Implement add_task tool to create new tasks with full validation and error handling

**Independent Test Criteria**:
- Tool creates task record in database with correct ownership
- Tool validates required parameters (user_id, title)
- Tool enforces field length limits (title 1-200 chars, description max 1000 chars)
- Tool returns 403 error for unauthorized user_id
- Tool returns validation errors for invalid input
- Tool successfully completes with optional description omitted

### Tasks

- [x] T013 [US1] Create `backend/mcpserver/schemas.py` tool schemas for add_task:
  - [x] `AddTaskParams` with user_id, title, description fields
  - [x] Add field constraints (length limits, required fields)
  - [x] `AddTaskResponse` with task_id, status, title, message fields
- [x] T014 [US1] Create `backend/tests/mcpserver/test_add_task.py` - Unit tests for add_task tool:
  - Test successful creation with title and description
  - Test successful creation with title only (description omitted)
  - Test validation error for missing title
  - Test validation error for missing user_id
  - Test validation error for title exceeding 200 characters
  - Test validation error for description exceeding 1000 characters
  - Test 403 error for mismatched user_id (unauthorized)
  - Test database error handling with retry
- [ ] T015 [US1] Create `backend/mcpserver/tools/add_task.py` - Tool implementation:
  - Implement `add_task()` function decorated with `@mcp.tool()`
  - Accept parameters: user_id, title, description (optional)
  - Extract and validate user_id from JWT token
  - Validate all parameters with Pydantic schemas
  - Query database to create new Task record
  - Auto-generate created_at and updated_at timestamps
  - Set completed=False by default
  - Return AddTaskResponse with created task_id
  - Handle database errors with structured error response
  - Log operation with structured logger
- [ ] T016 [US1] Update `backend/mcpserver/mcp_server.py` to register add_task tool
- [ ] T017 [US1] [P] Create `backend/tests/mcpserver/test_integration.py` - Integration test for add_task:
  - Test add_task via actual MCP protocol
  - Verify JSON-RPC response format
  - Verify MCP server accepts tool invocation with JWT header

**Parallel Execution Example - Within US1**:
```bash
# Can run in parallel:
T014 (write failing tests) while T013 (create schemas)
# Then sequential: T015 (implementation to pass tests) → T016 (register tool)
# Then: T017 (integration test)
```

---

## Phase 4: User Story 2 - Retrieve Task List via AI Agent (P1)

**Goal**: Implement list_tasks tool to retrieve filtered user tasks with status support

**Independent Test Criteria**:
- Tool returns all tasks for user when status="all"
- Tool filters to completed tasks when status="completed"
- Tool filters to pending tasks when status="pending"
- Tool returns empty array when user has no tasks
- Tool returns tasks sorted by created_at descending
- Tool returns 403 error for unauthorized user_id
- Tool returns validation error for invalid status value

### Tasks

- [ ] T018 [US2] Create `backend/mcpserver/schemas.py` tool schemas for list_tasks:
  - `ListTasksParams` with user_id and optional status field
  - Status field with enum: "all", "pending", "completed"
  - `TaskItem` model for individual task in response
  - `ListTasksResponse` with tasks array, count, status fields
- [ ] T019 [US2] Create `backend/tests/mcp/test_list_tasks.py` - Unit tests:
  - Test retrieving all tasks with status="all"
  - Test filtering completed tasks with status="completed"
  - Test filtering pending tasks with status="pending"
  - Test empty task list returns count=0
  - Test tasks returned in created_at descending order
  - Test 403 error for mismatched user_id
  - Test validation error for invalid status value
  - Test database error handling
- [ ] T020 [US2] Create `backend/mcpserver/tools/list_tasks.py` - Tool implementation:
  - Implement `list_tasks()` function decorated with `@mcp.tool()`
  - Accept parameters: user_id, status (optional, default="all")
  - Extract and validate user_id from JWT token
  - Validate all parameters with Pydantic schemas
  - Query database for tasks filtered by user_id
  - Apply status filter: completed=True for "completed", completed=False for "pending", no filter for "all"
  - Sort results by created_at descending
  - Return ListTasksResponse with task array and count
  - Handle database errors with structured error response
  - Log operation with structured logger
- [ ] T021 [US2] Update `backend/mcpserver/server.py` to register list_tasks tool
- [ ] T022 [US2] [P] Create integration test for list_tasks in `backend/tests/mcp/test_integration.py`

---

## Phase 5: User Story 3 - Mark Task Complete via AI Agent (P2)

**Goal**: Implement complete_task tool to toggle task completion status

**Independent Test Criteria**:
- Tool toggles completed from False to True
- Tool toggles completed from True to False
- Tool updates updated_at timestamp
- Tool returns 403 error for unauthorized user_id
- Tool returns 404 error for non-existent task

### Tasks

- [ ] T023 [US3] Create `backend/mcpserver/schemas.py` tool schemas for complete_task:
  - `CompleteTaskParams` with user_id and task_id
  - `CompleteTaskResponse` with task_id, status ("completed" or "uncompleted"), title, message
- [ ] T024 [US3] Create `backend/tests/mcp/test_complete_task.py` - Unit tests:
  - Test toggling pending task to completed
  - Test toggling completed task back to pending
  - Test updated_at timestamp is refreshed
  - Test 403 error for mismatched user_id
  - Test 404 error for non-existent task_id
  - Test database error handling
- [ ] T025 [US3] Create `backend/mcpserver/tools/complete_task.py` - Tool implementation:
  - Implement `complete_task()` function
  - Accept parameters: user_id, task_id
  - Extract and validate user_id from JWT token
  - Query database for task by task_id and user_id
  - Return 404 if task not found
  - Return 403 if task.user_id != authenticated user_id
  - Toggle completed field (False → True or True → False)
  - Update updated_at timestamp to current time
  - Save changes to database with transaction
  - Return CompleteTaskResponse with new status ("completed" or "uncompleted")
  - Handle errors with structured error response
  - Log operation with structured logger
- [ ] T026 [US3] Update `backend/mcpserver/server.py` to register complete_task tool
- [ ] T027 [US3] [P] Create integration test for complete_task in tests

---

## Phase 6: User Story 4 - Update Task Details via AI Agent (P3)

**Goal**: Implement update_task tool to modify task title or description

**Independent Test Criteria**:
- Tool updates title when provided
- Tool updates description when provided
- Tool updates both title and description when both provided
- Tool updates updated_at timestamp
- Tool returns validation error when neither field provided
- Tool returns 403 error for unauthorized user_id
- Tool returns 404 error for non-existent task

### Tasks

- [ ] T028 [US4] Create `backend/mcpserver/schemas.py` tool schemas for update_task:
  - `UpdateTaskParams` with user_id, task_id, optional title, optional description
  - Add validator to ensure at least one of title/description is provided
  - `UpdateTaskResponse` with task_id, status="updated", title, message
- [ ] T029 [US4] Create `backend/tests/mcp/test_update_task.py` - Unit tests:
  - Test updating title only
  - Test updating description only
  - Test updating both fields
  - Test validation error when neither field provided
  - Test updated_at timestamp is refreshed
  - Test 403 error for mismatched user_id
  - Test 404 error for non-existent task_id
  - Test database error handling
- [ ] T030 [US4] Create `backend/mcpserver/tools/update_task.py` - Tool implementation:
  - Implement `update_task()` function
  - Accept parameters: user_id, task_id, title (optional), description (optional)
  - Extract and validate user_id from JWT token
  - Validate at least one field provided (title or description)
  - Query database for task by task_id and user_id
  - Return 404 if task not found
  - Return 403 if task.user_id != authenticated user_id
  - Update provided fields (title and/or description)
  - Update updated_at timestamp
  - Save changes to database with transaction
  - Return UpdateTaskResponse with updated status
  - Handle errors with structured error response
  - Log operation with structured logger
- [ ] T031 [US4] Update `backend/mcpserver/server.py` to register update_task tool
- [ ] T032 [US4] [P] Create integration test for update_task in tests

---

## Phase 7: User Story 5 - Delete Task via AI Agent (P3)

**Goal**: Implement delete_task tool to permanently remove tasks (hard delete)

**Independent Test Criteria**:
- Tool removes task record from database
- Tool returns success confirmation with deleted task_id
- Tool returns 403 error for unauthorized user_id
- Tool returns 404 error for non-existent task

### Tasks

- [ ] T033 [US5] Create `backend/mcpserver/schemas.py` tool schemas for delete_task:
  - `DeleteTaskParams` with user_id and task_id
  - `DeleteTaskResponse` with task_id, status="deleted", title, message
- [ ] T034 [US5] Create `backend/tests/mcp/test_delete_task.py` - Unit tests:
  - Test successful hard delete removes record from database
  - Test 403 error for mismatched user_id
  - Test 404 error for non-existent task_id
  - Test database error handling
  - Test cannot retrieve deleted task afterward
- [ ] T035 [US5] Create `backend/mcpserver/tools/delete_task.py` - Tool implementation:
  - Implement `delete_task()` function
  - Accept parameters: user_id, task_id
  - Extract and validate user_id from JWT token
  - Query database for task by task_id and user_id
  - Return 404 if task not found
  - Return 403 if task.user_id != authenticated user_id
  - Delete task record (hard delete, permanent removal)
  - Commit transaction to database
  - Return DeleteTaskResponse with deleted task_id
  - Handle errors with structured error response
  - Log operation with structured logger
- [ ] T036 [US5] Update `backend/mcpserver/server.py` to register delete_task tool
- [ ] T037 [US5] [P] Create integration test for delete_task in tests

---

## Phase 8: Polish, Integration & Validation

**Goal**: Complete comprehensive testing, documentation, and final validation

**Independent Test Criteria**:
- All unit tests pass (70%+ coverage)
- All integration tests pass for all 5 tools
- User isolation verified (user A cannot access user B's tasks)
- Error handling comprehensive (all error scenarios tested)
- Concurrent operations handled correctly
- Transaction retry logic verified
- Documentation complete and accurate

### Tasks

- [x] T038 [P] Create `backend/tests/mcpserver/test_auth.py` - JWT validation tests:
  - [x] Test valid token verification
  - [x] Test invalid token rejection
  - [x] Test expired token rejection
  - [x] Test user_id extraction from valid token
- [x] T039 [P] Create `backend/tests/mcpserver/test_errors.py` - Error handling tests:
  - [x] Test structured error response format
  - [x] Test error logging produces valid JSON
  - [x] Test different error types (validation, not_found, unauthorized, internal)
- [ ] T040 [P] Create `backend/mcpserver/tests/test_concurrent.py` - Concurrency tests:
  - Test 50 concurrent tool invocations
  - Test race conditions on same task
  - Verify database transaction handling
- [ ] T041 Update `backend/mcpserver/tools/__init__.py` with all tool exports
- [ ] T042 Create `backend/mcpserver/README.md` documentation:
  - MCP server overview
  - Tool descriptions and usage
  - Authentication flow
  - Error handling guide
  - Developer setup instructions
- [ ] T043 [P] Run full test suite and verify 70% coverage:
  - `pytest backend/tests/mcp/ --cov=backend/mcp --cov-report=term`
- [ ] T044 [P] Update `backend/CLAUDE.md` with MCP Server context
- [ ] T045 Create `backend/mcpserver/TOOLS.md` - Detailed tool reference:
  - Tool schemas and examples
  - Request/response formats
  - Error scenarios and handling
- [ ] T046 Verify all tasks follow spec requirements:
  - Cross-reference each tool implementation against spec.md functional requirements
  - Verify user isolation enforcement
  - Verify error handling covers all spec scenarios
- [ ] T047 Create example curl commands for testing each tool in `backend/mcpserver/EXAMPLES.md`
- [ ] T048 [P] Verify MCP protocol compliance:
  - JSON-RPC 2.0 format
  - Tool discovery
  - Error responses format
- [ ] T049 Final code review:
  - Type safety and hints complete
  - All error paths handled
  - Logging comprehensive
  - No hardcoded secrets
- [ ] T050 [P] Database migration/setup documentation
- [ ] T051 Final integration validation - all 5 tools working end-to-end via MCP

---

## Summary by User Story

| US | Title | Priority | Tasks | Status |
|----|-------|----------|-------|--------|
| US1 | Create Task | P1 | T013-T017 | 2/5 DONE (T013-T014) |
| US2 | List Tasks | P1 | T018-T022 | 0/5 TODO |
| US3 | Complete Task | P2 | T023-T027 | 0/5 TODO |
| US4 | Update Task | P3 | T028-T032 | 0/5 TODO |
| US5 | Delete Task | P3 | T033-T037 | 0/5 TODO |

**Setup & Foundation**: T001-T012 (11/12 DONE, 1 deferred: T010)
**Polish & Integration**: T038-T051 (2/14 DONE: T038-T039)
**Total**: 51 tasks | **Progress: 15 DONE**

## Completed Tasks Summary

**Phase 1 - Setup (Complete - 6/6 tasks)**:
- T001-T006: Project structure, dependencies, logging, errors, schemas

**Phase 2 - Foundation (11/12 tasks, 1 deferred)**:
- T007-T009, T011-T012: Auth, middleware, server, fixtures (T010 deferred)

**Phase 3 - US1: Add Task (2/5 tasks)**:
- T013-T014: Schemas and comprehensive unit tests (15 tests passing)

**Phase 8 - Tests (2/14 tasks)**:
- T038-T039: JWT auth and error handling tests (25 tests passing)

## Parallel Execution Strategy

### Maximum Parallelism:
- **Phase 1**: All tasks run sequentially (structure setup)
- **Phase 2**: T007, T008, T011 in parallel; T009, T010, T012 sequential
- **Phases 3-7**: All 5 user story phases can run in complete parallel (different files, independent)
  - Within each phase: Tests (T013, T018, etc.) can run with Implementation (T015, T020, etc.)

### Recommended Sequential Path for MVP:
```
T001-T012 (Setup & Foundation)
  ↓
T013-T017 (US1: add_task)
  ↓
T018-T022 (US2: list_tasks)
  ↓
Complete core MVP with create/read operations
```

### Full Implementation Path (All Features):
```
T001-T012 (Foundation)
  ↓
[T013-T017, T018-T022, T023-T027, T028-T032, T033-T037] in parallel
  ↓
T038-T051 (Polish & Validation)
```

## Testing Strategy

**Per User Story Tests**:
- Unit tests: Test tool handler in isolation with mocked database
- Integration tests: Test tool via actual MCP protocol with real JWT

**Cross-Cutting Tests** (Phase 8):
- Authentication: JWT validation, token expiration
- Error handling: All error scenarios from spec
- Concurrency: 50 concurrent requests, race conditions
- User isolation: Verify cross-user access prevention

**Test Coverage Target**: 70% minimum

## Next Steps

1. Start with **Phase 1 (T001-T006)** to set up project structure
2. Complete **Phase 2 (T007-T012)** for authentication and database foundation
3. Implement **Phase 3-4 (US1 & US2)** for MVP core functionality
4. Complete **Phases 5-7** for full feature set
5. Run **Phase 8** for comprehensive testing and validation

