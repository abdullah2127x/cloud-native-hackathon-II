"""Pydantic schemas for MCP tools

Defines request parameters and response models for all 5 CRUD tools.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, model_validator


# ==================== add_task ====================


class AddTaskParams(BaseModel):
    """Parameters for add_task tool"""

    user_id: str = Field(..., min_length=1, description="Authenticated user ID")
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(
        None, max_length=1000, description="Task description (optional)"
    )


class AddTaskResponse(BaseModel):
    """Response from add_task tool"""

    task_id: int = Field(..., description="ID of created task")
    status: str = Field("created", description="Operation status")
    title: str = Field(..., description="Created task title")
    message: str = Field("Task created successfully", description="Success message")


# ==================== list_tasks ====================


class ListTasksParams(BaseModel):
    """Parameters for list_tasks tool"""

    user_id: str = Field(..., min_length=1, description="Authenticated user ID")
    status: Optional[str] = Field(
        "all",
        description="Filter by status: 'all', 'pending', or 'completed'",
        pattern="^(all|pending|completed)$",
    )


class TaskItem(BaseModel):
    """Individual task in list response"""

    id: int = Field(..., description="Task ID")
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    completed: bool = Field(..., description="Completion status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")


class ListTasksResponse(BaseModel):
    """Response from list_tasks tool"""

    tasks: list[TaskItem] = Field(..., description="Array of tasks")
    count: int = Field(..., description="Total number of tasks")
    status: str = Field("success", description="Operation status")


# ==================== complete_task ====================


class CompleteTaskParams(BaseModel):
    """Parameters for complete_task tool"""

    user_id: str = Field(..., min_length=1, description="Authenticated user ID")
    task_id: str | int = Field(..., description="ID of task to toggle")


class CompleteTaskResponse(BaseModel):
    """Response from complete_task tool"""

    task_id: int = Field(..., description="ID of toggled task")
    status: str = Field(..., description="New status: 'completed' or 'uncompleted'")
    title: str = Field(..., description="Task title")
    message: str = Field(..., description="Success message")


# ==================== update_task ====================


class UpdateTaskParams(BaseModel):
    """Parameters for update_task tool"""

    user_id: str = Field(..., min_length=1, description="Authenticated user ID")
    task_id: str | int = Field(..., description="ID of task to update")
    title: Optional[str] = Field(
        None, min_length=1, max_length=200, description="New title (optional)"
    )
    description: Optional[str] = Field(
        None, max_length=1000, description="New description (optional)"
    )

    @model_validator(mode='after')
    def check_at_least_one_field(self):
        """Ensure at least one of title or description is provided"""
        if self.title is None and self.description is None:
            raise ValueError("At least one of 'title' or 'description' must be provided")
        return self


class UpdateTaskResponse(BaseModel):
    """Response from update_task tool"""

    task_id: int = Field(..., description="ID of updated task")
    status: str = Field("updated", description="Operation status")
    title: str = Field(..., description="Updated task title")
    message: str = Field("Task updated successfully", description="Success message")


# ==================== delete_task ====================


class DeleteTaskParams(BaseModel):
    """Parameters for delete_task tool"""

    user_id: str = Field(..., min_length=1, description="Authenticated user ID")
    task_id: str | int = Field(..., description="ID of task to delete")


class DeleteTaskResponse(BaseModel):
    """Response from delete_task tool"""

    task_id: int = Field(..., description="ID of deleted task")
    status: str = Field("deleted", description="Operation status")
    title: str = Field(..., description="Deleted task title")
    message: str = Field("Task deleted successfully", description="Success message")
