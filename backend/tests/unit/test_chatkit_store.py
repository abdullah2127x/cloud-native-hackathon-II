# Task: T005 | Spec: specs/007-chatkit-ui-integration/spec.md
"""Unit tests for TodoPostgresStore contract (TDD — written before T004 implementation).

The behavioural contract is validated using a lightweight test-local InMemoryStore
that implements the same Store[TContext] interface as TodoPostgresStore.
Additionally, the _get_conninfo helper and the ChatKitRequestContext dataclass are tested.
"""
import pytest
from collections import defaultdict
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch, call

from chatkit.store import Store, NotFoundError
from chatkit.types import ThreadMetadata, ThreadItem, Attachment, Page, AssistantMessageItem

from src.chatkit.store import ChatKitRequestContext


# ---------------------------------------------------------------------------
# Test-local InMemoryStore (same interface as TodoPostgresStore)
# Used to validate the Store contract without requiring a live PostgreSQL server.
# ---------------------------------------------------------------------------

class _TestInMemoryStore(Store[ChatKitRequestContext]):
    """Minimal in-memory store for unit testing the Store contract."""

    def __init__(self):
        self._threads: dict[str, tuple[ThreadMetadata, str]] = {}   # id → (thread, user_id)
        self._items: dict[str, list[tuple[ThreadItem, str]]] = defaultdict(list)  # thread_id → [(item, user_id)]
        self._attachments: dict[str, Attachment] = {}

    async def load_thread(self, thread_id: str, context: ChatKitRequestContext) -> ThreadMetadata:
        entry = self._threads.get(thread_id)
        if entry is None or entry[1] != context.user_id:
            raise NotFoundError(f"Thread {thread_id} not found")
        return entry[0]

    async def save_thread(self, thread: ThreadMetadata, context: ChatKitRequestContext) -> None:
        self._threads[thread.id] = (thread, context.user_id)

    async def load_threads(self, limit: int, after: str | None, order: str, context: ChatKitRequestContext) -> Page[ThreadMetadata]:
        threads = [t for t, uid in self._threads.values() if uid == context.user_id]
        threads.sort(key=lambda t: t.created_at, reverse=(order == "desc"))
        data = threads[:limit]
        return Page(data=data, has_more=False, after=None)

    async def delete_thread(self, thread_id: str, context: ChatKitRequestContext) -> None:
        if thread_id in self._threads:
            del self._threads[thread_id]
        self._items.pop(thread_id, None)

    async def load_thread_items(self, thread_id: str, after: str | None, limit: int, order: str, context: ChatKitRequestContext) -> Page[ThreadItem]:
        all_items = [(item, uid) for item, uid in self._items.get(thread_id, []) if uid == context.user_id]
        all_items.sort(key=lambda t: t[0].created_at, reverse=(order == "desc"))
        data = [item for item, _ in all_items[:limit]]
        return Page(data=data, has_more=False, after=None)

    async def add_thread_item(self, thread_id: str, item: ThreadItem, context: ChatKitRequestContext) -> None:
        self._items[thread_id].append((item, context.user_id))

    async def save_item(self, thread_id: str, item: ThreadItem, context: ChatKitRequestContext) -> None:
        items = self._items[thread_id]
        for i, (existing, uid) in enumerate(items):
            if existing.id == item.id:
                items[i] = (item, uid)
                return
        items.append((item, context.user_id))

    async def load_item(self, thread_id: str, item_id: str, context: ChatKitRequestContext) -> ThreadItem:
        for item, uid in self._items.get(thread_id, []):
            if item.id == item_id and uid == context.user_id:
                return item
        raise NotFoundError(f"Item {item_id} not found")

    async def delete_thread_item(self, thread_id: str, item_id: str, context: ChatKitRequestContext) -> None:
        self._items[thread_id] = [
            (item, uid) for item, uid in self._items.get(thread_id, [])
            if item.id != item_id
        ]

    async def save_attachment(self, attachment: Attachment, context: ChatKitRequestContext) -> None:
        self._attachments[attachment.id] = attachment

    async def load_attachment(self, attachment_id: str, context: ChatKitRequestContext) -> Attachment:
        if attachment_id not in self._attachments:
            raise NotFoundError(f"Attachment {attachment_id} not found")
        return self._attachments[attachment_id]

    async def delete_attachment(self, attachment_id: str, context: ChatKitRequestContext) -> None:
        self._attachments.pop(attachment_id, None)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_thread(thread_id: str = "thread-1") -> ThreadMetadata:
    return ThreadMetadata(
        id=thread_id,
        created_at=datetime.now(timezone.utc),
        title=None,
    )


def _make_context(user_id: str = "user-1") -> ChatKitRequestContext:
    return ChatKitRequestContext(user_id=user_id, session=MagicMock())


def _make_item(item_id: str, thread_id: str = "t-test", created_at: datetime | None = None) -> AssistantMessageItem:
    return AssistantMessageItem(
        id=item_id,
        thread_id=thread_id,
        created_at=created_at or datetime.now(timezone.utc),
        content=[{"type": "output_text", "text": f"message {item_id}"}],
    )


# ---------------------------------------------------------------------------
# T005: Store contract tests
# ---------------------------------------------------------------------------

