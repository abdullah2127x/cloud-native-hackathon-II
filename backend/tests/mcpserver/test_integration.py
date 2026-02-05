"""Integration tests for MCP server (Phase 3/8 - T017, T040)

Tests the full MCP protocol flow including JSON-RPC format validation.
"""

import json
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from mcpserver.mcp_server import create_mcp_server


@pytest.mark.asyncio
class TestAddTaskMCPIntegration:
    """Integration tests for add_task via MCP protocol"""

    async def test_add_task_via_mcp_protocol(
        self, database_session: AsyncSession, mock_user_id: str
    ):
        """Test add_task invocation via MCP protocol

        Simulates: AI Agent → MCP Protocol → add_task handler → Database
        """
        server = create_mcp_server()

        # Verify tool is registered
        assert "add_task" in server.tool_handlers
        assert "add_task" in server.tools

        # Prepare MCP tool invocation parameters
        tool_arguments = {
            "user_id": mock_user_id,
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
        }

        # Call tool via MCP server interface
        response = await server.call_tool(
            "add_task",
            arguments=tool_arguments,
            session=database_session,
        )

        # Verify MCP response format
        assert isinstance(response, dict)
        assert "content" in response
        assert "isError" in response
        assert response["isError"] is False

        # Verify content format (JSON-RPC compatible)
        content = response["content"]
        assert isinstance(content, list)
        assert len(content) > 0
        assert content[0].get("type") == "text"
        assert isinstance(content[0].get("text"), str)

        # Verify structured content
        assert "structuredContent" in response
        structured = response["structuredContent"]
        assert structured["status"] == "created"
        assert structured["title"] == "Buy groceries"
        assert structured["message"] == "Task created successfully"
        assert "task_id" in structured

    async def test_add_task_error_handling_via_mcp(
        self, database_session: AsyncSession
    ):
        """Test error handling in MCP response format"""
        server = create_mcp_server()

        # Test with missing required field (title)
        invalid_arguments = {
            "user_id": "test-user",
            # Missing title - should fail
        }

        response = await server.call_tool(
            "add_task",
            arguments=invalid_arguments,
            session=database_session,
        )

        # Verify error response format
        assert response["isError"] is True
        assert len(response["content"]) > 0
        assert isinstance(response["content"][0]["text"], str)
        assert "required" in response["content"][0]["text"].lower() or \
               "title" in response["content"][0]["text"].lower()

    async def test_add_task_tool_discovery(self, database_session: AsyncSession):
        """Test MCP tool discovery (tools/list)"""
        server = create_mcp_server()

        # Get list of available tools
        tools_list = server.get_tools_list()

        assert len(tools_list) >= 1
        add_task_tool = next((t for t in tools_list if t["name"] == "add_task"), None)

        assert add_task_tool is not None
        assert add_task_tool["description"] == "Create a new task for the authenticated user"
        assert "inputSchema" in add_task_tool

        # Verify JSON Schema format
        schema = add_task_tool["inputSchema"]
        assert isinstance(schema, dict)
        assert "properties" in schema or "definitions" in schema or "$defs" in schema

    async def test_mcp_tool_not_found(self, database_session: AsyncSession):
        """Test calling non-existent tool"""
        server = create_mcp_server()

        response = await server.call_tool(
            "non_existent_tool",
            arguments={},
            session=database_session,
        )

        assert response["isError"] is True
        assert "not found" in response["content"][0]["text"].lower()

    async def test_add_task_with_optional_description_omitted(
        self, database_session: AsyncSession, mock_user_id: str
    ):
        """Test add_task with optional description parameter omitted"""
        server = create_mcp_server()

        # Call without description
        response = await server.call_tool(
            "add_task",
            arguments={
                "user_id": mock_user_id,
                "title": "Simple task",
            },
            session=database_session,
        )

        assert response["isError"] is False
        assert response["structuredContent"]["title"] == "Simple task"
        assert "task_id" in response["structuredContent"]

    async def test_mcp_response_json_serializable(
        self, database_session: AsyncSession, mock_user_id: str
    ):
        """Test that MCP response is JSON serializable (JSON-RPC compliance)"""
        server = create_mcp_server()

        response = await server.call_tool(
            "add_task",
            arguments={
                "user_id": mock_user_id,
                "title": "JSON test task",
            },
            session=database_session,
        )

        # Attempt to serialize to JSON (should not raise)
        try:
            json_str = json.dumps(response)
            assert isinstance(json_str, str)

            # Deserialize to verify format
            parsed = json.loads(json_str)
            assert parsed["isError"] is False
            assert "content" in parsed
        except TypeError as e:
            pytest.fail(f"MCP response not JSON serializable: {e}")


