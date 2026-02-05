"""
Message model for chat interface.

Task ID: T004
Spec: specs/001-chat-interface/spec.md
"""

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .conversation import Conversation


class Message(SQLModel, table=True):
    """
    Represents a single message in a conversation (either from user or AI assistant).

    Fields:
        - role: Either "user" or "assistant" (validated at application layer)
        - user_id: Denormalized for security filtering (duplicates conversation.user_id)
        - conversation_id: FK to conversation with CASCADE DELETE

    Relationships:
        - conversation: Bidirectional relationship to Conversation
    """
    __tablename__ = "message"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    conversation_id: UUID = Field(
        foreign_key="conversation.id",
        index=True,
        nullable=False
    )
    role: str = Field(nullable=False)  # "user" or "assistant" - validated by CHECK constraint in DB
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")
