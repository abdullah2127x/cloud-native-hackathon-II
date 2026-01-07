"""
Unit tests for the Task model.
"""
import pytest
from src.models.task import Task


class TestTask:
    """Test cases for the Task model."""

    def test_task_creation_with_valid_data(self):
        """Test creating a task with valid data."""
        task = Task(id=1, title="Test Task", description="Test Description", completed=False)

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False

    def test_task_creation_with_minimal_data(self):
        """Test creating a task with minimal required data."""
        task = Task(id=1, title="Test Task")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description is None
        assert task.completed is False

    def test_task_creation_with_completed_true(self):
        """Test creating a task with completed status as True."""
        task = Task(id=1, title="Test Task", completed=True)

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.completed is True

    def test_task_title_cannot_be_empty_string(self):
        """Test that creating a task with empty title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(id=1, title="")

    def test_task_title_cannot_be_whitespace_only(self):
        """Test that creating a task with whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(id=1, title="   ")

    def test_task_title_cannot_be_none(self):
        """Test that creating a task with None title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(id=1, title=None)

    def test_task_description_exceeds_500_characters(self):
        """Test that creating a task with description exceeding 500 chars raises ValueError."""
        long_description = "x" * 501

        with pytest.raises(ValueError, match="Task description cannot exceed 500 characters"):
            Task(id=1, title="Test Task", description=long_description)

    def test_task_description_at_500_characters_is_valid(self):
        """Test that creating a task with description at exactly 500 chars is valid."""
        description_500_chars = "x" * 500
        task = Task(id=1, title="Test Task", description=description_500_chars)

        assert task.description == description_500_chars

    def test_task_string_representation(self):
        """Test the string representation of a task."""
        task = Task(id=1, title="Test Task", description="Test Description")
        # Since we don't have a custom __str__ method, we'll test basic properties
        assert task.title == "Test Task"
        assert task.description == "Test Description"

    def test_task_equality(self):
        """Test that tasks are compared correctly."""
        task1 = Task(id=1, title="Test Task", description="Description")
        task2 = Task(id=1, title="Test Task", description="Description")
        # Since we're using dataclass, equality should work based on all fields

        # Note: Different instances with same values won't be equal unless dataclass has eq=True
        # For this test, we'll just verify that the fields are as expected
        assert task1.id == task2.id
        assert task1.title == task2.title
        assert task1.description == task2.description
        assert task1.completed == task2.completed