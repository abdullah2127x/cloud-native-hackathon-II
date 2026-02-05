"""List tasks tool implementation (Phase 4 - T020)"""

import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.task import Task
from mcpserver.errors import ValidationError, DatabaseError, create_success_response, create_error_response
from mcpserver.schemas import ListTasksParams, ListTasksResponse, TaskItem

logger = logging.getLogger(__name__)


async def list_tasks(
    user_id: str,
    status: str = "all",
    session: AsyncSession | None = None,
) -> dict[str, Any]:
    """Retrieve tasks for the authenticated user with optional status filtering

    Args:
        user_id: Authenticated user ID from JWT token
        status: Filter by status - "all", "pending", or "completed" (default: "all")
        session: Database session for retrieval

    Returns:
        MCP-compatible response with task list
    """
    try:
        # Validate parameters with Pydantic schema
        params = ListTasksParams(
            user_id=user_id,
            status=status,
        )

        logger.info(
            "list_tasks called",
            extra={
                "user_id": params.user_id,
                "status": params.status,
                "operation": "list",
            }
        )

        # Check if session is available
        if session is None:
            error = DatabaseError("Database session not available")
            logger.error(f"Database error: {error.message}", extra={"user_id": params.user_id})
            return create_error_response(error)

        # Build query for user's tasks
        statement = select(Task).where(Task.user_id == params.user_id)

        # Apply status filter if not "all"
        if params.status == "completed":
            statement = statement.where(Task.completed == True)
        elif params.status == "pending":
            statement = statement.where(Task.completed == False)

        # Sort by created_at descending
        statement = statement.order_by(Task.created_at.desc())

        # Execute query
        result = await session.execute(statement)
        tasks = result.scalars().all()

        # Convert tasks to TaskItem objects
        task_items = [
            TaskItem(
                id=int(task.id) if task.id.isdigit() else hash(task.id) % (10 ** 8),
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at,
                updated_at=task.updated_at,
            )
            for task in tasks
        ]

        # Build response
        response_data = ListTasksResponse(
            tasks=task_items,
            count=len(task_items),
            status="success",
        )

        logger.info(
            "tasks_listed",
            extra={
                "user_id": params.user_id,
                "status": params.status,
                "count": len(task_items),
                "operation": "list",
            }
        )

        # Return success response with structured content
        return create_success_response(
            content_text=f"Retrieved {len(task_items)} task(s) with status '{params.status}'",
            structured_content=response_data.model_dump(),
        )

    except ValueError as e:
        # Pydantic validation error
        error = ValidationError(str(e))
        logger.warning(f"Validation error: {error.message}", extra={"user_id": user_id})
        return create_error_response(error)

    except Exception as e:
        # Unexpected error
        error = DatabaseError(f"Failed to list tasks: {str(e)}")
        logger.error(
            f"Unexpected error in list_tasks: {error.message}",
            extra={
                "user_id": user_id,
                "error_type": type(e).__name__,
            },
            exc_info=True,
        )
        return create_error_response(error)
