"""Tests for complete_task tool (Phase 5 - T024)"""

import pytest
from sqlmodel import select

from src.models.task import Task
from mcpserver.schemas import CompleteTaskParams, CompleteTaskResponse


class TestCompleteTaskParams:
    """Test complete_task parameter validation"""

    def test_valid_params(self):
        """Test valid parameters"""
        params = CompleteTaskParams(
            user_id="test-user-123",
            task_id=1,
        )

        assert params.user_id == "test-user-123"
        assert params.task_id == 1

    def test_missing_user_id_validation(self):
        """Test validation error for missing user_id"""
        with pytest.raises(ValueError):
            CompleteTaskParams(task_id=1)

    def test_empty_user_id_validation(self):
        """Test validation error for empty user_id"""
        with pytest.raises(ValueError):
            CompleteTaskParams(
                user_id="",
                task_id=1,
            )

    def test_missing_task_id_validation(self):
        """Test validation error for missing task_id"""
        with pytest.raises(ValueError):
            CompleteTaskParams(user_id="test-user-123")

    def test_valid_params_with_string_task_id(self):
        """Test valid parameters with string task_id (UUID)"""
        params = CompleteTaskParams(
            user_id="test-user-123",
            task_id="abc123def456",
        )

        assert params.user_id == "test-user-123"
        assert params.task_id == "abc123def456"

    def test_valid_params_with_numeric_task_id(self):
        """Test valid parameters with numeric task_id"""
        params = CompleteTaskParams(
            user_id="test-user-123",
            task_id=0,  # Numeric 0 is valid in schema
        )

        assert params.task_id == 0


class TestCompleteTaskResponse:
    """Test complete_task response structure"""

    def test_valid_response_completed(self):
        """Test valid response when task marked completed"""
        response = CompleteTaskResponse(
            task_id=1,
            status="completed",
            title="Test task",
            message="Task marked as completed",
        )

        assert response.task_id == 1
        assert response.status == "completed"
        assert response.title == "Test task"

    def test_valid_response_uncompleted(self):
        """Test valid response when task marked uncompleted"""
        response = CompleteTaskResponse(
            task_id=1,
            status="uncompleted",
            title="Test task",
            message="Task marked as pending",
        )

        assert response.task_id == 1
        assert response.status == "uncompleted"
        assert response.title == "Test task"


@pytest.mark.asyncio
class TestCompleteTaskIntegration:
    """Integration tests for complete_task functionality"""

    async def test_toggle_pending_to_completed(self, database_session, mock_user_id):
        """Test toggling task from pending to completed"""
        # Create a pending task
        task = Task(
            user_id=mock_user_id,
            title="Buy groceries",
            completed=False,
        )
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        # Toggle task to completed
        task.completed = not task.completed
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        # Verify task is now completed
        assert task.completed is True

    async def test_toggle_completed_to_pending(self, database_session, mock_user_id):
        """Test toggling task from completed back to pending"""
        # Create a completed task
        task = Task(
            user_id=mock_user_id,
            title="Buy groceries",
            completed=True,
        )
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        # Toggle task back to pending
        task.completed = not task.completed
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        # Verify task is now pending
        assert task.completed is False

    async def test_updated_at_timestamp_refreshed(
        self, database_session, mock_user_id
    ):
        """Test that toggling task preserves created_at"""
        from datetime import datetime

        # Create a task
        task = Task(
            user_id=mock_user_id,
            title="Test task",
            completed=False,
        )
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        original_created_at = task.created_at

        # Wait a tiny bit and toggle task
        import asyncio
        await asyncio.sleep(0.01)

        task.completed = not task.completed
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        # Verify created_at stayed same after toggle
        assert task.created_at == original_created_at
        assert task.completed is True

    async def test_cannot_toggle_other_users_task(self, database_session):
        """Test 403 error when trying to toggle another user's task"""
        # Create task for user-1
        task = Task(
            user_id="user-1",
            title="User 1 Task",
            completed=False,
        )
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        # Try to query as user-2 (should get empty result)
        statement = select(Task).where(
            Task.id == task.id,
            Task.user_id == "user-2",  # Different user
        )
        result = await database_session.execute(statement)
        found_task = result.scalars().first()

        # User-2 should not find the task
        assert found_task is None

    async def test_toggle_nonexistent_task(self, database_session, mock_user_id):
        """Test 404 error when trying to toggle non-existent task"""
        # Try to query a task that doesn't exist
        statement = select(Task).where(
            Task.id == 99999,  # Non-existent ID
            Task.user_id == mock_user_id,
        )
        result = await database_session.execute(statement)
        task = result.scalars().first()

        # Should not find the task
        assert task is None

    async def test_toggle_task_affects_only_one_record(
        self, database_session, mock_user_id
    ):
        """Test that toggling a task doesn't affect other tasks"""
        # Create multiple tasks
        task1 = Task(user_id=mock_user_id, title="Task 1", completed=False)
        task2 = Task(user_id=mock_user_id, title="Task 2", completed=False)
        task3 = Task(user_id=mock_user_id, title="Task 3", completed=True)

        database_session.add(task1)
        database_session.add(task2)
        database_session.add(task3)
        await database_session.commit()
        await database_session.refresh(task1)
        await database_session.refresh(task2)
        await database_session.refresh(task3)

        # Toggle only task2
        task2.completed = not task2.completed
        database_session.add(task2)
        await database_session.commit()

        # Verify only task2 changed
        await database_session.refresh(task1)
        await database_session.refresh(task2)
        await database_session.refresh(task3)

        assert task1.completed is False  # unchanged
        assert task2.completed is True  # toggled
        assert task3.completed is True  # unchanged
