"""Tests for JWT authentication utilities (Phase 8 - T038)"""

import pytest
from jwt import encode
from datetime import datetime, timedelta, timezone

from src.config import settings
from mcpserver.auth import (
    verify_jwt_token,
    extract_user_id_from_token,
    extract_token_from_header,
)
from mcpserver.errors import UnauthorizedError


class TestVerifyJWTToken:
    """Test JWT token verification"""

    def test_valid_token_verification(self, mock_jwt_token: str):
        """Test verifying a valid JWT token"""
        payload = verify_jwt_token(mock_jwt_token)

        assert payload is not None
        assert payload["sub"] == "test-user-123"
        assert "iat" in payload
        assert "exp" in payload

    def test_invalid_token_rejection(self):
        """Test that invalid token is rejected"""
        invalid_token = "invalid.token.string"

        with pytest.raises(ValueError, match="Invalid token"):
            verify_jwt_token(invalid_token)

    def test_expired_token_rejection(self):
        """Test that expired token is rejected"""
        payload = {
            "sub": "test-user-123",
            "iat": int((datetime.now(timezone.utc) - timedelta(hours=2)).timestamp()),
            "exp": int((datetime.now(timezone.utc) - timedelta(hours=1)).timestamp()),
        }

        expired_token = encode(
            payload,
            settings.better_auth_secret,
            algorithm="HS256",
        )

        with pytest.raises(ValueError, match="expired"):
            verify_jwt_token(expired_token)

    def test_empty_token_rejection(self):
        """Test that empty token is rejected"""
        with pytest.raises(ValueError, match="required"):
            verify_jwt_token("")


class TestExtractUserID:
    """Test user ID extraction from token"""

    def test_user_id_extraction(self, mock_jwt_token: str):
        """Test extracting user ID from valid token"""
        user_id = extract_user_id_from_token(mock_jwt_token)

        assert user_id == "test-user-123"

    def test_missing_user_id_rejection(self):
        """Test that token without user ID is rejected"""
        payload = {
            "iat": 1234567890,
            "exp": 9999999999,
        }

        token_without_user_id = encode(
            payload,
            settings.better_auth_secret,
            algorithm="HS256",
        )

        with pytest.raises(ValueError, match="user ID"):
            extract_user_id_from_token(token_without_user_id)

    def test_invalid_token_rejection(self):
        """Test that invalid token is rejected"""
        with pytest.raises(ValueError, match="Invalid token"):
            extract_user_id_from_token("invalid.token")


class TestExtractTokenFromHeader:
    """Test token extraction from Authorization header"""

    def test_valid_header_parsing(self, mock_jwt_token: str):
        """Test parsing valid Authorization header"""
        header = f"Bearer {mock_jwt_token}"
        token = extract_token_from_header(header)

        assert token == mock_jwt_token

    def test_missing_header_rejection(self):
        """Test that missing header is rejected"""
        with pytest.raises(ValueError, match="required"):
            extract_token_from_header(None)

    def test_invalid_header_format_rejection(self):
        """Test that invalid header format is rejected"""
        with pytest.raises(ValueError, match="Invalid.*format"):
            extract_token_from_header("InvalidHeader token123")

    def test_missing_token_in_header_rejection(self):
        """Test that header without token is rejected"""
        with pytest.raises(ValueError, match="Invalid.*format"):
            extract_token_from_header("Bearer")

    def test_case_insensitive_bearer(self, mock_jwt_token: str):
        """Test that Bearer prefix is case insensitive"""
        header = f"bearer {mock_jwt_token}"
        token = extract_token_from_header(header)

        assert token == mock_jwt_token
