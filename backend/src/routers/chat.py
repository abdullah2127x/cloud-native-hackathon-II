"""
Chat API endpoints for conversational task management.

Task IDs: T101-T106
Spec: specs/001-chat-interface/spec.md
Research: specs/001-chat-interface/research.md (Task 4 - Stateless pattern)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime
import logging

from src.db.database import get_session
from src.auth.dependencies import get_current_user
from src.schemas.chat import ChatRequest, ChatResponse
from src.models.conversation import Conversation
from src.models.message import Message

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/{user_id}/chat", tags=["chat"])


@router.post("", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def send_chat_message(
    user_id: str,
    request: ChatRequest,
    authenticated_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Send a message to the chat interface and receive AI response.

    Stateless Principle: Every request fetches conversation history from database.
    No in-memory state is maintained between requests.

    Steps (T101-T106):
    1. Verify user_id matches JWT token (T101)
    2. Fetch conversation history from database if conversation_id provided (T102)
    3. Create new conversation if no conversation_id (T103)
    4. Save user message to database BEFORE AI processing (T104)
    5. Call AI agent (placeholder for now - actual AI in separate spec) (T105)
    6. Save AI response to database and return (T106)
    """

    # T101: Verify user_id matches JWT token
    if authenticated_user_id != user_id:
        logger.warning(f"User ID mismatch: JWT={authenticated_user_id}, path={user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in path does not match authenticated user"
        )

    # T102: Implement stateless conversation history fetch
    if request.conversation_id:
        # Fetch existing conversation with user_id filter for security
        conversation = session.get(Conversation, request.conversation_id)

        if not conversation or conversation.user_id != user_id:
            logger.warning(f"Conversation not found or access denied: {request.conversation_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or access denied"
            )

        logger.info(f"Continuing conversation {conversation.id} for user {user_id}")
    else:
        # T103: Create new conversation
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        logger.info(f"Created new conversation {conversation.id} for user {user_id}")

    # T104: Save user message to database BEFORE AI processing
    user_message = Message(
        user_id=user_id,
        conversation_id=conversation.id,
        role="user",
        content=request.message
    )
    session.add(user_message)
    session.commit()
    session.refresh(user_message)
    logger.info(f"Saved user message {user_message.id} to conversation {conversation.id}")

    # T105: Placeholder AI agent call
    # TODO: Replace with actual AI agent integration (separate spec)
    # For now, return a simple echo response
    ai_response_content = f"I received: {request.message}"
    logger.info(f"AI placeholder response generated for conversation {conversation.id}")

    # T106: Save AI response message to database
    assistant_message = Message(
        user_id=user_id,
        conversation_id=conversation.id,
        role="assistant",
        content=ai_response_content
    )
    session.add(assistant_message)

    # Update conversation updated_at timestamp
    conversation.updated_at = datetime.utcnow()
    session.add(conversation)

    session.commit()
    session.refresh(assistant_message)
    logger.info(f"Saved assistant message {assistant_message.id} to conversation {conversation.id}")

    # Return ChatResponse
    return ChatResponse(
        conversation_id=conversation.id,
        message=ai_response_content,
        role="assistant",
        created_at=assistant_message.created_at
    )
