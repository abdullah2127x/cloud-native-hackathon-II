"""CRUD operations for Task model"""
from sqlmodel import Session, select
from src.models.task import Task
from src.schemas.task import TaskCreate, TaskUpdate
from src.exceptions.base import TaskNotFoundError, UnauthorizedError
from datetime import datetime, UTC
from typing import List, Optional


def create_task(session: Session, task_data: TaskCreate, user_id: str) -> Task:
    """
    Create a new task for a user

    Args:
        session: Database session
        task_data: Task creation data
        user_id: ID of the user creating the task

    Returns:
        Created task
    """
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_task(session: Session, task_id: str, user_id: str) -> Task:
    """
    Get a task by ID, ensuring it belongs to the user

    Args:
        session: Database session
        task_id: ID of the task
        user_id: ID of the user

    Returns:
        Task if found and belongs to user

    Raises:
        TaskNotFoundError: If task doesn't exist or doesn't belong to user
    """
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    task = session.exec(statement).first()

    if not task:
        raise TaskNotFoundError(task_id)

    return task


def list_tasks(session: Session, user_id: str) -> List[Task]:
    """
    List all tasks for a user

    Args:
        session: Database session
        user_id: ID of the user

    Returns:
        List of tasks ordered by creation date (newest first)
    """
    statement = select(Task).where(
        Task.user_id == user_id
    ).order_by(Task.created_at.desc())

    tasks = session.exec(statement).all()
    return list(tasks)


def update_task(session: Session, task_id: str, user_id: str, task_data: TaskUpdate) -> Task:
    """
    Update a task

    Args:
        session: Database session
        task_id: ID of the task
        user_id: ID of the user
        task_data: Updated task data

    Returns:
        Updated task

    Raises:
        TaskNotFoundError: If task doesn't exist or doesn't belong to user
    """
    task = get_task(session, task_id, user_id)

    # Update only provided fields
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed

    task.updated_at = datetime.now(UTC)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task_id: str, user_id: str) -> None:
    """
    Delete a task

    Args:
        session: Database session
        task_id: ID of the task
        user_id: ID of the user

    Raises:
        TaskNotFoundError: If task doesn't exist or doesn't belong to user
    """
    task = get_task(session, task_id, user_id)
    session.delete(task)
    session.commit()


def toggle_task_completion(session: Session, task_id: str, user_id: str) -> Task:
    """
    Toggle task completion status

    Args:
        session: Database session
        task_id: ID of the task
        user_id: ID of the user

    Returns:
        Updated task

    Raises:
        TaskNotFoundError: If task doesn't exist or doesn't belong to user
    """
    task = get_task(session, task_id, user_id)
    task.completed = not task.completed
    task.updated_at = datetime.now(UTC)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task
