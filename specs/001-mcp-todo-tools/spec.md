# Feature Specification: MCP Server for Todo Operations

**Feature Branch**: `001-mcp-todo-tools`
**Created**: 2026-02-05
**Status**: Draft
**Input**: User description: "Create a specification for implementing an MCP (Model Context Protocol) server that exposes todo CRUD operations as tools for AI agents to use."

## Clarifications

### Session 2026-02-05

- Q: MCP Server Integration Model - How should the MCP server integrate with FastAPI? → A: MCP server runs as a FastAPI dependency/middleware that intercepts tool invocation requests
- Q: Authentication Context Flow - How does authenticated user context reach MCP tools for validation? → A: JWT token passed in tool invocation metadata/headers, MCP server validates and extracts user_id
- Q: Database Transaction Failure Handling - What happens when a database transaction fails mid-operation? → A: Automatic rollback with retry logic (1-2 attempts) before returning error to AI agent
- Q: Task Deletion Behavior - Is delete_task a hard delete or soft delete? → A: Hard delete - task record is completely removed from database with no recovery possible
- Q: Error and Security Logging Detail Level - What level of detail should be logged for errors and security events? → A: Structured logging with essential context - error type, timestamp, user_id, tool name, operation attempted (JSON format)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create Task via AI Agent (Priority: P1)

An AI agent receives a user request to create a new todo task and uses the MCP tool to add it to the database on behalf of the authenticated user.

**Why this priority**: This is the most fundamental operation - without the ability to create tasks, the AI agent cannot help users build their todo list. This represents the minimum viable functionality.

**Independent Test**: Can be fully tested by invoking the add_task tool with valid parameters and verifying a task record is created in the database with correct ownership and delivers the ability for users to add tasks through natural language conversation.

**Acceptance Scenarios**:

1. **Given** an authenticated user, **When** the AI agent invokes add_task with user_id, title, and description, **Then** a new task is created with completed=False and the agent receives confirmation with task_id
2. **Given** an authenticated user, **When** the AI agent invokes add_task with only user_id and title (no description), **Then** a new task is created with null description and the agent receives confirmation
3. **Given** an authenticated user, **When** the AI agent invokes add_task with missing required fields, **Then** the agent receives a validation error explaining which fields are missing
4. **Given** an authenticated user, **When** the AI agent attempts to create a task for a different user_id, **Then** the agent receives a 403 Forbidden error

---

### User Story 2 - Retrieve Task List via AI Agent (Priority: P1)

An AI agent receives a user request to view their todo tasks and uses the MCP tool to fetch the user's task list from the database.

**Why this priority**: Viewing tasks is equally critical to creating them - users need to see what they've added. Together with task creation, this forms the core read/write functionality.

**Independent Test**: Can be fully tested by invoking the list_tasks tool with a user_id and verifying all tasks belonging to that user are returned, sorted by creation date, and delivers the ability for users to view their tasks through conversation.

**Acceptance Scenarios**:

1. **Given** an authenticated user with 5 tasks, **When** the AI agent invokes list_tasks with user_id and status="all", **Then** all 5 tasks are returned sorted by created_at descending
2. **Given** an authenticated user with 3 completed and 2 pending tasks, **When** the AI agent invokes list_tasks with status="completed", **Then** only the 3 completed tasks are returned
3. **Given** an authenticated user with 3 completed and 2 pending tasks, **When** the AI agent invokes list_tasks with status="pending", **Then** only the 2 pending tasks are returned
4. **Given** an authenticated user, **When** the AI agent attempts to list tasks for a different user_id, **Then** the agent receives a 403 Forbidden error
5. **Given** an authenticated user, **When** the AI agent invokes list_tasks with an invalid status value, **Then** the agent receives a validation error

---

### User Story 3 - Mark Task Complete via AI Agent (Priority: P2)

An AI agent receives a user request to mark a task as complete and uses the MCP tool to toggle the task's completion status.

**Why this priority**: Completing tasks is a primary use case for todo lists. This enables the core workflow of adding and completing tasks, though users can still add and view tasks without this.

**Independent Test**: Can be fully tested by invoking the complete_task tool with a valid task_id and verifying the completed field is toggled and delivers the ability for users to mark tasks done through conversation.

**Acceptance Scenarios**:

1. **Given** an authenticated user with a pending task, **When** the AI agent invokes complete_task with the task_id, **Then** the task's completed field changes to True and updated_at is refreshed
2. **Given** an authenticated user with a completed task, **When** the AI agent invokes complete_task with the task_id, **Then** the task's completed field changes to False (toggle)
3. **Given** an authenticated user, **When** the AI agent attempts to complete a task belonging to a different user, **Then** the agent receives a 403 Forbidden error
4. **Given** an authenticated user, **When** the AI agent attempts to complete a non-existent task_id, **Then** the agent receives a 404 Not Found error

---

### User Story 4 - Update Task Details via AI Agent (Priority: P3)