class TestStoreContract:
    @pytest.fixture
    def store(self):
        return _TestInMemoryStore()

    @pytest.fixture
    def ctx(self):
        return _make_context("user-1")

    @pytest.fixture
    def other_ctx(self):
        return _make_context("user-2")

    # save_thread / load_thread round-trip
    @pytest.mark.asyncio
    async def test_save_and_load_thread_round_trip(self, store, ctx):
        thread = _make_thread("t-1")
        await store.save_thread(thread, ctx)
        loaded = await store.load_thread("t-1", ctx)
        assert loaded.id == "t-1"
        assert loaded.status.type == "active"

    @pytest.mark.asyncio
    async def test_load_thread_not_found_raises(self, store, ctx):
        with pytest.raises(NotFoundError):
            await store.load_thread("nonexistent", ctx)

    # add_thread_item / load_thread_items ordering
    @pytest.mark.asyncio
    async def test_items_returned_oldest_first_with_asc_order(self, store, ctx):
        thread = _make_thread("t-2")
        await store.save_thread(thread, ctx)

        t1 = datetime(2026, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        t2 = datetime(2026, 1, 1, 11, 0, 0, tzinfo=timezone.utc)
        item_old = _make_item("item-old", "t-2", t1)
        item_new = _make_item("item-new", "t-2", t2)

        await store.add_thread_item("t-2", item_old, ctx)
        await store.add_thread_item("t-2", item_new, ctx)

        page = await store.load_thread_items("t-2", after=None, limit=20, order="asc", context=ctx)
        assert isinstance(page, Page)
        assert len(page.data) == 2
        assert page.data[0].id == "item-old"
        assert page.data[1].id == "item-new"

    # User isolation: load_thread with wrong user_id
    @pytest.mark.asyncio
    async def test_load_thread_wrong_user_raises_not_found(self, store, ctx, other_ctx):
        thread = _make_thread("t-3")
        await store.save_thread(thread, ctx)           # saved as user-1
        with pytest.raises(NotFoundError):
            await store.load_thread("t-3", other_ctx)  # user-2 cannot see it

    # User isolation: load_thread_items with wrong user_id returns empty
    @pytest.mark.asyncio
    async def test_load_thread_items_wrong_user_returns_empty(self, store, ctx, other_ctx):
        thread = _make_thread("t-4")
        await store.save_thread(thread, ctx)
        await store.add_thread_item("t-4", _make_item("item-1"), ctx)

        page = await store.load_thread_items("t-4", after=None, limit=20, order="asc", context=other_ctx)
        assert page.data == []

    # delete_thread removes thread
    @pytest.mark.asyncio
    async def test_delete_thread_removes_thread(self, store, ctx):
        thread = _make_thread("t-5")
        await store.save_thread(thread, ctx)
        await store.delete_thread("t-5", ctx)
        with pytest.raises(NotFoundError):
            await store.load_thread("t-5", ctx)

    # delete_thread cascades to items
    @pytest.mark.asyncio
    async def test_delete_thread_cascades_to_items(self, store, ctx):
        thread = _make_thread("t-6")
        await store.save_thread(thread, ctx)
        await store.add_thread_item("t-6", _make_item("item-cascade"), ctx)

        await store.delete_thread("t-6", ctx)

        page = await store.load_thread_items("t-6", after=None, limit=20, order="asc", context=ctx)
        assert page.data == []


# ---------------------------------------------------------------------------
# ChatKitRequestContext dataclass
# ---------------------------------------------------------------------------

class TestChatKitRequestContext:
    def test_has_user_id_and_session(self):
        session = MagicMock()
        ctx = ChatKitRequestContext(user_id="u-1", session=session)
        assert ctx.user_id == "u-1"
        assert ctx.session is session

    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(ChatKitRequestContext)


# ---------------------------------------------------------------------------
# T006: _get_conninfo strips SQLAlchemy prefixes
# ---------------------------------------------------------------------------

class TestGetConninfo:
    def test_plain_postgres_url_unchanged(self):
        from src.chatkit.store import _get_conninfo
        with patch("src.chatkit.store.settings") as mock_settings:
            mock_settings.database_url = "postgresql://user:pass@host/db"
            result = _get_conninfo()
        assert result == "postgresql://user:pass@host/db"

    def test_strips_asyncpg_driver_prefix(self):
        from src.chatkit.store import _get_conninfo
        with patch("src.chatkit.store.settings") as mock_settings:
            mock_settings.database_url = "postgresql+asyncpg://user:pass@host/db"
            result = _get_conninfo()
        assert result == "postgresql://user:pass@host/db"

    def test_strips_psycopg2_driver_prefix(self):
        from src.chatkit.store import _get_conninfo
        with patch("src.chatkit.store.settings") as mock_settings:
            mock_settings.database_url = "postgresql+psycopg2://user:pass@host/db"
            result = _get_conninfo()
        assert result == "postgresql://user:pass@host/db"

    def test_settings_database_url_is_accessible(self):
        from src.config import settings
        assert hasattr(settings, "database_url")
        assert isinstance(settings.database_url, str)
        assert len(settings.database_url) > 0


# ---------------------------------------------------------------------------
# TodoPostgresStore: _init_schema called on construction (mocked psycopg)
# ---------------------------------------------------------------------------

class TestTodoPostgresStoreInit:
    def test_init_schema_called_on_construction(self):
        """TodoPostgresStore calls _init_schema on __init__."""
        mock_cursor = MagicMock()
        mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
        mock_cursor.__exit__ = MagicMock(return_value=False)

        mock_conn = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.cursor = MagicMock(return_value=mock_cursor)

        with patch("src.chatkit.store.psycopg.connect", return_value=mock_conn):
            from src.chatkit.store import TodoPostgresStore
            store = TodoPostgresStore(conninfo="postgresql://fake/test")

        # _init_schema should have executed SQL to create tables
        assert mock_cursor.execute.called
        calls_sql = " ".join(str(c) for c in mock_cursor.execute.call_args_list)
        assert "chatkit_threads" in calls_sql
        assert "chatkit_items" in calls_sql
