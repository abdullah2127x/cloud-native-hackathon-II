# Data Model: OpenAI ChatKit Conversation Interface

**Feature**: 001-chat-interface | **Date**: 2026-02-04 | **Phase**: 1 (Design & Contracts)

## Overview

This document defines the database schema and entity relationships for the conversation interface feature. All entities follow SQLModel conventions and integrate with the existing Neon PostgreSQL database.

---

## Entity Relationship Diagram

```
┌──────────────┐         ┌─────────────────┐         ┌──────────────┐
│     User     │         │  Conversation   │         │   Message    │
│  (existing)  │────────▶│     (new)       │◀────────│    (new)     │
└──────────────┘   1:N   └─────────────────┘  N:1    └──────────────┘
                                 │
                                 │ 1:N
                                 ▼
                          (CASCADE DELETE)
```

**Relationships**:
- `User` → `Conversation`: 1:N (one user has many conversations)
- `Conversation` → `Message`: 1:N with CASCADE DELETE (one conversation has many messages; deleting conversation deletes all messages)
- `User` → `Message`: 1:N (denormalized for security queries)

---

## Entity Definitions

### Conversation

**Purpose**: Represents a single chat session between a user and the AI assistant

**Table**: `conversation`

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique conversation identifier |
| `user_id` | String | NOT NULL, INDEX, FK → user.id | Owner of conversation (Better Auth user ID) |
| `created_at` | DateTime | NOT NULL, DEFAULT NOW() | Conversation creation timestamp |
| `updated_at` | DateTime | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes**:
- `PRIMARY KEY (id)`
- `INDEX idx_conversation_user_id (user_id)` - For filtering user's conversations

**Relationships**:
- `messages` → List[Message] (bidirectional, back_populates="conversation")
- `user` → User (via user_id foreign key)

**Validation Rules**:
- `user_id` MUST match authenticated JWT token user_id
- `updated_at` automatically updated on message creation

**State Transitions**:
- Created → Active (first message added)
- Active → Active (messages continue)
- Active → Archived (deleted by user - out of scope for this spec)

---

### Message

**Purpose**: Represents a single message in a conversation (either from user or AI assistant)

**Table**: `message`

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique message identifier |
| `user_id` | String | NOT NULL, INDEX | Denormalized user_id for security filtering |
| `conversation_id` | UUID | NOT NULL, INDEX, FK → conversation.id (CASCADE) | Parent conversation |
| `role` | Enum("user", "assistant") | NOT NULL | Message sender role |
| `content` | Text | NOT NULL | Message content (plain text or markdown) |
| `created_at` | DateTime | NOT NULL, DEFAULT NOW() | Message creation timestamp |

**Indexes**:
- `PRIMARY KEY (id)`
- `INDEX idx_message_user_id (user_id)` - For security queries
- `INDEX idx_message_conversation_id (conversation_id)` - For conversation history queries
- `INDEX idx_message_created_at (created_at)` - For ordering messages chronologically

**Relationships**:
- `conversation` → Conversation (bidirectional, back_populates="messages")

**Validation Rules**:
- `user_id` MUST match conversation.user_id
- `role` MUST be either "user" or "assistant"
- `content` MUST NOT be empty string
- `conversation_id` MUST reference existing conversation

**Constraints**:
- `ON DELETE CASCADE` on `conversation_id` foreign key (deleting conversation deletes all messages)

---

## SQLModel Implementation

### Conversation Model

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4

class Conversation(SQLModel, table=True):
    __tablename__ = "conversation"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    messages: list["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
```

### Message Model

```python
from typing import Literal

class Message(SQLModel, table=True):
    __tablename__ = "message"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    conversation_id: UUID = Field(
        foreign_key="conversation.id",
        ondelete="CASCADE",
        index=True,
        nullable=False
    )
    role: Literal["user", "assistant"] = Field(nullable=False)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")
```

---

## Database Migration

**Migration File**: `backend/migrations/versions/XXXX_add_conversation_message_tables.py`

**Operations**:
1. Create `conversation` table with fields and indexes
2. Create `message` table with fields, indexes, and foreign key constraint
3. Add CASCADE DELETE constraint on `message.conversation_id`

**Rollback**:
1. Drop `message` table (cascade removes foreign key)
2. Drop `conversation` table

---

## Query Patterns

### Fetch Conversation History

```python
# Get conversation with all messages
statement = (
    select(Conversation)
    .where(Conversation.id == conversation_id)
    .where(Conversation.user_id == user_id)  # Security filter
    .options(selectinload(Conversation.messages))  # Eager load
)
conversation = await session.exec(statement).first()
```

### List User's Conversations

```python
# Get all conversations for user (WITHOUT messages for performance)
statement = (
    select(Conversation)
    .where(Conversation.user_id == user_id)
    .order_by(Conversation.updated_at.desc())
)
conversations = await session.exec(statement).all()
```

### Save New Message

```python
# Add message to conversation
message = Message(
    user_id=user_id,
    conversation_id=conversation_id,
    role="user",  # or "assistant"
    content="Hello, AI!",
)
session.add(message)

# Update conversation.updated_at
conversation.updated_at = datetime.utcnow()

await session.commit()
await session.refresh(message)  # Get generated ID
```

---

## Security Considerations

### User Isolation

**All queries MUST filter by user_id**:
```python
# CORRECT: Always filter by authenticated user_id
where(Conversation.user_id == current_user.id)

# INCORRECT: Querying without user filter
where(Conversation.id == conversation_id)  # SECURITY RISK!
```

### Denormalized user_id in Message

- `Message.user_id` is denormalized (duplicates `Conversation.user_id`)
- **Why**: Enables efficient security queries without joining Conversation table
- **Tradeoff**: Slight data duplication for significant security benefit
- **Validation**: Backend MUST verify `message.user_id == conversation.user_id` on creation

---

## Performance Optimization

### Indexes

All foreign keys and frequently queried fields have indexes:
- `conversation.user_id` (INDEX)
- `message.user_id` (INDEX)
- `message.conversation_id` (INDEX)
- `message.created_at` (INDEX for ordering)

### Query Optimization

**List endpoints**: Use `select(Conversation)` WITHOUT `options(selectinload())` to avoid N+1 queries
**Detail endpoints**: Use `selectinload(Conversation.messages)` to eagerly load messages in single query

### Expected Performance

- List conversations: <50ms for 100 conversations
- Load conversation history: <100ms for 100 messages
- Save new message: <20ms (single INSERT)

---

## Data Constraints Summary

| Constraint | Enforcement |
|------------|-------------|
| User isolation | Application layer (JWT validation + user_id filter in queries) |
| Conversation ownership | Foreign key + user_id validation |
| Message ownership | Denormalized user_id + validation on creation |
| Conversation-message relationship | Foreign key with CASCADE DELETE |
| Role values | Database enum ("user", "assistant") |
| Non-empty content | Application layer validation (Pydantic schema) |

