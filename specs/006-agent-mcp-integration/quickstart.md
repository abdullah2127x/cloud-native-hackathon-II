# Quickstart: Agent MCP Integration

**Feature**: 006-agent-mcp-integration
**Date**: 2026-02-11

---

## Prerequisites

- Backend running (`uv run uvicorn src.main:app --reload`)
- `.env` file with `OPENROUTER_API_KEY` and `LLM_MODEL` set
- Existing tasks in the database (optional but useful for testing)

---

## Environment Variables (add to backend/.env)

```env
OPENROUTER_API_KEY=sk-or-...
LLM_MODEL=openai/gpt-4o-mini
LLM_PROVIDER=openrouter
```

---

## New Files to Create

```
backend/
├── src/
│   ├── models/
│   │   ├── conversation.py        # NEW: Conversation SQLModel
│   │   └── message.py             # NEW: Message SQLModel
│   ├── schemas/
│   │   └── chat.py                # NEW: ChatRequest, ChatResponse Pydantic schemas
│   ├── crud/
│   │   └── chat.py                # NEW: CRUD for conversations and messages
│   ├── agents/
│   │   └── todo_agent.py          # NEW: Agent with MCP function tools
│   └── routers/
│       └── chat.py                # NEW: POST /api/{user_id}/chat endpoint
└── tests/
    ├── unit/
    │   └── test_chat_crud.py      # NEW: Unit tests for conversation/message CRUD
    └── integration/
        └── test_chat_api.py       # NEW: Integration tests for chat endpoint
```

---

## Testing the Chat Endpoint

### 1. Start a new conversation
```bash
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries"}'
```

Expected response:
```json
{
  "conversation_id": 1,
  "response": "Done! I've added 'Buy groceries' to your task list.",
  "tool_calls": ["add_task"]
}
```

### 2. Continue the conversation
```bash
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me all my tasks", "conversation_id": 1}'
```

### 3. Run tests
```bash
cd backend
uv run pytest tests/unit/test_chat_crud.py -v
uv run pytest tests/integration/test_chat_api.py -v
```

---

## Key Integration Points

| Component | Location | Role |
|-----------|----------|------|
| `TodoMCPServer` | `mcpserver/mcp_server.py` | Existing, unchanged |
| `todo_agent.py` | `src/agents/todo_agent.py` | Wraps MCP tools as function tools for OpenAI Agents SDK |
| `chat.py` router | `src/routers/chat.py` | Stateless endpoint orchestrating history + agent + persistence |
| `Conversation` model | `src/models/conversation.py` | New DB model |
| `Message` model | `src/models/message.py` | New DB model |
