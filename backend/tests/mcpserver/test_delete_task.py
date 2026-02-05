"""Tests for delete_task tool (Phase 7 - T034)"""

import pytest
from sqlmodel import select

from src.models.task import Task
from mcpserver.schemas import DeleteTaskParams, DeleteTaskResponse


class TestDeleteTaskParams:
    """Test delete_task parameter validation"""

    def test_valid_params_with_string_id(self):
        """Test valid parameters with string task_id"""
        params = DeleteTaskParams(
            user_id="test-user-123",
            task_id="abc123def456",
        )

        assert params.user_id == "test-user-123"
        assert params.task_id == "abc123def456"

    def test_valid_params_with_numeric_id(self):
        """Test valid parameters with numeric task_id"""
        params = DeleteTaskParams(
            user_id="test-user-123",
            task_id=1,
        )

        assert params.task_id == 1

    def test_missing_user_id_validation(self):
        """Test validation error for missing user_id"""
        with pytest.raises(ValueError):
            DeleteTaskParams(task_id=1)

    def test_empty_user_id_validation(self):
        """Test validation error for empty user_id"""
        with pytest.raises(ValueError):
            DeleteTaskParams(
                user_id="",
                task_id=1,
            )

    def test_missing_task_id_validation(self):
        """Test validation error for missing task_id"""
        with pytest.raises(ValueError):
            DeleteTaskParams(user_id="test-user-123")


class TestDeleteTaskResponse:
    """Test delete_task response structure"""

    def test_valid_response(self):
        """Test valid response"""
        response = DeleteTaskResponse(
            task_id=1,
            status="deleted",
            title="Deleted Task",
            message="Task deleted successfully",
        )

        assert response.task_id == 1
        assert response.status == "deleted"
        assert response.title == "Deleted Task"


@pytest.mark.asyncio
class TestDeleteTaskIntegration:
    """Integration tests for delete_task functionality"""

    async def test_successful_hard_delete(self, database_session, mock_user_id):
        """Test successful hard delete removes record from database"""
        # Create a task
        task = Task(
            user_id=mock_user_id,
            title="Task to delete",
            description="This will be deleted",
        )
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        task_id = task.id

        # Delete the task
        statement = select(Task).where(Task.id == task_id)
        result = await database_session.execute(statement)
        task_to_delete = result.scalars().first()

        if task_to_delete:
            await database_session.delete(task_to_delete)
            await database_session.commit()

        # Verify task is deleted (cannot retrieve afterward)
        statement = select(Task).where(Task.id == task_id)
        result = await database_session.execute(statement)
        deleted_task = result.scalars().first()

        assert deleted_task is None

    async def test_cannot_delete_other_users_task(self, database_session):
        """Test that cannot delete another user's task"""
        # Create task for user-1
        task = Task(
            user_id="user-1",
            title="User 1 Task",
            description="Description",
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

    async def test_delete_nonexistent_task(self, database_session, mock_user_id):
        """Test error when deleting non-existent task"""
        # Try to query a task that doesn't exist
        statement = select(Task).where(
            Task.id == "nonexistent-id",
            Task.user_id == mock_user_id,
        )
        result = await database_session.execute(statement)
        task = result.scalars().first()

        # Should not find the task
        assert task is None

    async def test_delete_affects_only_one_task(
        self, database_session, mock_user_id
    ):
        """Test that deleting one task doesn't affect others"""
        # Create multiple tasks
        task1 = Task(user_id=mock_user_id, title="Task 1", description="Desc 1")
        task2 = Task(user_id=mock_user_id, title="Task 2", description="Desc 2")
        task3 = Task(user_id=mock_user_id, title="Task 3", description="Desc 3")

        database_session.add(task1)
        database_session.add(task2)
        database_session.add(task3)
        await database_session.commit()
        await database_session.refresh(task1)
        await database_session.refresh(task2)
        await database_session.refresh(task3)

        # Delete only task2
        statement = select(Task).where(Task.id == task2.id)
        result = await database_session.execute(statement)
        task_to_delete = result.scalars().first()

        if task_to_delete:
            await database_session.delete(task_to_delete)
            await database_session.commit()

        # Verify only task2 is deleted
        statement1 = select(Task).where(Task.id == task1.id)
        result1 = await database_session.execute(statement1)
        remaining_task1 = result1.scalars().first()

        statement3 = select(Task).where(Task.id == task3.id)
        result3 = await database_session.execute(statement3)
        remaining_task3 = result3.scalars().first()

        statement2 = select(Task).where(Task.id == task2.id)
        result2 = await database_session.execute(statement2)
        deleted_task2 = result2.scalars().first()

        assert remaining_task1 is not None  # task1 still exists
        assert deleted_task2 is None  # task2 is deleted
        assert remaining_task3 is not None  # task3 still exists

    async def test_deleted_task_not_retrievable(
        self, database_session, mock_user_id
    ):
        """Test that deleted task cannot be retrieved afterward"""
        # Create a task
        task = Task(
            user_id=mock_user_id,
            title="Temporary task",
            description="Will be deleted",
        )
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        task_id = task.id

        # Verify task exists
        statement = select(Task).where(Task.id == task_id)
        result = await database_session.execute(statement)
        existing_task = result.scalars().first()
        assert existing_task is not None

        # Delete the task
        statement = select(Task).where(Task.id == task_id)
        result = await database_session.execute(statement)
        task_to_delete = result.scalars().first()

        if task_to_delete:
            await database_session.delete(task_to_delete)
            await database_session.commit()

        # Verify task is no longer retrievable
        statement = select(Task).where(Task.id == task_id)
        result = await database_session.execute(statement)
        deleted_task = result.scalars().first()

        assert deleted_task is None