An AI agent receives a user request to modify a task's title or description and uses the MCP tool to update the task in the database.

**Why this priority**: Updating tasks enhances usability but is not critical for the core workflow. Users can still create, view, and complete tasks without this capability.

**Independent Test**: Can be fully tested by invoking the update_task tool with a task_id and new title/description and verifying the task record is updated and delivers the ability for users to edit tasks through conversation.

**Acceptance Scenarios**:

1. **Given** an authenticated user with a task, **When** the AI agent invokes update_task with a new title, **Then** the task's title is updated and updated_at is refreshed
2. **Given** an authenticated user with a task, **When** the AI agent invokes update_task with a new description, **Then** the task's description is updated and updated_at is refreshed
3. **Given** an authenticated user with a task, **When** the AI agent invokes update_task with both new title and description, **Then** both fields are updated
4. **Given** an authenticated user, **When** the AI agent invokes update_task without providing title or description, **Then** the agent receives a validation error
5. **Given** an authenticated user, **When** the AI agent attempts to update a task belonging to a different user, **Then** the agent receives a 403 Forbidden error
6. **Given** an authenticated user, **When** the AI agent attempts to update a non-existent task_id, **Then** the agent receives a 404 Not Found error

---

### User Story 5 - Delete Task via AI Agent (Priority: P3)

An AI agent receives a user request to remove a task and uses the MCP tool to permanently delete it from the database.

**Why this priority**: Deleting tasks is useful for cleanup but not essential for core functionality. Users can still create, view, complete, and update tasks without this capability.

**Independent Test**: Can be fully tested by invoking the delete_task tool with a valid task_id and verifying the task is removed from the database and delivers the ability for users to remove tasks through conversation.

**Acceptance Scenarios**:

1. **Given** an authenticated user with a task, **When** the AI agent invokes delete_task with the task_id, **Then** the task is permanently removed from the database and the agent receives confirmation
2. **Given** an authenticated user, **When** the AI agent attempts to delete a task belonging to a different user, **Then** the agent receives a 403 Forbidden error
3. **Given** an authenticated user, **When** the AI agent attempts to delete a non-existent task_id, **Then** the agent receives a 404 Not Found error

---

### Edge Cases

- What happens when a user has zero tasks and list_tasks is invoked?
  - System returns empty tasks array with count=0
- What happens when title exceeds 200 characters in add_task or update_task?
  - System returns validation error with character limit information
- What happens when description exceeds 1000 characters in add_task or update_task?
  - System returns validation error with character limit information
- What happens when the database connection fails during a tool operation?
  - System logs the error internally and returns a safe error message to the agent without exposing internal details
- What happens when two AI agents attempt to modify the same task concurrently?
  - Database transaction handling ensures data consistency, last write wins
- What happens when user_id format is invalid?
  - System returns validation error indicating invalid user_id format
- What happens when task_id is a string instead of integer?
  - System returns validation error indicating invalid task_id type
- What happens when status parameter has a typo (e.g., "complet" instead of "completed")?
  - System returns validation error listing valid status values: "all", "pending", "completed"

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST expose an add_task tool that creates a new task record in the database for the authenticated user
- **FR-002**: System MUST expose a list_tasks tool that retrieves all tasks belonging to the authenticated user with optional status filtering
- **FR-003**: System MUST expose a complete_task tool that toggles the completion status of a task owned by the authenticated user
- **FR-004**: System MUST expose a delete_task tool that permanently removes a task owned by the authenticated user via hard delete (complete removal from database with no recovery possible)
- **FR-005**: System MUST expose an update_task tool that modifies the title or description of a task owned by the authenticated user
- **FR-006**: System MUST validate user_id parameter in every tool invocation matches the authenticated user extracted from JWT token in tool invocation metadata/headers
- **FR-006a**: System MUST validate JWT token signature and expiration before extracting user_id from token claims
- **FR-007**: System MUST prevent cross-user data access by enforcing user_id filtering on all database queries
- **FR-008**: System MUST validate all required parameters before executing tool operations
- **FR-009**: System MUST return structured JSON responses with consistent format across all tools
- **FR-010**: System MUST distinguish between client errors (4xx) and server errors (5xx) in error responses
- **FR-011**: System MUST log authorization failures for security monitoring using structured JSON format with error type, timestamp, user_id, tool name, and operation attempted
- **FR-012**: System MUST log all errors for debugging purposes using structured JSON format with error type, timestamp, user_id, tool name, and operation attempted
- **FR-013**: System MUST never expose internal errors or stack traces to the AI agent
- **FR-014**: System MUST auto-generate timestamps (created_at, updated_at) for task records
- **FR-015**: System MUST set completed=False by default when creating new tasks
- **FR-016**: System MUST update updated_at timestamp whenever a task is modified
- **FR-017**: System MUST sort tasks by created_at descending when returning task lists
- **FR-018**: System MUST enforce title length limit of 200 characters
- **FR-019**: System MUST enforce description length limit of 1000 characters
- **FR-020**: System MUST support status filtering with values: "all", "pending", "completed"
- **FR-021**: System MUST require at least one field (title or description) when updating a task
- **FR-022**: System MUST use existing SQLModel Task model without creating new models
- **FR-023**: System MUST reuse existing database connection and session management
- **FR-024**: System MUST use database transactions for data consistency with automatic rollback and retry logic (1-2 attempts) on transient failures
- **FR-025**: System MUST handle concurrent tool calls safely
- **FR-026**: System MUST remain stateless with all state stored in the database
- **FR-027**: System MUST register all 5 tools at MCP server startup
- **FR-028**: System MUST integrate MCP server as a FastAPI dependency/middleware that intercepts tool invocation requests, ensuring proper authentication context flow
- **FR-029**: System MUST return user-friendly error messages suitable for AI agent to relay to users
- **FR-030**: System MUST properly close/commit all database operations

