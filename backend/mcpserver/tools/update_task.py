"""Update task tool implementation (Phase 6 - T030)"""

import logging
from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.task import Task
from mcpserver.errors import ValidationError, DatabaseError, NotFoundError, create_success_response, create_error_response
from mcpserver.schemas import UpdateTaskParams, UpdateTaskResponse

logger = logging.getLogger(__name__)


async def update_task(
    user_id: str,
    task_id: str | int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    session: AsyncSession | None = None,
) -> dict[str, Any]:
    """Update task title and/or description

    Args:
        user_id: Authenticated user ID from JWT token
        task_id: ID of task to update (string UUID or numeric)
        title: New task title (optional)
        description: New task description (optional)
        session: Database session for operation

    Returns:
        MCP-compatible response with updated task info
    """
    try:
        # Validate parameters with Pydantic schema
        params = UpdateTaskParams(
            user_id=user_id,
            task_id=task_id,
            title=title,
            description=description,
        )

        logger.info(
            "update_task called",
            extra={
                "user_id": params.user_id,
                "task_id": params.task_id,
                "fields": "title" if params.title else "" + ", description" if params.description else "",
                "operation": "update",
            }
        )

        # Check if session is available
        if session is None:
            error = DatabaseError("Database session not available")
            logger.error(f"Database error: {error.message}", extra={"user_id": params.user_id})
            return create_error_response(error)

        # Convert task_id to string (Task model uses string IDs)
        task_id_str = str(params.task_id)

        # Query database for task by task_id and user_id
        statement = select(Task).where(
            Task.id == task_id_str,
            Task.user_id == params.user_id,
        )
        result = await session.execute(statement)
        task = result.scalars().first()

        # Check if task exists
        if task is None:
            error = NotFoundError("Task", params.task_id)
            logger.warning(
                f"Task not found: {error.message}",
                extra={"user_id": params.user_id, "task_id": params.task_id}
            )
            return create_error_response(error)

        # Store original values for logging
        original_title = task.title
        original_description = task.description

        # Update provided fields
        if params.title is not None:
            task.title = params.title

        if params.description is not None:
            task.description = params.description

        # Update updated_at timestamp
        from datetime import datetime, UTC
        task.updated_at = datetime.now(UTC)

        # Save changes to database
        session.add(task)
        await session.commit()
        await session.refresh(task)

        # Build response
        response_data = UpdateTaskResponse(
            task_id=int(task.id) if task.id.isdigit() else hash(task.id) % (10 ** 8),
            status="updated",
            title=task.title,
            message="Task updated successfully",
        )

        logger.info(
            "task_updated",
            extra={
                "user_id": params.user_id,
                "task_id": params.task_id,
                "title_changed": original_title != task.title,
                "description_changed": original_description != task.description,
                "operation": "update",
            }
        )

        # Return success response
        return create_success_response(
            content_text=f"Task '{task.title}' updated successfully",
            structured_content=response_data.model_dump(),
        )

    except ValueError as e:
        # Pydantic validation error
        error = ValidationError(str(e))
        logger.warning(f"Validation error: {error.message}", extra={"user_id": user_id})
        return create_error_response(error)

    except Exception as e:
        # Unexpected error
        error = DatabaseError(f"Failed to update task: {str(e)}")
        logger.error(
            f"Unexpected error in update_task: {error.message}",
            extra={
                "user_id": user_id,
                "task_id": task_id,
                "error_type": type(e).__name__,
            },
            exc_info=True,
        )
        return create_error_response(error)
