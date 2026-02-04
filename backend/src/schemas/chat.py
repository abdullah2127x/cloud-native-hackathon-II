"""
Pydantic schemas for chat interface API.

Task IDs: T008, T009, T010
Spec: specs/001-chat-interface/spec.md
Contract: specs/001-chat-interface/contracts/chat-api.yaml
"""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Request schema for chat endpoint.

    Fields:
        - conversation_id: Optional UUID to continue existing conversation
        - message: User message content (1-4000 chars)
    """
    conversation_id: UUID | None = Field(None, description="Optional conversation ID to continue existing conversation")
    message: str = Field(..., min_length=1, max_length=4000, description="User message content")


class ChatResponse(BaseModel):
    """
    Response schema for chat endpoint.

    Fields:
        - conversation_id: Conversation ID (new or existing)
        - message: AI assistant response
        - role: Always "assistant"
        - created_at: ISO 8601 timestamp of message creation
    """
    conversation_id: UUID = Field(..., description="Conversation ID (new or existing)")
    message: str = Field(..., description="AI assistant response")
    role: Literal["assistant"] = Field("assistant", description="Always 'assistant' for chat responses")
    created_at: datetime = Field(..., description="ISO 8601 timestamp of message creation")

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    """
    Error response schema.

    Fields:
        - error: Error category
        - detail: Human-readable error message
    """
    error: str = Field(..., description="Error category")
    detail: str = Field(..., description="Human-readable error message")
