"""Tests for add_task tool (Phase 3 - T014)"""

import pytest
from sqlmodel import select

from src.models.task import Task
from mcpserver.schemas import AddTaskParams, AddTaskResponse


class TestAddTaskParams:
    """Test add_task parameter validation"""

    def test_valid_params_with_description(self):
        """Test valid parameters with title and description"""
        params = AddTaskParams(
            user_id="test-user-123",
            title="Buy groceries",
            description="Milk, eggs, bread",
        )

        assert params.user_id == "test-user-123"
        assert params.title == "Buy groceries"
        assert params.description == "Milk, eggs, bread"

    def test_valid_params_without_description(self):
        """Test valid parameters with title only"""
        params = AddTaskParams(
            user_id="test-user-123",
            title="Buy groceries",
        )

        assert params.user_id == "test-user-123"
        assert params.title == "Buy groceries"
        assert params.description is None

    def test_missing_user_id_validation(self):
        """Test validation error for missing user_id"""
        with pytest.raises(ValueError):
            AddTaskParams(
                title="Buy groceries",
                description="Milk, eggs, bread",
            )

    def test_missing_title_validation(self):
        """Test validation error for missing title"""
        with pytest.raises(ValueError):
            AddTaskParams(
                user_id="test-user-123",
                description="Milk, eggs, bread",
            )

    def test_empty_title_validation(self):
        """Test validation error for empty title"""
        with pytest.raises(ValueError):
            AddTaskParams(
                user_id="test-user-123",
                title="",
                description="Milk, eggs, bread",
            )

    def test_title_max_length_validation(self):
        """Test validation error for title exceeding 200 characters"""
        long_title = "x" * 201

        with pytest.raises(ValueError):
            AddTaskParams(
                user_id="test-user-123",
                title=long_title,
            )

    def test_title_max_length_boundary(self):
        """Test valid title at maximum length (200 chars)"""
        max_title = "x" * 200
        params = AddTaskParams(
            user_id="test-user-123",
            title=max_title,
        )

        assert len(params.title) == 200

    def test_description_max_length_validation(self):
        """Test validation error for description exceeding 1000 characters"""
        long_description = "x" * 1001

        with pytest.raises(ValueError):
            AddTaskParams(
                user_id="test-user-123",
                title="Buy groceries",
                description=long_description,
            )

    def test_description_max_length_boundary(self):
        """Test valid description at maximum length (1000 chars)"""
        max_description = "x" * 1000
        params = AddTaskParams(
            user_id="test-user-123",
            title="Buy groceries",
            description=max_description,
        )

        assert len(params.description) == 1000


class TestAddTaskResponse:
    """Test add_task response structure"""

    def test_valid_response(self):
        """Test valid add_task response"""
        response = AddTaskResponse(
            task_id=123,
            status="created",
            title="Buy groceries",
            message="Task created successfully",
        )

        assert response.task_id == 123
        assert response.status == "created"
        assert response.title == "Buy groceries"
        assert response.message == "Task created successfully"

    def test_response_status_is_created(self):
        """Test that response status is always 'created'"""
        response = AddTaskResponse(
            task_id=1,
            title="Test",
        )

        assert response.status == "created"

    def test_response_message_is_success(self):
        """Test that response message is success message"""
        response = AddTaskResponse(
            task_id=1,
            title="Test",
        )

        assert response.message == "Task created successfully"


@pytest.mark.asyncio
class TestAddTaskIntegration:
    """Integration tests for add_task functionality"""

    async def test_task_creation_in_database(self, database_session, mock_user_id: str):
        """Test that created task appears in database"""
        task = Task(
            user_id=mock_user_id,
            title="Buy groceries",
            description="Milk, eggs, bread",
            completed=False,
        )

        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        # Verify task was created with correct properties
        assert task.id is not None
        assert task.title == "Buy groceries"
        assert task.user_id == mock_user_id
        assert task.completed is False
        assert task.created_at is not None

    async def test_task_isolation_by_user(self, database_session, mock_user_id: str):
        """Test that tasks are isolated by user_id"""
        user1_id = "user-1"
        user2_id = "user-2"

        task1 = Task(
            user_id=user1_id,
            title="User 1 Task",
            completed=False,
        )

        task2 = Task(
            user_id=user2_id,
            title="User 2 Task",
            completed=False,
        )

        database_session.add(task1)
        database_session.add(task2)
        await database_session.commit()

        # Query user 1 tasks
        statement1 = select(Task).where(Task.user_id == user1_id)
        result1 = await database_session.execute(statement1)
        user1_tasks = result1.scalars().all()

        # Query user 2 tasks
        statement2 = select(Task).where(Task.user_id == user2_id)
        result2 = await database_session.execute(statement2)
        user2_tasks = result2.scalars().all()

        assert len(user1_tasks) == 1
        assert len(user2_tasks) == 1
        assert user1_tasks[0].title == "User 1 Task"
        assert user2_tasks[0].title == "User 2 Task"

    async def test_timestamps_set_automatically(self, database_session, mock_user_id: str):
        """Test that created_at is set automatically"""
        task = Task(
            user_id=mock_user_id,
            title="Test Task",
            completed=False,
        )

        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        assert task.created_at is not None
        assert task.updated_at is None  # Should be None initially
