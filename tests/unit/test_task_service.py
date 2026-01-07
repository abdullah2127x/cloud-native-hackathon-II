"""
Unit tests for the TaskService.
"""
import pytest
from src.services.task_service import TaskService


class TestTaskService:
    """Test cases for TaskService operations."""

    def test_add_task_creates_new_task(self):
        """Test that add_task creates a new task and returns its ID."""
        service = TaskService()

        task_id = service.add_task("Test Task", "Test Description")

        assert task_id == 1
        tasks = service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0]['id'] == 1
        assert tasks[0]['title'] == "Test Task"
        assert tasks[0]['description'] == "Test Description"
        assert tasks[0]['completed'] is False

    def test_add_task_without_description(self):
        """Test that add_task works with just a title."""
        service = TaskService()

        task_id = service.add_task("Test Task")

        assert task_id == 1
        tasks = service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0]['title'] == "Test Task"
        assert tasks[0]['description'] is None

    def test_add_task_with_empty_title_raises_error(self):
        """Test that add_task raises ValueError for empty title."""
        service = TaskService()

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.add_task("")

    def test_add_task_with_whitespace_title_raises_error(self):
        """Test that add_task raises ValueError for whitespace-only title."""
        service = TaskService()

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.add_task("   ")

    def test_add_task_with_long_description_raises_error(self):
        """Test that add_task raises ValueError for description exceeding 500 chars."""
        service = TaskService()
        long_description = "x" * 501

        with pytest.raises(ValueError, match="Task description cannot exceed 500 characters"):
            service.add_task("Test Task", long_description)

    def test_get_all_tasks_returns_all_tasks(self):
        """Test that get_all_tasks returns all tasks."""
        service = TaskService()
        service.add_task("Task 1", "Description 1")
        service.add_task("Task 2", "Description 2")
        service.add_task("Task 3")

        all_tasks = service.get_all_tasks()

        assert len(all_tasks) == 3
        assert all_tasks[0]['title'] == "Task 1"
        assert all_tasks[1]['title'] == "Task 2"
        assert all_tasks[2]['title'] == "Task 3"
        assert all_tasks[0]['description'] == "Description 1"
        assert all_tasks[1]['description'] == "Description 2"
        assert all_tasks[2]['description'] is None

    def test_get_all_tasks_returns_empty_list_when_no_tasks(self):
        """Test that get_all_tasks returns empty list when no tasks exist."""
        service = TaskService()

        all_tasks = service.get_all_tasks()

        assert all_tasks == []

    def test_get_task_by_id_returns_existing_task(self):
        """Test that get_task_by_id returns the correct task."""
        service = TaskService()
        task_id = service.add_task("Test Task", "Test Description")

        found_task = service.get_task_by_id(task_id)

        assert found_task is not None
        assert found_task['id'] == task_id
        assert found_task['title'] == "Test Task"
        assert found_task['description'] == "Test Description"
        assert found_task['completed'] is False

    def test_get_task_by_id_returns_none_for_nonexistent_task(self):
        """Test that get_task_by_id returns None for nonexistent task."""
        service = TaskService()
        service.add_task("Test Task")

        found_task = service.get_task_by_id(999)

        assert found_task is None

    def test_get_task_by_id_with_invalid_id_raises_error(self):
        """Test that get_task_by_id raises ValueError for invalid ID."""
        service = TaskService()

        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            service.get_task_by_id(-1)

        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            service.get_task_by_id(0)

        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            service.get_task_by_id("invalid")

    def test_update_task_updates_existing_task(self):
        """Test that update_task modifies an existing task."""
        service = TaskService()
        task_id = service.add_task("Old Title", "Old Description")

        success = service.update_task(task_id, "New Title", "New Description")

        assert success is True
        updated_task = service.get_task_by_id(task_id)
        assert updated_task['title'] == "New Title"
        assert updated_task['description'] == "New Description"

    def test_update_task_updates_only_provided_fields(self):
        """Test that update_task only updates provided fields."""
        service = TaskService()
        task_id = service.add_task("Old Title", "Old Description")

        success = service.update_task(task_id, title="New Title")  # Only update title

        assert success is True
        updated_task = service.get_task_by_id(task_id)
        assert updated_task['title'] == "New Title"
        assert updated_task['description'] == "Old Description"  # Should remain unchanged

    def test_update_task_returns_false_for_nonexistent_task(self):
        """Test that update_task returns False when task doesn't exist."""
        service = TaskService()
        service.add_task("Test Task")

        success = service.update_task(999, "New Title")

        assert success is False

    def test_update_task_with_invalid_id_raises_error(self):
        """Test that update_task raises ValueError for invalid ID."""
        service = TaskService()

        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            service.update_task(-1, "New Title")

        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            service.update_task(0, "New Title")

        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            service.update_task("invalid", "New Title")

    def test_update_task_with_invalid_title_raises_error(self):
        """Test that update_task raises ValueError for invalid title."""
        service = TaskService()
        task_id = service.add_task("Test Task")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.update_task(task_id, "")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.update_task(task_id, "   ")

    def test_update_task_with_long_description_raises_error(self):
        """Test that update_task raises ValueError for long description."""
        service = TaskService()
        task_id = service.add_task("Test Task")
        long_description = "x" * 501

        with pytest.raises(ValueError, match="Task description cannot exceed 500 characters"):
            service.update_task(task_id, description=long_description)

    def test_delete_task_removes_existing_task(self):
        """Test that delete_task removes an existing task."""
        service = TaskService()
        service.add_task("Task 1")
        task_id_to_delete = service.add_task("Task 2")
        service.add_task("Task 3")

        success = service.delete_task(task_id_to_delete)

        assert success is True
        all_tasks = service.get_all_tasks()
        assert len(all_tasks) == 2
        # Verify the specific task was deleted
        for task in all_tasks:
            assert task['id'] != task_id_to_delete

    def test_delete_task_returns_false_for_nonexistent_task(self):
        """Test that delete_task returns False when task doesn't exist."""
        service = TaskService()
        service.add_task("Test Task")

        success = service.delete_task(999)

        assert success is False

    def test_delete_task_with_invalid_id_raises_error(self):
        """Test that delete_task raises ValueError for invalid ID."""
        service = TaskService()

        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            service.delete_task(-1)

        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            service.delete_task(0)

        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            service.delete_task("invalid")

    def test_toggle_task_completion_toggles_status(self):
        """Test that toggle_task_completion toggles the completion status."""
        service = TaskService()
        task_id = service.add_task("Test Task")

        # Initially should be False
        task = service.get_task_by_id(task_id)
        assert task['completed'] is False

        # First toggle should make it True
        success = service.toggle_task_completion(task_id)
        assert success is True
        task = service.get_task_by_id(task_id)
        assert task['completed'] is True

        # Second toggle should make it False
        success = service.toggle_task_completion(task_id)
        assert success is True
        task = service.get_task_by_id(task_id)
        assert task['completed'] is False

    def test_toggle_task_completion_returns_false_for_nonexistent_task(self):
        """Test that toggle_task_completion returns False when task doesn't exist."""
        service = TaskService()
        service.add_task("Test Task")

        success = service.toggle_task_completion(999)

        assert success is False

    def test_toggle_task_completion_with_invalid_id_raises_error(self):
        """Test that toggle_task_completion raises ValueError for invalid ID."""
        service = TaskService()

        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            service.toggle_task_completion(-1)

        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            service.toggle_task_completion(0)

        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            service.toggle_task_completion("invalid")

    def test_get_task_count_returns_correct_count(self):
        """Test that get_task_count returns the correct number of tasks."""
        service = TaskService()

        assert service.get_task_count() == 0

        service.add_task("Task 1")
        assert service.get_task_count() == 1

        service.add_task("Task 2")
        assert service.get_task_count() == 2

    def test_get_completed_tasks_returns_only_completed_tasks(self):
        """Test that get_completed_tasks returns only completed tasks."""
        service = TaskService()
        task_id1 = service.add_task("Task 1")
        task_id2 = service.add_task("Task 2")
        task_id3 = service.add_task("Task 3")

        # Complete task 2
        service.toggle_task_completion(task_id2)

        completed_tasks = service.get_completed_tasks()

        assert len(completed_tasks) == 1
        assert completed_tasks[0]['id'] == task_id2
        assert completed_tasks[0]['completed'] is True

    def test_get_pending_tasks_returns_only_pending_tasks(self):
        """Test that get_pending_tasks returns only pending tasks."""
        service = TaskService()
        task_id1 = service.add_task("Task 1")
        task_id2 = service.add_task("Task 2")
        task_id3 = service.add_task("Task 3")

        # Complete task 2
        service.toggle_task_completion(task_id2)

        pending_tasks = service.get_pending_tasks()

        assert len(pending_tasks) == 2
        pending_task_ids = [task['id'] for task in pending_tasks]
        assert task_id1 in pending_task_ids
        assert task_id3 in pending_task_ids
        for task in pending_tasks:
            assert task['completed'] is False