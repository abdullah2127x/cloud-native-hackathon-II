# Task: T012/T013/T014 | Spec: specs/006-agent-mcp-integration/spec.md
"""Integration tests for POST /api/{user_id}/chat endpoint."""
import pytest
from unittest.mock import AsyncMock, patch

from src.models.message import Message
from sqlmodel import select

TEST_USER = "test-user-id"
OTHER_USER = "other-user-id"
CHAT_URL = f"/api/{TEST_USER}/chat"


# ---------------------------------------------------------------------------
# US1: Basic chat — new conversations and all 5 MCP tool verbs (T012)
# ---------------------------------------------------------------------------

class TestUS1NewConversation:
    def test_us1_new_conversation_returns_200_and_conversation_id(self, client, session, auth_headers):
        """No conversation_id → creates new conversation → 200 OK with conversation_id."""
        with patch("src.routers.chat.run_todo_agent", new=AsyncMock(return_value=("Hello!", []))):
            response = client.post(CHAT_URL, json={"message": "Hello"}, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "conversation_id" in data
        assert isinstance(data["conversation_id"], int)
        assert data["response"] == "Hello!"
        assert data["tool_calls"] == []

    def test_us1_add_task_via_natural_language(self, client, session, auth_headers):
        """Natural language add → tool_calls contains 'add_task'."""
        with patch("src.routers.chat.run_todo_agent", new=AsyncMock(
            return_value=("Created task: 'Buy groceries' (ID: 1)", ["add_task"])
        )):
            response = client.post(
                CHAT_URL,
                json={"message": "Add a task to buy groceries"},
                headers=auth_headers,
            )
        assert response.status_code == 200
        data = response.json()
        assert "add_task" in data["tool_calls"]

    def test_us1_list_tasks_returns_tool_call(self, client, session, auth_headers):
        """Show my tasks → tool_calls contains 'list_tasks'."""
        with patch("src.routers.chat.run_todo_agent", new=AsyncMock(
            return_value=("You have no tasks.", ["list_tasks"])
        )):
            response = client.post(
                CHAT_URL,
                json={"message": "Show my tasks"},
                headers=auth_headers,
            )
        assert response.status_code == 200
        assert "list_tasks" in response.json()["tool_calls"]

    def test_us1_complete_task_returns_tool_call(self, client, session, auth_headers):
        with patch("src.routers.chat.run_todo_agent", new=AsyncMock(
            return_value=("Task 'Buy milk' (ID: 1) completed.", ["complete_task"])
        )):
            response = client.post(
                CHAT_URL,
                json={"message": "Mark task 1 as done"},
                headers=auth_headers,
            )
        assert response.status_code == 200
        assert "complete_task" in response.json()["tool_calls"]

    def test_us1_delete_task_returns_tool_call(self, client, session, auth_headers):
        with patch("src.routers.chat.run_todo_agent", new=AsyncMock(
            return_value=("Deleted task 'Buy milk' (ID: 1).", ["delete_task"])
        )):
            response = client.post(
                CHAT_URL,
                json={"message": "Delete task 1"},
                headers=auth_headers,
            )
        assert response.status_code == 200
        assert "delete_task" in response.json()["tool_calls"]

    def test_us1_update_task_returns_tool_call(self, client, session, auth_headers):
        with patch("src.routers.chat.run_todo_agent", new=AsyncMock(
            return_value=("Updated task (ID: 1) — new title: 'Buy almond milk'.", ["update_task"])
        )):
            response = client.post(
                CHAT_URL,
                json={"message": "Change task 1 to Buy almond milk"},
                headers=auth_headers,
            )
        assert response.status_code == 200
        assert "update_task" in response.json()["tool_calls"]

    def test_us1_401_on_missing_auth(self, client, session):
        """No Authorization header → 401."""
        response = client.post(CHAT_URL, json={"message": "Hello"})
        assert response.status_code == 401

    def test_us1_401_on_wrong_user_in_path(self, client, session):
        """JWT user != path user_id → 401."""
        from src.main import app
        from src.auth.dependencies import get_current_user

        async def mock_other_user() -> str:
            return OTHER_USER

        app.dependency_overrides[get_current_user] = mock_other_user
        try:
            with patch("src.routers.chat.run_todo_agent", new=AsyncMock(return_value=("ok", []))):
                response = client.post(
                    CHAT_URL,
                    json={"message": "Hello"},
                    headers={"Authorization": "Bearer mock"},
                )
            assert response.status_code == 401
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    def test_us1_503_on_provider_failure_user_message_persisted(self, client, session, auth_headers):
        """Provider failure → 503 AND user message is already persisted in DB."""
        async def failing_agent(*args, **kwargs):
            raise RuntimeError("OpenRouter timeout")

        with patch("src.routers.chat.run_todo_agent", new=failing_agent):
            response = client.post(
                CHAT_URL,
                json={"message": "Add task milk"},
                headers=auth_headers,
            )
        assert response.status_code == 503
        # User message must be persisted even though provider failed
        msgs = session.exec(
            select(Message).where(
                Message.user_id == TEST_USER,
                Message.role == "user",
            )
        ).all()
        assert len(msgs) == 1
        assert msgs[0].content == "Add task milk"


# ---------------------------------------------------------------------------
# US2: Multi-turn conversations (T013)
# ---------------------------------------------------------------------------

class TestUS2MultiTurn:
    def test_us2_continuation_loads_prior_history(self, client, session, auth_headers):
        """Sending conversation_id loads the conversation's history."""
        # First message: create conversation
        with patch("src.routers.chat.run_todo_agent", new=AsyncMock(return_value=("Task added!", ["add_task"]))):
            r1 = client.post(CHAT_URL, json={"message": "Add groceries"}, headers=auth_headers)
        assert r1.status_code == 200
        conv_id = r1.json()["conversation_id"]

        # Second message: continue conversation
        with patch("src.routers.chat.run_todo_agent", new=AsyncMock(return_value=("Also added milk!", ["add_task"]))) as mock_agent:
            r2 = client.post(
                CHAT_URL,
                json={"message": "Also add milk", "conversation_id": conv_id},
                headers=auth_headers,
            )
        assert r2.status_code == 200
        assert r2.json()["conversation_id"] == conv_id
        # Agent received both the first user msg + first assistant msg + new user msg
        called_messages = mock_agent.call_args[1]["messages"] if mock_agent.call_args[1] else mock_agent.call_args[0][0]
        assert len(called_messages) >= 2

    def test_us2_new_session_returns_fresh_conversation_id(self, client, session, auth_headers):
        """Second call without conversation_id creates a new conversation."""
        with patch("src.routers.chat.run_todo_agent", new=AsyncMock(return_value=("ok", []))):
            r1 = client.post(CHAT_URL, json={"message": "msg 1"}, headers=auth_headers)
            r2 = client.post(CHAT_URL, json={"message": "msg 2"}, headers=auth_headers)
        assert r1.status_code == 200
        assert r2.status_code == 200
        assert r1.json()["conversation_id"] != r2.json()["conversation_id"]

    def test_us2_history_persisted_across_calls(self, client, session, auth_headers):
        """Messages from both turns are in the DB after two requests."""
        with patch("src.routers.chat.run_todo_agent", new=AsyncMock(return_value=("resp", []))):
            r1 = client.post(CHAT_URL, json={"message": "first"}, headers=auth_headers)
        conv_id = r1.json()["conversation_id"]
        with patch("src.routers.chat.run_todo_agent", new=AsyncMock(return_value=("resp2", []))):
            client.post(CHAT_URL, json={"message": "second", "conversation_id": conv_id}, headers=auth_headers)

        msgs = session.exec(
            select(Message).where(Message.conversation_id == conv_id)
        ).all()
        # 2 user messages + 2 assistant messages = 4
        assert len(msgs) == 4


# ---------------------------------------------------------------------------
# US3: Edge cases and error handling (T014)
# ---------------------------------------------------------------------------

class TestUS3ErrorHandling:
    def test_us3_off_topic_returns_200_with_scope_explanation(self, client, session, auth_headers):
        """Off-topic message → 200 with agent politely declining."""
        agent_reply = "I specialise in task management. How can I help with your tasks?"
        with patch("src.routers.chat.run_todo_agent", new=AsyncMock(return_value=(agent_reply, []))):
            response = client.post(
                CHAT_URL,
                json={"message": "What's the weather today?"},
                headers=auth_headers,
            )
        assert response.status_code == 200
        assert response.json()["tool_calls"] == []

    def test_us3_503_when_provider_raises(self, client, session, auth_headers):
        """Provider exception → 503 SERVICE_UNAVAILABLE."""
        async def raise_exc(*args, **kwargs):
            raise ConnectionError("OpenRouter down")

        with patch("src.routers.chat.run_todo_agent", new=raise_exc):
            response = client.post(CHAT_URL, json={"message": "list tasks"}, headers=auth_headers)
        assert response.status_code == 503

    def test_us3_404_for_conversation_belonging_to_other_user(self, client, session, auth_headers):
        """conversation_id belonging to other user → 404."""
        # Create a conversation as TEST_USER
        with patch("src.routers.chat.run_todo_agent", new=AsyncMock(return_value=("ok", []))):
            r = client.post(CHAT_URL, json={"message": "hello"}, headers=auth_headers)
        conv_id = r.json()["conversation_id"]

        # Try to use it as OTHER_USER
        from src.main import app
        from src.auth.dependencies import get_current_user

        async def mock_other() -> str:
            return OTHER_USER

        app.dependency_overrides[get_current_user] = mock_other
        other_url = f"/api/{OTHER_USER}/chat"
        try:
            with patch("src.routers.chat.run_todo_agent", new=AsyncMock(return_value=("ok", []))):
                response = client.post(
                    other_url,
                    json={"message": "hello", "conversation_id": conv_id},
                    headers={"Authorization": "Bearer mock"},
                )
            assert response.status_code == 404
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    def test_us3_400_on_empty_message(self, client, session, auth_headers):
        """Empty message string → 422 (Pydantic min_length=1 validation)."""
        response = client.post(CHAT_URL, json={"message": ""}, headers=auth_headers)
        assert response.status_code == 422

    def test_us3_400_on_message_exceeding_5000_chars(self, client, session, auth_headers):
        """Message > 5000 chars → 422 (Pydantic max_length=5000 validation)."""
        response = client.post(CHAT_URL, json={"message": "x" * 5001}, headers=auth_headers)
        assert response.status_code == 422
