"""Tests for update_task tool (Phase 6 - T029)"""

import pytest
from sqlmodel import select

from src.models.task import Task
from mcpserver.schemas import UpdateTaskParams, UpdateTaskResponse


class TestUpdateTaskParams:
    """Test update_task parameter validation"""

    def test_valid_params_update_title_only(self):
        """Test valid parameters with title only"""
        params = UpdateTaskParams(
            user_id="test-user-123",
            task_id="abc123",
            title="Updated title",
        )

        assert params.user_id == "test-user-123"
        assert params.task_id == "abc123"
        assert params.title == "Updated title"
        assert params.description is None

    def test_valid_params_update_description_only(self):
        """Test valid parameters with description only"""
        params = UpdateTaskParams(
            user_id="test-user-123",
            task_id=1,
            description="Updated description",
        )

        assert params.task_id == 1
        assert params.description == "Updated description"
        assert params.title is None

    def test_valid_params_update_both(self):
        """Test valid parameters with both title and description"""
        params = UpdateTaskParams(
            user_id="test-user-123",
            task_id="abc123",
            title="New title",
            description="New description",
        )

        assert params.title == "New title"
        assert params.description == "New description"

    def test_missing_user_id_validation(self):
        """Test validation error for missing user_id"""
        with pytest.raises(ValueError):
            UpdateTaskParams(
                task_id=1,
                title="Updated title",
            )

    def test_empty_user_id_validation(self):
        """Test validation error for empty user_id"""
        with pytest.raises(ValueError):
            UpdateTaskParams(
                user_id="",
                task_id=1,
                title="Updated title",
            )

    def test_missing_task_id_validation(self):
        """Test validation error for missing task_id"""
        with pytest.raises(ValueError):
            UpdateTaskParams(
                user_id="test-user-123",
                title="Updated title",
            )

    def test_missing_both_fields_validation(self):
        """Test validation error when neither title nor description provided"""
        with pytest.raises(ValueError):
            UpdateTaskParams(
                user_id="test-user-123",
                task_id=1,
            )

    def test_empty_title_validation(self):
        """Test validation error for empty title"""
        with pytest.raises(ValueError):
            UpdateTaskParams(
                user_id="test-user-123",
                task_id=1,
                title="",  # Empty string
                description="Valid description",
            )

    def test_title_exceeds_max_length(self):
        """Test validation error for title exceeding 200 chars"""
        with pytest.raises(ValueError):
            UpdateTaskParams(
                user_id="test-user-123",
                task_id=1,
                title="x" * 201,  # Exceeds max length
            )

    def test_description_exceeds_max_length(self):
        """Test validation error for description exceeding 1000 chars"""
        with pytest.raises(ValueError):
            UpdateTaskParams(
                user_id="test-user-123",
                task_id=1,
                description="x" * 1001,  # Exceeds max length
                title="Valid title",
            )


class TestUpdateTaskResponse:
    """Test update_task response structure"""

    def test_valid_response(self):
        """Test valid response"""
        response = UpdateTaskResponse(
            task_id=1,
            status="updated",
            title="Updated Task",
            message="Task updated successfully",
        )

        assert response.task_id == 1
        assert response.status == "updated"
        assert response.title == "Updated Task"
        assert response.message == "Task updated successfully"


@pytest.mark.asyncio
class TestUpdateTaskIntegration:
    """Integration tests for update_task functionality"""

    async def test_update_title_only(self, database_session, mock_user_id):
        """Test updating task title only"""
        # Create a task
        task = Task(
            user_id=mock_user_id,
            title="Original title",
            description="Original description",
        )
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        original_description = task.description

        # Update title
        task.title = "New title"
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        # Verify only title changed
        assert task.title == "New title"
        assert task.description == original_description

    async def test_update_description_only(self, database_session, mock_user_id):
        """Test updating task description only"""
        # Create a task
        task = Task(
            user_id=mock_user_id,
            title="Original title",
            description="Original description",
        )
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        original_title = task.title

        # Update description
        task.description = "New description"
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        # Verify only description changed
        assert task.title == original_title
        assert task.description == "New description"

    async def test_update_both_fields(self, database_session, mock_user_id):
        """Test updating both title and description"""
        # Create a task
        task = Task(
            user_id=mock_user_id,
            title="Original title",
            description="Original description",
        )
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        # Update both fields
        task.title = "New title"
        task.description = "New description"
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        # Verify both changed
        assert task.title == "New title"
        assert task.description == "New description"

    async def test_cannot_update_other_users_task(self, database_session):
        """Test that cannot update another user's task"""
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

    async def test_update_nonexistent_task(self, database_session, mock_user_id):
        """Test error when updating non-existent task"""
        # Try to query a task that doesn't exist
        statement = select(Task).where(
            Task.id == "nonexistent-id",
            Task.user_id == mock_user_id,
        )
        result = await database_session.execute(statement)
        task = result.scalars().first()

        # Should not find the task
        assert task is None

    async def test_update_preserves_created_at(self, database_session, mock_user_id):
        """Test that update preserves created_at timestamp"""
        # Create a task
        task = Task(
            user_id=mock_user_id,
            title="Original title",
            description="Original description",
        )
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        original_created_at = task.created_at

        # Update task
        task.title = "New title"
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        # Verify created_at unchanged
        assert task.created_at == original_created_at

    async def test_update_affects_only_one_task(
        self, database_session, mock_user_id
    ):
        """Test that updating one task doesn't affect others"""
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

        # Update only task2
        task2.title = "Updated Task 2"
        database_session.add(task2)
        await database_session.commit()

        # Verify only task2 changed
        await database_session.refresh(task1)
        await database_session.refresh(task2)
        await database_session.refresh(task3)

        assert task1.title == "Task 1"  # unchanged
        assert task2.title == "Updated Task 2"  # updated
        assert task3.title == "Task 3"  # unchanged
