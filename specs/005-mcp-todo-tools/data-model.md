# Data Model: MCP Server for Todo Operations

**Date**: 2026-02-05
**Feature**: 005-mcp-todo-tools
**Purpose**: Define Pydantic schemas for tool parameters, responses, and internal models

## Existing Entities (Reused)

### Task (SQLModel - from Phase II)

Existing database model - **NO MODIFICATIONS REQUIRED**

```python
class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Better Auth user ID
    title: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Validation Rules**:
- `user_id`: Required, non-empty string (from JWT token)
- `title`: Required, 1-200 characters
- `description`: Optional, max 1000 characters
- `completed`: Boolean, defaults to False
- `created_at`, `updated_at`: Auto-generated timestamps

**Relationships**:
- Belongs to User (Better Auth user table, via user_id foreign key)

**State Transitions**:
- `completed`: False → True (via complete_task)
- `completed`: True → False (via complete_task - toggle behavior)

## MCP Tool Schemas

### Common Response Models

#### BaseToolResponse

Base model for all tool responses

```python
from pydantic import BaseModel, Field

class BaseToolResponse(BaseModel):
    """Base response model for all MCP tools."""
    status: str = Field(..., description="Operation status: created, completed, uncompleted, updated, deleted, success")
    message: str = Field(..., description="Human-readable operation result message")
```

#### ToolError

Error response model (when `isError=True`)

```python
class ToolError(BaseModel):
    """Error response structure."""
    error_type: str = Field(..., description="Error category: validation, not_found, unauthorized, internal")
    message: str = Field(..., description="User-friendly error message")
    details: dict | None = Field(default=None, description="Additional error context")
```

### Tool 1: add_task

#### Parameters

```python
class AddTaskParams(BaseModel):
    """Parameters for add_task tool."""
    user_id: str = Field(..., description="Authenticated user ID", min_length=1)
    title: str = Field(..., description="Task title", min_length=1, max_length=200)
    description: str = Field(default="", description="Task description (optional)", max_length=1000)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": "auth0|abc123",
                    "title": "Buy groceries",
                    "description": "Milk, eggs, bread"
                }
            ]
        }
    }
```

#### Response

```python
class AddTaskResponse(BaseModel):
    """Response from add_task tool."""
    task_id: int = Field(..., description="ID of the created task")
    status: str = Field(default="created", description="Always 'created' for successful creation")
    title: str = Field(..., description="Title of the created task")
    message: str = Field(default="Task created successfully", description="Success message")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "task_id": 123,
                    "status": "created",
                    "title": "Buy groceries",
                    "message": "Task created successfully"
                }
            ]
        }
    }
```

### Tool 2: list_tasks

#### Parameters

```python
from typing import Literal

class ListTasksParams(BaseModel):
    """Parameters for list_tasks tool."""
    user_id: str = Field(..., description="Authenticated user ID", min_length=1)
    status: Literal["all", "pending", "completed"] = Field(
        default="all",
        description="Filter by completion status"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"user_id": "auth0|abc123", "status": "all"},
                {"user_id": "auth0|abc123", "status": "pending"},
                {"user_id": "auth0|abc123", "status": "completed"}
            ]
        }
    }
```

#### Response

```python
class TaskItem(BaseModel):
    """Individual task in list response."""
    id: int = Field(..., description="Task ID")
    title: str = Field(..., description="Task title")
    description: str | None = Field(None, description="Task description")
    completed: bool = Field(..., description="Completion status")
    created_at: str = Field(..., description="Creation timestamp (ISO 8601)")
    updated_at: str = Field(..., description="Last update timestamp (ISO 8601)")

class ListTasksResponse(BaseModel):
    """Response from list_tasks tool."""
    tasks: list[TaskItem] = Field(..., description="Array of tasks matching filter")
    count: int = Field(..., description="Number of tasks returned")
    status: str = Field(default="success", description="Always 'success' for successful query")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "tasks": [
                        {
                            "id": 123,
                            "title": "Buy groceries",
                            "description": "Milk, eggs, bread",
                            "completed": False,
                            "created_at": "2026-02-05T10:30:00Z",
                            "updated_at": "2026-02-05T10:30:00Z"
                        }
                    ],
                    "count": 1,
                    "status": "success"
                }
            ]
        }
    }
```

### Tool 3: complete_task

#### Parameters

```python
class CompleteTaskParams(BaseModel):
    """Parameters for complete_task tool."""
    user_id: str = Field(..., description="Authenticated user ID", min_length=1)
    task_id: int = Field(..., description="ID of the task to mark complete", gt=0)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"user_id": "auth0|abc123", "task_id": 123}
            ]
        }
    }
```

#### Response

```python
class CompleteTaskResponse(BaseModel):
    """Response from complete_task tool."""
    task_id: int = Field(..., description="ID of the completed/uncompleted task")
    status: Literal["completed", "uncompleted"] = Field(..., description="New completion status after toggle")
    title: str = Field(..., description="Title of the task")
    message: str = Field(..., description="Success message")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "task_id": 123,
                    "status": "completed",
                    "title": "Buy groceries",
                    "message": "Task marked as completed"
                },
                {
                    "task_id": 123,
                    "status": "uncompleted",
                    "title": "Buy groceries",
                    "message": "Task marked as uncompleted"
                }
            ]
        }
    }
