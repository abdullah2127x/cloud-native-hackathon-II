"""
Input validation utilities for the todo application.
"""
from typing import Optional


def validate_task_title(title: str) -> tuple[bool, str]:
    """
    Validate a task title.

    Args:
        title: The title to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if not title or not title.strip():
        return False, "Task title cannot be empty"

    if len(title) > 100:  # Reasonable limit for titles
        return False, "Task title cannot exceed 100 characters"

    return True, ""


def validate_task_description_length(description: str) -> tuple[bool, str]:
    """
    Validate the length of a task description.

    Args:
        description: The description to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if description and len(description) > 500:
        return False, "Task description cannot exceed 500 characters"

    return True, ""


def validate_duplicate_task(title: str, existing_titles: list) -> tuple[bool, str]:
    """
    Validate that a task title is not a duplicate.

    Args:
        title: The title to validate
        existing_titles: List of existing titles to check against

    Returns:
        tuple: (is_valid, error_message)
    """
    if title.lower().strip() in [t.lower().strip() for t in existing_titles]:
        return False, "Task with this title already exists"

    return True, ""


def validate_task_description(description: Optional[str]) -> tuple[bool, str]:
    """
    Validate a task description.

    Args:
        description: The description to validate (can be None)

    Returns:
        tuple: (is_valid, error_message)
    """
    if description is None:
        return True, ""

    if len(description) > 500:
        return False, "Task description cannot exceed 500 characters"

    return True, ""


def validate_task_id(task_id: int) -> tuple[bool, str]:
    """
    Validate a task ID.

    Args:
        task_id: The ID to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if not isinstance(task_id, int) or task_id <= 0:
        return False, "Task ID must be a positive integer"

    return True, ""


def is_valid_task_title(title: str) -> bool:
    """
    Check if a task title is valid.

    Args:
        title: The title to check

    Returns:
        bool: True if valid, False otherwise
    """
    is_valid, _ = validate_task_title(title)
    return is_valid


def is_valid_task_description(description: Optional[str]) -> bool:
    """
    Check if a task description is valid.

    Args:
        description: The description to check (can be None)

    Returns:
        bool: True if valid, False otherwise
    """
    is_valid, _ = validate_task_description(description)
    return is_valid


def is_valid_task_id(task_id: int) -> bool:
    """
    Check if a task ID is valid.

    Args:
        task_id: The ID to check

    Returns:
        bool: True if valid, False otherwise
    """
    is_valid, _ = validate_task_id(task_id)
    return is_valid