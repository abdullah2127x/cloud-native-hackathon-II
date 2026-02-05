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