### Key Entities *(include if feature involves data)*

- **Task**: Represents a todo item owned by a user. Key attributes: id (unique identifier), user_id (owner), title (task name, 1-200 characters), description (task details, optional, max 1000 characters), completed (boolean status), created_at (timestamp), updated_at (timestamp). Relationships: belongs to a User.

- **Tool Response**: Represents the structured output returned by MCP tools to the AI agent. Key attributes: task_id (for operations affecting single tasks), status (operation result: "created", "completed", "uncompleted", "updated", "deleted", "success"), title (task title for context), message (user-friendly description), tasks array (for list operations), count (number of tasks returned). Format: JSON-serializable dictionary.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: AI agent can successfully create a task and receive confirmation within 2 seconds under normal load
- **SC-002**: AI agent can retrieve a user's complete task list within 1 second for lists up to 100 tasks
- **SC-003**: AI agent can mark a task complete and receive confirmation within 1 second
- **SC-004**: AI agent can update task details and receive confirmation within 1 second
- **SC-005**: AI agent can delete a task and receive confirmation within 1 second
- **SC-006**: 100% of unauthorized access attempts (wrong user_id) are blocked with 403 Forbidden response
- **SC-007**: Users can only access and modify their own tasks, never seeing tasks belonging to other users
- **SC-008**: All error messages returned to AI agent are clear and actionable without exposing internal system details
- **SC-009**: System handles 50 concurrent tool invocations without data corruption or race conditions
- **SC-010**: 100% of tool responses follow consistent JSON format as specified
- **SC-011**: All validation errors clearly indicate which parameter is invalid and why
- **SC-012**: System recovers gracefully from database connection failures by automatically retrying (1-2 attempts) before returning appropriate error messages
- **SC-013**: Unit test coverage reaches at least 70% for all tool handler functions
- **SC-014**: Integration tests successfully verify user isolation (user A cannot access user B's tasks)
- **SC-015**: All 5 tools (add_task, list_tasks, complete_task, delete_task, update_task) are registered and invocable by the AI agent

### Assumptions

- The existing Better Auth JWT authentication is functioning correctly and provides reliable user_id
- The existing SQLModel Task model schema matches the requirements (id, user_id, title, description, completed, created_at, updated_at)
- The existing database connection pooling is properly configured for concurrent access
- The FastAPI application is already configured to handle database sessions
- The chat endpoint will pass authenticated user context when invoking MCP tools
- The Official MCP SDK for Python is compatible with the FastAPI application architecture
- Database transactions will use the default isolation level configured in the existing application
- Task creation, completion, update, and deletion operations do not trigger additional business logic beyond database persistence
- The AI agent invoking these tools has already verified user intent and handles conversational context
- Network latency between FastAPI application and Neon PostgreSQL database is reasonable (under 100ms)

### Dependencies

- Official MCP SDK for Python (must be installed via pip/uv)
- Existing SQLModel Task model from Phase II implementation
- Existing database connection and session management system
- Existing Better Auth JWT authentication system
- Existing FastAPI application infrastructure
- Existing Neon PostgreSQL database
- Chat endpoint from Phase III Spec 1 (Chatbot UI Integration)

### Out of Scope

- OpenAI Agents SDK integration (handled in separate specification)
- Chat endpoint logic and conversation management (already implemented in Spec 1)
- Natural language parsing or intent recognition (handled by AI agent layer)
- Frontend UI changes or modifications
- Advanced task features: search, complex filtering, sorting beyond status
- Task priority, tags, categories, or metadata
- Task due dates, reminders, or scheduling
- Task attachments or file uploads
- Task sharing or collaboration between users
- Task history or audit trail
- Bulk task operations (delete multiple, complete multiple)
- Task templates or recurring tasks
- Performance optimization beyond basic database queries
- Caching layer or in-memory state
- Real-time updates or WebSocket notifications
- Rate limiting or throttling of tool invocations
- Detailed logging or monitoring dashboards
- Migration scripts for database schema changes
