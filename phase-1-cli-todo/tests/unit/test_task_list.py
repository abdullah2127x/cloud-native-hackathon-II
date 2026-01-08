"""
Unit tests for the TaskList model.
"""
import pytest
from src.models.task_list import TaskList
from src.models.task import Task


class TestTaskList:
    """Test cases for the TaskList model."""

    def test_task_list_initialization(self):
        """Test that TaskList initializes with empty tasks and next_id as 1."""
        task_list = TaskList()

        assert len(task_list.tasks) == 0
        assert task_list.next_id == 1

    def test_add_task_creates_task_with_correct_id(self):
        """Test adding a task creates it with the correct ID."""
        task_list = TaskList()

        task_id = task_list.add_task("Test Task", "Test Description")

        assert task_id == 1
        assert len(task_list.tasks) == 1
        assert task_list.tasks[0].id == 1
        assert task_list.tasks[0].title == "Test Task"
        assert task_list.tasks[0].description == "Test Description"
        assert task_list.tasks[0].completed is False

    def test_add_multiple_tasks_assigns_sequential_ids(self):
        """Test that multiple tasks get sequential IDs."""
        task_list = TaskList()

        id1 = task_list.add_task("Task 1")
        id2 = task_list.add_task("Task 2")
        id3 = task_list.add_task("Task 3")

        assert id1 == 1
        assert id2 == 2
        assert id3 == 3

        assert len(task_list.tasks) == 3
        assert task_list.tasks[0].id == 1
        assert task_list.tasks[1].id == 2
        assert task_list.tasks[2].id == 3

    def test_get_all_tasks_returns_all_tasks(self):
        """Test that get_all_tasks returns all tasks in the list."""
        task_list = TaskList()
        task_list.add_task("Task 1")
        task_list.add_task("Task 2")
        task_list.add_task("Task 3")

        all_tasks = task_list.get_all_tasks()

        assert len(all_tasks) == 3
        assert all_tasks[0].title == "Task 1"
        assert all_tasks[1].title == "Task 2"
        assert all_tasks[2].title == "Task 3"

    def test_get_all_tasks_returns_copy_not_original(self):
        """Test that get_all_tasks returns a copy of the list."""
        task_list = TaskList()
        task_list.add_task("Task 1")

        original_tasks = task_list.tasks
        returned_tasks = task_list.get_all_tasks()

        assert returned_tasks is not original_tasks
        assert returned_tasks == original_tasks

    def test_get_task_by_id_finds_existing_task(self):
        """Test that get_task_by_id returns the correct task when it exists."""
        task_list = TaskList()
        task_list.add_task("Task 1")
        task_list.add_task("Task 2")
        expected_task = task_list.add_task("Task 3")

        found_task = task_list.get_task_by_id(3)

        assert found_task is not None
        assert found_task.id == 3
        assert found_task.title == "Task 3"

    def test_get_task_by_id_returns_none_for_nonexistent_task(self):
        """Test that get_task_by_id returns None when task doesn't exist."""
        task_list = TaskList()
        task_list.add_task("Task 1")
        task_list.add_task("Task 2")

        found_task = task_list.get_task_by_id(5)

        assert found_task is None

    def test_update_task_updates_existing_task(self):
        """Test that update_task modifies an existing task."""
        task_list = TaskList()
        task_id = task_list.add_task("Old Title", "Old Description")

        success = task_list.update_task(task_id, "New Title", "New Description")

        assert success is True
        updated_task = task_list.get_task_by_id(task_id)
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"

    def test_update_task_updates_only_provided_fields(self):
        """Test that update_task only updates provided fields."""
        task_list = TaskList()
        task_id = task_list.add_task("Old Title", "Old Description")

        success = task_list.update_task(task_id, title="New Title")  # Only update title

        assert success is True
        updated_task = task_list.get_task_by_id(task_id)
        assert updated_task.title == "New Title"
        assert updated_task.description == "Old Description"  # Should remain unchanged

    def test_update_task_returns_false_for_nonexistent_task(self):
        """Test that update_task returns False when task doesn't exist."""
        task_list = TaskList()
        task_list.add_task("Task 1")

        success = task_list.update_task(999, "New Title")

        assert success is False

    def test_delete_task_removes_existing_task(self):
        """Test that delete_task removes an existing task."""
        task_list = TaskList()
        task_list.add_task("Task 1")
        task_list.add_task("Task 2")
        task_id_to_delete = task_list.add_task("Task 3")
        task_list.add_task("Task 4")

        success = task_list.delete_task(task_id_to_delete)

        assert success is True
        assert len(task_list.tasks) == 3
        assert task_list.get_task_by_id(task_id_to_delete) is None

    def test_delete_task_returns_false_for_nonexistent_task(self):
        """Test that delete_task returns False when task doesn't exist."""
        task_list = TaskList()
        task_list.add_task("Task 1")

        success = task_list.delete_task(999)

        assert success is False
        assert len(task_list.tasks) == 1

    def test_toggle_task_completion_toggles_status(self):
        """Test that toggle_task_completion toggles the completion status."""
        task_list = TaskList()
        task_id = task_list.add_task("Task 1")

        # Initially should be False
        task = task_list.get_task_by_id(task_id)
        assert task.completed is False

        # First toggle should make it True
        success = task_list.toggle_task_completion(task_id)
        assert success is True
        task = task_list.get_task_by_id(task_id)
        assert task.completed is True

        # Second toggle should make it False
        success = task_list.toggle_task_completion(task_id)
        assert success is True
        task = task_list.get_task_by_id(task_id)
        assert task.completed is False

    def test_toggle_task_completion_returns_false_for_nonexistent_task(self):
        """Test that toggle_task_completion returns False when task doesn't exist."""
        task_list = TaskList()
        task_list.add_task("Task 1")

        success = task_list.toggle_task_completion(999)

        assert success is False

    def test_get_task_count_returns_correct_count(self):
        """Test that get_task_count returns the correct number of tasks."""
        task_list = TaskList()

        assert task_list.get_task_count() == 0

        task_list.add_task("Task 1")
        assert task_list.get_task_count() == 1

        task_list.add_task("Task 2")
        assert task_list.get_task_count() == 2

    def test_get_completed_tasks_returns_only_completed_tasks(self):
        """Test that get_completed_tasks returns only completed tasks."""
        task_list = TaskList()
        task_id1 = task_list.add_task("Task 1")
        task_id2 = task_list.add_task("Task 2")
        task_id3 = task_list.add_task("Task 3")

        # Complete task 2
        task_list.toggle_task_completion(task_id2)

        completed_tasks = task_list.get_completed_tasks()

        assert len(completed_tasks) == 1
        assert completed_tasks[0].id == task_id2
        assert completed_tasks[0].completed is True

    def test_get_pending_tasks_returns_only_pending_tasks(self):
        """Test that get_pending_tasks returns only pending tasks."""
        task_list = TaskList()
        task_id1 = task_list.add_task("Task 1")
        task_id2 = task_list.add_task("Task 2")
        task_id3 = task_list.add_task("Task 3")

        # Complete task 2
        task_list.toggle_task_completion(task_id2)

        pending_tasks = task_list.get_pending_tasks()

        assert len(pending_tasks) == 2
        pending_task_ids = [task.id for task in pending_tasks]
        assert task_id1 in pending_task_ids
        assert task_id3 in pending_task_ids
        for task in pending_tasks:
            assert task.completed is False