# Task: T010 | Spec: specs/006-agent-mcp-integration/spec.md
"""Stateless chat endpoint — POST /api/{user_id}/chat."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.auth.dependencies import get_current_user
from src.crud.chat import (
    add_message,
    create_conversation,
    get_conversation,
    get_messages,
    update_conversation_timestamp,
)
from src.db.database import get_session
from src.schemas.chat import ChatRequest, ChatResponse
from src.agents.todo_agent import run_todo_agent

router = APIRouter(prefix="/api", tags=["chat"])

SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    body: ChatRequest,
    session: SessionDep,
    authenticated_user_id: str = Depends(get_current_user),
) -> ChatResponse:
    """Send a natural language message and receive an AI agent response."""
    # Verify JWT user matches path user_id
    if authenticated_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token user does not match path user_id",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Resolve or create conversation
    if body.conversation_id is not None:
        conversation = get_conversation(body.conversation_id, user_id, session)
        if conversation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
                headers={"code": "CONVERSATION_NOT_FOUND"},
            )
    else:
        conversation = create_conversation(user_id, session)

    # Persist user message BEFORE calling provider (critical: must survive provider failure)
    add_message(conversation.id, user_id, "user", body.message, session)

    # Load last 50 messages for agent context
    db_messages = get_messages(conversation.id, user_id, session)
    agent_messages = [{"role": m.role, "content": m.content} for m in db_messages]

    # Run agent
    try:
        response_text, tool_calls = await run_todo_agent(
            messages=agent_messages,
            user_id=user_id,
            session=session,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI provider is currently unavailable. Please try again later.",
            headers={"code": "AI_PROVIDER_UNAVAILABLE"},
        )

    # Persist assistant response
    add_message(conversation.id, user_id, "assistant", response_text, session)
    update_conversation_timestamp(conversation, session)

    return ChatResponse(
        conversation_id=conversation.id,
        response=response_text,
        tool_calls=tool_calls,
    )
