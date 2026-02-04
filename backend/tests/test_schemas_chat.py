"""
Unit tests for Pydantic chat schemas.

Task ID: T013
Spec: specs/001-chat-interface/spec.md
"""

import pytest
from datetime import datetime
from uuid import uuid4
from pydantic import ValidationError

from src.schemas.chat import ChatRequest, ChatResponse, ErrorResponse


def test_chat_request_valid():
    """Test valid ChatRequest schema."""
    request = ChatRequest(message="Hello, AI!")
    assert request.message == "Hello, AI!"
    assert request.conversation_id is None


def test_chat_request_with_conversation_id():
    """Test ChatRequest with optional conversation_id."""
    conversation_id = uuid4()
    request = ChatRequest(
        conversation_id=conversation_id,
        message="Continue conversation"
    )
    assert request.conversation_id == conversation_id
    assert request.message == "Continue conversation"


def test_chat_request_message_validation():
    """Test message field validation (min/max length)."""
    # Empty message should fail
    with pytest.raises(ValidationError) as exc_info:
        ChatRequest(message="")
    assert "String should have at least 1 character" in str(exc_info.value)

    # Message too long should fail (>4000 chars)
    with pytest.raises(ValidationError) as exc_info:
        ChatRequest(message="x" * 4001)
    assert "String should have at most 4000 characters" in str(exc_info.value)

    # Valid message at boundaries
    request_min = ChatRequest(message="x")
    assert request_min.message == "x"

    request_max = ChatRequest(message="x" * 4000)
    assert len(request_max.message) == 4000


def test_chat_request_missing_message():
    """Test that message field is required."""
    with pytest.raises(ValidationError) as exc_info:
        ChatRequest(conversation_id=uuid4())
    assert "Field required" in str(exc_info.value)


def test_chat_response_valid():
    """Test valid ChatResponse schema."""
    conversation_id = uuid4()
    created_at = datetime.utcnow()

    response = ChatResponse(
        conversation_id=conversation_id,
        message="I received your message",
        role="assistant",
        created_at=created_at
    )

    assert response.conversation_id == conversation_id
    assert response.message == "I received your message"
    assert response.role == "assistant"
    assert response.created_at == created_at


def test_chat_response_role_always_assistant():
    """Test that role is always 'assistant' in ChatResponse."""
    response = ChatResponse(
        conversation_id=uuid4(),
        message="Response",
        role="assistant",
        created_at=datetime.utcnow()
    )
    assert response.role == "assistant"


def test_chat_response_required_fields():
    """Test that all required fields are enforced."""
    with pytest.raises(ValidationError) as exc_info:
        ChatResponse(message="Response")
    assert "Field required" in str(exc_info.value)


def test_error_response_valid():
    """Test valid ErrorResponse schema."""
    error = ErrorResponse(
        error="Validation error",
        detail="Message content cannot be empty"
    )
    assert error.error == "Validation error"
    assert error.detail == "Message content cannot be empty"


def test_error_response_required_fields():
    """Test that both error and detail are required."""
    with pytest.raises(ValidationError) as exc_info:
        ErrorResponse(error="Error")
    assert "Field required" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        ErrorResponse(detail="Detail")
    assert "Field required" in str(exc_info.value)
