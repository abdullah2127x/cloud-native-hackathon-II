# Research: Agent MCP Integration

**Feature**: 006-agent-mcp-integration
**Date**: 2026-02-11

---

## Decision 1: How to Wire the MCP Server to the OpenAI Agents SDK

**Decision**: Wrap each MCP tool as an OpenAI Agents SDK `@function_tool`, internally calling `server.call_tool()`.

**Rationale**: The existing `TodoMCPServer` is not a stdio-transport MCP server — it is a Python class with a `call_tool(name, arguments, session)` method. The OpenAI Agents SDK supports attaching MCP servers via `MCPServerStdio` or via function tools. Since the MCP server is in-process and already tested, wrapping each tool as a function tool is the simplest, most testable pattern. It avoids subprocess/transport overhead and allows passing the DB session directly.

**Alternatives considered**:
- `MCPServerStdio`: Would require launching a subprocess, stdio piping, and serialization overhead. Overkill for an in-process server. Rejected.
- Direct DB access from agent: Prohibited by constitution (XII: "MCP Server MUST be the only interface between AI agent and application logic").

---

## Decision 2: Agent Construction Pattern + RunContextWrapper

**Decision**: Use `RunContextWrapper[AppContext]` for dependency injection (DB session + user_id) into each function tool. This is the SDK's official mechanism — NOT closures.

**Rationale**: Verified from `references/core-agents.md`. `RunContextWrapper` is the correct way to inject request-scoped dependencies (DB session, user_id) into tools. It is **local only** — never sent to the LLM. The context is passed via `context=ctx` to `Runner.run()`.

**Verified Pattern** (from `references/core-agents.md`):
```python
from dataclasses import dataclass
from agents import Agent, Runner, RunContextWrapper, function_tool

@dataclass
class TodoContext:
    user_id: str
    session: Session   # SQLModel sync session — NOT sent to LLM

@function_tool
def add_task(
    wrapper: RunContextWrapper[TodoContext],
    title: str,
    description: str | None = None,
) -> str:
    """Create a new task for the current user. Use when user wants to add, create, or remember a task."""
    response = asyncio.run(
        mcp_server.call_tool("add_task", {
            "user_id": wrapper.context.user_id,
            "title": title,
            "description": description,
        }, session=wrapper.context.session)
    )
    # Extract clean response — don't return raw MCP dict
    if response.get("isError"):
        return response["content"][0]["text"]
    return f"Created task: {response['structuredContent']['title']} (ID: {response['structuredContent']['task_id']})"

# Runner call with context + max_turns (required in production)
ctx = TodoContext(user_id=user_id, session=session)
result = await Runner.run(agent, messages, context=ctx, max_turns=10, run_config=run_config)
response_text = result.final_output
```

**Key rules from skill**:
- First param `wrapper: RunContextWrapper[TodoContext]` → injects context (not sent to LLM)
- All other params → schema sent to LLM (use type annotations + descriptive docstrings)
- `max_turns=10` — always set in production (raises `MaxTurnsExceeded` if exceeded)
- `agent.clone(instructions=f"...")` can inject per-request user info into system prompt

**Alternatives considered**:
- Closures for session injection: Works but not idiomatic SDK pattern. Rejected in favour of RunContextWrapper.
- Persistent agent across requests: Would require in-memory state, violating stateless constraint (Constitution IX). Rejected.

---

## Decision 3: Message History Format for Agent Context

**Decision**: Load the last 50 messages from DB, convert each to a dict with `{"role": "user"|"assistant", "content": "..."}`, prepend the system prompt, and pass the full list as the `input` to `Runner.run()`.

**Rationale**: The OpenAI Agents SDK `Runner.run()` accepts a list of message dicts as input. This matches the DB storage format (role + content). The 50-message cap (from spec clarification) prevents context window overflow.

**Alternatives considered**:
- Passing only the new message and using `previous_response_id`: Requires tracking OpenAI response IDs, adds complexity without benefit for our stateless pattern. Rejected.

---

## Decision 4: Conversation ID Type

**Decision**: Integer primary key (auto-incremented), returned as an integer in the API response.

**Rationale**: Consistent with existing Task model pattern (integer IDs). Simpler client-side handling than UUID for a chatbot UI.

---

## Decision 5: Sync vs Async DB Session with Async Agent

**Decision**: Keep the existing synchronous SQLModel `Session` for DB operations. Run agent with `asyncio` by wrapping the sync FastAPI route as `async def` and using `await Runner.run(...)` directly. MCP tool wrappers call the sync DB session synchronously inside the async context.

**Rationale**: The existing DB engine and all CRUD functions are synchronous. Migrating to full async (asyncpg + async SQLModel) is a large refactor outside this feature's scope. The sync DB calls are fast (< 5ms) and won't block the event loop materially for this use case.

**Alternatives considered**:
- Full async migration: Valid long-term improvement, deferred to a future spec.
- `run_in_executor` wrapping: Over-engineering for current scale. Rejected.

---

## Decision 6: OpenRouter Integration

**Decision**: Use `AsyncOpenAI` client with `base_url="https://openrouter.ai/api/v1"` and wrap in `OpenAIChatCompletionsModel`. Pass as `model=` to the `Agent`. **Critically**: use `RunConfig(model=model, model_provider=client, tracing_disabled=True)` — tracing MUST be disabled for non-OpenAI providers to avoid SDK errors.

**Rationale**: Verified against `assets/agent_openrouter.py` in the openai-agents-sdk skill. The `run_config` with `tracing_disabled=True` is required for OpenRouter — without it the SDK attempts to send traces to the OpenAI platform using the wrong API key. The `model_provider=client` tells the SDK which client handles completions.

**Verified Pattern** (from skill `assets/agent_openrouter.py`):
```python
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents.run import RunConfig
from src.config import settings

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.openrouter_api_key,
)

model = OpenAIChatCompletionsModel(
    model=settings.llm_model,
    openai_client=client,
)

# REQUIRED for non-OpenAI providers
run_config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True,
)

agent = Agent(
    name="TodoAgent",
    instructions="You are a todo assistant...",
    tools=[...],
    model=model,
)

result = await Runner.run(agent, messages, run_config=run_config)
response_text = result.final_output
```

**Correction to original plan**: The `run_config` with `tracing_disabled=True` and `model_provider=client` was missing from the initial plan. This is required — implementation must include it.
