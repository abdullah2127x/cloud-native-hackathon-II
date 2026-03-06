# Task: T010 | Spec: specs/007-chatkit-ui-integration/spec.md
"""POST /chatkit router — ChatKit streaming endpoint."""
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import StreamingResponse

from chatkit.server import StreamingResult

from src.auth.dependencies import get_current_user
from src.chatkit.server import TodoChatKitServer, todo_postgres_store
from src.chatkit.store import ChatKitRequestContext
from src.db.database import get_session
from sqlmodel import Session

router = APIRouter(tags=["chatkit"])

# Module-level server instance (reuses shared store)
chatkit_server = TodoChatKitServer(store=todo_postgres_store)


@router.post("/chatkit")
async def chatkit_endpoint(
    request: Request,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """ChatKit streaming endpoint.

    Accepts ChatKit protocol request body, authenticates the user via JWT,
    and streams SSE events from the todo agent.
    """
    context = ChatKitRequestContext(user_id=user_id, session=session)
    result = await chatkit_server.process(await request.body(), context)

    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")
    return Response(content=result.json, media_type="application/json")
