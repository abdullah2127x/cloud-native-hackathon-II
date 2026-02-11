# Task: T005 | Spec: specs/006-agent-mcp-integration/spec.md
"""Pydantic schemas for the chat endpoint."""
from typing import Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    conversation_id: Optional[int] = None


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: list[str]
