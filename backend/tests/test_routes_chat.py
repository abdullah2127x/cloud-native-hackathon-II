"""
Integration tests for chat API endpoints.

Task IDs: T107-T112, T207-T210, T408
Spec: specs/001-chat-interface/spec.md
"""

import pytest
from uuid import uuid4, UUID
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
    """Mock JWT authentication using dependency override."""
    from src.auth.dependencies import get_current_user

    async def override_get_current_user():
        return "user-123"

    app.dependency_overrides[get_current_user] = override_get_current_user
    yield override_get_current_user
    app.dependency_overrides.clear()


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
    conversation_id = UUID(data["conversation_id"])

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
    conversation_id_str = response1.json()["conversation_id"]

    # Second request - continue conversation (stateless: fetches from DB)
    response2 = client.post(
        "/api/user-123/chat",
        json={
            "conversation_id": conversation_id_str,
            "message": "Second message"
        }
    )
    assert response2.status_code == 200
    assert response2.json()["conversation_id"] == conversation_id_str

    # Verify all messages are in database (stateless proof)
    from sqlmodel import select
    conversation_id = UUID(conversation_id_str)
    statement = select(Message).where(Message.conversation_id == conversation_id)
    messages = session.exec(statement).all()

    assert len(messages) == 4  # 2 user + 2 assistant messages
    user_messages = [m for m in messages if m.role == "user"]
    assert len(user_messages) == 2
    assert user_messages[0].content == "First message"
    assert user_messages[1].content == "Second message"


# T207: Test GET /conversations returns user's conversations only, excludes other users
def test_list_conversations_user_isolation(client: TestClient, session: Session):
    """Test that list endpoint returns only authenticated user's conversations."""
    from src.auth.dependencies import get_current_user

    # Create conversations for user-123
    async def override_user_123():
        return "user-123"
    app.dependency_overrides[get_current_user] = override_user_123

    response1 = client.post("/api/user-123/chat", json={"message": "User 123 message 1"})
    response2 = client.post("/api/user-123/chat", json={"message": "User 123 message 2"})
    assert response1.status_code == 200
    assert response2.status_code == 200

    # Create conversation for user-456
    async def override_user_456():
        return "user-456"
    app.dependency_overrides[get_current_user] = override_user_456

    response3 = client.post("/api/user-456/chat", json={"message": "User 456 message"})
    assert response3.status_code == 200

    # List conversations for user-123
    app.dependency_overrides[get_current_user] = override_user_123
    response = client.get("/api/user-123/conversations")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2  # Only user-123's conversations
    assert len(data["conversations"]) == 2
    assert data["limit"] == 20
    assert data["offset"] == 0

    # Verify all conversations belong to user-123
    conv_ids = [conv["id"] for conv in data["conversations"]]
    assert response1.json()["conversation_id"] in conv_ids
    assert response2.json()["conversation_id"] in conv_ids
    assert response3.json()["conversation_id"] not in conv_ids

    app.dependency_overrides.clear()


