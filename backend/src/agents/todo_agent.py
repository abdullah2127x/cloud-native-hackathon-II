# Task: T008/T009 | Spec: specs/006-agent-mcp-integration/spec.md
"""TodoAgent — wraps TodoMCPServer tools as OpenAI Agents SDK function tools."""
from dataclasses import dataclass
from typing import Optional
from sqlmodel import Session

from agents import Agent, Runner, function_tool, RunContextWrapper
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from agents.run import RunConfig
from openai import AsyncOpenAI

from src.config import settings
from mcpserver.mcp_server import TodoMCPServer

# Module-level MCP server instance (shared, stateless)
mcp_server = TodoMCPServer()


@dataclass
class TodoContext:
    """Request-scoped context injected into all tools. Never sent to the LLM."""
    user_id: str
    session: Session


# ---------------------------------------------------------------------------
# Tool implementations — plain async functions (testable directly)
# FunctionTool wrappers are created below via function_tool()
# ---------------------------------------------------------------------------

async def add_task(
    wrapper: RunContextWrapper[TodoContext],
    title: str,
    description: Optional[str] = None,
) -> str:
    """Create a new task for the current user. Use when the user wants to add,
    create, or remember a task. Returns the created task ID and title."""
    response = await mcp_server.call_tool(
        "add_task",
        {"user_id": wrapper.context.user_id, "title": title, "description": description},
        session=wrapper.context.session,
    )
    if response.get("isError"):
        return response["content"][0]["text"]
    sc = response.get("structuredContent", {})
    return f"Created task: '{sc.get('title', title)}' (ID: {sc.get('task_id', '?')})"


async def list_tasks(
    wrapper: RunContextWrapper[TodoContext],
    status: str = "all",
) -> str:
    """List the current user's tasks. status can be 'all', 'pending', or 'completed'.
    Use when the user asks to see, show, or list their tasks."""
    response = await mcp_server.call_tool(
        "list_tasks",
        {"user_id": wrapper.context.user_id, "status": status},
        session=wrapper.context.session,
    )
    if response.get("isError"):
        return response["content"][0]["text"]
    sc = response.get("structuredContent", {})
    tasks = sc.get("tasks", [])
    if not tasks:
        return "You have no tasks."
    lines = [f"- [{t.get('id')}] {t.get('title')} ({'done' if t.get('completed') else 'pending'})" for t in tasks]
    return f"Your tasks ({sc.get('total', len(tasks))} total):\n" + "\n".join(lines)


async def complete_task(
    wrapper: RunContextWrapper[TodoContext],
    task_id: int,
) -> str:
    """Toggle completion status of a task. Use when the user wants to mark a task
    as done, complete, or finished — or undo completion."""
    response = await mcp_server.call_tool(
        "complete_task",
        {"user_id": wrapper.context.user_id, "task_id": task_id},
        session=wrapper.context.session,
    )
    if response.get("isError"):
        return response["content"][0]["text"]
    sc = response.get("structuredContent", {})
    state = "completed" if sc.get("completed") else "marked pending"
    return f"Task '{sc.get('title', task_id)}' (ID: {task_id}) {state}."


async def update_task(
    wrapper: RunContextWrapper[TodoContext],
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
) -> str:
    """Update a task's title or description. Use when the user wants to change,
    rename, or edit an existing task. Provide at least one of title or description."""
    response = await mcp_server.call_tool(
        "update_task",
        {
            "user_id": wrapper.context.user_id,
            "task_id": task_id,
            "title": title,
            "description": description,
        },
        session=wrapper.context.session,
    )
    if response.get("isError"):
        return response["content"][0]["text"]
    sc = response.get("structuredContent", {})
    return f"Updated task (ID: {task_id}) — new title: '{sc.get('title', title)}'."


async def delete_task(
    wrapper: RunContextWrapper[TodoContext],
    task_id: int,
) -> str:
    """Permanently delete a task. Use when the user wants to remove or delete a task.
    This action cannot be undone."""
    response = await mcp_server.call_tool(
        "delete_task",
        {"user_id": wrapper.context.user_id, "task_id": task_id},
        session=wrapper.context.session,
    )
    if response.get("isError"):
        return response["content"][0]["text"]
    sc = response.get("structuredContent", {})
    return f"Deleted task '{sc.get('title', task_id)}' (ID: {task_id})."


# FunctionTool wrappers registered with the agent
_add_task_tool = function_tool(add_task)
_list_tasks_tool = function_tool(list_tasks)
_complete_task_tool = function_tool(complete_task)
_update_task_tool = function_tool(update_task)
_delete_task_tool = function_tool(delete_task)


# ---------------------------------------------------------------------------
# Agent runner
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = (
    "You are a helpful todo assistant. You help users manage their task list using "
    "natural language. You can create, list, complete, update, and delete tasks. "
    "Always use the available tools to perform task operations. "
    "If the user asks about something unrelated to todo management, politely explain "
    "that you specialise in task management and offer to help with their tasks."
)


async def run_todo_agent(
    messages: list[dict],
    user_id: str,
    session: Session,
) -> tuple[str, list[str]]:
    """Run the todo agent and return (response_text, tool_names_called).

    messages: list of {"role": "user"|"assistant", "content": "..."} dicts.
    user_id: authenticated user id.
    session: sync SQLModel session (not sent to the LLM).
    """
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=settings.openrouter_api_key,
    )
    model = OpenAIChatCompletionsModel(
        model=settings.llm_model,
        openai_client=client,
    )
    run_config = RunConfig(
        model=model,
        model_provider=client,
        tracing_disabled=True,
    )
    agent = Agent(
        name="TodoAgent",
        instructions=_SYSTEM_PROMPT,
        tools=[_add_task_tool, _list_tasks_tool, _complete_task_tool, _update_task_tool, _delete_task_tool],
        model=model,
    )
    ctx = TodoContext(user_id=user_id, session=session)
    result = await Runner.run(
        agent,
        messages,
        context=ctx,
        max_turns=10,
        run_config=run_config,
    )
    tool_names = [
        item.tool_name
        for item in result.new_items
        if hasattr(item, "tool_name")
    ]
    return result.final_output, tool_names
