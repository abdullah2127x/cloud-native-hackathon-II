"""MCP Server for Todo Operations

Exposes 5 CRUD tools for AI agents to create, read, update, and delete tasks.
"""

__all__ = ["create_mcp_server"]


def create_mcp_server():
    """Factory function to create MCP server instance

    Returns:
        Configured TodoMCPServer instance
    """
    from .mcp_server import create_mcp_server as _create_mcp_server
    return _create_mcp_server()
