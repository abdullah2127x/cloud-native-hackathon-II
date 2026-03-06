# Task: T004 | Spec: specs/007-chatkit-ui-integration/spec.md
"""TodoPostgresStore — ChatKit Store backed by Neon/PostgreSQL via psycopg3."""
from dataclasses import dataclass

import psycopg
from psycopg.rows import tuple_row
from psycopg.types.json import Jsonb
from sqlmodel import Session

from pydantic import TypeAdapter

from chatkit.store import Store, NotFoundError
from chatkit.types import ThreadMetadata, ThreadItem, Attachment, Page

from src.config import settings

_thread_item_adapter: TypeAdapter[ThreadItem] = TypeAdapter(ThreadItem)


@dataclass
class ChatKitRequestContext:
    """Per-request context passed to all Store methods and the ChatKitServer."""
    user_id: str
    session: Session


def _get_conninfo() -> str:
    """Return a psycopg3-compatible connection string from settings.database_url.

    Strips any SQLAlchemy driver prefix (e.g. postgresql+asyncpg:// → postgresql://).
    """
    url = settings.database_url
    # Strip SQLAlchemy-specific driver (+asyncpg, +psycopg2, etc.)
    if "://" in url:
        scheme, rest = url.split("://", 1)
        base_scheme = scheme.split("+")[0]
        url = f"{base_scheme}://{rest}"
    return url


