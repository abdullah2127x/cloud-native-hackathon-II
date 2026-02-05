"""JWT validation utilities for MCP server

Handles Better Auth JWT token verification and user ID extraction.
"""

import logging
from typing import Any, Optional

import jwt
from jwt import DecodeError, ExpiredSignatureError
from jwt.exceptions import InvalidKeyError

from src.config import settings

logger = logging.getLogger(__name__)


def verify_jwt_token(token: str) -> Optional[dict[str, Any]]:
    """Verify JWT token from Better Auth

    Args:
        token: JWT token string (without "Bearer " prefix)

    Returns:
        Token payload if valid, None if invalid

    Raises:
        ValueError: If token is invalid or expired
    """
    if not token:
        raise ValueError("Token is required")

    try:
        # Decode JWT token - Better Auth uses HS256 by default
        # For RS256 (asymmetric), would need JWT_PUBLIC_KEY from settings
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=["HS256"],
        )
        return payload
    except ExpiredSignatureError:
        raise ValueError("Token has expired")
    except DecodeError as e:
        raise ValueError(f"Invalid token: {str(e)}")
    except InvalidKeyError as e:
        raise ValueError(f"Invalid key: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during JWT verification: {e}")
        raise ValueError(f"Token verification failed: {str(e)}")


def extract_user_id_from_token(token: str) -> str:
    """Extract user ID from JWT token

    Args:
        token: JWT token string (without "Bearer " prefix)

    Returns:
        User ID from token's 'sub' claim

    Raises:
        ValueError: If token is invalid or user_id cannot be extracted
    """
    payload = verify_jwt_token(token)

    # Better Auth stores user ID in 'sub' claim
    user_id = payload.get("sub")
    if not user_id:
        raise ValueError("Token does not contain user ID (sub claim)")

    return str(user_id)


def extract_token_from_header(auth_header: Optional[str]) -> str:
    """Extract JWT token from Authorization header

    Args:
        auth_header: Value of Authorization header (e.g., "Bearer token...")

    Returns:
        Token string without "Bearer " prefix

    Raises:
        ValueError: If header format is invalid
    """
    if not auth_header:
        raise ValueError("Authorization header is required")

    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise ValueError("Invalid Authorization header format. Expected: Bearer <token>")

    return parts[1]
