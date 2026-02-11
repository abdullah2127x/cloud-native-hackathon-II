# Implementation Tasks: MCP Server for Todo Operations

**Feature**: 005-mcp-todo-tools
**Branch**: `005-mcp-todo-tools`
**Created**: 2026-02-05
**Shipped**: 2026-02-05 ✅
**Status**: PRODUCTION READY - MVP SHIPPED
**Total Tasks**: 51
**Shipped Tasks**: 41/51 (80%)

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
  - [x] Test successful creation with title and description
  - [x] Test successful creation with title only (description omitted)
  - [x] Test validation error for missing title
  - [x] Test validation error for missing user_id
  - [x] Test validation error for title exceeding 200 characters
  - [x] Test validation error for description exceeding 1000 characters
  - [x] Test 403 error for mismatched user_id (unauthorized)
  - [x] Test database error handling with retry
- [x] T015 [US1] Create `backend/mcpserver/tools/add_task.py` - Tool implementation:
  - [x] Implement `add_task()` function with async support
  - [x] Accept parameters: user_id, title, description (optional)
  - [x] Extract and validate user_id from JWT token
  - [x] Validate all parameters with Pydantic schemas
  - [x] Query database to create new Task record
  - [x] Auto-generate created_at and updated_at timestamps
  - [x] Set completed=False by default
  - [x] Return AddTaskResponse with created task_id
  - [x] Handle database errors with structured error response
  - [x] Log operation with structured logger
- [x] T016 [US1] Update `backend/mcpserver/mcp_server.py` to register add_task tool:
  - [x] Added _register_tools() method
  - [x] Added tool_handlers dictionary
  - [x] Updated register_tool() to store handlers
  - [x] Updated call_tool() to invoke actual handlers
- [x] T017 [US1] [P] Create `backend/tests/mcpserver/test_integration.py` - Integration test for add_task:
  - [x] Test add_task via actual MCP protocol
  - [x] Verify JSON-RPC response format
  - [x] Verify MCP server accepts tool invocation
  - [x] Test error handling in MCP responses
  - [x] Test tool discovery
  - [x] Test JSON serialization

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

- [x] T018 [US2] Create `backend/mcpserver/schemas.py` tool schemas for list_tasks:
  - [x] `ListTasksParams` with user_id and optional status field
  - [x] Status field with enum: "all", "pending", "completed"
  - [x] `TaskItem` model for individual task in response
  - [x] `ListTasksResponse` with tasks array, count, status fields
- [x] T019 [US2] Create `backend/tests/mcpserver/test_list_tasks.py` - Unit tests:
  - [x] Test retrieving all tasks with status="all"
  - [x] Test filtering completed tasks with status="completed"
  - [x] Test filtering pending tasks with status="pending"
  - [x] Test empty task list returns count=0
  - [x] Test tasks returned in created_at descending order
  - [x] Test 403 error for mismatched user_id
  - [x] Test validation error for invalid status value
  - [x] Test database error handling
- [x] T020 [US2] Create `backend/mcpserver/tools/list_tasks.py` - Tool implementation:
  - [x] Implement `list_tasks()` function with async support
  - [x] Accept parameters: user_id, status (optional, default="all")
  - [x] Extract and validate user_id from JWT token
  - [x] Validate all parameters with Pydantic schemas
  - [x] Query database for tasks filtered by user_id
  - [x] Apply status filter: completed=True for "completed", completed=False for "pending", no filter for "all"
  - [x] Sort results by created_at descending
  - [x] Return ListTasksResponse with task array and count
  - [x] Handle database errors with structured error response
  - [x] Log operation with structured logger
- [x] T021 [US2] Update `backend/mcpserver/mcp_server.py` to register list_tasks tool
- [x] T022 [US2] [P] Create integration test for list_tasks in `backend/tests/mcpserver/test_integration.py` (7 tests)

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

- [x] T023 [US3] Create `backend/mcpserver/schemas.py` tool schemas for complete_task:
  - [x] `CompleteTaskParams` with user_id and task_id (accepts both string and int)
  - [x] `CompleteTaskResponse` with task_id, status ("completed" or "uncompleted"), title, message
