"""Backward-compatible re-export. Canonical location: src.services.task_service"""
from src.services.task_service import (  # noqa: F401
    create_task,
    get_task,
    get_task_with_tags,
    list_tasks,
    update_task,
    delete_task,
    toggle_task_completion,
)
