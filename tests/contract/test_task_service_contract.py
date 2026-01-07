"""
Contract tests for the TaskService interface.
"""
import pytest
from src.services.task_service import TaskService


class TestTaskServiceContract:
    """Contract tests for TaskService interface compliance."""

    def test_add_task_signature_and_return_type(self):
        """Test that add_task has correct signature and return type."""
        service = TaskService()

        # Should accept title and optional description
        task_id = service.add_task("Test Title", "Test Description")

        # Should return an integer ID
        assert isinstance(task_id, int)
        assert task_id > 0

        # Should work with just title
        task_id2 = service.add_task("Test Title 2")
        assert isinstance(task_id2, int)
        assert task_id2 > 0

    def test_add_task_raises_value_error_for_empty_title(self):
        """Test that add_task raises ValueError when title is empty."""
        service = TaskService()

        with pytest.raises(ValueError):
            service.add_task("")

        with pytest.raises(ValueError):
            service.add_task("   ")

    def test_get_all_tasks_return_type(self):
        """Test that get_all_tasks returns a list of task dictionaries."""
        service = TaskService()

        result = service.get_all_tasks()

        # Should return a list
        assert isinstance(result, list)

        # When empty, should return empty list
        assert result == []

        # Add a task and verify structure
        service.add_task("Test Task", "Test Description")
        result = service.get_all_tasks()

        assert len(result) == 1
        task = result[0]
        assert isinstance(task, dict)
        assert 'id' in task
        assert 'title' in task
        assert 'description' in task
        assert 'completed' in task

    def test_get_task_by_id_signature_and_return_type(self):
        """Test that get_task_by_id has correct signature and return type."""
        service = TaskService()
        task_id = service.add_task("Test Task")

        # Should accept an integer ID
        result = service.get_task_by_id(task_id)

        # Should return a task dictionary or None
        assert result is None or isinstance(result, dict)

        # Test with non-existent ID
        non_existent_result = service.get_task_by_id(999)
        assert non_existent_result is None

    def test_get_task_by_id_raises_error_for_invalid_id(self):
        """Test that get_task_by_id raises ValueError for invalid ID."""
        service = TaskService()

        with pytest.raises(ValueError):
            service.get_task_by_id(-1)

        with pytest.raises(ValueError):
            service.get_task_by_id(0)

    def test_update_task_signature_and_return_type(self):
        """Test that update_task has correct signature and return type."""
        service = TaskService()
        task_id = service.add_task("Test Task")

        # Should accept task_id and optional title/description, return boolean
        result = service.update_task(task_id, "New Title", "New Description")

        # Should return boolean
        assert isinstance(result, bool)
        assert result is True

        # Should work with partial updates
        result2 = service.update_task(task_id, title="Updated Title")
        assert isinstance(result2, bool)

        result3 = service.update_task(task_id, description="Updated Description")
        assert isinstance(result3, bool)

    def test_update_task_returns_false_for_nonexistent_task(self):
        """Test that update_task returns False for non-existent task."""
        service = TaskService()

        result = service.update_task(999, "New Title")
        assert result is False

    def test_update_task_raises_error_for_invalid_params(self):
        """Test that update_task raises ValueError for invalid parameters."""
        service = TaskService()
        task_id = service.add_task("Test Task")

        # Should raise error for empty title
        with pytest.raises(ValueError):
            service.update_task(task_id, "")

        # Should raise error for invalid ID
        with pytest.raises(ValueError):
            service.update_task(-1, "Valid Title")

    def test_delete_task_signature_and_return_type(self):
        """Test that delete_task has correct signature and return type."""
        service = TaskService()
        task_id = service.add_task("Test Task")

        # Should accept task_id, return boolean
        result = service.delete_task(task_id)

        # Should return boolean
        assert isinstance(result, bool)
        assert result is True

    def test_delete_task_returns_false_for_nonexistent_task(self):
        """Test that delete_task returns False for non-existent task."""
        service = TaskService()

        result = service.delete_task(999)
        assert result is False

    def test_delete_task_raises_error_for_invalid_id(self):
        """Test that delete_task raises ValueError for invalid ID."""
        service = TaskService()

        with pytest.raises(ValueError):
            service.delete_task(-1)

        with pytest.raises(ValueError):
            service.delete_task(0)

    def test_toggle_task_completion_signature_and_return_type(self):
        """Test that toggle_task_completion has correct signature and return type."""
        service = TaskService()
        task_id = service.add_task("Test Task")

        # Should accept task_id, return boolean
        result = service.toggle_task_completion(task_id)

        # Should return boolean
        assert isinstance(result, bool)
        assert result is True

    def test_toggle_task_completion_returns_false_for_nonexistent_task(self):
        """Test that toggle_task_completion returns False for non-existent task."""
        service = TaskService()

        result = service.toggle_task_completion(999)
        assert result is False

    def test_toggle_task_completion_raises_error_for_invalid_id(self):
        """Test that toggle_task_completion raises ValueError for invalid ID."""
        service = TaskService()

        with pytest.raises(ValueError):
            service.toggle_task_completion(-1)

        with pytest.raises(ValueError):
            service.toggle_task_completion(0)

    def test_get_task_count_signature_and_return_type(self):
        """Test that get_task_count has correct signature and return type."""
        service = TaskService()

        # Should take no params, return integer
        result = service.get_task_count()

        # Should return integer
        assert isinstance(result, int)
        assert result >= 0

        # Add tasks and verify count increases
        service.add_task("Task 1")
        assert service.get_task_count() == 1

        service.add_task("Task 2")
        assert service.get_task_count() == 2

    def test_get_completed_tasks_signature_and_return_type(self):
        """Test that get_completed_tasks has correct signature and return type."""
        service = TaskService()

        # Should take no params, return list of task dicts
        result = service.get_completed_tasks()

        # Should return a list
        assert isinstance(result, list)

        # Add tasks and mark some as complete
        task_id1 = service.add_task("Task 1")
        task_id2 = service.add_task("Task 2")

        service.toggle_task_completion(task_id1)  # Mark as complete

        completed_tasks = service.get_completed_tasks()

        assert len(completed_tasks) == 1
        assert completed_tasks[0]['id'] == task_id1
        assert completed_tasks[0]['completed'] is True

    def test_get_pending_tasks_signature_and_return_type(self):
        """Test that get_pending_tasks has correct signature and return type."""
        service = TaskService()

        # Should take no params, return list of task dicts
        result = service.get_pending_tasks()

        # Should return a list
        assert isinstance(result, list)

        # Add tasks and mark some as complete
        task_id1 = service.add_task("Task 1")
        task_id2 = service.add_task("Task 2")

        service.toggle_task_completion(task_id1)  # Mark as complete

        pending_tasks = service.get_pending_tasks()

        assert len(pending_tasks) == 1
        assert pending_tasks[0]['id'] == task_id2
        assert pending_tasks[0]['completed'] is False