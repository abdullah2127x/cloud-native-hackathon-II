# Data Model: Agent MCP Integration

**Feature**: 006-agent-mcp-integration
**Date**: 2026-02-11

---

## New Models

### Conversation

Represents a chat session owned by a single user.

```python
class Conversation(SQLModel, table=True):
    __tablename__ = "conversation"

    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    messages: list["Message"] = Relationship(back_populates="conversation")
```

**Constraints**:
- `user_id` is indexed for fast per-user lookups
- `updated_at` updated on every new message insertion

---

### Message

Represents a single user or assistant turn in a conversation.

```python
class Message(SQLModel, table=True):
    __tablename__ = "message"

    id: int | None = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    role: str = Field()           # "user" or "assistant" only
    content: str = Field()
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    conversation: Conversation | None = Relationship(back_populates="messages")
```

**Constraints**:
- `role` MUST be one of `"user"` or `"assistant"` — tool calls are NOT stored
- `conversation_id` is indexed for fast history retrieval
- `user_id` stored redundantly for user isolation enforcement without a join
- Messages ordered by `created_at` ASC when loaded for agent context

---

## Existing Models (unchanged)

| Model | Location | Notes |
|-------|----------|-------|
| `Task` | `src/models/task.py` | No changes needed |
| `User` | `src/models/user.py` | No changes needed |
| `Tag` / `TaskTag` | `src/models/tag.py` | No changes needed |

---

## Database Migration

New tables added to `database.py` imports so `SQLModel.metadata.create_all(engine)` creates them automatically:

```python
# src/db/database.py — add these imports
from src.models.conversation import Conversation  # noqa: F401
from src.models.message import Message            # noqa: F401
```

No existing table changes. Migration is additive only.

---

## Key Queries

### Create conversation
```python
conversation = Conversation(user_id=user_id)
session.add(conversation)
session.commit()
session.refresh(conversation)
```

### Load last 50 messages for agent context
```python
messages = session.exec(
    select(Message)
    .where(Message.conversation_id == conversation_id, Message.user_id == user_id)
    .order_by(Message.created_at.asc())
    .limit(50)
).all()
```

### Persist a message
```python
message = Message(
    conversation_id=conversation_id,
    user_id=user_id,
    role="user",    # or "assistant"
    content=content,
)
session.add(message)
session.commit()
```

### Update conversation timestamp
```python
conversation.updated_at = datetime.utcnow()
session.add(conversation)
session.commit()
```
