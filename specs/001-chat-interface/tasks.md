# Tasks: OpenAI ChatKit Conversation Interface

**Feature**: 001-chat-interface | **Generated**: 2026-02-04 | **Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

## Task Organization

Tasks are organized by **user story** to enable independent implementation and testing. Each user story represents a vertical slice of functionality that can be developed, tested, and delivered independently.

### User Story Mapping

- **Setup & Foundations**: Infrastructure tasks required before any user story implementation
- **User Story 1 (P1)**: Start a New Chat Conversation
- **User Story 2 (P1)**: Persist and Resume Conversations
- **User Story 3 (P2)**: View Conversation History List
- **User Story 4 (P2)**: Handle Errors and Timeouts Gracefully
- **Polish & Deployment**: Cross-cutting concerns and deployment readiness

---

## Task Checklist

### Phase: Setup & Foundations

Tasks in this phase establish the infrastructure needed for all user stories.

- [X] [T001] [P] Install frontend dependencies: `npm install react-virtuoso @openai/chatkit` (frontend/package.json)
- [X] [T002] [P] Install backend dependencies: `uv add sqlmodel pydantic` (backend/pyproject.toml)
- [X] [T003] Create Conversation SQLModel with id, user_id, created_at, updated_at fields and messages relationship (backend/app/models/conversation.py)
- [X] [T004] Create Message SQLModel with id, user_id, conversation_id FK CASCADE, role enum, content, created_at and conversation relationship (backend/app/models/message.py)
- [X] [T005] Generate database migration: `alembic revision --autogenerate -m "Add conversation and message tables"` (backend/migrations/versions/)
- [X] [T006] Verify migration includes CASCADE DELETE on message.conversation_id foreign key, all indexes created correctly (backend/migrations/versions/XXXX_add_conversation_message_tables.py)
- [X] [T007] Run migration: `alembic upgrade head` and verify tables exist with `\d conversation` and `\d message` (database)
- [X] [T008] Create Pydantic ChatRequest schema with conversation_id (optional UUID) and message (string 1-4000 chars) (backend/app/schemas/chat.py)
- [X] [T009] Create Pydantic ChatResponse schema with conversation_id UUID, message string, role "assistant", created_at datetime (backend/app/schemas/chat.py)
- [X] [T010] Create Pydantic ErrorResponse schema with error string and detail string (backend/app/schemas/chat.py)
- [X] [T011] [Story:Setup] Write unit tests for Conversation model: creation, relationships, timestamps (backend/tests/test_models_conversation.py)
- [X] [T012] [Story:Setup] Write unit tests for Message model: creation, foreign key, CASCADE delete, role validation (backend/tests/test_models_message.py)
- [X] [T013] [Story:Setup] Write unit tests for Pydantic schemas: validation, field types, required fields (backend/tests/test_schemas_chat.py)

**Dependencies**: T003-T004 → T005, T005 → T006 → T007, T008-T010 → T013

---

### Phase: User Story 1 (P1) - Start a New Chat Conversation

**Objective**: Enable authenticated users to navigate to chat interface, see empty state, send messages, and receive AI responses.

**Acceptance Scenarios**: 5 scenarios from spec.md (load empty state, type message, submit, see typing indicator, chronological order)

#### Backend: Chat Endpoint

- [X] [T101] [Story:US1] Create POST `/api/{user_id}/chat` route with JWT dependency, verify user_id matches token or return 403 (backend/app/routes/chat.py)
- [X] [T102] [Story:US1] Implement stateless conversation history fetch: if conversation_id provided, fetch from database with user_id filter or return 404 (backend/app/routes/chat.py)
- [X] [T103] [Story:US1] Implement new conversation creation: if no conversation_id, create Conversation with user_id and commit (backend/app/routes/chat.py)
- [X] [T104] [Story:US1] Save user message to database BEFORE AI processing with user_id, conversation_id, role "user", content from request (backend/app/routes/chat.py)
- [X] [T105] [Story:US1] Add placeholder AI agent call (returns "I received: {message}" for now - actual AI logic in separate spec) (backend/app/routes/chat.py)
- [X] [T106] [Story:US1] Save AI response message to database with role "assistant", update conversation.updated_at, return ChatResponse (backend/app/routes/chat.py)
- [X] [T107] [Story:US1] Write endpoint test: 200 with conversation_id on successful request (backend/tests/test_routes_chat.py)
- [X] [T108] [Story:US1] Write endpoint test: 401 without valid JWT token (backend/tests/test_routes_chat.py)
- [X] [T109] [Story:US1] Write endpoint test: 403 if user_id doesn't match JWT user_id (backend/tests/test_routes_chat.py)
- [X] [T110] [Story:US1] Write endpoint test: 404 if conversation_id not found or not owned by user (backend/tests/test_routes_chat.py)
- [X] [T111] [Story:US1] Write endpoint test: verify user and assistant messages saved to database (backend/tests/test_routes_chat.py)
- [X] [T112] [Story:US1] Write endpoint test: verify stateless behavior (conversation history fetched from DB on each request) (backend/tests/test_routes_chat.py)

