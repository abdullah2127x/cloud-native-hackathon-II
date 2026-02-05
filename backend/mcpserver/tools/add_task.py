"""Add task tool implementation (Phase 3 - T015)"""

import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.task import Task
from mcpserver.errors import ValidationError, UnauthorizedError, DatabaseError, create_success_response, create_error_response
from mcpserver.schemas import AddTaskParams, AddTaskResponse

logger = logging.getLogger(__name__)


async def add_task(
    user_id: str,
    title: str,
    description: str | None = None,
    session: AsyncSession | None = None,
) -> dict[str, Any]:
    """Create a new task for the authenticated user

    Args:
        user_id: Authenticated user ID from JWT token
        title: Task title (1-200 chars)
        description: Optional task description (max 1000 chars)
        session: Database session for persistence

    Returns:
        MCP-compatible response with created task_id
    """
    try:
        # Validate parameters with Pydantic schema
        params = AddTaskParams(
            user_id=user_id,
            title=title,
            description=description,
        )

        logger.info(
            "add_task called",
            extra={
                "user_id": params.user_id,
                "title": params.title,
                "operation": "create",
            }
        )

        # Check if session is available
        if session is None:
            error = DatabaseError("Database session not available")
            logger.error(f"Database error: {error.message}", extra={"user_id": params.user_id})
            return create_error_response(error)

        # Create task record
        task = Task(
            user_id=params.user_id,
            title=params.title,
            description=params.description,
            completed=False,
        )

        # Add to database
        session.add(task)
        await session.commit()
        await session.refresh(task)

        # Build response
        response_data = AddTaskResponse(
            task_id=int(task.id) if task.id.isdigit() else hash(task.id) % (10 ** 8),
            status="created",
            title=task.title,
            message="Task created successfully",
        )

        logger.info(
            "task_created",
            extra={
                "user_id": params.user_id,
                "task_id": task.id,
                "title": task.title,
                "operation": "create",
            }
        )

        # Return success response with structured content
        return create_success_response(
            content_text=f"Task '{task.title}' created successfully",
            structured_content=response_data.model_dump(),
        )

    except ValueError as e:
        # Pydantic validation error
        error = ValidationError(str(e))
        logger.warning(f"Validation error: {error.message}", extra={"user_id": user_id})
        return create_error_response(error)

    except Exception as e:
        # Unexpected error
        error = DatabaseError(f"Failed to create task: {str(e)}")
        logger.error(
            f"Unexpected error in add_task: {error.message}",
            extra={
                "user_id": user_id,
                "error_type": type(e).__name__,
            },
            exc_info=True,
        )
        return create_error_response(error)
