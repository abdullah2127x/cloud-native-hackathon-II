"""
Unit tests for Message model.

Task ID: T012
Spec: specs/001-chat-interface/spec.md
"""

import pytest
from datetime import datetime
from sqlmodel import Session, create_engine, SQLModel, select
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


@pytest.fixture(name="conversation")
def conversation_fixture(session: Session):
    """Create a test conversation."""
    conversation = Conversation(user_id="user-123")
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation


def test_message_creation(session: Session, conversation: Conversation):
    """Test creating a message with required fields."""
    message = Message(
        user_id="user-123",
        conversation_id=conversation.id,
        role="user",
        content="Hello, AI!"
    )

    session.add(message)
    session.commit()
    session.refresh(message)

    assert message.id is not None
    assert message.user_id == "user-123"
    assert message.conversation_id == conversation.id
    assert message.role == "user"
    assert message.content == "Hello, AI!"
    assert isinstance(message.created_at, datetime)


def test_message_foreign_key(session: Session, conversation: Conversation):
    """Test foreign key relationship to conversation."""
    message = Message(
        user_id="user-123",
        conversation_id=conversation.id,
        role="assistant",
        content="Response"
    )
    session.add(message)
    session.commit()
    session.refresh(message)

    # Verify relationship
    assert message.conversation.id == conversation.id
    assert message.conversation.user_id == "user-123"


def test_message_cascade_delete(session: Session, conversation: Conversation):
    """Test CASCADE DELETE on conversation removal."""
    # Create messages
    message1 = Message(
        user_id="user-123",
        conversation_id=conversation.id,
        role="user",
        content="Message 1"
    )
    message2 = Message(
        user_id="user-123",
        conversation_id=conversation.id,
        role="assistant",
        content="Message 2"
    )
    session.add(message1)
    session.add(message2)
    session.commit()

    message1_id = message1.id
    message2_id = message2.id

    # Delete conversation
    session.delete(conversation)
    session.commit()

    # Verify messages were deleted
    result1 = session.get(Message, message1_id)
    result2 = session.get(Message, message2_id)
    assert result1 is None
    assert result2 is None


def test_message_role_validation(session: Session, conversation: Conversation):
    """Test role validation (user or assistant)."""
    # Valid roles
    user_message = Message(
        user_id="user-123",
        conversation_id=conversation.id,
        role="user",
        content="User message"
    )
    assistant_message = Message(
        user_id="user-123",
        conversation_id=conversation.id,
        role="assistant",
        content="Assistant message"
    )

    session.add(user_message)
    session.add(assistant_message)
    session.commit()

    assert user_message.role == "user"
    assert assistant_message.role == "assistant"
