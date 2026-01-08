"""
Task model representing a single todo item.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """
    Represents a single todo task with id, title, description, and completion status.
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    def __post_init__(self):
        """Validate the task after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")

        if self.description and len(self.description) > 500:
            raise ValueError("Task description cannot exceed 500 characters")