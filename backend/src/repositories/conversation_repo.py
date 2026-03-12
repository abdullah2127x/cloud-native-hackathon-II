"""Repository for Conversation and Message DB operations."""
from sqlmodel import Session, select
from typing import List, Optional

from src.models.conversation import Conversation
from src.models.message import Message
from src.utils.helpers import utc_now


class ConversationRepository:
    """Data-access layer for conversations and messages."""

    def create_conversation(self, session: Session, user_id: str) -> Conversation:
        """Create a new conversation for a user."""
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    def get_conversation(
        self, session: Session, conversation_id: str, user_id: str
    ) -> Optional[Conversation]:
        """Get a conversation by ID, ensuring it belongs to the user."""
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
        return session.exec(statement).first()

    def add_message(
        self,
        session: Session,
        conversation_id: str,
        user_id: str,
        role: str,
        content: str,
    ) -> Message:
        """Add a message to a conversation."""
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
        )
        session.add(message)

        # Update conversation's updated_at
        conversation = session.get(Conversation, conversation_id)
        if conversation:
            conversation.updated_at = utc_now()
            session.add(conversation)

        session.commit()
        session.refresh(message)
        return message

    def get_messages(
        self,
        session: Session,
        conversation_id: str,
        limit: int = 50,
    ) -> List[Message]:
        """Get messages for a conversation, ordered by created_at."""
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
        )
        return list(session.exec(statement).all())


# Module-level singleton
conversation_repo = ConversationRepository()
