# Feature Specification: ChatKit UI Integration

**Feature Branch**: `007-chatkit-ui-integration`
**Created**: 2026-02-11
**Status**: Draft
**Input**: Add ChatKit streaming UI integration — a backend SSE endpoint that wraps the existing todo AI agent and connects to the Next.js ChatKit conversational UI component

## Overview

Logged-in users need a conversational chat interface embedded in the todo web application. Instead of interacting with tasks through forms and buttons, users type natural language messages ("add buy milk", "show my tasks", "mark task 3 done") and receive real-time streaming replies. This feature adds the backend streaming endpoint and wires the frontend ChatKit UI component to it.

The AI brain (todo agent) already exists and is production-ready. This feature is purely about giving users a live chat window in the browser that talks to that agent.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Real-Time Conversational Chat (Priority: P1)

A logged-in user opens the chat interface, types a natural language message about their tasks, and sees the assistant's reply appear word-by-word in real time — exactly like a modern chat app. The reply is not a raw JSON dump; it is a readable, friendly sentence.

**Why this priority**: This is the entire visible experience of the feature. Without streaming replies, the UI is broken. Every other story builds on this baseline.

**Independent Test**: Open the chat UI, type "show my tasks", and verify the reply streams in character-by-character within 2 seconds of sending.

**Acceptance Scenarios**:

1. **Given** a logged-in user is on the chat page, **When** they type "add buy milk" and press Send, **Then** a streaming reply appears confirming the task was created (e.g., "Created task: 'Buy milk' (ID: 5)")
2. **Given** the user sends a message, **When** the server starts responding, **Then** the first characters appear within 2 seconds — the user does not wait for the full reply before seeing text
3. **Given** the user is not logged in, **When** they attempt to access the chat page, **Then** they are redirected to the login page

---

### User Story 2 — All Five Task Operations via Chat (Priority: P2)

A user can perform every task management operation — create, list, complete, update, and delete — by typing natural language in the chat window, without ever touching a form or button.

**Why this priority**: The chat UI must be functionally equivalent to the existing task management forms for the hackathon Phase III requirement to be met.

**Independent Test**: In one chat session, type five messages covering all five operations and verify each one results in the correct database change.

**Acceptance Scenarios**:

1. **Given** a user types "add pick up kids from school", **When** sent, **Then** a new task appears in the database and the reply confirms it
2. **Given** a user types "show my tasks", **When** sent, **Then** the reply lists all their tasks with IDs and completion status
3. **Given** task ID 3 exists, **When** the user types "mark task 3 as done", **Then** task 3 is marked complete in the database and the reply confirms
4. **Given** task ID 2 exists, **When** the user types "rename task 2 to Buy almond milk", **Then** task 2's title is updated and the reply confirms
5. **Given** task ID 4 exists, **When** the user types "delete task 4", **Then** task 4 is removed and the reply confirms

---

### User Story 3 — Conversation Context Across Messages (Priority: P3)

The chat window maintains context within a session. The user can refer back to prior messages and the assistant understands. Starting a new browser tab begins a fresh conversation.

**Why this priority**: Without context, users cannot do multi-step natural language interactions (e.g., "add groceries" then "also add milk"). Important but the UI is usable without it as a fallback.

**Independent Test**: Send "add buy groceries", then immediately send "also add milk" in the same window. Verify two separate tasks are created and the second reply reflects awareness of the first.

**Acceptance Scenarios**:

1. **Given** a user has sent several messages in one session, **When** they send a follow-up referencing "it" or "that task", **Then** the assistant resolves the reference correctly using prior context
2. **Given** a user opens a fresh browser tab, **When** they open the chat, **Then** there is no history from the previous session visible

---

### User Story 4 — Graceful Error Handling (Priority: P4)

When things go wrong — AI provider down, off-topic question, session expired — the user sees a clear, friendly message and can recover without refreshing the page.

**Why this priority**: Error resilience is required for production quality but the core feature (streaming chat) is usable without it in a demo context.

**Independent Test**: Simulate a provider outage while the chat is open. Verify a friendly error message appears in the chat window within 5 seconds and the input field remains enabled.

**Acceptance Scenarios**:

1. **Given** the AI provider is temporarily unavailable, **When** the user sends a message, **Then** a friendly error appears in the chat within 5 seconds — no blank screen, no raw error code
2. **Given** the user asks "what is the weather?", **When** sent, **Then** the assistant replies explaining it specialises in task management
3. **Given** the user's session has expired, **When** they try to send a message, **Then** they are prompted to log in again

---

### Edge Cases

- What happens when a message exceeds 5000 characters? The UI prevents submission and shows a character-limit warning before sending.
- What happens if the network drops mid-stream? The partially received reply remains visible; the input field becomes active again so the user can retry.
- What happens when a user tries to access another user's conversation by guessing a thread ID? The system returns a "not found" response — no data leakage.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a chat interface accessible to authenticated users from the main application navigation
- **FR-002**: The system MUST stream assistant replies in real time — text appears progressively, not all at once after a delay
- **FR-003**: The chat interface MUST support all five task operations: create, list, complete, update, delete — via natural language input
- **FR-004**: The system MUST authenticate every chat message using the user's existing session — unauthenticated requests must be rejected with a redirect to login
- **FR-005**: The system MUST enforce per-user data isolation — each user can only access and modify their own tasks through the chat interface
- **FR-006**: The system MUST return a user-friendly error message (not a crash or blank screen) when the AI provider is unavailable
- **FR-007**: The system MUST maintain conversation context within a browser session so follow-up messages are understood correctly
- **FR-008**: The chat input MUST reject messages exceeding 5000 characters with a clear validation message before sending
- **FR-009**: The system MUST respond to off-topic requests with a polite scope explanation
- **FR-010**: The chat interface MUST be accessible from the existing web application without requiring a separate login

### Key Entities

- **Chat Thread**: A conversation between one user and the assistant; has a unique ID; contains an ordered list of messages; scoped to one authenticated user; a new thread starts when no prior thread ID is provided
- **Chat Message**: A single turn in the conversation; has a role (user or assistant), text content, and a timestamp; belongs to one thread
- **Streaming Reply**: The progressive text response from the assistant, delivered as a real-time character stream to the browser

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users see the first word of the assistant's reply within 2 seconds of sending a message under normal conditions
- **SC-002**: All five task operations (create, list, complete, update, delete) succeed via natural language with clearly stated intent — 95% success rate in manual testing
- **SC-003**: 100% of unauthenticated chat requests are rejected before the AI agent is invoked
- **SC-004**: AI provider failures produce a visible, friendly error message within 5 seconds — zero blank screens or raw error codes shown to users
- **SC-005**: Off-topic messages receive a scope-explanation reply in 100% of cases — zero silent failures
- **SC-006**: The chat interface renders correctly on both desktop (1280px+) and mobile (375px+) screen sizes

---

## Assumptions

- The todo AI agent (`run_todo_agent`) is already implemented and production-ready (feature 006 complete)
- Users are authenticated via the existing Better Auth session — no new authentication system is needed
- The Next.js frontend can install the ChatKit UI package as a new dependency
- Conversation history persistence is provided by the existing Conversation/Message database tables from feature 006
- The streaming backend endpoint lives in the same FastAPI service as the existing REST API
- A single chat interface per user is sufficient — no multi-room or multi-agent routing needed in this phase
- The ChatKit UI component handles the streaming display logic; the backend's job is to emit the correct stream format