```

### Tool 4: delete_task

#### Parameters

```python
class DeleteTaskParams(BaseModel):
    """Parameters for delete_task tool."""
    user_id: str = Field(..., description="Authenticated user ID", min_length=1)
    task_id: int = Field(..., description="ID of the task to delete", gt=0)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"user_id": "auth0|abc123", "task_id": 123}
            ]
        }
    }
```

#### Response

```python
class DeleteTaskResponse(BaseModel):
    """Response from delete_task tool."""
    task_id: int = Field(..., description="ID of the deleted task")
    status: str = Field(default="deleted", description="Always 'deleted' for successful deletion")
    title: str = Field(..., description="Title of the deleted task")
    message: str = Field(default="Task deleted successfully", description="Success message")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "task_id": 123,
                    "status": "deleted",
                    "title": "Buy groceries",
                    "message": "Task deleted successfully"
                }
            ]
        }
    }
```

### Tool 5: update_task

#### Parameters

```python
from typing import Annotated

class UpdateTaskParams(BaseModel):
    """Parameters for update_task tool."""
    user_id: str = Field(..., description="Authenticated user ID", min_length=1)
    task_id: int = Field(..., description="ID of the task to update", gt=0)
    title: str | None = Field(None, description="New task title (optional)", min_length=1, max_length=200)
    description: str | None = Field(None, description="New task description (optional)", max_length=1000)

    @model_validator(mode='after')
    def check_at_least_one_field(self) -> 'UpdateTaskParams':
        """Validate that at least one field (title or description) is provided."""
        if self.title is None and self.description is None:
            raise ValueError("At least one field (title or description) must be provided")
        return self

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": "auth0|abc123",
                    "task_id": 123,
                    "title": "Buy organic groceries"
                },
                {
                    "user_id": "auth0|abc123",
                    "task_id": 123,
                    "description": "Milk, eggs, bread, cheese"
                },
                {
                    "user_id": "auth0|abc123",
                    "task_id": 123,
                    "title": "Buy organic groceries",
                    "description": "Milk, eggs, bread, cheese"
                }
            ]
        }
    }
```

#### Response

```python
class UpdateTaskResponse(BaseModel):
    """Response from update_task tool."""
    task_id: int = Field(..., description="ID of the updated task")
    status: str = Field(default="updated", description="Always 'updated' for successful update")
    title: str = Field(..., description="Current title of the task after update")
    message: str = Field(default="Task updated successfully", description="Success message")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "task_id": 123,
                    "status": "updated",
                    "title": "Buy organic groceries",
                    "message": "Task updated successfully"
                }
            ]
        }
    }
```

## Internal Models (not exposed to AI agents)

### AppContext

Lifespan context for dependency injection

```python
from dataclasses import dataclass
from sqlmodel import Engine

@dataclass
class AppContext:
    """Application-wide shared resources."""
    db_engine: Engine
    jwt_public_key: str
    config: dict[str, any]
```

### LogEntry

Structured log entry model

```python
class LogEntry(BaseModel):
    """Structured log entry for JSON logging."""
    timestamp: str = Field(..., description="ISO 8601 timestamp")
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    user_id: str | None = Field(None, description="User ID from JWT token")
    tool_name: str | None = Field(None, description="MCP tool invoked")
    operation: str | None = Field(None, description="Operation attempted")
    error_type: str | None = Field(None, description="Error class name if error occurred")
    error_message: str | None = Field(None, description="Error message if error occurred")
    details: dict | None = Field(None, description="Additional context")
```

## Validation Summary

### Field Constraints

| Field | Constraint | Enforcement |
|-------|------------|-------------|
| user_id | Required, non-empty | Pydantic `min_length=1` |
| title | 1-200 characters | Pydantic `min_length=1, max_length=200` |
| description | Max 1000 characters | Pydantic `max_length=1000` |
| task_id | Positive integer | Pydantic `gt=0` |
| status (filter) | Enum: all, pending, completed | Pydantic `Literal["all", "pending", "completed"]` |
| update fields | At least one required | Pydantic `@model_validator` |

### Error Codes

| Error Type | HTTP Equivalent | When Used |
|------------|-----------------|-----------|
| validation | 400 Bad Request | Invalid parameters (empty title, invalid status, etc.) |
| not_found | 404 Not Found | Task does not exist |
| unauthorized | 403 Forbidden | Task belongs to different user |
| internal | 500 Internal Server Error | Database errors, unexpected failures |

## Schema Files Location

JSON Schema files for each tool will be generated in `contracts/`:
- `contracts/add_task.json` - JSON Schema for add_task tool
- `contracts/list_tasks.json` - JSON Schema for list_tasks tool
- `contracts/complete_task.json` - JSON Schema for complete_task tool
- `contracts/delete_task.json` - JSON Schema for delete_task tool
- `contracts/update_task.json` - JSON Schema for update_task tool

These schemas are auto-generated from Pydantic models using `model.model_json_schema()`.

