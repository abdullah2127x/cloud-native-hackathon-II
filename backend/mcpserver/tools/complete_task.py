"""Complete task tool implementation (Phase 5 - T025)"""

import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.task import Task
from mcpserver.errors import ValidationError, DatabaseError, NotFoundError, create_success_response, create_error_response
from mcpserver.schemas import CompleteTaskParams, CompleteTaskResponse

logger = logging.getLogger(__name__)


async def complete_task(
    user_id: str,
    task_id: int,
    session: AsyncSession | None = None,
) -> dict[str, Any]:
    """Toggle task completion status

    Args:
        user_id: Authenticated user ID from JWT token
        task_id: ID of task to toggle
        session: Database session for operation

    Returns:
        MCP-compatible response with updated task status
    """
    try:
        # Validate parameters with Pydantic schema
        params = CompleteTaskParams(
            user_id=user_id,
            task_id=task_id,
        )

        logger.info(
            "complete_task called",
            extra={
                "user_id": params.user_id,
                "task_id": params.task_id,
                "operation": "complete",
            }
        )

        # Check if session is available
        if session is None:
            error = DatabaseError("Database session not available")
            logger.error(f"Database error: {error.message}", extra={"user_id": params.user_id})
            return create_error_response(error)

        # Query database for task by task_id and user_id
        # Task IDs can be either numeric (converted) or string (UUID)
        # Convert to string to match database format
        task_id_str = str(params.task_id)

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

        # Toggle completed status
        previous_status = task.completed
        task.completed = not task.completed
        new_status_str = "completed" if task.completed else "uncompleted"

        # Update updated_at timestamp
        from datetime import datetime, UTC
        task.updated_at = datetime.now(UTC)

        # Save changes to database
        session.add(task)
        await session.commit()
        await session.refresh(task)

        # Build response
        response_data = CompleteTaskResponse(
            task_id=int(task.id) if task.id.isdigit() else hash(task.id) % (10 ** 8),
            status=new_status_str,
            title=task.title,
            message=f"Task marked as {new_status_str}",
        )

        logger.info(
            "task_completed",
            extra={
                "user_id": params.user_id,
                "task_id": params.task_id,
                "status": new_status_str,
                "operation": "complete",
            }
        )

        # Return success response
        return create_success_response(
            content_text=f"Task '{task.title}' marked as {new_status_str}",
            structured_content=response_data.model_dump(),
        )

    except ValueError as e:
        # Pydantic validation error
        error = ValidationError(str(e))
        logger.warning(f"Validation error: {error.message}", extra={"user_id": user_id})
        return create_error_response(error)

    except Exception as e:
        # Unexpected error
        error = DatabaseError(f"Failed to toggle task: {str(e)}")
        logger.error(
            f"Unexpected error in complete_task: {error.message}",
            extra={
                "user_id": user_id,
                "task_id": task_id,
                "error_type": type(e).__name__,
            },
            exc_info=True,
        )
        return create_error_response(error)