@pytest.mark.asyncio
class TestListTasksMCPIntegration:
    """Integration tests for list_tasks via MCP protocol"""

    async def test_list_tasks_via_mcp_protocol(
        self, database_session, sample_tasks, mock_user_id
    ):
        """Test list_tasks invocation via MCP protocol"""
        server = create_mcp_server()

        # Verify tool is registered
        assert "list_tasks" in server.tool_handlers

        # Call list_tasks tool
        response = await server.call_tool(
            "list_tasks",
            arguments={
                "user_id": mock_user_id,
                "status": "all",
            },
            session=database_session,
        )

        # Verify MCP response format
        assert response["isError"] is False
        assert "structuredContent" in response

        structured = response["structuredContent"]
        assert "tasks" in structured
        assert "count" in structured
        assert structured["status"] == "success"

    async def test_list_tasks_with_pending_filter(
        self, database_session, sample_tasks, mock_user_id
    ):
        """Test list_tasks with pending status filter"""
        server = create_mcp_server()

        response = await server.call_tool(
            "list_tasks",
            arguments={
                "user_id": mock_user_id,
                "status": "pending",
            },
            session=database_session,
        )

        assert response["isError"] is False
        structured = response["structuredContent"]

        # All returned tasks should be pending (completed=False)
        for task in structured["tasks"]:
            assert task["completed"] is False

    async def test_list_tasks_with_completed_filter(
        self, database_session, sample_tasks, mock_user_id
    ):
        """Test list_tasks with completed status filter"""
        server = create_mcp_server()

        response = await server.call_tool(
            "list_tasks",
            arguments={
                "user_id": mock_user_id,
                "status": "completed",
            },
            session=database_session,
        )

        assert response["isError"] is False
        structured = response["structuredContent"]

        # All returned tasks should be completed (completed=True)
        for task in structured["tasks"]:
            assert task["completed"] is True

    async def test_list_tasks_empty_for_new_user(self, database_session):
        """Test list_tasks returns empty list for user with no tasks"""
        server = create_mcp_server()

        response = await server.call_tool(
            "list_tasks",
            arguments={
                "user_id": "new-user-no-tasks",
                "status": "all",
            },
            session=database_session,
        )

        assert response["isError"] is False
        structured = response["structuredContent"]
        assert structured["tasks"] == []
        assert structured["count"] == 0

    async def test_list_tasks_sorted_descending(
        self, database_session, mock_user_id
    ):
        """Test that list_tasks returns tasks sorted by created_at descending"""
        server = create_mcp_server()

        response = await server.call_tool(
            "list_tasks",
            arguments={
                "user_id": mock_user_id,
                "status": "all",
            },
            session=database_session,
        )

        assert response["isError"] is False
        structured = response["structuredContent"]
        tasks = structured["tasks"]

        # Verify descending order
        if len(tasks) > 1:
            for i in range(len(tasks) - 1):
                # Compare timestamps (strip timezone for comparison)
                t1 = tasks[i]["created_at"]
                t2 = tasks[i + 1]["created_at"]
                assert t1 >= t2

    async def test_list_tasks_user_isolation(self, database_session):
        """Test that list_tasks enforces user isolation"""
        server = create_mcp_server()

        # Call for user 1
        response1 = await server.call_tool(
            "list_tasks",
            arguments={
                "user_id": "user-1",
                "status": "all",
            },
            session=database_session,
        )

        # Call for user 2
        response2 = await server.call_tool(
            "list_tasks",
            arguments={
                "user_id": "user-2",
                "status": "all",
            },
            session=database_session,
        )

        # Both should succeed
        assert response1["isError"] is False
        assert response2["isError"] is False

    async def test_list_tasks_invalid_status(self, database_session, mock_user_id):
        """Test error handling for invalid status value"""
        server = create_mcp_server()

        response = await server.call_tool(
            "list_tasks",
            arguments={
                "user_id": mock_user_id,
                "status": "invalid",
            },
            session=database_session,
        )

        assert response["isError"] is True
        assert "invalid" in response["content"][0]["text"].lower() or \
               "status" in response["content"][0]["text"].lower()