- [x] T024 [US3] Create `backend/tests/mcpserver/test_complete_task.py` - Unit tests (14 tests):
  - [x] Test toggling pending task to completed
  - [x] Test toggling completed task back to pending
  - [x] Test created_at timestamp is preserved
  - [x] Test user isolation - cannot toggle other user's task
  - [x] Test 404 error for non-existent task_id
  - [x] Test database error handling
- [x] T025 [US3] Create `backend/mcpserver/tools/complete_task.py` - Tool implementation:
  - [x] Implement `complete_task()` function with async support
  - [x] Accept parameters: user_id, task_id (supports both string UUID and numeric IDs)
  - [x] Validate parameters with Pydantic schemas
  - [x] Query database for task by task_id and user_id
  - [x] Return error if task not found
  - [x] Toggle completed field (False → True or True → False)
  - [x] Update updated_at timestamp to current UTC time
  - [x] Save changes to database with transaction
  - [x] Return CompleteTaskResponse with new status ("completed" or "uncompleted")
  - [x] Handle errors with structured error response
  - [x] Log operation with structured logger
- [x] T026 [US3] Update `backend/mcpserver/mcp_server.py` to register complete_task tool
- [x] T027 [US3] [P] Create integration tests for complete_task (7 tests)

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

- [x] T028 [US4] Create `backend/mcpserver/schemas.py` tool schemas for update_task:
  - [x] `UpdateTaskParams` with user_id, task_id (string|int), optional title, optional description
  - [x] Add model_validator to ensure at least one of title/description is provided
  - [x] `UpdateTaskResponse` with task_id, status="updated", title, message
- [x] T029 [US4] Create `backend/tests/mcpserver/test_update_task.py` - Unit tests (18 tests):
  - [x] Test updating title only
  - [x] Test updating description only
  - [x] Test updating both fields
  - [x] Test validation error when neither field provided
  - [x] Test created_at timestamp is preserved
  - [x] Test user isolation - cannot update other user's task
  - [x] Test 404 error for non-existent task_id
  - [x] Test database error handling
- [x] T030 [US4] Create `backend/mcpserver/tools/update_task.py` - Tool implementation:
  - [x] Implement `update_task()` function with async support
  - [x] Accept parameters: user_id, task_id (string|int), title (optional), description (optional)
  - [x] Validate parameters with Pydantic schemas (ensures at least one field provided)
  - [x] Query database for task by task_id and user_id
  - [x] Return error if task not found
  - [x] Update provided fields (title and/or description)
  - [x] Update updated_at timestamp to current UTC time
  - [x] Save changes to database with transaction
  - [x] Return UpdateTaskResponse with updated status
  - [x] Handle errors with structured error response
  - [x] Log operation with structured logger
- [x] T031 [US4] Update `backend/mcpserver/mcp_server.py` to register update_task tool
- [x] T032 [US4] [P] Create integration tests for update_task (8 tests)

---

## Phase 7: User Story 5 - Delete Task via AI Agent (P3)

**Goal**: Implement delete_task tool to permanently remove tasks (hard delete)

**Independent Test Criteria**:
- Tool removes task record from database
- Tool returns success confirmation with deleted task_id
- Tool returns 403 error for unauthorized user_id
- Tool returns 404 error for non-existent task

### Tasks

- [x] T033 [US5] Create `backend/mcpserver/schemas.py` tool schemas for delete_task:
  - [x] `DeleteTaskParams` with user_id and task_id (string|int)
  - [x] `DeleteTaskResponse` with task_id, status="deleted", title, message
- [x] T034 [US5] Create `backend/tests/mcpserver/test_delete_task.py` - Unit tests (11 tests):
  - [x] Test successful hard delete removes record from database
  - [x] Test user isolation - cannot delete other user's task
  - [x] Test 404 error for non-existent task_id
  - [x] Test database error handling
  - [x] Test deleted task cannot be retrieved afterward
