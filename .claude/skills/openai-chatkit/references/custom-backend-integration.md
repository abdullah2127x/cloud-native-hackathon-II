# ChatKit Custom Backend Integration

## When to Use Custom Backend

Custom backend integration is needed when:
- ✅ Using FastAPI, Express, or other non-OpenAI backend
- ✅ Integrating with MCP tools (Phase 3)
- ✅ Custom AI logic or database queries
- ✅ Non-OpenAI APIs or models
- ✅ Stateless chat endpoint architecture

---

## Architecture: Custom Backend + ChatKit

```
┌─────────────────────┐
│   ChatKit UI        │
│   (Next.js)         │
└──────────┬──────────┘
           │
    Custom Fetch: POST /api/chat
    + JWT Token in header
           │
           ▼
┌──────────────────────────────────┐
│   FastAPI Backend                │
├──────────────────────────────────┤
│  POST /api/chat                  │
│    1. Validate JWT token         │
│    2. Fetch conversation history │
│    3. Build message array        │
│    4. Run OpenAI Agents SDK      │
│    5. Agent invokes MCP tools    │
│    6. Return streaming response  │
└──────────┬───────────────────────┘
           │
           ├─▶ OpenAI API (for AI responses)
           │
           └─▶ MCP Tools (for data operations)
                ├─ add_task
                ├─ list_tasks
                ├─ complete_task
                ├─ delete_task
                └─ update_task
```

---

## Frontend: Custom Fetch Configuration

```typescript
import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { useAuth } from '@/lib/auth';

export function ChatWithCustomBackend() {
  const { user, getToken } = useAuth();

  const { control } = useChatKit({
    api: {
      // Point to your custom backend
      url: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',

      // Domain key for ChatKit (if not using OpenAI directly)
      domainKey: process.env.NEXT_PUBLIC_CHATKIT_DOMAIN_KEY,

      // Custom fetch to inject JWT and handle auth
      fetch: async (input: string, init?: RequestInit) => {
        // Get JWT token from Better Auth
        const token = await getToken();

        if (!token) {
          throw new Error('Not authenticated');
        }

        // Inject authorization header
        const headers = new Headers(init?.headers);
        headers.set('Authorization', `Bearer ${token}`);
        headers.set('Content-Type', 'application/json');

        // Optional: Pass user context
        if (user) {
          headers.set('X-User-Id', user.id);
          headers.set('X-User-Email', user.email);
        }

        return fetch(input, {
          ...init,
          headers,
          // Ensure credentials are sent (for cookies if needed)
          credentials: 'include',
        });
      },
    },

    // Handle tool calls from custom backend
    onClientTool: async (toolCall) => {
      // Client tools remain the same (browser actions)
      // Data operations are handled by MCP tools on backend
      return handleClientTool(toolCall);
    },
  });

  return <ChatKit control={control} className="h-[600px] w-[400px]" />;
}
```

---

## Backend: FastAPI Chat Endpoint

### Basic Structure

```python
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
import httpx
import json
from typing import AsyncGenerator

router = APIRouter()

async def verify_token(request: Request) -> dict:
    """Verify JWT token and extract user info"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Unauthorized')

    token = auth_header[7:]  # Remove "Bearer " prefix

    # Verify JWT with Better Auth secret
    # This is simplified; use python-jose for real implementation
    try:
        decoded = verify_jwt_token(token)
        return decoded
    except Exception:
        raise HTTPException(status_code=401, detail='Invalid token')


@router.post('/api/chat')
async def chat(request: Request, user = Depends(verify_token)):
    """
    Stateless chat endpoint for ChatKit.
    Receives message from frontend, returns AI response.
    """
    body = await request.json()
    user_id = user.get('sub')  # JWT subject is user ID
    messages = body.get('messages', [])
    conversation_id = body.get('conversation_id')

    # Fetch conversation history from database
    if conversation_id:
        history = fetch_conversation_history(conversation_id, user_id)
    else:
        history = []

    # Build message array for AI agent
    message_array = [
        {'role': msg['role'], 'content': msg['content']}
        for msg in history
    ] + messages

    # Run OpenAI Agents SDK with MCP tools
    ai_response = await run_agent_with_mcp_tools(
        user_id=user_id,
        messages=message_array,
        conversation_id=conversation_id,
    )

    # Return streaming response to ChatKit
    async def generate():
        async for chunk in ai_response:
            yield f"data: {json.dumps(chunk)}\n\n"

    return StreamingResponse(generate(), media_type='text/event-stream')
```

### Complete Implementation

