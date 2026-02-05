"""
Unit tests for Conversation model.

Task ID: T011
Spec: specs/001-chat-interface/spec.md
"""

import pytest
from datetime import datetime
from uuid import uuid4
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.pool import StaticPool

from src.models.conversation import Conversation
from src.models.message import Message


@pytest.fixture(name="session")
def session_fixture():
    """Create in-memory database for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_conversation_creation(session: Session):
    """Test creating a conversation with required fields."""
    user_id = "user-123"
    conversation = Conversation(user_id=user_id)

    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    assert conversation.id is not None
    assert conversation.user_id == user_id
    assert isinstance(conversation.created_at, datetime)
    assert isinstance(conversation.updated_at, datetime)


def test_conversation_relationships(session: Session):
    """Test conversation-message relationship with CASCADE delete."""
    user_id = "user-123"
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    # Add messages to conversation
    message1 = Message(
        user_id=user_id,
        conversation_id=conversation.id,
        role="user",
        content="Hello"
    )
    message2 = Message(
        user_id=user_id,
        conversation_id=conversation.id,
        role="assistant",
        content="Hi there!"
    )
    session.add(message1)
    session.add(message2)
    session.commit()

    # Verify messages are linked
    session.refresh(conversation)
    assert len(conversation.messages) == 2
    assert conversation.messages[0].content in ["Hello", "Hi there!"]

    # Test CASCADE delete
    session.delete(conversation)
    session.commit()

    # Messages should be deleted automatically
    remaining_messages = session.query(Message).filter(
        Message.conversation_id == conversation.id
    ).all()
    assert len(remaining_messages) == 0


def test_conversation_timestamps(session: Session):
    """Test that timestamps are set correctly."""
    conversation = Conversation(user_id="user-123")
    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    created = conversation.created_at
    updated = conversation.updated_at

    assert created is not None
    assert updated is not None
    assert created == updated  # Initially same
