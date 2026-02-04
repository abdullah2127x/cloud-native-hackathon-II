# Research: OpenAI ChatKit Conversation Interface

**Feature**: 001-chat-interface | **Date**: 2026-02-04 | **Phase**: 0 (Research & Discovery)

## Overview

This document consolidates research findings to resolve all technical unknowns identified in the implementation plan's Technical Context. Each research task addresses a specific decision point needed before proceeding to Phase 1 (Design & Contracts).

---

## Research Task 1: OpenAI ChatKit Integration Patterns

**Question**: How to integrate OpenAI ChatKit React component in Next.js 16 App Router with custom FastAPI backend?

**Investigation Approach**: Reviewed openai-chatkit skill documentation, authentication patterns, custom backend integration

### Decision: Custom Fetch Pattern with JWT Injection

**Rationale**:
- ChatKit supports custom backend integration via `api.fetch` override
- Allows injection of JWT Bearer token from Better Auth
- Enables routing to FastAPI backend (`POST /api/{user_id}/chat`) instead of OpenAI API
- Maintains secure authentication flow

**Implementation Pattern**:
```typescript
const { control } = useChatKit({
  api: {
    url: '/api/chat',  // FastAPI backend endpoint
    domainKey: process.env.NEXT_PUBLIC_CHATKIT_DOMAIN_KEY,
    fetch: async (input, init) => {
      const session = await getSession();  // Better Auth session
      return fetch(input, {
        ...init,
        headers: {
          ...init?.headers,
          'Authorization': `Bearer ${session.token}`,
        },
      });
    },
  },
  onError: ({ error }) => {
    errorTracking.captureException(error);
  },
});
```

**Domain Allowlist Requirement**:
- Production deployment MUST register domain at: `https://platform.openai.com/settings/organization/security/domain-allowlist`
- Obtain `NEXT_PUBLIC_CHATKIT_DOMAIN_KEY` from OpenAI platform
- Localhost typically works without registration (development)

**Backend Responsibilities** (FastAPI):
1. Accept ChatKit requests at `/api/{user_id}/chat`
2. Validate JWT Bearer token (Better Auth verification)
3. Extract `user_id` from token, verify it matches URL parameter
4. Process message with AI agent (out of scope - separate spec)
5. Return ChatKit-compatible response format
6. Save conversation and message to database

**Alternatives Considered**:
- **Client Secret Pattern**: Requires OpenAI API directly; we're using custom FastAPI backend → Rejected
- **Direct Client Token**: Less secure, token embedded in frontend → Rejected
- **Custom Fetch**: ✅ Selected - Full control, supports JWT, routes to FastAPI

---

## Research Task 2: Virtual Scrolling Library Selection

**Question**: Which virtual scrolling library should be used for handling 100+ message conversations in ChatKit?

**Investigation Approach**: Web search for React virtual scrolling libraries 2026, examined performance benchmarks, TypeScript support, and chat-specific features

### Decision: React Virtuoso

**Rationale**:
- **Chat-specific design**: Built-in chat interface component for human/AI conversations
- **Auto-sizing**: Handles variable-sized messages without manual height calculations
- **Streaming support**: Works with streaming AI responses (ChatKit compatibility)
- **TypeScript native**: Full TypeScript support out of the box
- **Performance**: Handles thousands of dynamic rows at 60 FPS
- **Stream Chat integration**: Used by Stream Chat's VirtualizedMessageList (production-proven)
- **Auto-scroll**: Automatic scroll to bottom for new messages

**Installation**:
```bash
npm install react-virtuoso
```

**Implementation Pattern**:
```typescript
import { Virtuoso } from 'react-virtuoso';

<Virtuoso
  data={messages}
  initialTopMostItemIndex={messages.length - 1}  // Start at bottom
  followOutput="smooth"  // Auto-scroll on new messages
  itemContent={(index, message) => (
    <MessageBubble key={message.id} message={message} />
  )}
/>
```

