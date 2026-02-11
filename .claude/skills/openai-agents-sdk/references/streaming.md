# OpenAI Agents SDK — Streaming

Source: openai/openai-agents-python (Context7, benchmark 89.9, High reputation)

---

## Overview

`Runner.run_streamed()` returns a `RunResultStreaming` object. Iterate with `.stream_events()` to receive events as they're produced.

```python
from agents import Runner, ItemHelpers

result = Runner.run_streamed(agent, "input text", context=ctx)

async for event in result.stream_events():
    # process events here
    pass

# After stream completes, access full result
print(result.final_output)
print(result.new_items)
```

---

## Event Types

Three event types from `.stream_events()`:

| Event Type | `event.type` value | When It Fires | Use For |
|------------|-------------------|---------------|---------|
| Raw response | `"raw_response_event"` | Every LLM token delta | Token-level streaming to UI |
| Run item | `"run_item_stream_event"` | When an item is fully complete | Progress updates (message done, tool called) |
| Agent updated | `"agent_updated_stream_event"` | When a handoff occurs | Multi-agent UI updates |

---

## Pattern 1: Token Streaming (Chat UI)

Stream each text token as it arrives — best for chat interfaces:

```python
from agents import Runner

result = Runner.run_streamed(agent, user_input)

async for event in result.stream_events():
    if event.type == "raw_response_event":
        data = event.data
        # OpenAI Responses API delta format
        if hasattr(data, "type") and data.type == "response.output_text.delta":
            print(data.delta, end="", flush=True)

print()  # newline after stream
```

---

## Pattern 2: Item-Level Streaming (Progress Tracking)

React to complete items — best for tool call monitoring and progress:

```python
from agents import Runner, ItemHelpers

result = Runner.run_streamed(agent, user_input)

async for event in result.stream_events():
    if event.type == "raw_response_event":
        continue  # skip low-level deltas

    elif event.type == "agent_updated_stream_event":
        # A handoff occurred
        print(f"[Switched to agent: {event.new_agent.name}]")

    elif event.type == "run_item_stream_event":
        item = event.item
        if item.type == "tool_call_item":
            print(f"[Calling tool: {item.name}]")
        elif item.type == "tool_call_output_item":
            print(f"[Tool result: {item.output[:100]}]")
        elif item.type == "message_output_item":
            text = ItemHelpers.text_message_output(item)
            print(f"[Assistant]: {text}")
```

---

## Pattern 3: FastAPI Streaming Endpoint

Stream agent output via Server-Sent Events (SSE) to a frontend:

```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from agents import Agent, Runner, ItemHelpers
import json

app = FastAPI()
agent = Agent(name="Assistant", instructions="Be helpful.", model="gpt-4o-mini")

@app.post("/stream")
async def stream_agent(request: Request):
    body = await request.json()
    user_input = body.get("message", "")

    async def event_generator():
        result = Runner.run_streamed(agent, user_input)
        async for event in result.stream_events():
            if event.type == "raw_response_event":
                data = event.data
                if hasattr(data, "type") and data.type == "response.output_text.delta":
                    payload = json.dumps({"type": "delta", "text": data.delta})
                    yield f"data: {payload}\n\n"

            elif event.type == "run_item_stream_event":
                if event.item.type == "message_output_item":
                    text = ItemHelpers.text_message_output(event.item)
                    payload = json.dumps({"type": "message_complete", "text": text})
                    yield f"data: {payload}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

---

## Pattern 4: ChatKit Server Integration

When using the `chatkit-server` skill, stream via `stream_agent_response`:

```python
from chatkit.agents import AgentContext, Runner as ChatKitRunner, stream_agent_response, simple_to_agent_input
from agents import Agent

assistant = Agent(
    name="Assistant",
    instructions="Be helpful.",
    model="gpt-4o-mini",
)

# In ChatKitServer.respond():
async def respond(self, thread, input_user_message, context):
    items_page = await self.store.load_thread_items(thread.id, after=None, limit=20, order="asc", context=context)
    input_items = await simple_to_agent_input(items_page.data)
    agent_context = AgentContext(thread=thread, store=self.store, request_context=context)
    result = ChatKitRunner.run_streamed(assistant, input_items, context=agent_context)
    async for event in stream_agent_response(agent_context, result):
        yield event
```

---

## RunResultStreaming Properties

After the stream completes:

```python
result = Runner.run_streamed(agent, input)
async for event in result.stream_events():
    pass  # consume stream first

# Then access:
result.final_output          # str or output_type instance
result.new_items             # list[RunItem] — all items generated this run
result.last_agent            # Agent that produced final output
result.input                 # original input
result.is_complete           # True after stream ends
```

---

## ItemHelpers

```python
from agents import ItemHelpers

# Extract plain text from a message output item
text = ItemHelpers.text_message_output(item)

# Concatenate text across all message items
full_text = ItemHelpers.text_message_outputs(result.new_items)

# Extract input text from input items
input_text = ItemHelpers.input_to_new_input_list(result.input)
```
