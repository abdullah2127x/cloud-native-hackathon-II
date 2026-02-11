# Feature Specification: AI Agent MCP Integration for Todo Chatbot

**Feature Branch**: `006-agent-mcp-integration`
**Created**: 2026-02-11
**Status**: Draft
**Input**: User description: "i have tested all the test passes now generate the spec for the current task related to openai agents sdk integration using mcps that we discussed now"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Natural Language Task Management via Chat (Priority: P1)

A logged-in user types a natural language message (e.g., "Add buy groceries to my list") into the chat interface. The system interprets the message, invokes the appropriate MCP tool (`add_task`), and responds with a friendly confirmation ("Done! I added 'Buy groceries' to your list").

**Why this priority**: This is the core value proposition of Phase III — turning the app from a form-based CRUD UI into a conversational AI interface. Without this, the chatbot has no purpose.

**Independent Test**: Can be fully tested by sending a POST request to the chat endpoint with a natural language message and verifying the task is created in the database and a confirmation response is returned.

**Acceptance Scenarios**:

1. **Given** a logged-in user with no tasks, **When** they send "Add a task to buy groceries", **Then** a new task titled "Buy groceries" is created and the agent responds with a confirmation message.
2. **Given** a user sends "Show me all my tasks", **Then** the agent calls `list_tasks` and returns a readable summary of the user's tasks.
3. **Given** a user sends "Mark task 3 as complete", **Then** the agent calls `complete_task` for task 3 and confirms the update.
4. **Given** a user sends "Delete the groceries task", **Then** the agent calls `list_tasks` to find it, then calls `delete_task`, and confirms deletion.
5. **Given** a user sends "Change task 1 to 'Call mom tonight'", **Then** the agent calls `update_task` and confirms the new title.

---

### User Story 2 - Persistent Conversation Context Across Requests (Priority: P2)

A user sends multiple messages in a session. The chatbot remembers what was said earlier in the conversation so follow-up messages like "actually, delete that one" or "and also add milk" are understood in context.

**Why this priority**: Stateless per-message processing without history makes the chatbot feel broken for multi-turn conversations. Conversation persistence directly impacts usability.

**Independent Test**: Can be tested by sending two consecutive messages — first creating a task, then referencing "it" in a follow-up — and verifying the agent understands the reference from prior context.

**Acceptance Scenarios**:

1. **Given** a user previously created "Buy groceries" in the same conversation, **When** they send "also add milk", **Then** the agent creates a new task without confusion about context.
2. **Given** a user starts a new chat session (no conversation_id provided), **When** they send a message, **Then** no history from a previous session is loaded, and a new conversation_id is returned.
3. **Given** a server restart after a conversation, **When** the user sends a follow-up with the same conversation_id, **Then** the agent still has access to the full prior message history from the database.

---

### User Story 3 - Graceful Error Handling in Conversations (Priority: P3)

When the agent cannot fulfill a request (e.g., task not found, ambiguous command), it responds with a helpful message rather than failing silently or returning a raw error.

**Why this priority**: Error recovery directly impacts user trust. A chatbot that crashes or gives raw error messages feels unpolished.

**Independent Test**: Can be tested by asking the agent to complete or delete a task that does not exist and verifying a friendly, informative response is returned.

**Acceptance Scenarios**:

1. **Given** a user says "Mark task 999 as complete" and task 999 does not exist, **Then** the agent responds with a friendly message indicating the task was not found.
2. **Given** a user sends a completely unrelated message (e.g., "What's the weather?"), **Then** the agent responds helpfully, explaining it specializes in todo management.
3. **Given** a tool call fails due to a database error, **Then** the agent responds with a user-friendly apology and does not expose internal error details.

---

### Edge Cases

