"""MCP-specific error handling utilities"""

from typing import Any, Optional
from mcp.types import TextContent


class MCPToolError(Exception):
    """Base exception for MCP tool operations"""

    def __init__(self, message: str, error_code: str = "INTERNAL_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(message)

    def to_mcp_response(self) -> dict[str, Any]:
        """Convert to MCP error response"""
        return {
            "content": [{"type": "text", "text": self.message}],
            "isError": True,
        }


class ValidationError(MCPToolError):
    """Validation error in tool parameters"""

    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR")


class NotFoundError(MCPToolError):
    """Resource not found error"""

    def __init__(self, resource: str, identifier: Any):
        message = f"{resource} {identifier} not found"
        super().__init__(message, "NOT_FOUND")


class UnauthorizedError(MCPToolError):
    """User not authorized to access resource"""

    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message, "UNAUTHORIZED")


class DatabaseError(MCPToolError):
    """Database operation error"""

    def __init__(self, message: str):
        super().__init__(message, "DATABASE_ERROR")


def create_success_response(
    content_text: str, structured_content: Optional[dict[str, Any]] = None
) -> dict[str, Any]:
    """Create a successful MCP tool response

    Args:
        content_text: Text representation of the response
        structured_content: Optional structured data in the response

    Returns:
        MCP-compatible response dictionary
    """
    response = {
        "content": [{"type": "text", "text": content_text}],
        "isError": False,
    }

    if structured_content:
        response["structuredContent"] = structured_content

    return response


def create_error_response(error: MCPToolError) -> dict[str, Any]:
    """Create an error MCP tool response

    Args:
        error: MCPToolError instance

    Returns:
        MCP-compatible error response dictionary
    """
    return {
        "content": [{"type": "text", "text": error.message}],
        "isError": True,
    }