**Dependencies**: T001-T013 → T101, T101 → T102-T103, T102-T103 → T104, T104 → T105 → T106, T101-T106 → T107-T112

#### Frontend: Chat Page & ChatKit Component

- [X] [T121] [Story:US1] Create `/app/chat/page.tsx` route with Server Component wrapper and Better Auth session check, redirect to login if unauthenticated (frontend/app/chat/page.tsx)
- [X] [T122] [Story:US1] Create ChatContainer client component with useChatKit hook, custom fetch injecting JWT Bearer token, domainKey from env var (frontend/app/components/chat/ChatContainer.tsx)
- [X] [T123] [Story:US1] Implement custom fetch function: extract session token via Better Auth, inject Authorization header, call `/api/{user_id}/chat` (frontend/app/components/chat/ChatContainer.tsx)
- [X] [T124] [Story:US1] Add onError handler to useChatKit capturing errors to console (will enhance in US4) (frontend/app/components/chat/ChatContainer.tsx)
- [X] [T125] [Story:US1] Create MessageList component with React Virtuoso, configure initialTopMostItemIndex to messages.length-1, followOutput "smooth" (frontend/app/components/chat/MessageList.tsx)
- [X] [T126] [Story:US1] Implement message rendering in MessageList: user messages right-aligned, assistant left-aligned, display content and timestamp (frontend/app/components/chat/MessageList.tsx)
- [X] [T127] [Story:US1] Create ChatInput component with text input field, send button, Enter key submission (frontend/app/components/chat/ChatInput.tsx)
- [X] [T128] [Story:US1] Update NavBar to include "Chat" link routing to `/chat` (frontend/app/components/navigation/NavBar.tsx)
- [X] [T129] [Story:US1] Create API client function `sendMessage(user_id, message, conversation_id?, token)` calling POST endpoint (frontend/app/lib/api/chat.ts)
- [X] [T130] [Story:US1] Write component test: ChatContainer initializes useChatKit with correct config (frontend/__tests__/chat/ChatContainer.test.tsx)
- [X] [T131] [Story:US1] Write component test: MessageList renders messages in correct order, scrolls to bottom (frontend/__tests__/chat/MessageList.test.tsx)
- [X] [T132] [Story:US1] Write component test: ChatInput accepts text, submits on Enter/button click, clears after submit (frontend/__tests__/chat/ChatInput.test.tsx)
- [X] [T133] [Story:US1] Integration test: user sends message → saved to DB → AI responds → response saved → UI updates (frontend/__tests__/integration/chat-flow.test.tsx)

**Dependencies**: T101-T106 (backend ready) → T121, T121 → T122, T122 → T123-T124, T001 → T125, T125 → T126, T127 parallel to T125-T126, T128 parallel to T121-T127, T123 → T129, T122-T129 → T130-T133

---

### Phase: User Story 2 (P1) - Persist and Resume Conversations

**Objective**: Enable conversation persistence across page refreshes and navigation events.

**Acceptance Scenarios**: 4 scenarios from spec.md (refresh preserves history, return shows option, continue loads full history, new conversation creates new ID)

#### Backend: Conversation List & Detail Endpoints