- What happens when the user sends an empty message?
- How does the system handle a very long message (over 5000 characters)?
- What if the agent tries to call a non-existent tool?
- What happens when two requests arrive simultaneously for the same conversation_id?
- What happens if the user provides a conversation_id that belongs to a different user?
- **AI provider failure**: If the AI provider (OpenRouter) fails or times out, the endpoint MUST return HTTP 503 with a friendly user-facing message. No retries are attempted. The user message IS still persisted to the database before the provider call so it is not lost.
- **Concurrent requests**: If two messages arrive simultaneously for the same conversation_id, both are processed independently. Message ordering in the conversation history is determined by database insertion timestamp.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a stateless HTTP endpoint (`POST /api/{user_id}/chat`) that accepts a user message and an optional conversation_id, runs the AI agent, and returns the agent's response.
- **FR-002**: The chat endpoint MUST be stateless — it fetches full conversation history from the database on every request and holds no in-memory conversation state between requests.
- **FR-003**: The AI agent MUST use the existing MCP server tools (`add_task`, `list_tasks`, `complete_task`, `update_task`, `delete_task`) to execute task operations requested in natural language.
- **FR-004**: The system MUST persist every user message and every agent response to the database, associated with the correct conversation_id.
- **FR-005**: When no conversation_id is provided, the system MUST create a new Conversation record and return the new conversation_id in the response.
- **FR-006**: When a valid conversation_id is provided, the system MUST load the most recent 50 messages for that conversation from the database and include them in the agent's context window. If fewer than 50 messages exist, all are loaded.
- **FR-007**: The agent MUST correctly handle all natural language command patterns for creating, listing (all/pending/completed), completing, deleting, and updating tasks.
- **FR-008**: The chat response MUST include the conversation_id, the agent's text response, and the list of MCP tool names that were invoked during the request.
- **FR-009**: The chat endpoint MUST reject requests without a valid authentication token with a 401 Unauthorized response.
- **FR-010**: The system MUST enforce user isolation — a user can only access their own conversation history and tasks; accessing another user's conversation_id returns 404.
- **FR-011**: The system MUST create two new database models — Conversation and Message — to store chat state persistently.

### Key Entities

- **Conversation**: Represents a chat session. Owned by a user (user_id), has a unique identifier, and tracks creation and last-update timestamps.
- **Message**: A single turn in a conversation. Belongs to a Conversation, has a role (`user` or `assistant` only — tool calls are not stored as messages), text content, and a creation timestamp.
- **AgentResponse**: The structured output returned by the endpoint — includes the agent's reply text, the conversation_id, and the list of tool names invoked.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can send a natural language message and receive a task confirmation response in under 5 seconds under normal load.
- **SC-002**: All 5 task operations (create, list, complete, update, delete) are accessible through conversational language without requiring exact command syntax.
- **SC-003**: Conversation history is correctly restored after a server restart — users can resume prior conversations with full context preserved.
- **SC-004**: The chat endpoint handles at least 10 concurrent users without returning errors.
- **SC-005**: 100% of tool invocations are correctly reflected in the database — no task operation is silently lost.
- **SC-006**: All error scenarios return human-readable messages — no raw exceptions or stack traces are ever exposed to the user.

## Clarifications

### Session 2026-02-11

- Q: When loading conversation history into the agent context, should there be a maximum number of messages? → A: Last 50 messages per conversation (cap at 50, load all if fewer exist)
- Q: When the AI provider fails or times out, what should the endpoint return? → A: Return 503 immediately with a friendly user-facing message (no retries)
- Q: If two messages arrive simultaneously for the same conversation_id, how should the system behave? → A: Process both independently; message ordering determined by DB insertion timestamp (last-write-wins)
- Q: Should tool calls/results be stored as messages in the database? → A: Store only user and assistant text turns; tool invocations are not persisted as separate message records

## Assumptions

- The existing MCP server (`mcpserver/mcp_server.py`) is production-ready and all 5 tools are tested and passing. No changes to MCP tool logic are needed for this feature.
- The existing database models (Task, User) do not need modification — only the two new models (Conversation, Message) are added.
- Authentication is handled by the existing Better Auth + JWT pattern already implemented. No auth changes are required.
- The AI provider is OpenRouter with a configurable model via environment variable. No provider-switching UI is required in this phase.
- The ChatKit frontend integration is a separate concern — this spec covers only the backend agent wiring and chat endpoint.
- Conversation history is stored indefinitely (no expiry or pruning in this phase).