class TodoPostgresStore(Store[ChatKitRequestContext]):
    """Postgres-backed ChatKit Store with user-scoped thread isolation."""

    def __init__(self, conninfo: str | None = None) -> None:
        self._conninfo = conninfo or _get_conninfo()
        # Only attempt schema init for PostgreSQL connections
        if self._conninfo.startswith("postgresql"):
            self._init_schema()

    def _connection(self):
        return psycopg.connect(self._conninfo)

    def _init_schema(self) -> None:
        with self._connection() as conn, conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS chatkit_threads (
                    id          TEXT PRIMARY KEY,
                    user_id     TEXT NOT NULL,
                    created_at  TIMESTAMPTZ NOT NULL,
                    data        JSONB NOT NULL
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_chatkit_threads_user_id
                ON chatkit_threads(user_id)
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS chatkit_items (
                    id          TEXT PRIMARY KEY,
                    thread_id   TEXT NOT NULL REFERENCES chatkit_threads(id) ON DELETE CASCADE,
                    user_id     TEXT NOT NULL,
                    created_at  TIMESTAMPTZ NOT NULL,
                    data        JSONB NOT NULL
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_chatkit_items_thread_id
                ON chatkit_items(thread_id)
            """)
            conn.commit()

    # ------------------------------------------------------------------
    # Thread operations
    # ------------------------------------------------------------------

    async def load_thread(
        self, thread_id: str, context: ChatKitRequestContext
    ) -> ThreadMetadata:
        with self._connection() as conn, conn.cursor(row_factory=tuple_row) as cur:
            cur.execute(
                "SELECT data FROM chatkit_threads WHERE id = %s AND user_id = %s",
                (thread_id, context.user_id),
            )
            row = cur.fetchone()
        if row is None:
            raise NotFoundError(f"Thread {thread_id} not found")
        return ThreadMetadata.model_validate(row[0])

    async def save_thread(
        self, thread: ThreadMetadata, context: ChatKitRequestContext
    ) -> None:
        payload = thread.model_dump(mode="json")
        with self._connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO chatkit_threads (id, user_id, created_at, data)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET data = EXCLUDED.data
                """,
                (thread.id, context.user_id, thread.created_at, Jsonb(payload)),
            )
            conn.commit()

    async def load_threads(
        self,
        limit: int,
        after: str | None,
        order: str,
        context: ChatKitRequestContext,
    ) -> "Page[ThreadMetadata]":
        direction = "ASC" if order == "asc" else "DESC"
        with self._connection() as conn, conn.cursor(row_factory=tuple_row) as cur:
            if after:
                cur.execute(
                    f"SELECT data FROM chatkit_threads WHERE user_id = %s AND id > %s "
                    f"ORDER BY created_at {direction} LIMIT %s",
                    (context.user_id, after, limit + 1),
                )
            else:
                cur.execute(
                    f"SELECT data FROM chatkit_threads WHERE user_id = %s "
                    f"ORDER BY created_at {direction} LIMIT %s",
                    (context.user_id, limit + 1),
                )
            rows = cur.fetchall()
        has_more = len(rows) > limit
        data = [ThreadMetadata.model_validate(r[0]) for r in rows[:limit]]
        next_after = data[-1].id if has_more and data else None
        return Page(data=data, has_more=has_more, after=next_after)

    async def delete_thread(
        self, thread_id: str, context: ChatKitRequestContext
    ) -> None:
        with self._connection() as conn, conn.cursor() as cur:
            cur.execute(
                "DELETE FROM chatkit_threads WHERE id = %s AND user_id = %s",
                (thread_id, context.user_id),
            )
            conn.commit()

    # ------------------------------------------------------------------
    # Item operations
    # ------------------------------------------------------------------

    async def load_thread_items(
        self,
        thread_id: str,
        after: str | None,
        limit: int,
        order: str,
        context: ChatKitRequestContext,
    ) -> "Page[ThreadItem]":
        direction = "ASC" if order == "asc" else "DESC"
        with self._connection() as conn, conn.cursor(row_factory=tuple_row) as cur:
            if after:
                cur.execute(
                    f"SELECT data FROM chatkit_items WHERE thread_id = %s AND user_id = %s "
                    f"AND id > %s ORDER BY created_at {direction} LIMIT %s",
                    (thread_id, context.user_id, after, limit + 1),
                )
            else:
                cur.execute(
                    f"SELECT data FROM chatkit_items WHERE thread_id = %s AND user_id = %s "
                    f"ORDER BY created_at {direction} LIMIT %s",
                    (thread_id, context.user_id, limit + 1),
                )
            rows = cur.fetchall()
        has_more = len(rows) > limit
        data = [_thread_item_adapter.validate_python(r[0]) for r in rows[:limit]]
        next_after = data[-1].id if has_more and data else None
        return Page(data=data, has_more=has_more, after=next_after)

    async def add_thread_item(
        self, thread_id: str, item: ThreadItem, context: ChatKitRequestContext
    ) -> None:
        payload = item.model_dump(mode="json")
        with self._connection() as conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO chatkit_items (id, thread_id, user_id, created_at, data) "
                "VALUES (%s, %s, %s, %s, %s)",
                (item.id, thread_id, context.user_id, item.created_at, Jsonb(payload)),
            )
            conn.commit()

    async def save_item(
        self, thread_id: str, item: ThreadItem, context: ChatKitRequestContext
    ) -> None:
        payload = item.model_dump(mode="json")
        with self._connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO chatkit_items (id, thread_id, user_id, created_at, data)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET data = EXCLUDED.data
                """,
                (item.id, thread_id, context.user_id, item.created_at, Jsonb(payload)),
            )
            conn.commit()

    async def load_item(
        self, thread_id: str, item_id: str, context: ChatKitRequestContext
    ) -> ThreadItem:
        with self._connection() as conn, conn.cursor(row_factory=tuple_row) as cur:
            cur.execute(
                "SELECT data FROM chatkit_items WHERE id = %s AND thread_id = %s AND user_id = %s",
                (item_id, thread_id, context.user_id),
            )
            row = cur.fetchone()
        if row is None:
            raise NotFoundError(f"Item {item_id} not found")
        return _thread_item_adapter.validate_python(row[0])

    async def delete_thread_item(
        self, thread_id: str, item_id: str, context: ChatKitRequestContext
    ) -> None:
        with self._connection() as conn, conn.cursor() as cur:
            cur.execute(
                "DELETE FROM chatkit_items WHERE id = %s AND thread_id = %s AND user_id = %s",
                (item_id, thread_id, context.user_id),
            )
            conn.commit()

    # ------------------------------------------------------------------
    # Attachments — not required for this feature
    # ------------------------------------------------------------------

    async def save_attachment(
        self, attachment: Attachment, context: ChatKitRequestContext
    ) -> None:
        raise NotImplementedError("Attachment storage not configured")

    async def load_attachment(
        self, attachment_id: str, context: ChatKitRequestContext
    ) -> Attachment:
        raise NotImplementedError("Attachment storage not configured")

    async def delete_attachment(
        self, attachment_id: str, context: ChatKitRequestContext
    ) -> None:
        raise NotImplementedError("Attachment storage not configured")
