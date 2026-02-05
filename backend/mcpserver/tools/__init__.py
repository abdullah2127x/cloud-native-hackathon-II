"""MCP Tools - CRUD operations for tasks

Exports all tool handlers for use by MCP server:
- add_task: Create new task
- list_tasks: Retrieve user's tasks with optional status filtering
- complete_task: Toggle task completion status
- update_task: Modify task title or description
- delete_task: Permanently delete task
"""

from .add_task import add_task
from .list_tasks import list_tasks
from .complete_task import complete_task
from .update_task import update_task
from .delete_task import delete_task

__all__ = ["add_task", "list_tasks", "complete_task", "update_task", "delete_task"]