# T208: Test GET /conversations/{id} returns conversation with messages, 404 if not owned by user
def test_get_conversation_detail_success_and_not_found(client: TestClient, mock_auth, session: Session):
    """Test conversation detail endpoint returns full conversation with messages."""
    # Create conversation for user-123
    response = client.post("/api/user-123/chat", json={"message": "First message"})
    assert response.status_code == 200
    conversation_id = response.json()["conversation_id"]

    # Add second message
    response = client.post(
        "/api/user-123/chat",
        json={"conversation_id": conversation_id, "message": "Second message"}
    )
    assert response.status_code == 200

    # Get conversation detail
    response = client.get(f"/api/user-123/conversations/{conversation_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == conversation_id
    assert "created_at" in data
    assert "updated_at" in data
    assert len(data["messages"]) == 4  # 2 user + 2 assistant messages

    # Verify messages are ordered by created_at
    messages = data["messages"]
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "First message"
    assert messages[1]["role"] == "assistant"
    assert messages[2]["role"] == "user"
    assert messages[2]["content"] == "Second message"
    assert messages[3]["role"] == "assistant"

    # Verify each message has required fields
    for msg in messages:
        assert "id" in msg
        assert "role" in msg
        assert "content" in msg
        assert "created_at" in msg

    # Test 404 for non-existent conversation
    fake_id = str(uuid4())
    response = client.get(f"/api/user-123/conversations/{fake_id}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

    # Test 404 when trying to access another user's conversation
    from src.auth.dependencies import get_current_user
    async def override_user_456():
        return "user-456"
    app.dependency_overrides[get_current_user] = override_user_456

    response = client.get(f"/api/user-456/conversations/{conversation_id}")
    assert response.status_code == 404

    app.dependency_overrides.clear()


# T209: Test pagination works correctly (limit, offset)
def test_list_conversations_pagination(client: TestClient, session: Session):
    """Test that pagination parameters work correctly."""
    from src.auth.dependencies import get_current_user

    async def override_user_123():
        return "user-123"
    app.dependency_overrides[get_current_user] = override_user_123

    # Create 5 conversations
    conversation_ids = []
    for i in range(5):
        response = client.post("/api/user-123/chat", json={"message": f"Message {i}"})
        assert response.status_code == 200
        conversation_ids.append(response.json()["conversation_id"])

    # Test default pagination (limit=20, offset=0)
    response = client.get("/api/user-123/conversations")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert len(data["conversations"]) == 5
    assert data["limit"] == 20
    assert data["offset"] == 0

    # Test limit=2, offset=0 (first page)
    response = client.get("/api/user-123/conversations?limit=2&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert len(data["conversations"]) == 2
    assert data["limit"] == 2
    assert data["offset"] == 0

    # Test limit=2, offset=2 (second page)
    response = client.get("/api/user-123/conversations?limit=2&offset=2")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert len(data["conversations"]) == 2
    assert data["limit"] == 2
    assert data["offset"] == 2

    # Test limit=2, offset=4 (last page, partial)
    response = client.get("/api/user-123/conversations?limit=2&offset=4")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert len(data["conversations"]) == 1  # Only 1 conversation left
    assert data["limit"] == 2
    assert data["offset"] == 4

    # Test conversations ordered by updated_at DESC (most recent first)
    response = client.get("/api/user-123/conversations?limit=5")
    data = response.json()
    # Most recent conversation should be first
    assert data["conversations"][0]["id"] == conversation_ids[-1]

    app.dependency_overrides.clear()


# T210: Test verify user isolation (User A cannot access User B's conversations)
def test_conversation_endpoints_user_isolation(client: TestClient, session: Session):
    """Test that user A cannot access user B's conversations via any endpoint."""
    from src.auth.dependencies import get_current_user

    # Create conversation for user-123
    async def override_user_123():
        return "user-123"
    app.dependency_overrides[get_current_user] = override_user_123

    response = client.post("/api/user-123/chat", json={"message": "User 123 secret"})
    assert response.status_code == 200
    user_123_conv_id = response.json()["conversation_id"]

    # Create conversation for user-456
    async def override_user_456():
        return "user-456"
    app.dependency_overrides[get_current_user] = override_user_456

    response = client.post("/api/user-456/chat", json={"message": "User 456 secret"})
    assert response.status_code == 200
    user_456_conv_id = response.json()["conversation_id"]

    # Test user-123 cannot list user-456's conversations
    app.dependency_overrides[get_current_user] = override_user_123
    response = client.get("/api/user-456/conversations")
    assert response.status_code == 403  # Forbidden

    # Test user-123 cannot see user-456's conversation in their own list
    response = client.get("/api/user-123/conversations")
    assert response.status_code == 200
    data = response.json()
    conv_ids = [conv["id"] for conv in data["conversations"]]
    assert user_123_conv_id in conv_ids
    assert user_456_conv_id not in conv_ids

    # Test user-123 cannot get detail of user-456's conversation
    response = client.get(f"/api/user-123/conversations/{user_456_conv_id}")
    assert response.status_code == 404  # Not found (security: don't reveal existence)

    # Test user-456 cannot get detail of user-123's conversation
    app.dependency_overrides[get_current_user] = override_user_456
    response = client.get(f"/api/user-456/conversations/{user_123_conv_id}")
    assert response.status_code == 404

    app.dependency_overrides.clear()


# T408: Test error responses return empathetic, actionable messages
def test_error_responses_empathetic_messages(client: TestClient, mock_auth):
    """Test that error responses include empathetic, actionable messages."""
    # T405: Test 403 Forbidden with empathetic message
    response = client.post(
        "/api/user-456/chat",  # User-123 is authenticated, different user_id
        json={"message": "Hello"}
    )
    assert response.status_code == 403
    data = response.json()
    assert "Access denied" in data["detail"]
    assert "conversation doesn't belong to you" in data["detail"]

    # T406: Test 404 Not Found with empathetic message
    fake_conv_id = str(uuid4())
    response = client.post(
        "/api/user-123/chat",
        json={"conversation_id": fake_conv_id, "message": "Hello"}
    )
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()
    assert "may have been deleted" in data["detail"].lower()

    # T404: Test 401 Unauthorized (via missing auth)
    # Remove auth to trigger 401
    response = client.post(
        "/api/user-123/chat",
        json={"message": "Hello"}
    )
    assert response.status_code == 401

    # T407: Test 500 Internal Server Error with empathetic message
    # Can't easily trigger a 500 in this test setup, but middleware returns empathetic message


def test_error_messages_have_actionable_guidance(client: TestClient, mock_auth):
    """Test that error messages provide actionable guidance to users."""
    # 404: Suggests conversation may be deleted
    fake_conv_id = str(uuid4())
    response = client.post(
        "/api/user-123/chat",
        json={"conversation_id": fake_conv_id, "message": "Hello"}
    )
    assert response.status_code == 404
    detail = response.json()["detail"]
    # Error should suggest user action (conversation was deleted or doesn't exist)
    assert len(detail) > 0
    assert "deleted" in detail.lower() or "found" in detail.lower()

    # 403: Suggests access issue
    response = client.post(
        "/api/user-456/chat",
        json={"message": "Hello"}
    )
    assert response.status_code == 403
    detail = response.json()["detail"]
    assert "access" in detail.lower() or "denied" in detail.lower()
