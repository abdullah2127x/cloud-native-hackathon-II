"""
Chat API endpoints for conversational task management.

Task IDs: T101-T106, T201-T210
Spec: specs/001-chat-interface/spec.md
Research: specs/001-chat-interface/research.md (Task 4 - Stateless pattern)
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, func
from sqlalchemy.orm import selectinload
from datetime import datetime
import logging

from src.db.database import get_session
from src.auth.dependencies import get_current_user
from src.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ConversationList,
    ConversationDetail,
    ConversationSummary,
    MessageSchema,
)
from src.models.conversation import Conversation
from src.models.message import Message

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/{user_id}", tags=["chat"])


@router.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
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


@router.get("/conversations", response_model=ConversationList, status_code=status.HTTP_200_OK)
async def list_conversations(
    user_id: str,
    authenticated_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session),
    limit: int = Query(20, ge=1, le=100, description="Maximum conversations per page"),
    offset: int = Query(0, ge=0, description="Number of conversations to skip"),
):
    """
    List all conversations for authenticated user with pagination.

    Stateless Principle: Every request fetches from database.
    No messages are loaded (only conversation metadata).

    Steps (T201-T203):
    1. Verify user_id matches JWT token (T201)
    2. Fetch conversations WHERE user_id = authenticated user, ORDER BY updated_at DESC (T202)
    3. Return ConversationList schema with total count, limit, offset (T203)
    """

    # T201: Verify user_id matches JWT token
    if authenticated_user_id != user_id:
        logger.warning(f"User ID mismatch: JWT={authenticated_user_id}, path={user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in path does not match authenticated user"
        )

    # T202: Fetch conversations WHERE user_id = authenticated user, ORDER BY updated_at DESC
    # Count total conversations for this user
    count_statement = select(func.count()).select_from(Conversation).where(
        Conversation.user_id == user_id
    )
    total = session.exec(count_statement).one()

    # Fetch paginated conversations (no messages loaded)
    statement = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .limit(limit)
        .offset(offset)
    )
    conversations = session.exec(statement).all()

    logger.info(f"Fetched {len(conversations)} conversations for user {user_id} (total: {total})")

    # T203: Return ConversationList schema
    return ConversationList(
        conversations=[
            ConversationSummary(
                id=conv.id,
                created_at=conv.created_at,
                updated_at=conv.updated_at
            )
            for conv in conversations
        ],
        total=total,
        limit=limit,
        offset=offset
    )


@router.get("/conversations/{conversation_id}", response_model=ConversationDetail, status_code=status.HTTP_200_OK)
async def get_conversation_detail(
    user_id: str,
    conversation_id: str,
    authenticated_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Get conversation detail with all messages.

    Stateless Principle: Every request fetches from database with eager loading.

    Steps (T204-T206):
    1. Verify user_id matches JWT token (T204)
    2. Fetch conversation with selectinload(messages), filter by user_id, return 404 if not found (T205)
    3. Return ConversationDetail schema with messages ordered by created_at (T206)
    """
    from uuid import UUID

    # T204: Verify user_id matches JWT token
    if authenticated_user_id != user_id:
        logger.warning(f"User ID mismatch: JWT={authenticated_user_id}, path={user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in path does not match authenticated user"
        )

    # Convert string conversation_id to UUID
    try:
        conv_id_uuid = UUID(conversation_id)
    except ValueError:
        logger.warning(f"Invalid conversation ID format: {conversation_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied"
        )

    # T205: Fetch conversation with selectinload(messages), filter by user_id
    statement = (
        select(Conversation)
        .where(Conversation.id == conv_id_uuid, Conversation.user_id == user_id)
        .options(selectinload(Conversation.messages))
    )
    conversation = session.exec(statement).first()

    if not conversation:
        logger.warning(f"Conversation not found or access denied: {conversation_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied"
        )

    logger.info(f"Fetched conversation {conversation_id} with {len(conversation.messages)} messages")

    # T206: Return ConversationDetail schema with messages ordered by created_at
    return ConversationDetail(
        id=conversation.id,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        messages=[
            MessageSchema(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at
            )
            for msg in sorted(conversation.messages, key=lambda m: m.created_at)
        ]
    )
