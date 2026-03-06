# Task: T008 | Spec: specs/007-chatkit-ui-integration/spec.md
"""TodoChatKitServer — ChatKit streaming server backed by the 5 MCP todo tools."""
from typing import AsyncIterator
from dataclasses import dataclass

from agents import Agent, Runner, function_tool, RunContextWrapper
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from agents.run import RunConfig
from agents.model_settings import ModelSettings
from openai import AsyncOpenAI

from chatkit.server import ChatKitServer, ThreadMetadata, UserMessageItem, ThreadStreamEvent
from chatkit.agents import AgentContext, simple_to_agent_input, stream_agent_response

from src.chatkit.store import TodoPostgresStore, ChatKitRequestContext
from src.config import settings
from mcpserver.mcp_server import TodoMCPServer

# ---------------------------------------------------------------------------
# Module-level shared instances
# ---------------------------------------------------------------------------

todo_postgres_store = TodoPostgresStore()

mcp_server = TodoMCPServer()

# Lazily initialized — avoids AuthenticationError when api_key is None in tests
openai_client: AsyncOpenAI | None = None
_chatkit_model: OpenAIChatCompletionsModel | None = None


def _get_openai_client() -> AsyncOpenAI:
    global openai_client
    if openai_client is None:
        openai_client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.openrouter_api_key,
        )
    return openai_client


def _get_chatkit_model() -> OpenAIChatCompletionsModel:
    global _chatkit_model
    if _chatkit_model is None:
        _chatkit_model = OpenAIChatCompletionsModel(
            model=settings.llm_model,
            openai_client=_get_openai_client(),
        )
    return _chatkit_model

_SYSTEM_PROMPT = (
    "You are a helpful todo assistant. You help users manage their task list using "
    "natural language. You can create, list, complete, update, and delete tasks. "
    "Always use the available tools to perform task operations. "
    "If the user asks about something unrelated to todo management, politely explain "
    "that you specialise in task management and offer to help with their tasks."
)


# ---------------------------------------------------------------------------
# Tool adapter functions
# Bridge RunContextWrapper[AgentContext] → mcp_server.call_tool() via request_context
# ---------------------------------------------------------------------------

@function_tool
async def add_task_adapted(
    ctx: RunContextWrapper[AgentContext],
    title: str,
    description: str | None = None,
) -> str:
    """Create a new task for the current user. Use when the user wants to add,
    create, or remember a task. Returns the created task ID and title."""
    rctx: ChatKitRequestContext = ctx.context.request_context
    response = await mcp_server.call_tool(
        "add_task",
        {"user_id": rctx.user_id, "title": title, "description": description},
        session=rctx.session,
    )
    if response.get("isError"):
        return response["content"][0]["text"]
    sc = response.get("structuredContent", {})
    return f"Created task: '{sc.get('title', title)}' (ID: {sc.get('task_id', '?')})"


@function_tool
async def list_tasks_adapted(
    ctx: RunContextWrapper[AgentContext],
    status: str = "all",
) -> str:
    """List the current user's tasks. status can be 'all', 'pending', or 'completed'.
    Use when the user asks to see, show, or list their tasks."""
    rctx: ChatKitRequestContext = ctx.context.request_context
    response = await mcp_server.call_tool(
        "list_tasks",
        {"user_id": rctx.user_id, "status": status},
        session=rctx.session,
    )
    if response.get("isError"):
        return response["content"][0]["text"]
    sc = response.get("structuredContent", {})
    tasks = sc.get("tasks", [])
    if not tasks:
        return "You have no tasks."
    lines = [
        f"- [{t.get('id')}] {t.get('title')} ({'done' if t.get('completed') else 'pending'})"
        for t in tasks
    ]
    return f"Your tasks ({sc.get('total', len(tasks))} total):\n" + "\n".join(lines)


@function_tool
async def complete_task_adapted(
    ctx: RunContextWrapper[AgentContext],
    task_id: int,
) -> str:
    """Toggle completion status of a task. Use when the user wants to mark a task
    as done, complete, or finished — or undo completion."""
    rctx: ChatKitRequestContext = ctx.context.request_context
    response = await mcp_server.call_tool(
        "complete_task",
        {"user_id": rctx.user_id, "task_id": task_id},
        session=rctx.session,
    )
    if response.get("isError"):
        return response["content"][0]["text"]
    sc = response.get("structuredContent", {})
    state = "completed" if sc.get("completed") else "marked pending"
    return f"Task '{sc.get('title', task_id)}' (ID: {task_id}) {state}."


@function_tool
async def update_task_adapted(
    ctx: RunContextWrapper[AgentContext],
    task_id: int,
    title: str | None = None,
    description: str | None = None,
) -> str:
    """Update a task's title or description. Use when the user wants to change,
    rename, or edit an existing task. Provide at least one of title or description."""
    rctx: ChatKitRequestContext = ctx.context.request_context
    response = await mcp_server.call_tool(
        "update_task",
        {
            "user_id": rctx.user_id,
            "task_id": task_id,
            "title": title,
            "description": description,
        },
        session=rctx.session,
    )
    if response.get("isError"):
        return response["content"][0]["text"]
    sc = response.get("structuredContent", {})
    return f"Updated task (ID: {task_id}) — new title: '{sc.get('title', title)}'."


@function_tool
async def delete_task_adapted(
    ctx: RunContextWrapper[AgentContext],
    task_id: int,
) -> str:
    """Permanently delete a task. Use when the user wants to remove or delete a task.
    This action cannot be undone."""
    rctx: ChatKitRequestContext = ctx.context.request_context
    response = await mcp_server.call_tool(
        "delete_task",
        {"user_id": rctx.user_id, "task_id": task_id},
        session=rctx.session,
    )
    if response.get("isError"):
        return response["content"][0]["text"]
    sc = response.get("structuredContent", {})
    return f"Deleted task '{sc.get('title', task_id)}' (ID: {task_id})."


_TODO_TOOLS = [
    add_task_adapted,
    list_tasks_adapted,
    complete_task_adapted,
    update_task_adapted,
    delete_task_adapted,
]


# ---------------------------------------------------------------------------
# TodoChatKitServer
# ---------------------------------------------------------------------------

class TodoChatKitServer(ChatKitServer[ChatKitRequestContext]):
    """ChatKit server that streams todo agent responses via SSE."""

    async def respond(
        self,
        thread: ThreadMetadata,
        input_user_message: UserMessageItem | None,
        context: ChatKitRequestContext,
    ) -> AsyncIterator[ThreadStreamEvent]:
        # Load last 20 items in chronological order for agent context
        items_page = await todo_postgres_store.load_thread_items(
            thread.id, after=None, limit=20, order="asc", context=context
        )

        # Convert ChatKit items → agent SDK input format
        input_items = await simple_to_agent_input(items_page.data)

        # Resolve lazy instances
        model = _get_chatkit_model()
        client = _get_openai_client()

        # Build a fresh Agent with 5 adapted tools per request
        assistant = Agent(
            name="TodoAgent",
            instructions=_SYSTEM_PROMPT,
            tools=_TODO_TOOLS,
            model=model,
        )

        # Create AgentContext carrying our request context
        agent_context = AgentContext(
            thread=thread,
            store=todo_postgres_store,
            request_context=context,
        )

        # Run streamed → yield ChatKit SSE events
        run_config = RunConfig(
            model=model,
            model_provider=client,
            tracing_disabled=True,
            model_settings=ModelSettings(max_tokens=1024),
        )
        result = Runner.run_streamed(
            assistant, input_items, context=agent_context, run_config=run_config
        )
        async for event in stream_agent_response(agent_context, result):
            yield event