```python
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select, create_engine
from sqlmodel import SQLModel
import httpx
import json
import os
from typing import Optional
from datetime import datetime
import asyncio

# Database models
from models import Conversation, Message, Task, User

# JWT verification
from jose import JWTError, jwt

app = FastAPI()
router = APIRouter()

# Database
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

async def verify_jwt_token(token: str) -> dict:
    """Verify JWT token from Better Auth"""
    try:
        secret = os.getenv("BETTER_AUTH_SECRET")
        decoded = jwt.decode(token, secret, algorithms=["HS256"])
        return decoded
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def verify_token(request: Request) -> dict:
    """Extract and verify JWT from request"""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = auth_header[7:]
    return await verify_jwt_token(token)

@router.post("/api/chat")
async def chat_endpoint(
    request: Request,
    user_claims = Depends(verify_token),
    session: Session = Depends(get_session)
):
    """
    Stateless chat endpoint.
    Flow:
    1. Validate JWT
    2. Extract conversation history
    3. Build message array
    4. Run AI agent with MCP tools
    5. Stream response back
    """
    try:
        # Extract user ID from JWT
        user_id = user_claims.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Parse request
        body = await request.json()
        messages = body.get("messages", [])
        conversation_id = body.get("conversation_id")

        # Fetch or create conversation
        if conversation_id:
            conversation = session.exec(
                select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id
                )
            ).first()
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            # Create new conversation
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

        # Fetch conversation history
        history_messages = session.exec(
            select(Message).where(Message.conversation_id == conversation.id)
        ).all()

        # Build message array for agent
        message_array = [
            {"role": msg.role, "content": msg.content}
            for msg in history_messages
        ]
        message_array.extend(messages)

        # Store user message in database
        user_message = Message(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content=messages[-1]["content"] if messages else ""
        )
        session.add(user_message)
        session.commit()

        # Stream response back to client
        async def generate():
            # Run AI agent with MCP tools
            mcp_tools = create_mcp_tools(user_id, session)

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "gpt-4",
                        "messages": message_array,
                        "stream": True,
                        "tools": mcp_tools,
                    },
                    stream=True,
                )

                # Handle streaming response
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        chunk = line[6:]
                        if chunk != "[DONE]":
                            yield f"data: {chunk}\n\n"

                        # If tool call in chunk, invoke MCP tool
                        if "tool_calls" in chunk:
                            tool_result = await invoke_mcp_tool(chunk)
                            # Send tool result back to AI

            # Store assistant response
            assistant_message = Message(
                conversation_id=conversation.id,
                user_id=user_id,
                role="assistant",
                content="[See streaming response above]"
            )
            session.add(assistant_message)
            session.commit()

        return StreamingResponse(generate(), media_type="text/event-stream")

    except HTTPException:
        raise
    except Exception as e:
        print(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail="Chat failed")

def create_mcp_tools(user_id: str, session: Session) -> list:
    """Create MCP tool definitions for agent"""
    return [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Create a new task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                    },
                    "required": ["title"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "List user's tasks",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["all", "pending", "completed"],
                        },
                    },
                },
            },
        },
        # ... more tools
    ]

async def invoke_mcp_tool(tool_call: str, user_id: str, session: Session):
    """Invoke MCP tool based on tool_call"""
    parsed = json.loads(tool_call)

    if parsed.get("name") == "add_task":
        params = parsed.get("arguments", {})
        task = Task(
            user_id=user_id,
            title=params.get("title"),
            description=params.get("description"),
        )
        session.add(task)
        session.commit()
        return {
            "task_id": task.id,
            "status": "created",
            "title": task.title,
        }

    # Handle other tools...

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## Request/Response Flow

### Request from ChatKit

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Add a task to buy groceries"
    }
  ],
  "conversation_id": 5
}
```

### Response (Streaming)

```
data: {"id":"chatcmpl-...", "object":"chat.completion.chunk", "created": 1234567890, "model":"gpt-4", "choices":[{"delta":{"content":"I'll"}}]}

data: {"id":"chatcmpl-...", "object":"chat.completion.chunk", "created": 1234567890, "model":"gpt-4", "choices":[{"delta":{"content":" add"}}]}

data: {"id":"chatcmpl-...", "object":"chat.completion.chunk", "created": 1234567890, "model":"gpt-4", "choices":[{"delta":{"tool_calls":[{"name":"add_task", "arguments":{"title":"Buy groceries"}}]}}]}

data: [DONE]
```

---

## Error Handling

```python
@router.post("/api/chat")
async def chat_endpoint(...):
    try:
        # Validate token
        if not user_claims:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Validate request body
        if not messages or not isinstance(messages, list):
            raise HTTPException(status_code=400, detail="Invalid messages")

        # Check conversation exists
        if conversation_id and not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Run chat logic...

    except HTTPException as e:
        # Known error - return to client
        raise e

    except httpx.HTTPError as e:
        # API error
        logger.error(f"API error: {str(e)}")
        raise HTTPException(status_code=502, detail="External service error")

    except Exception as e:
        # Unexpected error
        logger.error(f"Chat error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
```

---

## Environment Variables

```bash
# Backend
DATABASE_URL=postgresql://user:password@localhost/todo_db
OPENAI_API_KEY=sk-...
BETTER_AUTH_SECRET=your-secret-key

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CHATKIT_DOMAIN_KEY=dk_...
```

---

## Testing Custom Backend

### Test Chat Endpoint

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Add a task"}
    ],
    "conversation_id": null
  }'
```

### Test with Python

```python
import httpx
import asyncio

async def test_chat():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/chat",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json={
                "messages": [
                    {"role": "user", "content": "What are my tasks?"}
                ],
                "conversation_id": None,
            },
        )

        async for line in response.aiter_lines():
            if line.startswith("data: "):
                print(line[6:])

asyncio.run(test_chat())
```

---

## Advantages of Custom Backend

✅ **Full Control**: Implement custom business logic
✅ **MCP Integration**: Use MCP tools for data operations
✅ **Security**: JWT validation before processing
✅ **Scalability**: Stateless design enables horizontal scaling
✅ **Flexibility**: Use any AI API, not just OpenAI
✅ **Data Integrity**: All operations go through validated backend

