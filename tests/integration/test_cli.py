"""
Integration tests for the CLI interface.
"""
import pytest
from unittest.mock import patch, MagicMock
from src.cli.interactive_cli import InteractiveCLI
from src.services.task_service import TaskService


class TestCLIIterface:
    """Integration tests for the CLI interface."""

    @patch('src.cli.interactive_cli.inquirer.prompt')
    def test_add_task_integration(self, mock_prompt):
        """Test adding a task through the CLI interface."""
        # Mock the user selections
        mock_prompt.side_effect = [
            {'action': 'Add Task'},  # Main menu selection
            {'title': 'Test Task'},  # Task title input
            {'description': 'Test Description'},  # Task description input
            {'action': 'Exit'}  # Exit selection
        ]

        cli = InteractiveCLI()
        # We'll test that the service method is called correctly
        original_add_task = cli.service.add_task
        with patch.object(cli.service, 'add_task', wraps=original_add_task) as mock_add_task:
            cli.run()  # This will trigger the mock prompts
            # Verify that add_task was called with correct parameters
            mock_add_task.assert_called_once_with('Test Task', 'Test Description')

    @patch('src.cli.interactive_cli.inquirer.prompt')
    def test_view_tasks_integration(self, mock_prompt):
        """Test viewing tasks through the CLI interface."""
        cli = InteractiveCLI()

        # Add a test task first
        cli.service.add_task("Test Task", "Test Description")

        # Mock the user selections
        mock_prompt.side_effect = [
            {'action': 'View Tasks'},  # Main menu selection
            {'action': 'Exit'}  # Exit selection
        ]

        # Run the CLI and verify it works without errors
        cli.run()

    @patch('src.cli.interactive_cli.inquirer.prompt')
    def test_update_task_integration(self, mock_prompt):
        """Test updating a task through the CLI interface."""
        cli = InteractiveCLI()

        # Add a test task first
        task_id = cli.service.add_task("Original Task", "Original Description")

        # Test the update task functionality directly by mocking each step
        # First, mock the main menu selection
        mock_prompt.side_effect = [
            {'selected_task': f'ID: {task_id} - Original Task'},  # Select task to update
            {'title': 'Updated Task'},  # New title
            {'description': 'Updated Description'},  # New description
        ]

        # Call the update_task method directly instead of running full CLI
        cli._update_task()

        # Check that the task was updated by verifying its new values
        updated_task = cli.service.get_task_by_id(task_id)
        assert updated_task is not None
        assert updated_task['title'] == 'Updated Task'
        assert updated_task['description'] == 'Updated Description'

    @patch('src.cli.interactive_cli.inquirer.prompt')
    def test_delete_task_integration(self, mock_prompt):
        """Test deleting a task through the CLI interface."""
        cli = InteractiveCLI()

        # Add a test task first
        task_id = cli.service.add_task("Task to Delete", "Description")

        # Mock the user selections for the delete task method directly
        mock_prompt.side_effect = [
            {'selected_task': f'ID: {task_id} - Task to Delete'},  # Select task to delete
            {'confirm': True},  # Confirm deletion
        ]

        # Call the delete_task method directly instead of running full CLI
        cli._delete_task()

        # Check that the task was deleted by verifying it no longer exists
        deleted_task = cli.service.get_task_by_id(task_id)
        assert deleted_task is None

    @patch('src.cli.interactive_cli.inquirer.prompt')
    def test_toggle_task_completion_integration(self, mock_prompt):
        """Test toggling task completion through the CLI interface."""
        cli = InteractiveCLI()

        # Add a test task first
        task_id = cli.service.add_task("Toggle Task", "Description")

        # Initially task should be pending
        initial_task = cli.service.get_task_by_id(task_id)
        assert initial_task is not None
        assert initial_task['completed'] is False

        # Mock the user selections for the toggle method directly
        mock_prompt.side_effect = [
            {'selected_task': f'[○] ID: {task_id} - Toggle Task'},  # Select task to toggle
        ]

        # Call the toggle_task_completion method directly instead of running full CLI
        cli._toggle_task_completion()

        # Check that the task completion status was toggled
        toggled_task = cli.service.get_task_by_id(task_id)
        assert toggled_task is not None
        assert toggled_task['completed'] is True  # Should now be completed

    @patch('src.cli.interactive_cli.inquirer.prompt')
    def test_exit_integration(self, mock_prompt):
        """Test exiting the CLI interface."""
        mock_prompt.return_value = {'action': 'Exit'}

        cli = InteractiveCLI()
        # This should exit without errors
        cli.run()


class TestCompleteUserWorkflows:
    """Test complete user workflows across all functionality."""

    def test_complete_workflow_add_view_update_delete(self):
        """Test a complete workflow: add, view, update, delete."""
        cli = InteractiveCLI()

        # Test adding a task
        task_id = cli.service.add_task("Workflow Task", "Workflow Description")
        initial_tasks = cli.service.get_all_tasks()
        assert len(initial_tasks) == 1

        # Test viewing tasks
        tasks = cli.service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0]['title'] == 'Workflow Task'

        # Test updating task
        success = cli.service.update_task(task_id, "Updated Workflow Task", "Updated Description")
        assert success is True

        updated_task = cli.service.get_task_by_id(task_id)
        assert updated_task is not None
        assert updated_task['title'] == 'Updated Workflow Task'
        assert updated_task['description'] == 'Updated Description'

        # Test toggling completion status
        initial_completed = updated_task['completed']
        success = cli.service.toggle_task_completion(task_id)
        assert success is True

        toggled_task = cli.service.get_task_by_id(task_id)
        assert toggled_task is not None
        assert toggled_task['completed'] != initial_completed  # Should be toggled

        # Test deleting task
        success = cli.service.delete_task(task_id)
        assert success is True

        # Verify the final state
        final_tasks = cli.service.get_all_tasks()
        assert len(final_tasks) == 0  # Task should be deleted

    def test_performance_large_task_list(self):
        """Test performance with a large number of tasks."""
        cli = InteractiveCLI()

        # Add 100 tasks to test performance
        for i in range(100):
            cli.service.add_task(f"Task {i}", f"Description for task {i}")

        # Get all tasks - this should be fast (< 5 seconds as per requirements)
        import time
        start_time = time.time()
        tasks = cli.service.get_all_tasks()
        end_time = time.time()

        assert len(tasks) == 100
        assert (end_time - start_time) < 5  # Should complete in under 5 seconds

        # Test memory usage indirectly by checking task retrieval performance
        # Add more tasks and measure performance
        for i in range(100, 150):
            cli.service.add_task(f"Task {i}", f"Description for task {i}")

        start_time = time.time()
        task = cli.service.get_task_by_id(50)
        end_time = time.time()

        assert task is not None
        assert (end_time - start_time) < 5  # Individual operations should be fast