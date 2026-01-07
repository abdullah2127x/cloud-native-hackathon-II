# Tasks: CLI Todo Application

**Feature**: CLI Todo Application
**Branch**: 001-cli-todo
**Input**: Feature specification and implementation plan from `/specs/001-cli-todo/`

## Implementation Strategy

MVP scope: Implement User Story 1 (Add and View Tasks) with basic interactive CLI functionality. Deliver core functionality first, then enhance with additional user stories.

## Dependencies

User stories should be implemented in priority order:
- US1 (P1) → US2 (P2) → US3 (P3)
- Each story builds on the foundational components established in earlier phases

## Parallel Execution Examples

Within each user story, these tasks can be executed in parallel:
- Model creation and validation utilities
- Service implementation and unit tests
- CLI interface components

## Phase 1: Setup

- [ ] T001 Create project structure with src/, tests/ directories per implementation plan
- [ ] T002 Set up Python project with pyproject.toml and dependencies (inquirer, py-cli-beautifier, python-test-generator)
- [ ] T003 Create initial directory structure: src/models/, src/services/, src/cli/, src/lib/, tests/unit/, tests/integration/

## Phase 2: Foundational Components

- [ ] T004 [P] Create Task model in src/models/task.py with id, title, description, completed fields
- [ ] T005 [P] Create TaskList model in src/models/task_list.py with tasks list and next_id counter
- [ ] T006 [P] Create validators module in src/lib/validators.py for input validation
- [ ] T007 [P] Create requirements.txt with project dependencies
- [ ] T008 Create basic test structure in tests/ with conftest.py

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1)

**Goal**: Implement core functionality to add new tasks and view all tasks in the CLI

**Independent Test**: Can be fully tested by adding tasks through the command-line interface and viewing the list of tasks. Delivers the fundamental value of task tracking.

- [ ] T009 [P] [US1] Create TaskService in src/services/task_service.py with add_task and get_all_tasks methods
- [ ] T010 [P] [US1] Generate unit tests for Task model in tests/unit/test_task.py using python-test-generator
- [ ] T011 [P] [US1] Generate unit tests for TaskList model in tests/unit/test_task_list.py using python-test-generator
- [ ] T012 [US1] Generate unit tests for TaskService add_task and get_all_tasks in tests/unit/test_task_service.py using python-test-generator
- [ ] T013 [P] [US1] Create basic CLI main module in src/cli/main.py with entry point
- [ ] T014 [P] [US1] Create interactive CLI interface in src/cli/interactive_cli.py with basic menu structure
- [ ] T015 [US1] Implement add task functionality with validation in interactive CLI
- [ ] T016 [US1] Implement view tasks functionality with basic display in interactive CLI
- [ ] T017 [US1] Integrate TaskService with interactive CLI for add/view operations
- [ ] T018 [US1] Add error handling for empty titles with user prompt in validators
- [ ] T019 [US1] Test User Story 1 acceptance scenarios: add task and view tasks

## Phase 4: User Story 2 - Update and Delete Tasks (Priority: P2)

**Goal**: Implement functionality to update or delete tasks from the todo list

**Independent Test**: Can be fully tested by updating task details and deleting tasks by ID. Delivers the value of maintaining an up-to-date task list.

- [ ] T020 [P] [US2] Extend TaskService with update_task and delete_task methods in src/services/task_service.py
- [ ] T021 [P] [US2] Generate unit tests for update_task in tests/unit/test_task_service.py using python-test-generator
- [ ] T022 [P] [US2] Generate unit tests for delete_task in tests/unit/test_task_service.py using python-test-generator
- [ ] T023 [US2] Implement update task functionality in interactive CLI with ID validation
- [ ] T024 [US2] Implement delete task functionality in interactive CLI with ID validation
- [ ] T025 [US2] Add validation for task existence before update/delete operations
- [ ] T026 [US2] Integrate update/delete operations with TaskService in interactive CLI
- [ ] T027 [US2] Test User Story 2 acceptance scenarios: update and delete tasks

## Phase 5: User Story 3 - Mark Tasks as Complete (Priority: P3)

**Goal**: Implement functionality to mark tasks as complete/incomplete to track progress

**Independent Test**: Can be fully tested by marking tasks as complete/incomplete and viewing the updated status. Delivers the value of progress tracking.

- [ ] T028 [P] [US3] Extend TaskService with toggle_task_completion method in src/services/task_service.py
- [ ] T029 [P] [US3] Generate unit tests for toggle_task_completion in tests/unit/test_task_service.py using python-test-generator
- [ ] T030 [US3] Implement mark complete/incomplete functionality in interactive CLI
- [ ] T031 [US3] Add visual indicators for completed vs pending tasks in CLI display
- [ ] T032 [US3] Integrate toggle completion with TaskService in interactive CLI
- [ ] T033 [US3] Test User Story 3 acceptance scenarios: mark complete/incomplete

## Phase 6: Interactive CLI Enhancement

**Goal**: Enhance CLI with arrow-key navigation and beautified output as specified

- [ ] T034 [P] Integrate inquirer library for interactive selection in src/cli/interactive_cli.py
- [ ] T035 Implement arrow-key navigation for menu selection in interactive CLI
- [ ] T035.1 [P] [US1] Implement arrow-key navigation for task selection in view operations
- [ ] T035.2 [P] [US2] Implement arrow-key navigation for task selection in update operations
- [ ] T035.3 [P] [US2] Implement arrow-key navigation for task selection in delete operations
- [ ] T035.4 [P] [US3] Implement arrow-key navigation for task selection in mark complete operations
- [ ] T036 [P] Integrate py-cli-beautifier for colored output and formatting
- [ ] T037 Add icons and colors to distinguish completed vs pending tasks
- [ ] T038 Enhance task display with formatting using py-cli-beautifier
- [ ] T039 Implement proper error messages with formatting using py-cli-beautifier
- [ ] T039.1 [US1] Add pagination or scrolling for displaying many tasks in view operations

## Phase 7: Edge Cases and Validation

**Goal**: Handle all edge cases and validation scenarios as specified

- [ ] T040 [P] Add validation for non-existent tasks during update/delete operations
- [ ] T040.1 [US2] Handle non-existent task update with appropriate error message
- [ ] T040.2 [US2] Handle non-existent task delete with appropriate error message
- [ ] T041 Add validation for invalid task IDs during operations
- [ ] T042 Handle empty task list scenario in view operations
- [ ] T042.1 [US1] Handle empty task list when viewing with appropriate message
- [ ] T043 Add description length validation (max 500 characters)
- [ ] T044 Add proper error handling and user feedback for all operations
- [ ] T044.1 [US1] Handle empty task title input with user prompt and validation
- [ ] T044.2 [US2,US3] Handle invalid task IDs during operations with error message
- [ ] T045 Generate contract tests for TaskService interface in tests/contract/test_task_service_contract.py

## Phase 8: Integration and Polish

**Goal**: Complete integration testing and polish the application

- [ ] T046 [P] Create integration tests for CLI interface in tests/integration/test_cli.py
- [ ] T047 Test complete user workflows across all functionality
- [ ] T048 Add comprehensive error handling throughout application
- [ ] T049 Verify application handles 100+ tasks in memory with <5 seconds response time per operation per SC-001, <100MB memory usage per constitution
- [ ] T050 Final testing and validation of all user stories and requirements
- [ ] T051 Update quickstart guide with complete usage instructions
- [ ] T052 Verify all implemented functionality complies with constitution principles (no network communication, in-memory only, TDD approach)