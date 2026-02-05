# Quickstart Guide: OpenAI ChatKit Conversation Interface

**Feature**: 001-chat-interface | **Date**: 2026-02-04 | **Phase**: 1 (Design & Contracts)

## Overview

This guide provides a step-by-step walkthrough for implementing the OpenAI ChatKit conversation interface. Follow these steps in order to build the feature according to the specification and design documents.

---

## Prerequisites

Before starting implementation, ensure you have:

✅ **Specification Documents**:
- [spec.md](./spec.md) - Feature requirements and acceptance criteria
- [plan.md](./plan.md) - Implementation plan and architecture
- [research.md](./research.md) - Technical decisions and research findings
- [data-model.md](./data-model.md) - Database schema and entity relationships
- [contracts/chat-api.yaml](./contracts/chat-api.yaml) - API contract (OpenAPI spec)

✅ **Development Environment**:
- Node.js 18+ and npm (frontend)
- Python 3.11+ and uv (backend)
- PostgreSQL (Neon Serverless)
- Better Auth configured with JWT tokens

✅ **Dependencies to Install**:
```bash
# Frontend
cd frontend
npm install react-virtuoso @openai/chatkit

# Backend
cd backend
uv add sqlmodel pydantic
```

✅ **Environment Variables**:
```bash
# Frontend (.env.local)
NEXT_PUBLIC_CHATKIT_DOMAIN_KEY=your-domain-key-from-openai

# Backend (.env)
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=your-secret
```

---

## Implementation Sequence

### Phase 1: Database Setup (Backend)

**Duration**: ~30 minutes

**Steps**:

1. **Create SQLModel Models** (`backend/app/models/`)
   - Reference: [data-model.md](./data-model.md)
   - Create `conversation.py` with Conversation model
   - Create `message.py` with Message model
   - Add relationship attributes and indexes

2. **Generate Database Migration**
   ```bash
   cd backend
   alembic revision --autogenerate -m "Add conversation and message tables"
   ```

3. **Review Migration File**
   - Verify CASCADE DELETE on message.conversation_id
   - Check all indexes created correctly

4. **Run Migration**
   ```bash
   alembic upgrade head
   ```

5. **Verify Tables**
   ```sql
   \d conversation
   \d message
   ```

**Acceptance**:
- ✅ Tables created in database
- ✅ Foreign key with CASCADE exists
- ✅ Indexes on user_id, conversation_id, created_at

---

### Phase 2: Backend API Endpoint (Backend)

**Duration**: ~1 hour

**Steps**:

1. **Create Pydantic Schemas** (`backend/app/schemas/chat.py`)
   - ChatRequest (conversation_id?, message)
   - ChatResponse (conversation_id, message, role, created_at)
   - Reference: [chat-api.yaml](./contracts/chat-api.yaml)

2. **Create Chat Route** (`backend/app/routes/chat.py`)
   - POST `/api/{user_id}/chat` endpoint
   - Reference: [research.md](./research.md) Task 4 (Stateless pattern)
   - Steps:
     1. Verify JWT token
     2. Fetch conversation history from database
     3. Save user message
     4. Call AI agent (placeholder for now - separate spec)
     5. Save AI response
     6. Return ChatResponse

3. **Add JWT Verification Dependency**
   - Reuse existing `backend/app/middleware/auth.py`
   - Verify user_id from JWT matches path parameter

4. **Test Endpoint Manually**
   ```bash
   curl -X POST http://localhost:8000/api/user123/chat \
     -H "Authorization: Bearer $JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello, AI!"}'
   ```

**Acceptance**:
- ✅ Endpoint returns 200 with conversation_id
- ✅ User and assistant messages saved to database
- ✅ Returns 401 without valid JWT
- ✅ Returns 403 if user_id doesn't match JWT

---

### Phase 3: ChatKit Frontend Component (Frontend)

**Duration**: ~1.5 hours

**Steps**:

1. **Create Chat Page** (`frontend/app/chat/page.tsx`)
   - Next.js 16 App Router route
   - Server component wrapper with auth check

