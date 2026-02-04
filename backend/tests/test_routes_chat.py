"""
Integration tests for chat API endpoints.

Task IDs: T107-T112
Spec: specs/001-chat-interface/spec.md
"""

import pytest
from uuid import uuid4
from fastapi.testclient import TestClient
from unittest.mock import patch
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.pool import StaticPool

from src.main import app
from src.db.database import get_session
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


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create test client with dependency override."""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="mock_auth")
def mock_auth_fixture():
    """Mock JWT authentication."""
    with patch('src.auth.dependencies.get_current_user') as mock:
        mock.return_value = "user-123"
        yield mock


# T107: Test 200 with conversation_id on successful request
def test_send_message_success(client: TestClient, mock_auth, session: Session):
    """Test successful message send and AI response."""
    response = client.post(
        "/api/user-123/chat",
        json={"message": "Hello, AI!"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "conversation_id" in data
    assert data["message"] == "I received: Hello, AI!"
    assert data["role"] == "assistant"
    assert "created_at" in data


# T108: Test 401 without valid JWT token
def test_send_message_unauthorized(client: TestClient):
    """Test that endpoint returns 401 without valid JWT."""
    # Remove auth mock to simulate no token
    response = client.post(
        "/api/user-123/chat",
        json={"message": "Hello"}
    )

    assert response.status_code == 401


# T109: Test 403 if user_id doesn't match JWT user_id
def test_send_message_forbidden(client: TestClient, mock_auth):
    """Test that endpoint returns 403 when user_id doesn't match JWT."""
    mock_auth.return_value = "user-123"

    response = client.post(
        "/api/user-456/chat",  # Different user_id
        json={"message": "Hello"}
    )

    assert response.status_code == 403
    assert "does not match" in response.json()["detail"].lower()


# T110: Test 404 if conversation_id not found or not owned by user
def test_send_message_conversation_not_found(client: TestClient, mock_auth):
    """Test that endpoint returns 404 for non-existent conversation."""
    fake_conversation_id = str(uuid4())

    response = client.post(
        "/api/user-123/chat",
        json={
            "conversation_id": fake_conversation_id,
            "message": "Hello"
        }
    )

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


# T111: Test verify user and assistant messages saved to database
def test_messages_saved_to_database(client: TestClient, mock_auth, session: Session):
    """Test that both user and assistant messages are saved to database."""
    response = client.post(
        "/api/user-123/chat",
        json={"message": "Test message"}
    )

    assert response.status_code == 200
    data = response.json()
    conversation_id = data["conversation_id"]

    # Query database for messages
    from sqlmodel import select
    statement = select(Message).where(Message.conversation_id == conversation_id)
    messages = session.exec(statement).all()

    assert len(messages) == 2  # User message + Assistant message

    user_message = [m for m in messages if m.role == "user"][0]
    assistant_message = [m for m in messages if m.role == "assistant"][0]

    assert user_message.content == "Test message"
    assert assistant_message.content == "I received: Test message"
    assert user_message.user_id == "user-123"
    assert assistant_message.user_id == "user-123"


# T112: Test verify stateless behavior (conversation history fetched from DB on each request)
def test_stateless_behavior(client: TestClient, mock_auth, session: Session):
    """Test that conversation history is fetched from database on each request."""
    # First request - create conversation
    response1 = client.post(
        "/api/user-123/chat",
        json={"message": "First message"}
    )
    assert response1.status_code == 200
    conversation_id = response1.json()["conversation_id"]

    # Second request - continue conversation (stateless: fetches from DB)
    response2 = client.post(
        "/api/user-123/chat",
        json={
            "conversation_id": conversation_id,
            "message": "Second message"
        }
    )
    assert response2.status_code == 200
    assert response2.json()["conversation_id"] == conversation_id

    # Verify all messages are in database (stateless proof)
    from sqlmodel import select
    statement = select(Message).where(Message.conversation_id == conversation_id)
    messages = session.exec(statement).all()

    assert len(messages) == 4  # 2 user + 2 assistant messages
    user_messages = [m for m in messages if m.role == "user"]
    assert len(user_messages) == 2
    assert user_messages[0].content == "First message"
    assert user_messages[1].content == "Second message"
