"""Task model for todo items"""
from sqlmodel import SQLModel, Field
from datetime import datetime, UTC
from typing import Optional
import uuid


def utc_now() -> datetime:
    """Get current UTC time"""
    return datetime.now(UTC)


def generate_uuid() -> str:
    """Generate UUID string"""
    return str(uuid.uuid4())


class Task(SQLModel, table=True):
    """Task model for user todo items"""

    id: str = Field(default_factory=generate_uuid, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=utc_now, index=True)
    updated_at: Optional[datetime] = Field(default=None)
