# Task: T007 | Spec: specs/007-chatkit-ui-integration/spec.md
"""Unit tests for TodoChatKitServer.respond() (TDD — written before T008 implementation)."""
import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from collections.abc import AsyncIterator

from chatkit.types import ThreadMetadata, AssistantMessageItem, Page
from chatkit.agents import AgentContext

from src.chatkit.store import ChatKitRequestContext


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_thread(thread_id: str = "t-1") -> ThreadMetadata:
    return ThreadMetadata(id=thread_id, created_at=datetime.now(timezone.utc))


def _make_context(user_id: str = "user-1") -> ChatKitRequestContext:
    return ChatKitRequestContext(user_id=user_id, session=MagicMock())


def _make_item(item_id: str, thread_id: str = "t-1") -> AssistantMessageItem:
    return AssistantMessageItem(
        id=item_id,
        thread_id=thread_id,
        created_at=datetime.now(timezone.utc),
        content=[{"type": "output_text", "text": f"message {item_id}"}],
    )


async def _fake_stream_events(*events):
    for e in events:
        yield e


# ---------------------------------------------------------------------------
# T007: TodoChatKitServer.respond() unit tests
# ---------------------------------------------------------------------------

class TestTodoChatKitServerRespond:
    """Tests for TodoChatKitServer.respond() with mocked store and agent runner."""

    @pytest.fixture(autouse=True)
    def mock_store_and_client(self):
        """Mock module-level store and OpenAI client so no external connections needed."""
        item1 = _make_item("item-1")
        item2 = _make_item("item-2")
        mock_store = MagicMock()
        mock_store.load_thread_items = AsyncMock(
            return_value=Page(data=[item1, item2], has_more=False, after=None)
        )
        mock_model = MagicMock()
        with patch("src.chatkit.server.todo_postgres_store", mock_store), \
             patch("src.chatkit.server._get_chatkit_model", return_value=mock_model), \
             patch("src.chatkit.server._get_openai_client", return_value=MagicMock()):
            self._mock_store = mock_store
            yield mock_store

    @pytest.fixture
    def server(self):
        from src.chatkit.server import TodoChatKitServer
        from src.chatkit.store import TodoPostgresStore
        mock_store = MagicMock(spec=TodoPostgresStore)
        mock_store.load_thread_items = AsyncMock(
            return_value=Page(data=[], has_more=False, after=None)
        )
        return TodoChatKitServer(store=mock_store)

    def _agent_patches(self):
        """Common patch set for respond() tests."""
        return (
            patch("src.chatkit.server.simple_to_agent_input", new_callable=AsyncMock, return_value=[]),
            patch("src.chatkit.server.Agent"),
            patch("src.chatkit.server.Runner"),
            patch("src.chatkit.server.stream_agent_response"),
        )

    @pytest.mark.asyncio
    async def test_respond_calls_load_thread_items(self, mock_store_and_client, server):
        """respond() calls store.load_thread_items with thread.id and context."""
        thread = _make_thread("t-1")
        ctx = _make_context()

        with patch("src.chatkit.server.simple_to_agent_input", new_callable=AsyncMock, return_value=[]), \
             patch("src.chatkit.server.Agent"), \
             patch("src.chatkit.server.Runner") as mock_runner, \
             patch("src.chatkit.server.stream_agent_response") as mock_sar:

            mock_runner.run_streamed.return_value = MagicMock()
            mock_sar.return_value = _fake_stream_events(MagicMock())

            result = server.respond(thread, None, ctx)
            _ = [e async for e in result]

        mock_store_and_client.load_thread_items.assert_awaited_once_with(
            "t-1", after=None, limit=20, order="asc", context=ctx
        )

    @pytest.mark.asyncio
    async def test_respond_calls_simple_to_agent_input(self, mock_store_and_client, server):
        """respond() passes thread items to simple_to_agent_input."""
        thread = _make_thread("t-1")
        ctx = _make_context()

        with patch("src.chatkit.server.simple_to_agent_input", new_callable=AsyncMock, return_value=[]) as mock_sti, \
             patch("src.chatkit.server.Agent"), \
             patch("src.chatkit.server.Runner") as mock_runner, \
             patch("src.chatkit.server.stream_agent_response") as mock_sar:

            mock_runner.run_streamed.return_value = MagicMock()
            mock_sar.return_value = _fake_stream_events()

            result = server.respond(thread, None, ctx)
            _ = [e async for e in result]

        assert mock_sti.called

    @pytest.mark.asyncio
    async def test_respond_yields_stream_events(self, mock_store_and_client, server):
        """respond() yields events from stream_agent_response."""
        thread = _make_thread("t-1")
        ctx = _make_context()
        event_a, event_b = MagicMock(), MagicMock()

        with patch("src.chatkit.server.simple_to_agent_input", new_callable=AsyncMock, return_value=[]), \
             patch("src.chatkit.server.Agent"), \
             patch("src.chatkit.server.Runner") as mock_runner, \
             patch("src.chatkit.server.stream_agent_response") as mock_sar:

            mock_runner.run_streamed.return_value = MagicMock()
            mock_sar.return_value = _fake_stream_events(event_a, event_b)

            result = server.respond(thread, None, ctx)
            events = [e async for e in result]

        assert events == [event_a, event_b]

    @pytest.mark.asyncio
    async def test_respond_creates_agent_with_5_tools(self, mock_store_and_client, server):
        """respond() creates an Agent called with exactly 5 tools."""
        thread = _make_thread("t-1")
        ctx = _make_context()

        with patch("src.chatkit.server.simple_to_agent_input", new_callable=AsyncMock, return_value=[]), \
             patch("src.chatkit.server.Agent") as mock_agent_cls, \
             patch("src.chatkit.server.Runner") as mock_runner, \
             patch("src.chatkit.server.stream_agent_response") as mock_sar:

            mock_runner.run_streamed.return_value = MagicMock()
            mock_sar.return_value = _fake_stream_events()

            result = server.respond(thread, None, ctx)
            _ = [e async for e in result]

        assert mock_agent_cls.called
        _, kwargs = mock_agent_cls.call_args
        tools_passed = kwargs.get("tools", [])
        assert len(tools_passed) == 5


# ---------------------------------------------------------------------------
# T007 extra: Module-level instances exist
# ---------------------------------------------------------------------------

class TestModuleLevelInstances:
    def test_todo_postgres_store_instance_exists(self):
        """src.chatkit.server has a module-level todo_postgres_store instance."""
        with patch("src.chatkit.store.psycopg.connect") as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
            mock_cursor.__exit__ = MagicMock(return_value=False)
            mock_conn_inst = MagicMock()
            mock_conn_inst.__enter__ = MagicMock(return_value=mock_conn_inst)
            mock_conn_inst.__exit__ = MagicMock(return_value=False)
            mock_conn_inst.cursor = MagicMock(return_value=mock_cursor)
            mock_conn.return_value = mock_conn_inst

            import importlib
            import src.chatkit.server as server_mod
            assert hasattr(server_mod, "todo_postgres_store")

    def test_openrouter_client_exists(self):
        """src.chatkit.server has a module-level openai_client instance."""
        import src.chatkit.server as server_mod
        assert hasattr(server_mod, "openai_client")
