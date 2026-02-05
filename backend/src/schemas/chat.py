"""
Pydantic schemas for chat interface API.

Task IDs: T008, T009, T010, T201-T206
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


class MessageSchema(BaseModel):
    """
    Message schema for conversation detail response.

    Fields:
        - id: Message UUID
        - role: Either "user" or "assistant"
        - content: Message text
        - created_at: ISO 8601 timestamp of message creation
    """
    id: UUID = Field(..., description="Message UUID")
    role: str = Field(..., description="Either 'user' or 'assistant'")
    content: str = Field(..., description="Message text")
    created_at: datetime = Field(..., description="ISO 8601 timestamp of message creation")

    class Config:
        from_attributes = True


class ConversationSummary(BaseModel):
    """
    Conversation summary schema for list response (no messages).

    Fields:
        - id: Conversation UUID
        - created_at: ISO 8601 timestamp of conversation creation
        - updated_at: ISO 8601 timestamp of last update
    """
    id: UUID = Field(..., description="Conversation UUID")
    created_at: datetime = Field(..., description="ISO 8601 timestamp of conversation creation")
    updated_at: datetime = Field(..., description="ISO 8601 timestamp of last update")

    class Config:
        from_attributes = True


class ConversationList(BaseModel):
    """
    Response schema for conversation list endpoint.

    Fields:
        - conversations: Array of conversation summaries (no messages)
        - total: Total number of conversations for this user
        - limit: Maximum conversations per page
        - offset: Number of conversations skipped
    """
    conversations: list[ConversationSummary] = Field(..., description="Array of conversation summaries")
    total: int = Field(..., description="Total number of conversations for this user")
    limit: int = Field(..., description="Maximum conversations per page")
    offset: int = Field(..., description="Number of conversations skipped")


class ConversationDetail(BaseModel):
    """
    Response schema for conversation detail endpoint.

    Fields:
        - id: Conversation UUID
        - created_at: ISO 8601 timestamp of conversation creation
        - updated_at: ISO 8601 timestamp of last update
        - messages: Array of messages ordered by created_at
    """
    id: UUID = Field(..., description="Conversation UUID")
    created_at: datetime = Field(..., description="ISO 8601 timestamp of conversation creation")
    updated_at: datetime = Field(..., description="ISO 8601 timestamp of last update")
    messages: list[MessageSchema] = Field(..., description="Array of messages ordered by created_at")

    class Config:
        from_attributes = True