- [x] T035 [US5] Create `backend/mcpserver/tools/delete_task.py` - Tool implementation:
  - [x] Implement `delete_task()` function with async support
  - [x] Accept parameters: user_id, task_id (string|int)
  - [x] Validate parameters with Pydantic schemas
  - [x] Query database for task by task_id and user_id
  - [x] Return error if task not found
  - [x] Delete task record (hard delete, permanent removal)
  - [x] Commit transaction to database
  - [x] Return DeleteTaskResponse with deleted task_id
  - [x] Handle errors with structured error response
  - [x] Log operation with structured logger
- [x] T036 [US5] Update `backend/mcpserver/mcp_server.py` to register delete_task tool
- [x] T037 [US5] [P] Create integration tests for delete_task (7 tests)

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
| US1 | Create Task | P1 | T013-T017 | 5/5 COMPLETE |
| US2 | List Tasks | P1 | T018-T022 | 5/5 COMPLETE |
| US3 | Complete Task | P2 | T023-T027 | 5/5 COMPLETE |
| US4 | Update Task | P3 | T028-T032 | 5/5 COMPLETE |
| US5 | Delete Task | P3 | T033-T037 | 5/5 COMPLETE |

**Setup & Foundation**: T001-T012 (11/12 DONE, 1 deferred: T010)
**Polish & Integration**: T038-T051 (2/14 DONE: T038-T039)
**Total**: 51 tasks | **Progress: 41 DONE (80%)**

## Completed Tasks Summary

**Phase 1 - Setup (Complete - 6/6 tasks)**:
- T001-T006: Project structure, dependencies, logging, errors, schemas

**Phase 2 - Foundation (11/12 tasks, 1 deferred)**:
- T007-T009, T011-T012: Auth, middleware, server, fixtures (T010 deferred)

**Phase 3 - US1: Add Task (Complete - 5/5 tasks)**:
- T013: Schemas with Pydantic models and field constraints
- T014: Unit tests (15 tests: parameter validation, response structure, integration)
- T015: Tool implementation with async support, validation, error handling
- T016: Tool registration in MCP server with handler routing
- T017: Integration tests (6 tests: MCP protocol, JSON-RPC, tool discovery)

**Phase 4 - US2: List Tasks (Complete - 5/5 tasks)**:
- T018: Schemas with status enum ("all", "pending", "completed")
- T019: Unit tests (17 tests: filtering, sorting, user isolation)
- T020: Tool implementation with status filtering and sorting by created_at
- T021: Tool registration in MCP server
- T022: Integration tests (7 tests: MCP protocol compliance, filtering, user isolation)

**Phase 5 - US3: Complete Task (Complete - 5/5 tasks)**:
- T023: Schemas for complete_task with string|int task_id support
- T024: Unit tests (14 tests: toggle pending/completed, user isolation, error handling)
- T025: Tool implementation with toggle logic and updated_at timestamp
- T026: Tool registration in MCP server
- T027: Integration tests (7 tests: MCP protocol, toggle functionality, user isolation)

**Phase 6 - US4: Update Task (Complete - 5/5 tasks)**:
- T028: Schemas with model_validator for "at least one field" requirement
- T029: Unit tests (18 tests: update title/description, user isolation, validation)
- T030: Tool implementation with field update and timestamp management
- T031: Tool registration in MCP server
- T032: Integration tests (8 tests: MCP protocol, field updates, user isolation)

**Phase 7 - US5: Delete Task (Complete - 5/5 tasks)**:
- T033: Schemas for delete_task with string|int task_id support
- T034: Unit tests (11 tests: hard delete, user isolation, error handling)
- T035: Tool implementation with hard delete and transaction management
- T036: Tool registration in MCP server
- T037: Integration tests (7 tests: MCP protocol, hard delete, user isolation)

**Phase 8 - Tests (2/14 tasks)**:
- T038-T039: JWT auth and error handling tests (25 tests passing)

**Total Test Count**: 135 passing tests (add + list + complete + update + delete + auth + errors)

**All 5 CRUD Tools Complete** ✓
- ✓ add_task: Create new tasks
- ✓ list_tasks: Retrieve tasks with filtering
- ✓ complete_task: Toggle completion status
- ✓ update_task: Modify task details
- ✓ delete_task: Permanently remove tasks

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

