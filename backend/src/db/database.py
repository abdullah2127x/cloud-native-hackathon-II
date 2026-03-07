"""Backward-compatible re-export. Canonical location: src.core.database"""
from src.core.database import (  # noqa: F401
    engine,
    create_db_and_tables,
    get_session,
)
