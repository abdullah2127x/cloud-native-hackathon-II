"""Delete task tool implementation (Phase 7 - T035)"""

import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.task import Task
from mcpserver.errors import ValidationError, DatabaseError, NotFoundError, create_success_response, create_error_response
from mcpserver.schemas import DeleteTaskParams, DeleteTaskResponse

logger = logging.getLogger(__name__)


async def delete_task(
    user_id: str,
    task_id: str | int,
    session: AsyncSession | None = None,
) -> dict[str, Any]:
    """Delete task (hard delete - permanent removal)

    Args:
        user_id: Authenticated user ID from JWT token
        task_id: ID of task to delete (string UUID or numeric)
        session: Database session for operation

    Returns:
        MCP-compatible response with deleted task info
    """
    try:
        # Validate parameters with Pydantic schema
        params = DeleteTaskParams(
            user_id=user_id,
            task_id=task_id,
        )

        logger.info(
            "delete_task called",
            extra={
                "user_id": params.user_id,
                "task_id": params.task_id,
                "operation": "delete",
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

        # Store task info for response
        task_title = task.title
        task_id_response = int(task.id) if task.id.isdigit() else hash(task.id) % (10 ** 8)

        # Delete task (hard delete - permanent removal)
        await session.delete(task)
        await session.commit()

        # Build response
        response_data = DeleteTaskResponse(
            task_id=task_id_response,
            status="deleted",
            title=task_title,
            message="Task deleted successfully",
        )

        logger.info(
            "task_deleted",
            extra={
                "user_id": params.user_id,
                "task_id": params.task_id,
                "task_title": task_title,
                "operation": "delete",
            }
        )

        # Return success response
        return create_success_response(
            content_text=f"Task '{task_title}' deleted successfully",
            structured_content=response_data.model_dump(),
        )

    except ValueError as e:
        # Pydantic validation error
        error = ValidationError(str(e))
        logger.warning(f"Validation error: {error.message}", extra={"user_id": user_id})
        return create_error_response(error)

    except Exception as e:
        # Unexpected error
        error = DatabaseError(f"Failed to delete task: {str(e)}")
        logger.error(
            f"Unexpected error in delete_task: {error.message}",
            extra={
                "user_id": user_id,
                "task_id": task_id,
                "error_type": type(e).__name__,
            },
            exc_info=True,
        )
        return create_error_response(error)
