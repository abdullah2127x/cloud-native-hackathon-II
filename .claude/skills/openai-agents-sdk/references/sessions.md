# OpenAI Agents SDK — Sessions & Persistent Memory

Source: openai/openai-agents-python (Context7, benchmark 89.9, High reputation)

---

## Overview

Sessions persist agent state across multiple runs, enabling:
- Multi-turn conversations
- Memory of previous interactions
- Accumulated context
- Stateful workflows

---

## Basic Session Usage

```python
from agents import Agent, Runner, Session

agent = Agent(
    name="Assistant",
    instructions="Remember what the user tells you.",
    model="gpt-4o-mini",
)

# Create a session (in-memory by default)
session = Session()

# First run
result1 = await Runner.run(
    agent,
    "My name is Alice",
    session=session,
)
print(result1.final_output)  # "Nice to meet you, Alice!"

# Second run - agent remembers
result2 = await Runner.run(
    agent,
    "What is my name?",
    session=session,
)
print(result2.final_output)  # "Your name is Alice"
```

---

## In-Memory Sessions

Default behavior. State stored in memory (lost on restart):

```python
from agents import Session

# Default: in-memory
session = Session()

# Use for development and testing
await Runner.run(agent, "input 1", session=session)
await Runner.run(agent, "input 2", session=session)
```

**Pros:** Simple, fast, no setup
**Cons:** Lost on restart, not scalable

---

## Persistent Sessions (Database)

Store session state in database for production:

```python
from agents import Session
from sqlalchemy import create_engine
from sqlmodel import Session as SQLSession

# Setup database
engine = create_engine("postgresql://localhost/agents")

# Create persistent session
db_session = SQLSession(engine)
session = Session(
    storage=db_session,  # Use database backend
    session_id="user_123_conversation",  # Unique ID
)

# State persists across runs
await Runner.run(agent, "input 1", session=session)
# ... app restarts ...
await Runner.run(agent, "input 2", session=session)  # Remembers input 1
```

---

## Session Context Type

Sessions can hold custom context:

```python
from pydantic import BaseModel

class UserContext(BaseModel):
    user_id: str
    preferences: dict
    session_data: dict

# Pass context type to agent
agent = Agent[UserContext](
    name="Assistant",
    instructions="Use user preferences to personalize responses.",
    model="gpt-4o-mini",
)

# Create session with context
context = UserContext(
    user_id="123",
    preferences={"language": "en", "timezone": "UTC"},
    session_data={},
)

session = Session(context=context)

result = await Runner.run(agent, user_input, session=session)
```

---

## Multi-Turn Conversations

Sessions enable natural conversations:

```python
from agents import Agent, Runner, Session

agent = Agent(
    name="Customer Support",
    instructions="Help customers with their issues. Remember context from previous messages.",
    model="gpt-4o-mini",
)

session = Session()
messages = [
    "I'm having trouble with my order",
    "Order #12345",
    "It hasn't shipped yet and I ordered 3 days ago",
    "Can you check on this?",
]

for message in messages:
    result = await Runner.run(agent, message, session=session)
    print(f"User: {message}")
    print(f"Agent: {result.final_output}\n")

# Agent remembers all previous context
```

---

## Session Lifecycle

```python
from agents import Session

# Create
session = Session(session_id="conversation_1")

# Use in multiple runs
await Runner.run(agent, "message 1", session=session)
await Runner.run(agent, "message 2", session=session)

# Access session data
print(session.id)  # "conversation_1"
print(session.context)  # User context if provided

# Clear session (optional)
session.clear()  # Resets memory

# Delete session (permanent)
session.delete()
```

---

## Session Storage Backends

### In-Memory (Default)

```python
session = Session()  # Uses memory storage
```

**Use for:** Development, testing, short-lived conversations

### File-Based

```python
from agents import FileSession

session = FileSession(path="./sessions/session_1.json")
```

**Use for:** Simple persistence, small data

### Database

```python
from agents import DatabaseSession
from sqlalchemy import create_engine

engine = create_engine("postgresql://localhost/agents")

session = DatabaseSession(
    engine=engine,
    session_id="user_conversation_123",
    table_name="agent_sessions",  # Custom table
)
```

**Use for:** Production, scalability, concurrent users

### Redis (Advanced)

```python
from agents import RedisSession
import redis

r = redis.Redis(host="localhost", port=6379)

session = RedisSession(
    redis_client=r,
    session_id="conversation_123",
    ttl=3600,  # 1 hour expiry
)
```

**Use for:** High-performance, distributed systems

---

## Session Data Management

```python
session = Session()

# Store custom data
session.data["user_id"] = "123"
session.data["preferences"] = {"theme": "dark"}

# Retrieve custom data
user_id = session.data.get("user_id")
prefs = session.data.get("preferences", {})

# Update session
session.update_data({"last_action": "search"})

# Access conversation history
for message in session.messages:
    print(f"{message.role}: {message.content}")
```

---

## Session Cleanup

Regular maintenance prevents bloat:

```python
from datetime import datetime, timedelta
from agents import Session

# Delete old sessions (manual)
cutoff_date = datetime.now() - timedelta(days=30)

# For database backend:
sessions_to_delete = db.query(Session).filter(
    Session.created_at < cutoff_date
).all()

for session in sessions_to_delete:
    session.delete()
```

---

## Common Patterns

### Pattern 1: User-Per-Session

```python
from agents import Session

# Each user gets own session
sessions = {}

def get_session(user_id: str) -> Session:
    if user_id not in sessions:
        sessions[user_id] = Session(session_id=f"user_{user_id}")
    return sessions[user_id]

# Use
user_session = get_session("alice")
result = await Runner.run(agent, user_input, session=user_session)
```

### Pattern 2: Conversation Chains

```python
# Multi-agent conversation with shared session
session = Session()

# Agent 1 processes
result1 = await Runner.run(agent1, user_input, session=session)

# Agent 2 continues (sees agent1's output in context)
result2 = await Runner.run(agent2, result1.final_output, session=session)

# Both agents share conversation history
```

### Pattern 3: Session with Context

```python
class RequestContext(BaseModel):
    user_id: str
    request_id: str
    timestamp: datetime

session = Session(
    session_id=f"req_{uuid.uuid4()}",
    context=RequestContext(
        user_id="123",
        request_id="req_456",
        timestamp=datetime.now(),
    ),
)
```

---

## Session Configuration

```python
session = Session(
    session_id="my_session",
    max_history=100,  # Keep last 100 messages
    ttl=3600,  # 1 hour timeout
    storage="database",  # or "memory", "file", "redis"
    compress=True,  # Compress old messages
)
```

---

## Best Practices

1. **Use unique session IDs**
   ```python
   import uuid
   session = Session(session_id=str(uuid.uuid4()))
   ```

2. **Handle session not found**
   ```python
   try:
       session = Session.load(session_id)
   except SessionNotFoundError:
       session = Session(session_id=session_id)
   ```

3. **Clean up expired sessions**
   ```python
   # Run periodically (daily)
   cleanup_expired_sessions()
   ```

4. **Monitor session size**
   ```python
   if len(session.messages) > 1000:
       # Archive or warn user
       session.archive()
   ```

5. **Encrypt sensitive data**
   ```python
   session.encrypt_sensitive_fields(["password", "credit_card"])
   ```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Session not found" | Check session_id, ensure storage backend accessible |
| "Memory growing indefinitely" | Set max_history, implement cleanup |
| "State not persisting" | Verify storage backend (file/DB), check permissions |
| "Slow responses" | Reduce session history, use compression, migrate to Redis |
