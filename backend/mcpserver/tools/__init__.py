"""MCP Tools - CRUD operations for tasks

Exports all tool handlers for use by MCP server:
- add_task: Create new task
- list_tasks: Retrieve user's tasks with optional status filtering
- complete_task: Toggle task completion status
- update_task: Modify task title or description
- delete_task: Permanently delete task
"""

from .add_task import add_task

__all__ = ["add_task"]
