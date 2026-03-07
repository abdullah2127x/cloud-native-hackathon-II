"""Business logic layer for Tag operations."""
from sqlmodel import Session
from typing import List

from src.models.tag import Tag
from src.exceptions.base import TagNotFoundError
from src.repositories import tag_repo


def get_or_create(session: Session, tag_name: str, user_id: str) -> Tag:
    """Get an existing tag or create a new one (case-insensitive)."""
    tag_name = tag_name.lower().strip()
    tag = tag_repo.find_by_name(session, tag_name, user_id)
    if not tag:
        tag = Tag(user_id=user_id, name=tag_name)
        tag_repo.insert_tag(session, tag)
    return tag


def get_tag_by_id(session: Session, tag_id: str, user_id: str) -> Tag:
    """Get a tag by ID, ensuring it belongs to the user."""
    tag = tag_repo.find_by_id(session, tag_id, user_id)
    if not tag:
        raise TagNotFoundError(tag_id)
    return tag


def list_tags(session: Session, user_id: str) -> List[Tag]:
    """List all tags for a user."""
    return tag_repo.find_all(session, user_id)


def get_tags_for_task(session: Session, task_id: str, user_id: str) -> List[Tag]:
    """Get all tags associated with a task."""
    from src.repositories import task_repo
    task = task_repo.find_by_id(session, task_id, user_id)
    if not task:
        raise TagNotFoundError(f"Task {task_id} not found for user {user_id}")
    return tag_repo.find_for_task(session, task_id)


def get_tag_stats(session: Session, user_id: str) -> List[dict]:
    """Get tag statistics with task counts."""
    return tag_repo.get_stats(session, user_id)


def cleanup_orphan_tags(session: Session, user_id: str) -> int:
    """Clean up orphan tags (tags with no associated tasks)."""
    orphans = tag_repo.find_orphans(session, user_id)
    for tag in orphans:
        tag_repo.delete(session, tag)
    if orphans:
        session.commit()
    return len(orphans)
