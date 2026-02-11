# Task: T007 | Spec: specs/006-agent-mcp-integration/spec.md
"""Unit tests for conversation and message CRUD functions."""
import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool

from src.models.conversation import Conversation  # noqa: F401
from src.models.message import Message  # noqa: F401
from src.models.user import User  # noqa: F401
from src.models.task import Task  # noqa: F401
from src.models.tag import Tag, TaskTag  # noqa: F401
from src.crud.chat import (
    create_conversation,
    get_conversation,
    add_message,
    get_messages,
)


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


class TestCreateConversation:
    def test_creates_conversation_with_correct_user_id(self, session):
        conv = create_conversation("user-1", session)
        assert conv.id is not None
        assert conv.user_id == "user-1"
        assert conv.created_at is not None
        assert conv.updated_at is not None

    def test_two_conversations_get_different_ids(self, session):
        c1 = create_conversation("user-1", session)
        c2 = create_conversation("user-1", session)
        assert c1.id != c2.id


class TestGetConversation:
    def test_returns_conversation_for_correct_owner(self, session):
        conv = create_conversation("user-1", session)
        result = get_conversation(conv.id, "user-1", session)
        assert result is not None
        assert result.id == conv.id

    def test_returns_none_for_wrong_user_id(self, session):
        conv = create_conversation("user-1", session)
        result = get_conversation(conv.id, "user-2", session)
        assert result is None

    def test_returns_none_for_nonexistent_id(self, session):
        result = get_conversation(9999, "user-1", session)
        assert result is None


class TestAddMessage:
    def test_persists_role_and_content(self, session):
        conv = create_conversation("user-1", session)
        msg = add_message(conv.id, "user-1", "user", "Hello agent", session)
        assert msg.id is not None
        assert msg.role == "user"
        assert msg.content == "Hello agent"
        assert msg.conversation_id == conv.id
        assert msg.user_id == "user-1"

    def test_persists_assistant_role(self, session):
        conv = create_conversation("user-1", session)
        msg = add_message(conv.id, "user-1", "assistant", "Done!", session)
        assert msg.role == "assistant"


class TestGetMessages:
    def test_returns_messages_in_asc_order(self, session):
        conv = create_conversation("user-1", session)
        add_message(conv.id, "user-1", "user", "First", session)
        add_message(conv.id, "user-1", "assistant", "Second", session)
        add_message(conv.id, "user-1", "user", "Third", session)

        msgs = get_messages(conv.id, "user-1", session)
        assert len(msgs) == 3
        assert msgs[0].content == "First"
        assert msgs[2].content == "Third"

    def test_returns_max_50_messages(self, session):
        conv = create_conversation("user-1", session)
        for i in range(60):
            add_message(conv.id, "user-1", "user", f"msg {i}", session)

        msgs = get_messages(conv.id, "user-1", session, limit=50)
        assert len(msgs) == 50

    def test_returns_empty_list_for_wrong_user_id(self, session):
        conv = create_conversation("user-1", session)
        add_message(conv.id, "user-1", "user", "Hello", session)

        msgs = get_messages(conv.id, "user-2", session)
        assert msgs == []

    def test_returns_all_messages_when_fewer_than_limit(self, session):
        conv = create_conversation("user-1", session)
        add_message(conv.id, "user-1", "user", "Only one", session)

        msgs = get_messages(conv.id, "user-1", session)
        assert len(msgs) == 1