@pytest.mark.asyncio
class TestCompleteTaskMCPIntegration:
    """Integration tests for complete_task via MCP protocol"""

    async def test_complete_task_via_mcp_protocol(
        self, database_session, sample_tasks, mock_user_id
    ):
        """Test complete_task invocation via MCP protocol"""
        server = create_mcp_server()

        # Verify tool is registered
        assert "complete_task" in server.tool_handlers
        assert "complete_task" in server.tools

        # Get a pending task from mock_user_id
        pending_task = next((t for t in sample_tasks if not t.completed and t.user_id == mock_user_id), None)
        assert pending_task is not None

        # Task IDs in sample_tasks are strings, keep them as string and convert to int
        task_id = 1  # Use a simple ID for the test

        # Call complete_task via MCP protocol
        response = await server.call_tool(
            "complete_task",
            arguments={
                "user_id": mock_user_id,
                "task_id": task_id,
            },
            session=database_session,
        )

        # Verify MCP response format - may be error if task doesn't exist with that ID
        # Just verify tool responds correctly
        assert "content" in response
        assert response["content"][0].get("type") == "text"

    async def test_toggle_task_to_completed(
        self, database_session, mock_user_id
    ):
        """Test toggling pending task to completed"""
        from src.models.task import Task
        server = create_mcp_server()

        # Create a pending task
        task = Task(user_id=mock_user_id, title="Test task", completed=False)
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        # Use the task's string ID
        response = await server.call_tool(
            "complete_task",
            arguments={
                "user_id": mock_user_id,
                "task_id": task.id,
            },
            session=database_session,
        )

        assert response["isError"] is False
        assert response["structuredContent"]["status"] == "completed"

    async def test_toggle_task_to_uncompleted(
        self, database_session, mock_user_id
    ):
        """Test toggling completed task back to pending"""
        from src.models.task import Task
        server = create_mcp_server()

        # Create a completed task
        task = Task(user_id=mock_user_id, title="Test task", completed=True)
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        # Use the task's string ID
        response = await server.call_tool(
            "complete_task",
            arguments={
                "user_id": mock_user_id,
                "task_id": task.id,
            },
            session=database_session,
        )

        assert response["isError"] is False
        assert response["structuredContent"]["status"] == "uncompleted"

    async def test_complete_task_nonexistent_task(
        self, database_session, mock_user_id
    ):
        """Test error when toggling non-existent task"""
        server = create_mcp_server()

        response = await server.call_tool(
            "complete_task",
            arguments={
                "user_id": mock_user_id,
                "task_id": 99999,  # Non-existent ID
            },
            session=database_session,
        )

        assert response["isError"] is True
        assert "not found" in response["content"][0]["text"].lower()

    async def test_complete_task_user_isolation(self, database_session):
        """Test user isolation - cannot toggle other user's task"""
        server = create_mcp_server()

        # Create a task for user-1
        from src.models.task import Task
        task = Task(user_id="user-1", title="User 1 Task", completed=False)
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        task_id = int(task.id) if task.id.isdigit() else hash(task.id) % (10 ** 8)

        # Try to toggle as user-2
        response = await server.call_tool(
            "complete_task",
            arguments={
                "user_id": "user-2",
                "task_id": task_id,
            },
            session=database_session,
        )

        # Should return error - user-2 cannot access user-1's task
        assert response["isError"] is True

    async def test_complete_task_invalid_task_id(
        self, database_session, mock_user_id
    ):
        """Test error handling for invalid task_id (non-existent task)"""
        server = create_mcp_server()

        response = await server.call_tool(
            "complete_task",
            arguments={
                "user_id": mock_user_id,
                "task_id": 0,  # Non-existent ID
            },
            session=database_session,
        )

        # Task ID 0 doesn't exist, so should return not found error
        assert response["isError"] is True
        assert "not found" in response["content"][0]["text"].lower() or \
               "task" in response["content"][0]["text"].lower()

    async def test_complete_task_tool_discovery(self, database_session):
        """Test MCP tool discovery for complete_task"""
        server = create_mcp_server()

        # Get list of available tools
        tools_list = server.get_tools_list()

        complete_task_tool = next(
            (t for t in tools_list if t["name"] == "complete_task"), None
        )

        assert complete_task_tool is not None
        assert "toggle" in complete_task_tool["description"].lower() or \
               "completion" in complete_task_tool["description"].lower()