- [x] [T201] [Story:US2] Create GET `/api/{user_id}/conversations` route with JWT dependency, pagination (limit, offset) query params (backend/app/routes/chat.py)
- [x] [T202] [Story:US2] Implement conversation list query: fetch conversations WHERE user_id = authenticated user, ORDER BY updated_at DESC, no messages loaded (backend/app/routes/chat.py)
- [x] [T203] [Story:US2] Return ConversationList schema with conversations array, total count, limit, offset (backend/app/routes/chat.py)
- [x] [T204] [Story:US2] Create GET `/api/{user_id}/conversations/{conversation_id}` route with JWT dependency (backend/app/routes/chat.py)
- [x] [T205] [Story:US2] Implement conversation detail query: fetch conversation with selectinload(messages), filter by user_id for security, return 404 if not found (backend/app/routes/chat.py)
- [x] [T206] [Story:US2] Return ConversationDetail schema with id, timestamps, messages array ordered by created_at (backend/app/routes/chat.py)
- [x] [T207] [Story:US2] Write endpoint test: GET /conversations returns user's conversations only, excludes other users (backend/tests/test_routes_chat.py)
- [x] [T208] [Story:US2] Write endpoint test: GET /conversations/{id} returns conversation with messages, 404 if not owned by user (backend/tests/test_routes_chat.py)
- [x] [T209] [Story:US2] Write endpoint test: pagination works correctly (limit, offset) (backend/tests/test_routes_chat.py)
- [x] [T210] [Story:US2] Write endpoint test: verify user isolation (User A cannot access User B's conversations) (backend/tests/test_routes_chat.py)

**Dependencies**: T101-T112 → T201, T201 → T202 → T203, T204 → T205 → T206, T201-T206 → T207-T210

#### Frontend: History Loading & State Management

- [x] [T221] [Story:US2] Create useConversationHistory hook: fetch conversation list on mount, return conversations state (frontend/app/hooks/useConversationHistory.ts)
- [x] [T222] [Story:US2] Create API client function `listConversations(user_id, token, limit?, offset?)` calling GET endpoint (frontend/app/lib/api/chat.ts)
- [x] [T223] [Story:US2] Create API client function `getConversation(user_id, conversation_id, token)` calling GET endpoint (frontend/app/lib/api/chat.ts)
- [x] [T224] [Story:US2] Create useChat hook: manage conversation_id state, handle message submission, update conversation list on new message (frontend/app/hooks/useChat.ts)
- [x] [T225] [Story:US2] Integrate useConversationHistory into ChatContainer: load conversation on page mount, pass to MessageList (frontend/app/components/chat/ChatContainer.tsx)
- [x] [T226] [Story:US2] Add conversation_id persistence: store in localStorage or URL parameter for session recovery (frontend/app/components/chat/ChatContainer.tsx)
- [x] [T227] [Story:US2] Implement history restoration: on page load, if conversation_id exists, fetch conversation with messages and display (frontend/app/components/chat/ChatContainer.tsx)
- [x] [T228] [Story:US2] Write hook test: useConversationHistory fetches conversations on mount (frontend/__tests__/hooks/useConversationHistory.test.ts)
- [x] [T229] [Story:US2] Write hook test: useChat manages conversation_id state correctly (frontend/__tests__/hooks/useChat.test.ts)
- [x] [T230] [Story:US2] Integration test: create conversation, refresh page, verify history restored (frontend/__tests__/integration/conversation-persistence.test.tsx)

**Dependencies**: T201-T210 (backend ready) → T221, T221 → T222-T223, T222-T223 → T224, T224-T225 → T226-T227, T221-T227 → T228-T230

---

### Phase: User Story 3 (P2) - View Conversation History List

**Objective**: Display sidebar or list of past conversations for navigation between them.

**Acceptance Scenarios**: 3 scenarios from spec.md (list displays with timestamps, click loads conversation, new conversation button)

#### Frontend: Conversation Sidebar Component

- [x] [T301] [Story:US3] Create ConversationSidebar component displaying list of conversations from useConversationHistory (frontend/app/components/chat/ConversationSidebar.tsx)
- [x] [T302] [Story:US3] Implement conversation item rendering: display created_at timestamp, first message preview (if available), active state for current conversation (frontend/app/components/chat/ConversationSidebar.tsx)
- [x] [T303] [Story:US3] Add click handler: onClick loads selected conversation via getConversation API call (frontend/app/components/chat/ConversationSidebar.tsx)
- [x] [T304] [Story:US3] Add "New Conversation" button at top of sidebar, onClick clears conversation_id and resets state (frontend/app/components/chat/ConversationSidebar.tsx)
- [x] [T305] [Story:US3] Integrate ConversationSidebar into ChatContainer layout: sidebar on left (desktop) or collapsible menu (mobile) (frontend/app/components/chat/ChatContainer.tsx)
- [x] [T306] [Story:US3] Implement responsive design: sidebar visible on desktop (≥768px), hidden behind hamburger menu on mobile (<768px) (frontend/app/components/chat/ChatContainer.tsx)
- [x] [T307] [Story:US3] Write component test: ConversationSidebar renders conversation list correctly (frontend/__tests__/chat/ConversationSidebar.test.tsx)
- [x] [T308] [Story:US3] Write component test: clicking conversation loads that conversation (frontend/__tests__/chat/ConversationSidebar.test.tsx)
- [x] [T309] [Story:US3] Write component test: "New Conversation" button creates fresh state (frontend/__tests__/chat/ConversationSidebar.test.tsx)
- [x] [T310] [Story:US3] Integration test: create multiple conversations, verify list displays, verify clicking switches between them (frontend/__tests__/integration/conversation-list.test.tsx)

**Dependencies**: T221-T230 (US2 backend + frontend) → T301, T301 → T302 → T303 → T304 → T305 → T306, T301-T306 → T307-T310

---

### Phase: User Story 4 (P2) - Handle Errors and Timeouts Gracefully

**Objective**: Display empathetic, actionable error messages when API failures occur.

**Acceptance Scenarios**: 4 scenarios from spec.md (backend unavailable, timeout, retry button, input remains enabled)

#### Backend: Error Response Handling

- [ ] [T401] [Story:US4] Add error handling middleware: catch exceptions, return ErrorResponse with empathetic messages (backend/app/middleware/error_handler.py)
- [ ] [T402] [Story:US4] Implement timeout handling: set request timeout (3s threshold per SC-007), return 408 with "Request timed out. Please try again." (backend/app/routes/chat.py)
- [ ] [T403] [Story:US4] Update 400 Bad Request response: "Validation error: {detail}" (backend/app/routes/chat.py)
- [ ] [T404] [Story:US4] Update 401 Unauthorized response: "Session expired. Please log in again." (backend/app/routes/chat.py)
- [ ] [T405] [Story:US4] Update 403 Forbidden response: "Access denied. This conversation doesn't belong to you." (backend/app/routes/chat.py)
- [ ] [T406] [Story:US4] Update 404 Not Found response: "Conversation not found. It may have been deleted." (backend/app/routes/chat.py)
- [ ] [T407] [Story:US4] Update 500 Internal Server Error response: "Something went wrong on our end. Please try again." (backend/app/routes/chat.py)
- [ ] [T408] [Story:US4] Write endpoint test: verify all error responses return empathetic, actionable messages (backend/tests/test_routes_chat.py)

**Dependencies**: T101-T112 → T401, T401 → T402-T407, T402-T407 → T408

#### Frontend: Error UI & Retry Logic

- [ ] [T421] [Story:US4] Create ErrorMessage component: display error with icon, empathetic message, retry button (frontend/app/components/chat/ErrorMessage.tsx)
- [ ] [T422] [Story:US4] Update ChatContainer onError handler: parse error response, display ErrorMessage with appropriate message (frontend/app/components/chat/ChatContainer.tsx)
- [ ] [T423] [Story:US4] Implement error classification: network errors ("Connection lost. Check your internet or try again."), timeouts ("Request timed out. Please try again."), auth errors ("Session expired. Please log in again.") (frontend/app/components/chat/ChatContainer.tsx)
- [ ] [T424] [Story:US4] Add retry functionality: onRetry re-submits last message with exponential backoff (frontend/app/components/chat/ChatContainer.tsx)
- [ ] [T425] [Story:US4] Ensure input field remains enabled during errors (FR-017): user can type different message or edit previous (frontend/app/components/chat/ChatInput.tsx)
- [ ] [T426] [Story:US4] Add loading state management: disable send button during API call, show typing indicator, re-enable on response or error (frontend/app/components/chat/ChatInput.tsx)
- [ ] [T427] [Story:US4] Write component test: ErrorMessage displays correct message and retry button (frontend/__tests__/chat/ErrorMessage.test.tsx)
- [ ] [T428] [Story:US4] Write component test: onError handler correctly classifies errors (frontend/__tests__/chat/ChatContainer.test.tsx)
- [ ] [T429] [Story:US4] Write component test: retry button re-submits message (frontend/__tests__/chat/ErrorMessage.test.tsx)
- [ ] [T430] [Story:US4] Integration test: simulate API failure, verify error message appears, verify retry works (frontend/__tests__/integration/error-handling.test.tsx)

**Dependencies**: T401-T408 (backend errors ready) → T421, T421 → T422, T422 → T423 → T424, T425-T426 parallel to T421-T424, T421-T426 → T427-T430

---

### Phase: Polish & Deployment

Cross-cutting concerns and production readiness.

#### Performance & UX Polish

- [ ] [T501] [P] Add typing indicator: display while waiting for AI response, appears <500ms after message submission (SC-009) (frontend/app/components/chat/TypingIndicator.tsx)
- [ ] [T502] [P] Implement skeleton loader for conversation history: shown while loading conversations (frontend/app/components/chat/ConversationSkeleton.tsx)
- [ ] [T503] Verify responsive design: test on 320px, 768px, 1920px viewports (SC-003) (frontend/app/chat/page.tsx)
- [ ] [T504] Verify auto-scroll behavior: messages scroll to bottom on new message (FR-016), smooth scroll with followOutput (frontend/app/components/chat/MessageList.tsx)
- [ ] [T505] Verify virtual scrolling performance: test with 100+ messages, ensure smooth 60 FPS scrolling (SC-011) (frontend/app/components/chat/MessageList.tsx)
- [ ] [T506] Add ARIA labels and keyboard navigation for accessibility (frontend/app/components/chat/)
- [ ] [T507] Implement focus management: focus input field after message submission (frontend/app/components/chat/ChatInput.tsx)

**Dependencies**: T122-T127 → T501-T502, T121-T133 → T503-T507

#### Environment & Configuration

- [ ] [T521] Add NEXT_PUBLIC_CHATKIT_DOMAIN_KEY to frontend .env.local with instructions (frontend/.env.local.example)
- [ ] [T522] Add DATABASE_URL, BETTER_AUTH_SECRET to backend .env with instructions (backend/.env.example)
- [ ] [T523] Document domain registration requirement: register at https://platform.openai.com/settings/organization/security/domain-allowlist (README.md or docs/)
- [ ] [T524] Verify all environment variables loaded correctly in both frontend and backend (frontend/app/lib/env.ts, backend/app/config.py)

**Dependencies**: Independent, can run anytime after T001-T002

#### Documentation

- [ ] [T541] Update main README: add chat feature description, navigation instructions (README.md)
- [ ] [T542] Create API documentation: document POST /chat, GET /conversations, GET /conversations/{id} endpoints with examples (docs/api/chat-endpoints.md)
- [ ] [T543] Document troubleshooting common issues: "Domain not allowed", messages not appearing, JWT validation fails (docs/troubleshooting.md)

**Dependencies**: T101-T210 (all endpoints complete) → T542, T121-T133 (frontend complete) → T541, T401-T408 (error handling) → T543

#### Testing & Verification

- [ ] [T561] Run backend tests: `pytest backend/tests/ --cov=app --cov-report=term` and verify ≥70% coverage (backend/)
- [ ] [T562] Run frontend tests: `npm test -- --coverage` and verify ≥70% coverage (frontend/)
- [ ] [T563] Verify all success criteria from spec.md (SC-001 through SC-011) (specs/001-chat-interface/spec.md)
- [ ] [T564] Verify all functional requirements from spec.md (FR-001 through FR-018, FR-014a) (specs/001-chat-interface/spec.md)
- [ ] [T565] Manual QA: test all user stories end-to-end with real Better Auth session (specs/001-chat-interface/spec.md)
- [ ] [T566] Security audit: verify user isolation (User A cannot access User B's data), JWT validation on all endpoints (specs/001-chat-interface/spec.md)

**Dependencies**: T001-T507 (all implementation) → T561-T566

---

## Dependency Graph

```
Setup & Foundations (T001-T013)
    ├─→ User Story 1 Backend (T101-T112)
    │       ├─→ User Story 1 Frontend (T121-T133)
    │       └─→ User Story 2 Backend (T201-T210)
    │               ├─→ User Story 2 Frontend (T221-T230)
    │               │       └─→ User Story 3 Frontend (T301-T310)
    │               └─→ User Story 4 Backend (T401-T408)
    │                       └─→ User Story 4 Frontend (T421-T430)
    └─→ Polish & Deployment (T501-T566)
```

### Critical Path

**Minimum viable path to demonstrate US1**:
T001-T013 → T101-T106 → T121-T127 → T129 → T133

**Full P1 implementation (US1 + US2)**:
T001-T013 → T101-T112 → T201-T210 → T121-T133 → T221-T230 → T561-T566

**Full P2 implementation (all user stories)**:
Add T301-T310 (US3), T401-T430 (US4) after P1 complete

---

## Parallel Execution Examples

**During Setup Phase**:
- T001 and T002 can run in parallel (different package managers)
- T003 and T004 can run in parallel (independent models)
- T008, T009, T010 can run in parallel (independent schemas)
- T011, T012, T013 can run in parallel (independent test files)

**During US1 Backend**:
- T107-T112 can run in parallel (independent test files)

**During US1 Frontend**:
- T125-T126 (MessageList) and T127 (ChatInput) can run in parallel
- T130, T131, T132 can run in parallel (independent test files)

**During Polish**:
- T501 and T502 can run in parallel (independent components)
- T521, T522, T523, T524 can run in parallel (independent config files)
- T541, T542, T543 can run in parallel (independent documentation)

---

## Task Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| Setup & Foundations | T001-T013 | Database models, migrations, schemas, foundational tests |
| User Story 1 (P1) | T101-T133 | Backend endpoint + Frontend chat interface |
| User Story 2 (P1) | T201-T230 | Conversation persistence + History loading |
| User Story 3 (P2) | T301-T310 | Conversation list sidebar |
| User Story 4 (P2) | T401-T430 | Error handling + Empathetic error messages |
| Polish & Deployment | T501-T566 | UX polish, environment setup, documentation, testing |

**Total Tasks**: 66 tasks across 6 phases

**Estimated Duration**:
- Setup & Foundations: ~2 hours
- User Story 1 (P1): ~3 hours
- User Story 2 (P1): ~2 hours
- User Story 3 (P2): ~1.5 hours
- User Story 4 (P2): ~2 hours
- Polish & Deployment: ~2 hours

**Total Estimate**: ~12.5 hours of development time (can be reduced with parallel execution)

---

## Validation Checklist

Before marking feature complete:

- [ ] All tasks completed and checked off
- [ ] Test coverage ≥70% for both frontend and backend (T561, T562)
- [ ] All success criteria from spec.md verified (T563)
- [ ] All functional requirements from spec.md verified (T564)
- [ ] Manual QA passed (T565)
- [ ] Security audit passed (T566)
- [ ] Constitution compliance verified (stateless architecture, user isolation, JWT auth)
- [ ] Documentation complete (README, API docs, troubleshooting)
- [ ] Environment variables documented and configured
- [ ] Ready for deployment

---

## Implementation Notes

1. **Task Order**: Tasks are ordered by dependency. Complete tasks in the order shown unless marked with [P] for parallelizable.

2. **User Story Independence**: Each user story can be implemented and tested independently. US1 and US2 are P1 (must-have), US3 and US4 are P2 (should-have).

3. **Test-First Approach**: Tests are defined as tasks before implementation. Follow TDD: write test first (red), implement feature (green), refactor.

4. **Stateless Architecture**: Backend tasks T102, T112 explicitly enforce stateless pattern (fetch conversation history from database on each request).

5. **User Isolation**: Tasks T109, T110, T205, T210, T566 verify user isolation at multiple layers (endpoint, query, security audit).

6. **Empathetic Errors**: Tasks T401-T407 (backend) and T421-T430 (frontend) implement FR-014a requirement for empathetic, actionable error messages.

7. **Virtual Scrolling**: Tasks T125-T126, T505 implement and verify virtual scrolling performance for 100+ messages (SC-011).

8. **Environment Setup**: Tasks T521-T524 must be completed before any integration testing or deployment.

9. **Placeholder AI**: Task T105 uses placeholder AI response for this spec. Actual AI agent logic is in separate specification and will replace placeholder later.

10. **MCP Tools**: Not included in this specification. MCP server implementation is a separate spec that will integrate with the chat endpoint.
