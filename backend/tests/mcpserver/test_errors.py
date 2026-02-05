"""Tests for error handling (Phase 8 - T039)"""

import pytest
import json

from mcpserver.errors import (
    MCPToolError,
    ValidationError,
    NotFoundError,
    UnauthorizedError,
    DatabaseError,
    create_success_response,
    create_error_response,
)


class TestMCPToolError:
    """Test base MCPToolError exception"""

    def test_error_creation(self):
        """Test creating base error"""
        error = MCPToolError("Test error", "TEST_ERROR")

        assert error.message == "Test error"
        assert error.error_code == "TEST_ERROR"

    def test_error_to_mcp_response(self):
        """Test converting error to MCP response"""
        error = MCPToolError("Test error", "TEST_ERROR")
        response = error.to_mcp_response()

        assert response["isError"] is True
        assert len(response["content"]) == 1
        assert response["content"][0]["text"] == "Test error"


class TestValidationError:
    """Test ValidationError"""

    def test_validation_error_creation(self):
        """Test creating validation error"""
        error = ValidationError("Invalid input")

        assert error.message == "Invalid input"
        assert error.error_code == "VALIDATION_ERROR"

    def test_validation_error_response(self):
        """Test validation error MCP response"""
        error = ValidationError("Missing required field")
        response = error.to_mcp_response()

        assert response["isError"] is True
        assert "Missing required field" in response["content"][0]["text"]


class TestNotFoundError:
    """Test NotFoundError"""

    def test_not_found_error_creation(self):
        """Test creating not found error"""
        error = NotFoundError("Task", 123)

        assert error.message == "Task 123 not found"
        assert error.error_code == "NOT_FOUND"


class TestUnauthorizedError:
    """Test UnauthorizedError"""

    def test_unauthorized_error_creation(self):
        """Test creating unauthorized error"""
        error = UnauthorizedError("User not authorized")

        assert error.message == "User not authorized"
        assert error.error_code == "UNAUTHORIZED"

    def test_unauthorized_error_default_message(self):
        """Test unauthorized error with default message"""
        error = UnauthorizedError()

        assert error.message == "Unauthorized access"


class TestDatabaseError:
    """Test DatabaseError"""

    def test_database_error_creation(self):
        """Test creating database error"""
        error = DatabaseError("Connection failed")

        assert error.message == "Connection failed"
        assert error.error_code == "DATABASE_ERROR"


class TestSuccessResponse:
    """Test success response creation"""

    def test_success_response_without_structured_content(self):
        """Test creating success response without structured content"""
        response = create_success_response("Operation successful")

        assert response["isError"] is False
        assert len(response["content"]) == 1
        assert response["content"][0]["type"] == "text"
        assert response["content"][0]["text"] == "Operation successful"
        assert "structuredContent" not in response

    def test_success_response_with_structured_content(self):
        """Test creating success response with structured content"""
        structured = {"id": 123, "title": "Task"}
        response = create_success_response("Task created", structured)

        assert response["isError"] is False
        assert response["structuredContent"] == structured

    def test_success_response_format_compliance(self):
        """Test that success response follows MCP format"""
        response = create_success_response("Test", {"data": "value"})

        # Must have these fields
        assert "content" in response
        assert "isError" in response
        assert "structuredContent" in response

        # Content must be list with text objects
        assert isinstance(response["content"], list)
        assert all(c.get("type") == "text" for c in response["content"])


class TestErrorResponse:
    """Test error response creation"""

    def test_error_response_creation(self):
        """Test creating error response"""
        error = ValidationError("Invalid input")
        response = create_error_response(error)

        assert response["isError"] is True
        assert len(response["content"]) == 1
        assert response["content"][0]["type"] == "text"
        assert "Invalid input" in response["content"][0]["text"]

    def test_error_response_format_compliance(self):
        """Test that error response follows MCP format"""
        error = NotFoundError("Task", 999)
        response = create_error_response(error)

        # Must have these fields
        assert "content" in response
        assert "isError" in response

        # Content must be list with text objects
        assert isinstance(response["content"], list)
        assert all(c.get("type") == "text" for c in response["content"])
