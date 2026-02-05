"""JWT validation middleware for MCP server

Intercepts tool invocation requests and validates JWT tokens.
"""

import logging
from typing import Any, Optional

from mcp.server import Request, RequestContext

from .auth import extract_token_from_header, extract_user_id_from_token
from .errors import UnauthorizedError

logger = logging.getLogger(__name__)


class JWTMiddleware:
    """Middleware to validate JWT tokens in MCP tool invocations"""

    async def validate_request(self, request: Request) -> tuple[Request, str]:
        """Validate JWT token in request and extract user_id

        Args:
            request: MCP request object

        Returns:
            Tuple of (request, authenticated_user_id)

        Raises:
            UnauthorizedError: If token is invalid or missing
        """
        # Extract Authorization header from request
        # MCP requests include headers in the request context
        headers = getattr(request, "headers", {}) or {}

        auth_header = None
        for key, value in headers.items():
            if key.lower() == "authorization":
                auth_header = value
                break

        if not auth_header:
            logger.warning("Missing Authorization header in MCP request")
            raise UnauthorizedError("Authorization header required")

        try:
            # Extract token from "Bearer <token>" format
            token = extract_token_from_header(auth_header)

            # Extract and validate user ID from token
            user_id = extract_user_id_from_token(token)

            logger.debug(f"Successfully authenticated user: {user_id}")
            return request, user_id

        except ValueError as e:
            logger.warning(f"JWT validation failed: {str(e)}")
            raise UnauthorizedError(str(e))
        except Exception as e:
            logger.error(f"Unexpected error during JWT validation: {e}")
            raise UnauthorizedError("Authentication failed")