2. **Create ChatKit Wrapper Component** (`frontend/app/components/chat/ChatContainer.tsx`)
   - Import `useChatKit` from `@openai/chatkit`
   - Configure custom fetch with JWT injection
   - Reference: [research.md](./research.md) Task 1 (Custom Fetch pattern)
   - Example:
     ```typescript
     const { control } = useChatKit({
       api: {
         url: '/api/chat',
         domainKey: process.env.NEXT_PUBLIC_CHATKIT_DOMAIN_KEY,
         fetch: async (input, init) => {
           const session = await getSession();
           return fetch(input, {
             ...init,
             headers: {
               ...init?.headers,
               'Authorization': `Bearer ${session.token}`,
             },
           });
         },
       },
       onError: ({ error }) => console.error('Chat error:', error),
     });
     ```

3. **Create Virtual Scrolling Message List** (`frontend/app/components/chat/MessageList.tsx`)
   - Import `Virtuoso` from `react-virtuoso`
   - Reference: [research.md](./research.md) Task 2 (Virtual scrolling)
   - Configure auto-scroll to bottom

4. **Add Navigation Link**
   - Update `frontend/app/components/navigation/NavBar.tsx`
   - Add "Chat" link to `/chat`

**Acceptance**:
- ✅ Chat page accessible at `/chat`
- ✅ ChatKit renders with custom styling
- ✅ Messages display in virtual scrolling list
- ✅ Navigation includes chat link

---

### Phase 4: State Management & History Loading (Frontend)

**Duration**: ~1 hour

**Steps**:

1. **Create Chat Hook** (`frontend/app/hooks/useChat.ts`)
   - Manage conversation_id state
   - Handle message submission
   - Update conversation list on new message

2. **Create Conversation History Hook** (`frontend/app/hooks/useConversationHistory.ts`)
   - Fetch conversation list on mount
   - Fetch specific conversation with messages
   - Reference: [chat-api.yaml](./contracts/chat-api.yaml) for endpoints

3. **Create API Client** (`frontend/app/lib/api/chat.ts`)
   - `listConversations(user_id, token)`
   - `getConversation(user_id, conversation_id, token)`
   - `sendMessage(user_id, message, conversation_id?, token)`

4. **Integrate History into ChatKit**
   - Load conversation on page mount
   - Display conversation selector (if multiple conversations)

**Acceptance**:
- ✅ Conversation history loads on page refresh
- ✅ Messages persist across sessions
- ✅ New conversations create new conversation_id
- ✅ Conversation list displays previous chats

---

### Phase 5: Error Handling & UX Polish (Frontend)

**Duration**: ~45 minutes

**Steps**:

1. **Implement Error Messages**
   - Reference: [spec.md](./spec.md) FR-014a (Empathetic & actionable)
   - Connection errors: "Connection lost. Check your internet or try again."
   - Timeout errors: "Request timed out. Please try again."
   - Auth errors: "Session expired. Please log in again."

2. **Add Typing Indicator**
   - Show while waiting for AI response
   - Reference: SC-009 (<500ms appearance target)

3. **Loading States**
   - Skeleton loader for conversation history
   - Disabled input during API call (but keep input field responsive - FR-017)

4. **Responsive Design**
   - Test on 320px, 768px, 1920px viewports
   - Reference: SC-003 (320px-1920px+ support)

**Acceptance**:
- ✅ Error messages empathetic and actionable
- ✅ Typing indicator appears <500ms
- ✅ Responsive on all viewport sizes
- ✅ Input field remains functional during loading

---

### Phase 6: Testing (Frontend & Backend)

**Duration**: ~2 hours

**Steps**:

1. **Backend Unit Tests** (`backend/tests/`)
   - `test_models_conversation.py` - Conversation model tests
   - `test_models_message.py` - Message model tests
   - `test_routes_chat.py` - Chat endpoint tests (auth, user isolation, stateless behavior)

2. **Frontend Component Tests** (`frontend/__tests__/`)
   - `ChatContainer.test.tsx` - ChatKit initialization, error handling
   - `MessageList.test.tsx` - Virtual scrolling, message rendering
   - `ChatInput.test.tsx` - Input validation, submission

