"""
TaskService providing business logic for task operations.
"""
from typing import List, Optional, Dict
from src.models.task_list import TaskList
from src.models.task import Task
from src.lib.validators import validate_task_title, validate_task_description, validate_task_id, validate_duplicate_task


class TaskService:
    """
    Business logic layer for task operations.
    """
    def __init__(self):
        self._task_list = TaskList()

    def add_task(self, title: str, description: str = None) -> int:
        """
        Add a new task to the task list.

        Args:
            title: Task title (required, non-empty)
            description: Task description (optional, max 500 chars)

        Returns:
            int: The auto-generated ID of the new task

        Raises:
            ValueError: If title is empty or validation fails
        """
        is_valid, error_msg = validate_task_title(title)
        if not is_valid:
            raise ValueError(error_msg)

        is_valid, error_msg = validate_task_description(description)
        if not is_valid:
            raise ValueError(error_msg)

        # Check for duplicate task titles
        all_tasks = self.get_all_tasks()
        existing_titles = [task['title'] for task in all_tasks]
        is_valid, error_msg = validate_duplicate_task(title, existing_titles)
        if not is_valid:
            raise ValueError(error_msg)

        return self._task_list.add_task(title, description)

    def get_all_tasks(self) -> List[Dict]:
        """
        Retrieve all tasks in the task list.

        Returns:
            List of task dictionaries with id, title, description, completed fields
            Returns empty list if no tasks exist
        """
        tasks = self._task_list.get_all_tasks()
        return [
            {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'completed': task.completed
            }
            for task in tasks
        ]

    def get_task_by_id(self, task_id: int) -> Optional[Dict]:
        """
        Retrieve a specific task by its ID.

        Args:
            task_id: ID of task to retrieve

        Returns:
            Dict of task details if found, None if not found
        """
        is_valid, error_msg = validate_task_id(task_id)
        if not is_valid:
            raise ValueError(error_msg)

        task = self._task_list.get_task_by_id(task_id)
        if task:
            return {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'completed': task.completed
            }
        return None

    def update_task(self, task_id: int, title: str = None, description: str = None) -> bool:
        """
        Update an existing task's details.

        Args:
            task_id: ID of task to update
            title: New title if provided
            description: New description if provided

        Returns:
            bool: True if update successful, False if task not found
        """
        is_valid, error_msg = validate_task_id(task_id)
        if not is_valid:
            raise ValueError(error_msg)

        if title is not None:
            is_valid, error_msg = validate_task_title(title)
            if not is_valid:
                raise ValueError(error_msg)

        if description is not None:
            is_valid, error_msg = validate_task_description(description)
            if not is_valid:
                raise ValueError(error_msg)

        return self._task_list.update_task(task_id, title, description)

    def delete_task(self, task_id: int) -> bool:
        """
        Remove a task from the task list.

        Args:
            task_id: ID of task to delete

        Returns:
            bool: True if deletion successful, False if task not found
        """
        is_valid, error_msg = validate_task_id(task_id)
        if not is_valid:
            raise ValueError(error_msg)

        return self._task_list.delete_task(task_id)

    def toggle_task_completion(self, task_id: int) -> bool:
        """
        Toggle the completion status of a task.

        Args:
            task_id: ID of task to toggle

        Returns:
            bool: True if toggle successful, False if task not found
        """
        is_valid, error_msg = validate_task_id(task_id)
        if not is_valid:
            raise ValueError(error_msg)

        return self._task_list.toggle_task_completion(task_id)

    def get_task_count(self) -> int:
        """
        Get the total number of tasks in the list.

        Returns:
            int: Total count of tasks
        """
        return self._task_list.get_task_count()

    def get_completed_tasks(self) -> List[Dict]:
        """
        Retrieve all completed tasks.

        Returns:
            List of completed task dictionaries
        """
        completed_tasks = self._task_list.get_completed_tasks()
        return [
            {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'completed': task.completed
            }
            for task in completed_tasks
        ]

    def get_pending_tasks(self) -> List[Dict]:
        """
        Retrieve all pending tasks.

        Returns:
            List of pending task dictionaries
        """
        pending_tasks = self._task_list.get_pending_tasks()
        return [
            {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'completed': task.completed
            }
            for task in pending_tasks
        ]