# Quick Start: MCP Server for Todo Operations

**Feature**: 005-mcp-todo-tools
**Date**: 2026-02-05
**Purpose**: Developer guide for setting up, testing, and using the MCP server

## Prerequisites

- Python 3.11+ installed
- `uv` package manager installed
- PostgreSQL database running (Neon or local)
- Better Auth JWT public key configured
- FastAPI backend from Phase II running

## Installation

### 1. Install MCP SDK

Add to `backend/requirements.txt` or `backend/pyproject.toml`:

```toml
[project]
dependencies = [
    "fastapi>=0.104.0",
    "sqlmodel>=0.0.14",
    "pydantic>=2.5.0",
    "mcp>=1.0.0",  # Official MCP SDK
    "PyJWT>=2.8.0",
    "structlog>=24.1.0",
    "uvicorn>=0.25.0"
]
```

Install dependencies:

```bash
cd backend
uv pip install -r requirements.txt
```

### 2. Environment Variables

Add to `backend/.env`:

```env
# Existing variables (keep these)
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname
BETTER_AUTH_SECRET=your-secret-key

# New variables for MCP server
JWT_PUBLIC_KEY=-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----
MCP_SERVER_URL=http://localhost:8000
AUTH_ISSUER_URL=https://your-auth-server.com
```

## Project Structure

After implementation, your `backend/` directory will look like:

```
backend/
├── mcp/
│   ├── __init__.py               # MCP server exports
│   ├── server.py                 # Main MCP server setup
│   ├── middleware.py             # JWT validation middleware
│   ├── schemas.py                # Pydantic models for tools
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── add_task.py
│   │   ├── list_tasks.py
│   │   ├── complete_task.py
│   │   ├── delete_task.py
│   │   └── update_task.py
│   ├── auth.py                   # JWT utilities
│   ├── errors.py                 # Error handling
│   └── logging_config.py         # Structured logging
├── src/
│   ├── models/                   # Existing Task model
│   ├── database.py               # Existing database config
│   └── main.py                   # Modified: mount MCP server
└── tests/
    └── mcp/
        ├── conftest.py           # Test fixtures
        ├── test_add_task.py
        ├── test_list_tasks.py
        ├── test_complete_task.py
        ├── test_delete_task.py
        ├── test_update_task.py
        ├── test_auth.py
        ├── test_errors.py
        └── test_integration.py
```

## Running the Server

### Development Mode

```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

The MCP server will be mounted at:
- **MCP Endpoint**: `http://localhost:8000/mcp`
- **Health Check**: `http://localhost:8000/health`

### Production Mode

```bash
cd backend
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Testing

### Run All Tests

```bash
cd backend
pytest tests/mcp/ -v
```

### Run Specific Test Suite

```bash
# Unit tests only
pytest tests/mcp/test_add_task.py -v

# Integration tests
pytest tests/mcp/test_integration.py -v

# With coverage report
pytest tests/mcp/ --cov=mcp --cov-report=html
```

### Test with Real MCP Client

Using the MCP Inspector tool:

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Run inspector
mcp-inspector http://localhost:8000/mcp
```

## Using the MCP Server

### Authentication Flow

1. Obtain JWT token from Better Auth
2. Include token in `Authorization` header
3. MCP server validates token and extracts `user_id`
4. Tools enforce user isolation using `user_id`

### Tool Invocation (JSON-RPC Format)

#### Example: Create Task

**Request**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "add_task",
    "arguments": {
      "user_id": "auth0|abc123",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread"
    }
  }
}
```

**Headers**:
```
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Response**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"task_id\": 123, \"status\": \"created\", \"title\": \"Buy groceries\", \"message\": \"Task created successfully\"}"
      }
    ],
    "structuredContent": {
      "task_id": 123,
      "status": "created",
      "title": "Buy groceries",
      "message": "Task created successfully"
    },
    "isError": false
  }
}
```

#### Example: List Tasks

**Request**:
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "list_tasks",
    "arguments": {
      "user_id": "auth0|abc123",
      "status": "pending"
    }
  }
}
```

**Response**:
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"tasks\": [{\"id\": 123, \"title\": \"Buy groceries\", \"description\": \"Milk, eggs, bread\", \"completed\": false, \"created_at\": \"2026-02-05T10:30:00Z\", \"updated_at\": \"2026-02-05T10:30:00Z\"}], \"count\": 1, \"status\": \"success\"}"
      }
    ],
    "structuredContent": {
      "tasks": [
        {
          "id": 123,
          "title": "Buy groceries",
          "description": "Milk, eggs, bread",
          "completed": false,
          "created_at": "2026-02-05T10:30:00Z",
          "updated_at": "2026-02-05T10:30:00Z"
        }
      ],
      "count": 1,
      "status": "success"
    },
    "isError": false
  }
}
```

#### Example: Error Response

**Request** (unauthorized access):
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "delete_task",
    "arguments": {
      "user_id": "auth0|abc123",
      "task_id": 999
    }
  }
}
```

**Response**:
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Task 999 not found"
      }
    ],
    "isError": true
  }
}
```

## Debugging

### Enable Debug Logging

Set environment variable:
```bash
export LOG_LEVEL=DEBUG
uvicorn src.main:app --reload
```

### View Structured Logs

Logs are output in JSON format:
```json
{
  "timestamp": "2026-02-05T10:30:00.123Z",
  "level": "INFO",
  "user_id": "auth0|abc123",
  "tool_name": "add_task",
  "operation": "create",
  "message": "task_created",
  "task_id": 123
}
```

### Common Issues

**Issue**: `401 Unauthorized` error

**Solution**: Check JWT token is valid and not expired
```bash
# Decode JWT to inspect claims
echo "YOUR_JWT_TOKEN" | jwt decode -
```

**Issue**: `403 Forbidden` error

**Solution**: Verify `user_id` in token matches `user_id` parameter
```python
# Check token claims
payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
print(payload.get("sub"))  # Should match user_id parameter
```

**Issue**: Database connection errors

**Solution**: Verify `DATABASE_URL` is correct and database is accessible
```bash
# Test database connection
psql "postgresql://user:pass@host:5432/dbname"
```

## Integration with AI Agent

The MCP server is designed to be used by AI agents (OpenAI Agents SDK, Claude, etc.):

```python
# Example: OpenAI Agents SDK integration (separate spec)
from openai import OpenAI
from mcp import MCPClient

client = OpenAI(api_key="...")
mcp_client = MCPClient("http://localhost:8000/mcp", bearer_token="YOUR_JWT")

# AI agent discovers and uses tools
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Add a task to buy groceries"}
    ],
    tools=mcp_client.list_tools(),  # MCP tools exposed to AI
)
```

## Performance Monitoring

### Metrics to Track

- Tool invocation latency (should be < 2s)
- Database query time
- JWT validation time
- Error rate by tool
- Concurrent requests handled

### Health Check Endpoint

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "mcp_server": "running",
  "database": "connected"
}
```

## Next Steps

After implementation:

1. Run full test suite to verify all 5 tools work correctly
2. Test with real AI agent using OpenAI Agents SDK (separate spec)
3. Monitor structured logs for errors
4. Verify user isolation with multiple test users
5. Load test with 50+ concurrent requests

## Resources

- [MCP SDK Documentation](https://modelcontextprotocol.github.io/python-sdk/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/docs/sdk)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Better Auth JWT Guide](https://www.better-auth.com/docs/concepts/session-management)

