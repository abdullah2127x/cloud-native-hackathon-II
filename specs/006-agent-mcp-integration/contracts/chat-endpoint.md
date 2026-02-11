# API Contract: Chat Endpoint

**Feature**: 006-agent-mcp-integration
**Date**: 2026-02-11

---

## POST /api/{user_id}/chat

Send a natural language message and receive an AI agent response with task actions applied.

### Authentication

```
Authorization: Bearer <jwt_token>
```

JWT must match `user_id` in URL path. Returns `401` if missing or invalid.

---

### Request

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string | Yes | The authenticated user's ID |

**Body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | string | Yes | The user's natural language message (1–5000 chars) |
| `conversation_id` | integer | No | Existing conversation ID. Omit to start a new conversation. |

**Example Request**
```json
{
  "message": "Add a task to buy groceries",
  "conversation_id": 42
}
```

---

### Response

**200 OK**

```json
{
  "conversation_id": 42,
  "response": "Done! I've added 'Buy groceries' to your task list.",
  "tool_calls": ["add_task"]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `conversation_id` | integer | The conversation ID (new or existing) |
| `response` | string | The agent's natural language reply |
| `tool_calls` | array[string] | Names of MCP tools invoked (empty if none) |

---

### Error Responses

| Status | Code | When |
|--------|------|------|
| `400` | `INVALID_REQUEST` | Empty message or message > 5000 chars |
| `401` | `UNAUTHORIZED` | Missing or invalid JWT token |
| `404` | `CONVERSATION_NOT_FOUND` | `conversation_id` provided but not found or belongs to another user |
| `503` | `AI_PROVIDER_UNAVAILABLE` | OpenRouter API failed or timed out |
| `500` | `INTERNAL_ERROR` | Unexpected server error |

**Error body**:
```json
{
  "detail": "Human-readable error message",
  "code": "ERROR_CODE"
}
```

---

### Stateless Request Cycle

```
1. Validate JWT → extract user_id
2. Validate request body
3. Resolve conversation:
   - If conversation_id provided → load from DB, verify ownership → 404 if not found
   - If not provided → create new Conversation record
4. Persist user message to DB (role="user")
5. Load last 50 messages from DB for agent context
6. Build agent input: system_prompt + message history + new user message
7. Run agent → agent calls MCP tools as needed
8. Persist agent response to DB (role="assistant")
9. Update conversation.updated_at
10. Return: conversation_id + response text + tool_calls list
```

---

### Natural Language Command Mapping

| User says | Agent calls |
|-----------|-------------|
| "Add / create / remember X" | `add_task` |
| "Show / list / what are my tasks" | `list_tasks(status="all")` |
| "What's pending / not done" | `list_tasks(status="pending")` |
| "What have I completed" | `list_tasks(status="completed")` |
| "Mark task N as done / complete" | `complete_task(task_id=N)` |
| "Delete / remove task N" | `delete_task(task_id=N)` |
| "Delete X task" (by name) | `list_tasks` → `delete_task` |
| "Change / update task N to Y" | `update_task(task_id=N, title=Y)` |
