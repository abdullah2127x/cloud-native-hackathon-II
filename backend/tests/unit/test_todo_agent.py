# Task: T007b | Spec: specs/006-agent-mcp-integration/spec.md
"""Unit tests for todo_agent tool functions (TDD — written before T008 implementation)."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


def _make_wrapper(user_id: str = "user-1", session=None):
    """Create a minimal RunContextWrapper mock with context."""
    ctx = MagicMock()
    ctx.user_id = user_id
    ctx.session = session or MagicMock()
    wrapper = MagicMock()
    wrapper.context = ctx
    return wrapper


class TestAddTaskTool:
    @pytest.mark.asyncio
    async def test_returns_created_task_string_on_success(self):
        success_response = {
            "isError": False,
            "content": [{"type": "text", "text": "Task 'Buy milk' created successfully"}],
            "structuredContent": {"task_id": 1, "title": "Buy milk", "operation": "create"},
        }
        with patch("src.agents.todo_agent.mcp_server") as mock_server:
            mock_server.call_tool = AsyncMock(return_value=success_response)
            from src.agents.todo_agent import add_task
            result = await add_task(wrapper=_make_wrapper(), title="Buy milk")
        assert "Buy milk" in result
        assert "1" in result

    @pytest.mark.asyncio
    async def test_returns_error_text_on_is_error(self):
        error_response = {
            "isError": True,
            "content": [{"type": "text", "text": "Validation error: title too long"}],
        }
        with patch("src.agents.todo_agent.mcp_server") as mock_server:
            mock_server.call_tool = AsyncMock(return_value=error_response)
            from src.agents.todo_agent import add_task
            result = await add_task(wrapper=_make_wrapper(), title="x" * 300)
        assert "Validation error" in result


class TestListTasksTool:
    @pytest.mark.asyncio
    async def test_returns_tasks_string_on_success(self):
        success_response = {
            "isError": False,
            "content": [{"type": "text", "text": "Found 1 task(s)"}],
            "structuredContent": {"tasks": [{"id": 1, "title": "Buy milk", "completed": False}], "total": 1},
        }
        with patch("src.agents.todo_agent.mcp_server") as mock_server:
            mock_server.call_tool = AsyncMock(return_value=success_response)
            from src.agents.todo_agent import list_tasks
            result = await list_tasks(wrapper=_make_wrapper(), status="all")
        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_returns_error_text_on_is_error(self):
        error_response = {
            "isError": True,
            "content": [{"type": "text", "text": "Invalid status filter"}],
        }
        with patch("src.agents.todo_agent.mcp_server") as mock_server:
            mock_server.call_tool = AsyncMock(return_value=error_response)
            from src.agents.todo_agent import list_tasks
            result = await list_tasks(wrapper=_make_wrapper(), status="invalid")
        assert "Invalid status filter" in result


class TestCompleteTaskTool:
    @pytest.mark.asyncio
    async def test_returns_completion_confirmation_on_success(self):
        success_response = {
            "isError": False,
            "content": [{"type": "text", "text": "Task toggled successfully"}],
            "structuredContent": {"task_id": 5, "title": "Buy milk", "completed": True},
        }
        with patch("src.agents.todo_agent.mcp_server") as mock_server:
            mock_server.call_tool = AsyncMock(return_value=success_response)
            from src.agents.todo_agent import complete_task
            result = await complete_task(wrapper=_make_wrapper(), task_id=5)
        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_returns_error_text_on_is_error(self):
        error_response = {
            "isError": True,
            "content": [{"type": "text", "text": "Task not found"}],
        }
        with patch("src.agents.todo_agent.mcp_server") as mock_server:
            mock_server.call_tool = AsyncMock(return_value=error_response)
            from src.agents.todo_agent import complete_task
            result = await complete_task(wrapper=_make_wrapper(), task_id=999)
        assert "Task not found" in result


class TestDeleteTaskTool:
    @pytest.mark.asyncio
    async def test_returns_deletion_confirmation_on_success(self):
        success_response = {
            "isError": False,
            "content": [{"type": "text", "text": "Task deleted successfully"}],
            "structuredContent": {"task_id": 3, "title": "Old task"},
        }
        with patch("src.agents.todo_agent.mcp_server") as mock_server:
            mock_server.call_tool = AsyncMock(return_value=success_response)
            from src.agents.todo_agent import delete_task
            result = await delete_task(wrapper=_make_wrapper(), task_id=3)
        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_returns_error_text_on_is_error(self):
        error_response = {
            "isError": True,
            "content": [{"type": "text", "text": "Task not found"}],
        }
        with patch("src.agents.todo_agent.mcp_server") as mock_server:
            mock_server.call_tool = AsyncMock(return_value=error_response)
            from src.agents.todo_agent import delete_task
            result = await delete_task(wrapper=_make_wrapper(), task_id=999)
        assert "Task not found" in result


class TestUpdateTaskTool:
    @pytest.mark.asyncio
    async def test_returns_update_confirmation_on_success(self):
        success_response = {
            "isError": False,
            "content": [{"type": "text", "text": "Task updated successfully"}],
            "structuredContent": {"task_id": 2, "title": "New title"},
        }
        with patch("src.agents.todo_agent.mcp_server") as mock_server:
            mock_server.call_tool = AsyncMock(return_value=success_response)
            from src.agents.todo_agent import update_task
            result = await update_task(wrapper=_make_wrapper(), task_id=2, title="New title")
        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_returns_error_text_on_is_error(self):
        error_response = {
            "isError": True,
            "content": [{"type": "text", "text": "Task not found"}],
        }
        with patch("src.agents.todo_agent.mcp_server") as mock_server:
            mock_server.call_tool = AsyncMock(return_value=error_response)
            from src.agents.todo_agent import update_task
            result = await update_task(wrapper=_make_wrapper(), task_id=999, title="x")
        assert "Task not found" in result
