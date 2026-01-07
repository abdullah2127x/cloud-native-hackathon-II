"""
Test configuration and fixtures for the todo application tests.
"""
import pytest
from src.models.task_list import TaskList


@pytest.fixture
def empty_task_list():
    """Fixture that provides an empty TaskList for testing."""
    return TaskList()


@pytest.fixture
def task_list_with_tasks():
    """Fixture that provides a TaskList with some sample tasks."""
    task_list = TaskList()
    task_list.add_task("Task 1", "Description for task 1")
    task_list.add_task("Task 2", "Description for task 2")
    task_list.add_task("Task 3")  # No description
    return task_list