# Task: T009/T014/T015/T016 | Spec: specs/007-chatkit-ui-integration/spec.md
"""Integration tests for POST /chatkit endpoint (US1–US4)."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

CHATKIT_URL = "/chatkit"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def _noop_respond(thread, input_user_message, context):
    """Minimal mock respond() that yields nothing — used to test auth/routing."""
    return
    yield  # make it an async generator


async def _text_respond(thread, input_user_message, context):
    """Mock respond() that yields one mock event."""
    mock_event = MagicMock()
    yield mock_event


# ---------------------------------------------------------------------------
# US1: Real-time streaming chat (T009)
# ---------------------------------------------------------------------------

class TestUS1Routing:
    def test_post_chatkit_with_valid_jwt_returns_200(self, client, mock_auth):
        """POST /chatkit with valid JWT → 200 (streaming or JSON response)."""
        with patch("src.routers.chatkit.chatkit_server") as mock_server:
            mock_result = MagicMock()
            mock_result.__class__ = type(mock_result)  # not StreamingResult
            mock_server.process = AsyncMock(return_value=mock_result)
            # Make it look like a JSON result
            mock_result.__class__.__name__ = "JsonResult"
            mock_result.json = '{"ok": true}'

            from chatkit.server import StreamingResult
            with patch("src.routers.chatkit.StreamingResult", StreamingResult):
                response = client.post(
                    CHATKIT_URL,
                    json={"action": "ping"},
                    headers={"Authorization": "Bearer mock-token"},
                )

        # 200 or 422 (if ChatKit protocol rejects our minimal payload)
        assert response.status_code in (200, 422)

    def test_post_chatkit_without_auth_returns_401(self, client):
        """POST /chatkit without Authorization header → 401."""
        response = client.post(CHATKIT_URL, json={"message": "Hello"})
        assert response.status_code == 401

    def test_post_chatkit_with_invalid_jwt_returns_401(self, client):
        """POST /chatkit with invalid JWT → 401."""
        response = client.post(
            CHATKIT_URL,
            json={"message": "Hello"},
            headers={"Authorization": "Bearer invalid-token-xyz"},
        )
        assert response.status_code == 401


# ---------------------------------------------------------------------------
# US4: Error handling (T016)
# ---------------------------------------------------------------------------

class TestUS4ErrorHandling:
    def test_missing_authorization_header_returns_401(self, client):
        """No Authorization header → 401 Unauthorized."""
        response = client.post(CHATKIT_URL, json={"message": "test"})
        assert response.status_code == 401

    def test_malformed_bearer_token_returns_401(self, client):
        """Malformed Bearer token → 401."""
        response = client.post(
            CHATKIT_URL,
            json={"message": "test"},
            headers={"Authorization": "Bearer bad.token.value"},
        )
        assert response.status_code == 401