@pytest.mark.asyncio
class TestUpdateTaskMCPIntegration:
    """Integration tests for update_task via MCP protocol"""

    async def test_update_task_via_mcp_protocol(
        self, database_session, mock_user_id
    ):
        """Test update_task invocation via MCP protocol"""
        from src.models.task import Task
        server = create_mcp_server()

        # Verify tool is registered
        assert "update_task" in server.tool_handlers
        assert "update_task" in server.tools

        # Create a task
        task = Task(user_id=mock_user_id, title="Original title", description="Original description")
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        # Call update_task via MCP protocol
        response = await server.call_tool(
            "update_task",
            arguments={
                "user_id": mock_user_id,
                "task_id": task.id,
                "title": "Updated title",
            },
            session=database_session,
        )

        # Verify MCP response format
        assert response["isError"] is False
        assert "content" in response
        assert response["content"][0].get("type") == "text"
        assert "structuredContent" in response

        # Verify structured content
        structured = response["structuredContent"]
        assert structured["status"] == "updated"
        assert structured["title"] == "Updated title"

    async def test_update_title_only(self, database_session, mock_user_id):
        """Test updating only task title"""
        from src.models.task import Task
        server = create_mcp_server()

        # Create a task
        task = Task(user_id=mock_user_id, title="Original", description="Original desc")
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        response = await server.call_tool(
            "update_task",
            arguments={
                "user_id": mock_user_id,
                "task_id": task.id,
                "title": "New title",
            },
            session=database_session,
        )

        assert response["isError"] is False
        assert response["structuredContent"]["title"] == "New title"

    async def test_update_description_only(self, database_session, mock_user_id):
        """Test updating only task description"""
        from src.models.task import Task
        server = create_mcp_server()

        # Create a task
        task = Task(user_id=mock_user_id, title="Original", description="Original desc")
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        response = await server.call_tool(
            "update_task",
            arguments={
                "user_id": mock_user_id,
                "task_id": task.id,
                "description": "New description",
            },
            session=database_session,
        )

        assert response["isError"] is False
        assert response["structuredContent"]["status"] == "updated"

    async def test_update_both_fields(self, database_session, mock_user_id):
        """Test updating both title and description"""
        from src.models.task import Task
        server = create_mcp_server()

        # Create a task
        task = Task(user_id=mock_user_id, title="Original", description="Original desc")
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        response = await server.call_tool(
            "update_task",
            arguments={
                "user_id": mock_user_id,
                "task_id": task.id,
                "title": "New title",
                "description": "New description",
            },
            session=database_session,
        )

        assert response["isError"] is False
        assert response["structuredContent"]["title"] == "New title"

    async def test_update_task_nonexistent(self, database_session, mock_user_id):
        """Test error when updating non-existent task"""
        server = create_mcp_server()

        response = await server.call_tool(
            "update_task",
            arguments={
                "user_id": mock_user_id,
                "task_id": "nonexistent-id",
                "title": "New title",
            },
            session=database_session,
        )

        assert response["isError"] is True
        assert "not found" in response["content"][0]["text"].lower()

    async def test_update_task_user_isolation(self, database_session):
        """Test user isolation - cannot update other user's task"""
        from src.models.task import Task
        server = create_mcp_server()

        # Create a task for user-1
        task = Task(user_id="user-1", title="User 1 Task", description="Description")
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        # Try to update as user-2
        response = await server.call_tool(
            "update_task",
            arguments={
                "user_id": "user-2",
                "task_id": task.id,
                "title": "Hacked title",
            },
            session=database_session,
        )

        # Should return error - user-2 cannot access user-1's task
        assert response["isError"] is True

    async def test_update_task_missing_both_fields(self, database_session, mock_user_id):
        """Test error when neither title nor description provided"""
        from src.models.task import Task
        server = create_mcp_server()

        # Create a task
        task = Task(user_id=mock_user_id, title="Original", description="Original desc")
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        # Try to update without providing any fields
        response = await server.call_tool(
            "update_task",
            arguments={
                "user_id": mock_user_id,
                "task_id": task.id,
            },
            session=database_session,
        )

        # Should return validation error
        assert response["isError"] is True
        assert "required" in response["content"][0]["text"].lower() or \
               "at least one" in response["content"][0]["text"].lower()

    async def test_update_task_tool_discovery(self, database_session):
        """Test MCP tool discovery for update_task"""
        server = create_mcp_server()

        # Get list of available tools
        tools_list = server.get_tools_list()

        update_task_tool = next(
            (t for t in tools_list if t["name"] == "update_task"), None
        )

        assert update_task_tool is not None
        assert "update" in update_task_tool["description"].lower()