3. **Frontend Hook Tests** (`frontend/__tests__/hooks/`)
   - `useChat.test.ts` - State management
   - `useConversationHistory.test.ts` - History loading

4. **Integration Tests**
   - End-to-end flow: user sends message → saved to DB → AI responds → response saved → UI updates
   - Cross-user isolation: User A cannot see User B's conversations

**Acceptance**:
- ✅ Test coverage ≥70% (constitutional requirement)
- ✅ All user stories have corresponding tests
- ✅ Security tests verify user isolation

---

## Verification Checklist

Before marking feature complete, verify all success criteria from [spec.md](./spec.md):

### Performance (SC-001 through SC-011)
- [ ] SC-001: Chat accessible within 2 clicks, loads <2s
- [ ] SC-002: First message → AI response <5s
- [ ] SC-003: Responsive 320px-1920px+
- [ ] SC-004: 100% conversation history restored on refresh
- [ ] SC-005: Unauthenticated users redirected to login
- [ ] SC-006: 0% cross-user message leakage
- [ ] SC-007: 95% of requests complete within 3s
- [ ] SC-008: All errors show user-friendly messages
- [ ] SC-009: Typing indicator <500ms, AI response <5s
- [ ] SC-010: Input field functional during API call
- [ ] SC-011: Virtual scrolling smooth with 100+ messages

### Functional Requirements (FR-001 through FR-018 + FR-014a)
- [ ] FR-001: `/chat` route accessible from navigation
- [ ] FR-002: Empty state displayed for new conversations
- [ ] FR-003: Send button and Enter key both work
- [ ] FR-004: User messages appear immediately
- [ ] FR-005: Backend endpoint called correctly
- [ ] FR-006: Typing indicator displayed
- [ ] FR-007: AI responses displayed in correct order
- [ ] FR-008: All conversations/messages persisted
- [ ] FR-009: History fetched and displayed on load
- [ ] FR-010: New conversation created automatically
- [ ] FR-011: User isolation enforced
- [ ] FR-012: JWT authentication on all endpoints
- [ ] FR-013: 401 for invalid tokens
- [ ] FR-014: Error messages displayed
- [ ] FR-014a: Errors are empathetic & actionable
- [ ] FR-015: Responsive design working
- [ ] FR-016: Auto-scroll to latest message
- [ ] FR-017: Input state maintained during API calls
- [ ] FR-018: Chat accessible from main navigation

### User Stories (Priority P1)
- [ ] User Story 1: Start new chat conversation
- [ ] User Story 2: Persist and resume conversations

---

## Troubleshooting Common Issues

### ChatKit "Domain not allowed" Error
**Solution**: Register domain at https://platform.openai.com/settings/organization/security/domain-allowlist

### Messages not appearing
**Solution**: Verify custom fetch function includes `Authorization: Bearer ${token}` header

### Virtual scrolling performance issues
**Solution**: Ensure `react-virtuoso` installed; check `initialTopMostItemIndex` set to `messages.length - 1`

### Database migration fails
**Solution**: Check PostgreSQL connection; verify no existing tables with same names

### JWT validation fails
**Solution**: Verify `BETTER_AUTH_SECRET` matches between frontend and backend

---

## Next Steps

After completing this feature:

1. **Create separate specifications for**:
   - AI Agent Logic (OpenAI Agents SDK integration)
   - MCP Tools (task management tool implementation)

2. **Consider enhancements** (P2 features from spec):
   - Conversation history list (User Story 3)
   - Enhanced error handling (User Story 4)

3. **Documentation**:
   - Update main README with chat feature
   - Add API documentation to developer portal

---

## Resources

- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Research Findings](./research.md)
- [Data Model](./data-model.md)
- [API Contract](./contracts/chat-api.yaml)
- [OpenAI ChatKit Docs](https://github.com/openai/chatkit-js)
- [React Virtuoso Docs](https://virtuoso.dev/)
- [SQLModel Docs](https://sqlmodel.tiangolo.com/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)

