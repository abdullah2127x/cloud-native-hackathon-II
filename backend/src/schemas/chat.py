"""Pydantic schemas for Chat API requests/responses (per spec)."""
from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    """Chat request schema.

    Per spec:
    - conversation_id: optional (creates new if not provided)
    - message: required (user's natural language message)
    """
    conversation_id: Optional[str] = Field(
        default=None,
        description="Existing conversation ID (creates new if not provided)"
    )
    message: str = Field(
        ...,
        min_length=1,
        description="User's natural language message"
    )


class ToolCallInfo(BaseModel):
    """Info about an MCP tool that was invoked."""
    tool_name: str
    arguments: dict = Field(default_factory=dict)
    result: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response schema.

    Per spec:
    - conversation_id: the conversation ID
    - response: AI assistant's response
    - tool_calls: list of MCP tools invoked
    """
    conversation_id: str = Field(description="The conversation ID")
    response: str = Field(description="AI assistant's response")
    # tool_calls: list[ToolCallInfo] = Field(
    #     default_factory=list,
    #     description="List of MCP tools invoked"
    # )
