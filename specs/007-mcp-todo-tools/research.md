# Research: MCP Server for Todo Operations

**Date**: 2026-02-05
**Feature**: 007-mcp-todo-tools
**Purpose**: Research technical patterns for implementing MCP server with FastAPI, JWT authentication, and database integration

## Decision Log

### 1. MCP SDK Choice

**Decision**: Use Official MCP SDK for Python with FastMCP high-level API

**Rationale**:
- FastMCP provides production-ready patterns for FastAPI integration
- Built-in support for OAuth 2.1 JWT authentication
- Stateless HTTP transport aligns with constitutional requirements
- Type-safe context management for dependency injection
- Automatic JSON Schema generation from type hints

**Alternatives Considered**:
- Building custom MCP protocol implementation → Rejected: Unnecessary complexity, protocol implementation is well-established
- Using lower-level MCP SDK primitives → Rejected: FastMCP provides same functionality with less boilerplate

### 2. FastAPI Integration Pattern

**Decision**: Mount MCP server using `app.mount("/mcp", mcp.streamable_http_app())`

**Rationale**:
- Cleanly separates MCP tools from REST API endpoints
- Allows independent lifecycl management for MCP server
- Provides dedicated endpoint path for AI agent tool invocations
- Maintains existing FastAPI app structure

**Implementation Pattern**:
```python
from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI

mcp = FastMCP("Todo Service", stateless_http=True, json_response=True)

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp.session_manager.run():
        yield

app = FastAPI(lifespan=lifespan)
app.mount("/mcp", mcp.streamable_http_app())
```

**Alternatives Considered**:
- Separate MCP server process → Rejected: Adds deployment complexity, shared database sessions preferred
- Custom middleware → Rejected: FastMCP mount pattern is standard and well-tested

### 3. JWT Authentication Strategy

**Decision**: Implement custom `TokenVerifier` that validates Better Auth JWT tokens

**Rationale**:
- MCP SDK provides `TokenVerifier` interface for custom authentication
- Validates token signature using public key (RS256 algorithm)
- Extracts `user_id` from token claims for user isolation
- Integrates with existing Better Auth infrastructure

**Implementation Pattern**:
```python
from mcp.server.auth.provider import AccessToken, TokenVerifier
import jwt

class BetterAuthTokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        try:
            payload = jwt.decode(
                token,
                PUBLIC_KEY,
                algorithms=["RS256"],
                audience="todo-api"
            )
            return AccessToken(
                token=token,
                scopes=payload.get("scope", "").split(),
                expires_at=payload.get("exp"),
                claims={"user_id": payload.get("sub")}
            )
        except jwt.InvalidTokenError:
            return None
```

**Alternatives Considered**:
- Session-based authentication → Rejected: Violates stateless principle
- API key authentication → Rejected: JWT is more secure and already implemented

### 4. User Isolation Pattern

**Decision**: Extract `user_id` from JWT token claims in every tool, validate against parameter

**Rationale**:
- Token claims provide cryptographically verified user identity
- Comparing token user_id with parameter prevents unauthorized access
- Allows flexible testing with explicit user_id parameters
- Prevents cross-user data access at tool boundary

**Implementation Pattern**:
```python
@mcp.tool()
def list_tasks(user_id: str, ctx: Context) -> list[dict]:
    # Extract from validated token
    token_user_id = ctx.request_context.access_token.claims["user_id"]

    # Validate match
    if user_id != token_user_id:
        return CallToolResult(
            content=[TextContent(type="text", text="Access denied")],
            isError=True
        )

    # Safe to proceed with database query
    return db.query_tasks(user_id)
```

**Alternatives Considered**:
- Only use token user_id (no parameter) → Rejected: Limits testing flexibility and AI agent clarity
- Trust user_id parameter without validation → Rejected: Security vulnerability

### 5. Database Connection Management

**Decision**: Use MCP lifespan context for shared database session

**Rationale**:
- Lifespan context provides dependency injection for shared resources
- Database connection initialized once at startup, reused across tools
- Automatic cleanup on shutdown
- Type-safe access via `ctx.request_context.lifespan_context`

**Implementation Pattern**:
```python
@dataclass
class AppContext:
    db_engine: Engine
    config: dict

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    engine = create_engine(DATABASE_URL)
    try:
        yield AppContext(db_engine=engine, config={})
    finally:
        engine.dispose()

mcp = FastMCP("Todo Service", lifespan=app_lifespan)

@mcp.tool()
def create_task(title: str, ctx: Context[ServerSession, AppContext]) -> dict:
    db = Database(ctx.request_context.lifespan_context.db_engine)
    # Use database...
```

**Alternatives Considered**:
- Global database connection → Rejected: Not thread-safe, harder to test
- Create connection per tool call → Rejected: Performance overhead, connection pool exhaustion

### 6. Error Handling Strategy

**Decision**: Return `CallToolResult` with `isError=True` for business logic errors

**Rationale**:
- Distinguishes between protocol errors (MCP framework) and tool errors (business logic)
- AI agents can self-correct from tool errors with clear messages
- Structured error responses maintain consistent format
- Never expose internal stack traces or sensitive data

**Implementation Pattern**:
```python
@mcp.tool()
def delete_task(task_id: str, user_id: str, ctx: Context) -> dict | CallToolResult:
    task = db.get_task(task_id)
    if not task:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Task {task_id} not found")],
            isError=True
        )

    if task.user_id != user_id:
        return CallToolResult(
            content=[TextContent(type="text", text="Access denied")],
            isError=True
        )

    db.delete_task(task_id)
    return {"success": True, "deleted_id": task_id}
```

