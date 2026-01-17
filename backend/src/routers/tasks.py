"""Task API endpoints"""
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from typing import List

from src.db.database import get_session
from src.auth.dependencies import get_current_user
from src.schemas.task import TaskCreate, TaskUpdate, TaskRead
from src.crud import task as task_crud


router = APIRouter(prefix="/api/todos", tags=["tasks"])


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Create a new task"""
    task = task_crud.create_task(session, task_data, user_id)
    return task


@router.get("/", response_model=List[TaskRead])
async def list_tasks(
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """List all tasks for the authenticated user"""
    tasks = task_crud.list_tasks(session, user_id)
    return tasks


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: str,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Get a specific task by ID"""
    task = task_crud.get_task(session, task_id, user_id)
    return task


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Update a task"""
    task = task_crud.update_task(session, task_id, user_id, task_data)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Delete a task"""
    task_crud.delete_task(session, task_id, user_id)


@router.post("/{task_id}/toggle", response_model=TaskRead)
async def toggle_task_completion(
    task_id: str,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Toggle task completion status"""
    task = task_crud.toggle_task_completion(session, task_id, user_id)
    return task
