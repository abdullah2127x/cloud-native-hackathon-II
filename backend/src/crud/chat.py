# Task: T006 | Spec: specs/006-agent-mcp-integration/spec.md
"""CRUD functions for Conversation and Message models."""
from datetime import datetime
from typing import Optional
from sqlmodel import Session, select

from src.models.conversation import Conversation
from src.models.message import Message


def create_conversation(user_id: str, session: Session) -> Conversation:
    """Create a new conversation for the given user."""
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation


def get_conversation(
    conversation_id: int, user_id: str, session: Session
) -> Optional[Conversation]:
    """Return the conversation if it exists and belongs to user_id, else None."""
    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id,
    )
    return session.exec(statement).first()


def add_message(
    conversation_id: int,
    user_id: str,
    role: str,
    content: str,
    session: Session,
) -> Message:
    """Persist a single message and commit immediately."""
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content,
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


def get_messages(
    conversation_id: int,
    user_id: str,
    session: Session,
    limit: int = 50,
) -> list[Message]:
    """Return the last `limit` messages for the conversation, ordered oldest-first."""
    statement = (
        select(Message)
        .where(
            Message.conversation_id == conversation_id,
            Message.user_id == user_id,
        )
        .order_by(Message.created_at.asc())
        .limit(limit)
    )
    return list(session.exec(statement).all())


def update_conversation_timestamp(conversation: Conversation, session: Session) -> None:
    """Update conversation.updated_at to now and commit."""
    conversation.updated_at = datetime.utcnow()
    session.add(conversation)
    session.commit()
