"""Backward-compatible re-export. Canonical location: src.services.tag_service"""
from src.services.tag_service import (  # noqa: F401
    get_or_create as get_or_create_tag,
    get_tag_by_id,
    list_tags,
    get_tags_for_task,
    get_tag_stats,
    cleanup_orphan_tags,
)