**Alternatives Considered**:
- Raise exceptions → Rejected: Produces 500 errors instead of structured tool errors
- Return None for errors → Rejected: Not descriptive enough for AI self-correction

### 7. Transaction Retry Logic

**Decision**: Implement retry decorator with exponential backoff for database operations

**Rationale**:
- Handles transient database failures gracefully
- 1-2 retry attempts per constitutional requirement
- Automatic rollback on failure maintains data consistency
- Logged retries for observability

**Implementation Pattern**:
```python
from functools import wraps
import time

def retry_on_db_error(max_attempts=2, backoff_ms=100):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except DBException as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(backoff_ms / 1000)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@retry_on_db_error(max_attempts=2)
def db_operation():
    # Database operation...
```

**Alternatives Considered**:
- Manual retry in each tool → Rejected: Code duplication, inconsistent behavior
- No retry logic → Rejected: Violates specification requirement (SC-012)

### 8. Structured Logging Format

**Decision**: Use Python `structlog` with JSON formatter for all logs

**Rationale**:
- Constitutional requirement for structured logging
- JSON format includes: error_type, timestamp, user_id, tool_name, operation
- Machine-parseable for log aggregation and monitoring
- Easy integration with observability platforms

**Implementation Pattern**:
```python
import structlog

logger = structlog.get_logger()

@mcp.tool()
def create_task(title: str, user_id: str, ctx: Context) -> dict:
    try:
        result = db.create_task(title, user_id)
        logger.info(
            "task_created",
            user_id=user_id,
            task_id=result["id"],
            tool="add_task",
            operation="create"
        )
        return result
    except Exception as e:
        logger.error(
            "task_creation_failed",
            user_id=user_id,
            tool="add_task",
            operation="create",
            error_type=type(e).__name__,
            error_message=str(e)
        )
        raise
```

**Alternatives Considered**:
- Plain text logging → Rejected: Not machine-parseable, violates specification
- Per-tool log formatters → Rejected: Inconsistent, hard to aggregate

### 9. Tool Response Schema

**Decision**: Use Pydantic `BaseModel` for all tool responses

**Rationale**:
- Type-safe validation of response structure
- Automatic JSON schema generation for AI agents
- Consistent format across all 5 tools
- Integrates seamlessly with FastMCP

**Implementation Pattern**:
```python
from pydantic import BaseModel

class TaskResponse(BaseModel):
    task_id: int
    status: str  # "created", "completed", "updated", "deleted", "success"
    title: str
    message: str

class TaskListResponse(BaseModel):
    tasks: list[dict]
    count: int
    status: str = "success"

@mcp.tool()
def add_task(title: str, description: str, user_id: str) -> TaskResponse:
    task = db.create_task(title, description, user_id)
    return TaskResponse(
        task_id=task.id,
        status="created",
        title=task.title,
        message="Task created successfully"
    )
```

**Alternatives Considered**:
- Plain dict responses → Rejected: No validation, inconsistent structure
- TypedDict → Rejected: No runtime validation

### 10. Tool Parameter Validation

**Decision**: Use Pydantic `Field` with constraints for all tool parameters

**Rationale**:
- Enforces character limits (title 200, description 1000)
- Validates required fields before execution
- Automatic error messages for validation failures
- Prevents database constraint violations

**Implementation Pattern**:
```python
from pydantic import Field

@mcp.tool()
def add_task(
    user_id: str,
    title: str = Field(..., min_length=1, max_length=200),
    description: str = Field("", max_length=1000)
) -> TaskResponse:
    # Validation happens automatically before function executes
    task = db.create_task(title, description, user_id)
    return TaskResponse(...)
```

**Alternatives Considered**:
- Manual validation in tool body → Rejected: Code duplication
- Database-level validation only → Rejected: Less clear error messages for AI agents

## Technology Stack Summary

**Required Dependencies** (to be added to `backend/requirements.txt` or `pyproject.toml`):
- `mcp` - Official MCP SDK for Python (latest version)
- `PyJWT` - JWT token validation (already installed via Better Auth)
- `structlog` - Structured logging
- `tenacity` - Retry logic with exponential backoff (optional, can use custom decorator)

**Existing Dependencies** (reuse):
- `fastapi` - Web framework
- `sqlmodel` - ORM for database
- `pydantic` - Data validation
- `asyncpg` - PostgreSQL async driver

## Implementation Guidelines

### Tool Development Checklist

For each of the 5 tools (add_task, list_tasks, complete_task, delete_task, update_task):

1. ✅ Define Pydantic schema for parameters with Field constraints
2. ✅ Define Pydantic schema for response
3. ✅ Decorate function with `@mcp.tool()`
4. ✅ Accept `ctx: Context[ServerSession, AppContext]` parameter
5. ✅ Extract and validate `user_id` from JWT token
6. ✅ Implement database operation with retry logic
7. ✅ Handle errors with `CallToolResult(isError=True)`
8. ✅ Log operation with structured logger
9. ✅ Return typed response (Pydantic model)
10. ✅ Write unit tests with mocked database
11. ✅ Write integration test with real database

### Testing Strategy

**Unit Tests**:
- Mock database operations
- Mock JWT token validation
- Test successful operations
- Test error cases (not found, unauthorized, validation)

**Integration Tests**:
- Real database (test database)
- Real JWT tokens (test keys)
- Test MCP protocol compliance
- Test user isolation
- Test concurrent operations

## Next Steps

Phase 1 deliverables:
1. `data-model.md` - Tool schemas and response models
2. `contracts/` - JSON schema files for each tool
3. `quickstart.md` - Developer setup guide
4. Update `.specify/memory/agent-context.claude.md` with MCP SDK

