"""Main MCP Server for Todo Operations

Initializes FastMCP server with stateless HTTP configuration and registers tools.
"""

import json
import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from mcp.server import Server
from mcp.types import Tool

from .logging_config import configure_logging
from .tools import add_task
from .schemas import AddTaskParams

logger = logging.getLogger(__name__)


class TodoMCPServer:
    """MCP Server for Todo operations

    Exposes 5 CRUD tools for AI agents:
    - add_task: Create new task
    - list_tasks: Retrieve user's tasks
    - complete_task: Toggle task completion
    - update_task: Modify task details
    - delete_task: Delete task
    """

    def __init__(self):
        """Initialize MCP server"""
        # Configure structured logging
        configure_logging()

        # Initialize MCP server
        self.server = Server("todo-mcp")
        self.tools: dict[str, Any] = {}
        self.tool_handlers: dict[str, Any] = {}

        # Register all tools
        self._register_tools()

        logger.info("MCP Server initialized")

    def _register_tools(self) -> None:
        """Register all available tools"""
        # Register add_task tool
        self.register_tool(
            name="add_task",
            description="Create a new task for the authenticated user",
            input_schema=AddTaskParams.model_json_schema(),
            handler=add_task,
        )

    async def initialize_lifespan(self) -> AsyncGenerator[None, None]:
        """Lifespan context manager for server startup/shutdown

        Sets up database connections and other resources.
        """
        logger.info("MCP Server starting up")

        # TODO: Initialize database connection pool
        # TODO: Load configuration
        # TODO: Set up resources

        yield

        logger.info("MCP Server shutting down")
        # TODO: Close database connections
        # TODO: Cleanup resources

    def register_tool(
        self,
        name: str,
        description: str,
        input_schema: dict[str, Any],
        handler: Any,
    ) -> None:
        """Register a tool with the MCP server

        Args:
            name: Tool name (e.g., "add_task")
            description: Tool description
            input_schema: JSON Schema for tool parameters
            handler: Async function to handle tool invocation
        """
        logger.info(f"Registering tool: {name}")

        # Store tool info
        self.tools[name] = {
            "name": name,
            "description": description,
            "inputSchema": input_schema,
        }

        # Store handler for invocation
        self.tool_handlers[name] = handler

    async def call_tool(
        self, name: str, arguments: dict[str, Any], session: Any = None
    ) -> dict[str, Any]:
        """Call a registered tool

        Args:
            name: Tool name
            arguments: Tool parameters
            session: Optional database session

        Returns:
            Tool response

        Raises:
            ValueError: If tool not found
        """
        if name not in self.tool_handlers:
            raise ValueError(f"Tool '{name}' not found")

        logger.info(f"Calling tool: {name} with arguments: {arguments}")

        try:
            # Call tool handler with session
            handler = self.tool_handlers[name]
            response = await handler(**arguments, session=session)
            return response
        except Exception as e:
            logger.error(f"Error calling tool {name}: {str(e)}", exc_info=True)
            return {
                "content": [{"type": "text", "text": f"Error calling tool: {str(e)}"}],
                "isError": True,
            }

    def get_tools_list(self) -> list[Tool]:
        """Get list of available tools

        Returns:
            List of Tool objects with schemas
        """
        return list(self.tools.values())


def create_mcp_server() -> TodoMCPServer:
    """Factory function to create MCP server instance

    Returns:
        Configured TodoMCPServer instance
    """
    return TodoMCPServer()
