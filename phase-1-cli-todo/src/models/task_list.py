"""
TaskList model representing a collection of tasks with in-memory storage.
"""
from typing import List, Optional
from .task import Task


class TaskList:
    """
    Represents a collection of tasks with in-memory storage and auto-incrementing IDs.
    """
    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id: int = 1

    def add_task(self, title: str, description: Optional[str] = None) -> int:
        """
        Add a new task to the list with auto-generated ID.

        Args:
            title: Task title
            description: Optional task description (max 500 chars)

        Returns:
            int: The ID of the newly created task
        """
        task = Task(id=self.next_id, title=title, description=description)
        self.tasks.append(task)
        task_id = self.next_id
        self.next_id += 1
        return task_id

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks in the list."""
        return self.tasks.copy()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get a specific task by its ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: str = None, description: str = None) -> bool:
        """
        Update an existing task's details.

        Args:
            task_id: ID of the task to update
            title: New title if provided
            description: New description if provided

        Returns:
            bool: True if update was successful, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description

        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: ID of the task to delete

        Returns:
            bool: True if deletion was successful, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        self.tasks.remove(task)
        return True

    def toggle_task_completion(self, task_id: int) -> bool:
        """
        Toggle the completion status of a task.

        Args:
            task_id: ID of the task to toggle

        Returns:
            bool: True if toggle was successful, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        task.completed = not task.completed
        return True

    def get_task_count(self) -> int:
        """Get the total number of tasks."""
        return len(self.tasks)

    def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks."""
        return [task for task in self.tasks if task.completed]

    def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks."""
        return [task for task in self.tasks if not task.completed]