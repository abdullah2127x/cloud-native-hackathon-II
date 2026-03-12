"""Chat API endpoint for AI-powered todo management.

Per spec: POST /api/chat — sends message & gets AI response.
The endpoint is authenticated via JWT, conversation state is persisted to DB.
"""
import logging

from fastapi import APIRouter, status

from src.api.deps import CurrentUser, DbSession
from src.schemas.chat import ChatRequest, ChatResponse
from src.services.agent.agent_service import handle_chat

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(
    chat_request: ChatRequest,
    user_id: CurrentUser,
    session: DbSession,
):
    """Send a message and get an AI response.

    Per spec stateless flow:
    1. Receives user message
    2. Fetches conversation history from database
    3. Runs agent with MCP tools
    4. Stores messages in database
    5. Returns response (server holds NO state)

    Request:
        - message: User's natural language message (required)
        - conversation_id: Existing conversation ID (optional, creates new if not provided)

    Response:
        - conversation_id: The conversation ID
        - response: AI assistant's response
        - tool_calls: List of MCP tools invoked
    """
    logger.info(f"Chat request from user {user_id}: {chat_request.message[:50]}...")

    response = await handle_chat(
        user_id=user_id,
        message=chat_request.message,
        conversation_id=chat_request.conversation_id,
        session=session,
    )

    return response
