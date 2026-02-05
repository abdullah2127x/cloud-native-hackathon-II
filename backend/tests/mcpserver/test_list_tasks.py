"""Tests for list_tasks tool (Phase 4 - T019)"""

import pytest
from sqlmodel import select

from src.models.task import Task
from mcpserver.schemas import ListTasksParams, ListTasksResponse, TaskItem


class TestListTasksParams:
    """Test list_tasks parameter validation"""

    def test_valid_params_with_all_status(self):
        """Test valid parameters with status='all'"""
        params = ListTasksParams(
            user_id="test-user-123",
            status="all",
        )

        assert params.user_id == "test-user-123"
        assert params.status == "all"

    def test_valid_params_with_pending_status(self):
        """Test valid parameters with status='pending'"""
        params = ListTasksParams(
            user_id="test-user-123",
            status="pending",
        )

        assert params.status == "pending"

    def test_valid_params_with_completed_status(self):
        """Test valid parameters with status='completed'"""
        params = ListTasksParams(
            user_id="test-user-123",
            status="completed",
        )

        assert params.status == "completed"

    def test_valid_params_default_status(self):
        """Test valid parameters with default status"""
        params = ListTasksParams(
            user_id="test-user-123",
        )

        assert params.status == "all"

    def test_missing_user_id_validation(self):
        """Test validation error for missing user_id"""
        with pytest.raises(ValueError):
            ListTasksParams(status="all")

    def test_empty_user_id_validation(self):
        """Test validation error for empty user_id"""
        with pytest.raises(ValueError):
            ListTasksParams(
                user_id="",
                status="all",
            )

    def test_invalid_status_validation(self):
        """Test validation error for invalid status value"""
        with pytest.raises(ValueError):
            ListTasksParams(
                user_id="test-user-123",
                status="invalid",
            )


class TestListTasksResponse:
    """Test list_tasks response structure"""

    def test_valid_response_with_tasks(self):
        """Test valid response with task list"""
        task = TaskItem(
            id=1,
            title="Test task",
            description="Description",
            completed=False,
            created_at="2026-02-05T12:00:00",
            updated_at=None,
        )

        response = ListTasksResponse(
            tasks=[task],
            count=1,
            status="success",
        )

        assert len(response.tasks) == 1
        assert response.count == 1
        assert response.status == "success"

    def test_valid_response_empty_list(self):
        """Test valid response with empty task list"""
        response = ListTasksResponse(
            tasks=[],
            count=0,
            status="success",
        )

        assert response.tasks == []
        assert response.count == 0

    def test_task_item_with_all_fields(self):
        """Test TaskItem with all fields populated"""
        task = TaskItem(
            id=123,
            title="Buy groceries",
            description="Milk, eggs, bread",
            completed=False,
            created_at="2026-02-05T10:30:00",
            updated_at="2026-02-05T11:00:00",
        )

        assert task.id == 123
        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"
        assert task.completed is False

    def test_task_item_without_description(self):
        """Test TaskItem without optional description"""
        task = TaskItem(
            id=123,
            title="Simple task",
            completed=True,
            created_at="2026-02-05T10:30:00",
        )

        assert task.description is None
        assert task.completed is True


@pytest.mark.asyncio
class TestListTasksIntegration:
    """Integration tests for list_tasks functionality"""

    async def test_list_all_tasks_for_user(self, database_session, sample_tasks):
        """Test listing all tasks for a user"""
        user_id = sample_tasks[0].user_id

        # Query all tasks for user
        statement = select(Task).where(Task.user_id == user_id)
        result = await database_session.execute(statement)
        tasks = result.scalars().all()

        assert len(tasks) >= 2
        assert all(task.user_id == user_id for task in tasks)

    async def test_list_pending_tasks_only(self, database_session, sample_tasks):
        """Test filtering to pending tasks only"""
        user_id = sample_tasks[0].user_id

        # Query pending tasks
        statement = select(Task).where(
            Task.user_id == user_id,
            Task.completed == False,
        )
        result = await database_session.execute(statement)
        tasks = result.scalars().all()

        assert len(tasks) >= 1
        assert all(task.completed is False for task in tasks)

    async def test_list_completed_tasks_only(self, database_session, sample_tasks):
        """Test filtering to completed tasks only"""
        user_id = sample_tasks[0].user_id

        # Query completed tasks
        statement = select(Task).where(
            Task.user_id == user_id,
            Task.completed == True,
        )
        result = await database_session.execute(statement)
        tasks = result.scalars().all()

        assert len(tasks) >= 1
        assert all(task.completed is True for task in tasks)

    async def test_empty_task_list_for_user(self, database_session, mock_user_id):
        """Test empty list when user has no tasks"""
        user_without_tasks = "user-with-no-tasks"

        statement = select(Task).where(Task.user_id == user_without_tasks)
        result = await database_session.execute(statement)
        tasks = result.scalars().all()

        assert len(tasks) == 0

    async def test_tasks_sorted_by_created_at_descending(
        self, database_session, mock_user_id
    ):
        """Test that tasks are returned sorted by created_at descending"""
        # Create multiple tasks
        for i in range(3):
            task = Task(
                user_id=mock_user_id,
                title=f"Task {i}",
                completed=False,
            )
            database_session.add(task)

        await database_session.commit()

        # Query tasks ordered by created_at descending
        statement = select(Task).where(Task.user_id == mock_user_id).order_by(
            Task.created_at.desc()
        )
        result = await database_session.execute(statement)
        tasks = result.scalars().all()

        # Verify descending order (at least 1 task)
        assert len(tasks) >= 1
        for i in range(len(tasks) - 1):
            # Compare timestamps - strip timezone info if present
            t1 = tasks[i].created_at.replace(tzinfo=None) if tasks[i].created_at else None
            t2 = tasks[i + 1].created_at.replace(tzinfo=None) if tasks[i + 1].created_at else None
            if t1 and t2:
                assert t1 >= t2

    async def test_user_isolation_in_list(self, database_session):
        """Test that list_tasks enforces user isolation"""
        user1_id = "user-1"
        user2_id = "user-2"

        # Create tasks for different users
        task1 = Task(user_id=user1_id, title="User 1 Task", completed=False)
        task2 = Task(user_id=user2_id, title="User 2 Task", completed=False)

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

        # User 1 should not see user 2's tasks
        assert all(t.user_id == user1_id for t in user1_tasks)
        assert all(t.user_id == user2_id for t in user2_tasks)
        assert len(user1_tasks) == 1
        assert len(user2_tasks) == 1