**Alternatives Considered**:
- **TanStack Virtual**: Excellent performance but requires manual height measurement → Rejected (more complex)
- **React Cool Virtual**: TypeScript support, but less chat-specific → Rejected (not specialized)
- **react-window**: Popular but doesn't handle variable heights as elegantly → Rejected (less suitable for chat)
- **React Virtuoso**: ✅ Selected - Chat-specific, auto-sizing, streaming support, production-proven

**Performance Benefits**:
- Reduces render time by 40-70% for conversations with thousands of messages
- Maintains 60 FPS scrolling performance
- Only renders visible messages in DOM (typically ~20 visible at once)

**Sources**:
- [React Virtuoso](https://virtuoso.dev/)
- [VirtualizedMessageList - React Chat Messaging Docs](https://getstream.io/chat/docs/sdk/react/components/core-components/virtualized_list/)
- [How to speed up long lists with TanStack Virtual - LogRocket Blog](https://blog.logrocket.com/speed-up-long-lists-tanstack-virtual/)
- [Virtual scrolling: Core principles and basic implementation in React - LogRocket Blog](https://blog.logrocket.com/virtual-scrolling-core-principles-and-basic-implementation-in-react/)

---

## Research Task 3: SQLModel Conversation-Message Relationship Pattern

**Question**: How to design SQLModel schemas for Conversation and Message tables with proper foreign key relationships?

**Investigation Approach**: Web search for SQLModel relationships, foreign key patterns, FastAPI integration best practices

### Decision: Bidirectional Relationship with CASCADE Delete

**Rationale**:
- **Back-populates**: Creates bidirectional navigation (Conversation.messages ↔ Message.conversation)
- **CASCADE delete**: When conversation deleted, all messages deleted automatically
- **Index on foreign key**: Improves query performance for message filtering
- **Separate response models**: List endpoints exclude relationships for performance; detail endpoints include them

**Implementation Pattern**:
```python
# Conversation model
class Conversation(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True)  # Better Auth user ID
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    messages: list["Message"] = Relationship(back_populates="conversation")

# Message model
class Message(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True)  # Denormalized for security queries
    conversation_id: UUID = Field(
        foreign_key="conversation.id",
        ondelete="CASCADE",
        index=True
    )
    role: Literal["user", "assistant"] = Field()
    content: str = Field()
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    conversation: Conversation = Relationship(back_populates="messages")
```

**API Response Models**:
```python
# List endpoint: exclude relationships for performance
class ConversationList(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime

# Detail endpoint: include messages
class ConversationDetail(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    messages: list[MessageRead]
```

**Alternatives Considered**:
- **No relationship attributes**: Use only foreign keys → Rejected (requires manual joins, less intuitive)
- **Soft delete**: Add `deleted_at` field → Rejected (adds complexity, not required by spec)
- **Bidirectional with CASCADE**: ✅ Selected - Standard pattern, automatic cleanup, intuitive navigation

**Sources**:
- [Models with Relationships in FastAPI - SQLModel](https://sqlmodel.tiangolo.com/tutorial/fastapi/relationships/)
- [Working with Relationships | fastapi/sqlmodel | DeepWiki](https://deepwiki.com/fastapi/sqlmodel/3.3-working-with-relationships)
- [Relationships in APIs | fastapi/sqlmodel | DeepWiki](https://deepwiki.com/fastapi/sqlmodel/4.3-relationships-in-apis)

---

## Research Task 4: Stateless Chat Endpoint Architecture

**Question**: How to design a stateless FastAPI chat endpoint that fetches conversation history from database on each request?

**Investigation Approach**: Web search for stateless chat patterns, FastAPI conversation management, database integration best practices

### Decision: Database-Backed Stateless Request Pattern

**Rationale**:
- **Stateless principle**: Server holds no in-memory conversation state between requests
- **Horizontal scalability**: Any server instance can handle any request
- **Database as source of truth**: PostgreSQL stores all conversation history
- **Async database access**: Efficient I/O handling with async/await
- **Each request is independent**: Fetch history → process message → save response → return

**Implementation Pattern**:
```python
@router.post("/api/{user_id}/chat")
async def chat(
    user_id: str,
    request: ChatRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(verify_jwt_token)
):
    # 1. Security: Verify user_id from JWT matches URL parameter
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # 2. Fetch conversation history from database
    if request.conversation_id:
        conversation = await session.get(Conversation, request.conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Load messages for this conversation
        statement = select(Message).where(
            Message.conversation_id == request.conversation_id
        ).order_by(Message.created_at)
        messages = await session.exec(statement)
        message_history = [msg for msg in messages]
    else:
        # Create new conversation
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        await session.commit()
        message_history = []

    # 3. Save user message to database BEFORE AI processing
    user_message = Message(
        user_id=user_id,
        conversation_id=conversation.id,
        role="user",
        content=request.message,
    )
    session.add(user_message)
    await session.commit()

    # 4. Call AI agent with full message history (out of scope - separate spec)
    ai_response = await process_with_ai_agent(message_history + [user_message])

    # 5. Save AI response to database
    assistant_message = Message(
        user_id=user_id,
        conversation_id=conversation.id,
        role="assistant",
        content=ai_response.content,
    )
    session.add(assistant_message)
    await session.commit()

    # 6. Return response (server forgets everything after this)
    return ChatResponse(
        conversation_id=conversation.id,
        message=ai_response.content,
    )
```

**Key Principles**:
1. **Every request fetches state from database** - No in-memory caching
2. **Database connection lifecycle managed** - Use FastAPI lifespan or dependency injection
3. **Async I/O for performance** - Non-blocking database queries
4. **Security first** - JWT validation before any data access
5. **Atomicity** - Use database transactions to ensure consistency

**Alternatives Considered**:
- **In-memory session cache**: Store conversation in Redis/memory → Rejected (violates stateless principle, breaks horizontal scaling)
- **Client-side conversation management**: Pass full history in each request → Rejected (inefficient, security risk)
- **Database-backed stateless**: ✅ Selected - Constitutional requirement, enables scaling, single source of truth

**Sources**:
- [Conversation state | OpenAI API](https://platform.openai.com/docs/guides/conversation-state)
- [Chat App with FastAPI - Pydantic AI](https://ai.pydantic.dev/examples/chat-app/)
- [How to Build an Agentic Chatbot with FastAPI and PostgreSQL - ORFIUM](https://www.orfium.com/engineering/how-to-build-an-agentic-chatbot-with-fastapi-and-postgresql/)
- [FastAPI Best Practices: A Complete Guide for Building Production-Ready APIs | by Abirami | Medium](https://medium.com/@abipoongodi1211/fastapi-best-practices-a-complete-guide-for-building-production-ready-apis-bb27062d7617)
- [GitHub - zhanymkanov/fastapi-best-practices: FastAPI Best Practices and Conventions](https://github.com/zhanymkanov/fastapi-best-practices)

---

## Research Summary

All technical unknowns from the implementation plan have been resolved through skill-based research (OpenAI ChatKit skill) and web research (virtual scrolling, SQLModel patterns, stateless architecture).

### Key Decisions Made

| Decision Point | Selected Solution | Rationale |
|----------------|-------------------|-----------|
| ChatKit Integration | Custom Fetch with JWT | Enables FastAPI backend, secure JWT injection |
| Virtual Scrolling | React Virtuoso | Chat-specific, auto-sizing, streaming support, 60 FPS |
| Database Relationships | Bidirectional CASCADE | Standard pattern, automatic cleanup, intuitive navigation |
| Chat Endpoint Architecture | Database-backed stateless | Constitutional requirement, horizontal scalability, single source of truth |

### Dependencies Identified

**Frontend**:
- `react-virtuoso` (virtual scrolling)
- `@openai/chatkit` (ChatKit component)
- Better Auth session management (existing)

**Backend**:
- SQLModel relationships (existing)
- Better Auth JWT verification (existing)
- Async PostgreSQL (existing via SQLModel)

**Configuration**:
- `NEXT_PUBLIC_CHATKIT_DOMAIN_KEY` (OpenAI domain allowlist)

### Ready for Phase 1

All research tasks complete. No remaining NEEDS CLARIFICATION items. Proceeding to Phase 1: Design & Contracts.