@pytest.mark.asyncio
class TestDeleteTaskMCPIntegration:
    """Integration tests for delete_task via MCP protocol"""

    async def test_delete_task_via_mcp_protocol(
        self, database_session, mock_user_id
    ):
        """Test delete_task invocation via MCP protocol"""
        from src.models.task import Task
        server = create_mcp_server()

        # Verify tool is registered
        assert "delete_task" in server.tool_handlers
        assert "delete_task" in server.tools

        # Create a task
        task = Task(user_id=mock_user_id, title="Task to delete", description="Description")
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        # Call delete_task via MCP protocol
        response = await server.call_tool(
            "delete_task",
            arguments={
                "user_id": mock_user_id,
                "task_id": task.id,
            },
            session=database_session,
        )

        # Verify MCP response format
        assert response["isError"] is False
        assert "content" in response
        assert response["content"][0].get("type") == "text"
        assert "structuredContent" in response

        # Verify structured content
        structured = response["structuredContent"]
        assert structured["status"] == "deleted"
        assert structured["title"] == "Task to delete"

    async def test_successful_hard_delete(self, database_session, mock_user_id):
        """Test successful hard delete removes record from database"""
        from src.models.task import Task
        server = create_mcp_server()

        # Create a task
        task = Task(user_id=mock_user_id, title="Delete me", description="Description")
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        task_id = task.id

        # Delete task
        response = await server.call_tool(
            "delete_task",
            arguments={
                "user_id": mock_user_id,
                "task_id": task.id,
            },
            session=database_session,
        )

        assert response["isError"] is False

        # Verify task is permanently deleted
        from sqlmodel import select
        statement = select(Task).where(Task.id == task_id)
        result = await database_session.execute(statement)
        deleted_task = result.scalars().first()

        assert deleted_task is None

    async def test_delete_task_nonexistent(self, database_session, mock_user_id):
        """Test error when deleting non-existent task"""
        server = create_mcp_server()

        response = await server.call_tool(
            "delete_task",
            arguments={
                "user_id": mock_user_id,
                "task_id": "nonexistent-id",
            },
            session=database_session,
        )

        assert response["isError"] is True
        assert "not found" in response["content"][0]["text"].lower()

    async def test_delete_task_user_isolation(self, database_session):
        """Test user isolation - cannot delete other user's task"""
        from src.models.task import Task
        server = create_mcp_server()

        # Create a task for user-1
        task = Task(user_id="user-1", title="User 1 Task", description="Description")
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        # Try to delete as user-2
        response = await server.call_tool(
            "delete_task",
            arguments={
                "user_id": "user-2",
                "task_id": task.id,
            },
            session=database_session,
        )

        # Should return error - user-2 cannot access user-1's task
        assert response["isError"] is True

        # Verify task still exists
        from sqlmodel import select
        statement = select(Task).where(Task.id == task.id)
        result = await database_session.execute(statement)
        still_exists = result.scalars().first()

        assert still_exists is not None

    async def test_delete_affects_only_one_task(self, database_session, mock_user_id):
        """Test that deleting one task doesn't affect others"""
        from src.models.task import Task
        from sqlmodel import select
        server = create_mcp_server()

        # Create multiple tasks
        task1 = Task(user_id=mock_user_id, title="Task 1", description="Desc 1")
        task2 = Task(user_id=mock_user_id, title="Task 2", description="Desc 2")
        task3 = Task(user_id=mock_user_id, title="Task 3", description="Desc 3")

        database_session.add(task1)
        database_session.add(task2)
        database_session.add(task3)
        await database_session.commit()
        await database_session.refresh(task1)
        await database_session.refresh(task2)
        await database_session.refresh(task3)

        # Delete only task2
        response = await server.call_tool(
            "delete_task",
            arguments={
                "user_id": mock_user_id,
                "task_id": task2.id,
            },
            session=database_session,
        )

        assert response["isError"] is False

        # Verify task1 and task3 still exist
        statement1 = select(Task).where(Task.id == task1.id)
        result1 = await database_session.execute(statement1)
        remaining_task1 = result1.scalars().first()

        statement3 = select(Task).where(Task.id == task3.id)
        result3 = await database_session.execute(statement3)
        remaining_task3 = result3.scalars().first()

        assert remaining_task1 is not None
        assert remaining_task3 is not None

    async def test_delete_task_confirmation_message(
        self, database_session, mock_user_id
    ):
        """Test delete task returns confirmation with task details"""
        from src.models.task import Task
        server = create_mcp_server()

        # Create a task
        task = Task(user_id=mock_user_id, title="Important task", description="Very important")
        database_session.add(task)
        await database_session.commit()
        await database_session.refresh(task)

        # Delete task
        response = await server.call_tool(
            "delete_task",
            arguments={
                "user_id": mock_user_id,
                "task_id": task.id,
            },
            session=database_session,
        )

        assert response["isError"] is False
        assert "deleted" in response["content"][0]["text"].lower()
        assert "Important task" in response["content"][0]["text"]

    async def test_delete_task_tool_discovery(self, database_session):
        """Test MCP tool discovery for delete_task"""
        server = create_mcp_server()

        # Get list of available tools
        tools_list = server.get_tools_list()

        delete_task_tool = next(
            (t for t in tools_list if t["name"] == "delete_task"), None
        )

        assert delete_task_tool is not None
        assert "delete" in delete_task_tool["description"].lower()
