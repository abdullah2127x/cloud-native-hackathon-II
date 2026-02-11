# OpenAI Agents SDK — Custom LLM Providers

Source: learning-openai project analysis (2026-02-11)

---

## Overview

The OpenAI Agents SDK supports any OpenAI-compatible API or provider via `AsyncOpenAI` client + `OpenAIChatCompletionsModel` wrapper. Three proven patterns:

| Provider | Pattern | Cost | Speed | Best For |
|----------|---------|------|-------|----------|
| **Gemini** | AsyncOpenAI + OpenAIChatCompletionsModel | Cheapest | Fast | Prototyping, personal projects |
| **OpenRouter** | AsyncOpenAI + OpenAIChatCompletionsModel | Medium | Varies | Model flexibility, fallbacks |
| **LiteLLM** | Direct LitellmModel wrapper | N/A | Varies | Unified multi-provider interface |

---

## Pattern 1: Gemini (Recommended for Cost)

### Setup

```python
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"  # Fast and cost-effective
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
```

### Create Agent

```python
client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url=BASE_URL
)

model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=client
)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model=model,
)
```

### Run Agent

```python
import asyncio

async def main():
    result = await Runner.run(agent, "Hello!")
    print(result.final_output)

asyncio.run(main())
```

### Available Gemini Models

- `gemini-2.5-flash` (latest, fastest, cheapest)
- `gemini-2.0-flash` (stable, proven)
- `gemini-1.5-pro` (powerful but slower)
- `gemini-1.5-flash` (older)

---

## Pattern 2: OpenRouter (Recommended for Model Choice)

### Setup

```python
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
```

### Choose Model

```python
# Available via OpenRouter:
MODEL = "openai/gpt-4o-mini"           # OpenAI (default)
MODEL = "anthropic/claude-3-5-sonnet"  # Anthropic
MODEL = "google/gemini-2.0-flash"      # Google
MODEL = "meta-llama/llama-3.1-70b"     # Meta
MODEL = "xai/grok-2"                   # xAI

# See https://openrouter.ai/docs/models for all options
```

### Create Agent

```python
client = AsyncOpenAI(
    base_url=BASE_URL,
    api_key=OPENROUTER_API_KEY,
)

model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=client
)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model=model,
)
```

### Run Agent

```python
import asyncio

async def main():
    result = await Runner.run(agent, "Hello!")
    print(result.final_output)

asyncio.run(main())
```

---

## Pattern 3: LiteLLM (Unified Interface)

### Setup

```python
from agents.extensions.models.litellm_model import LitellmModel
from agents import Agent, Runner
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini/gemini-2.5-flash"  # Format: "provider/model-id"
```

### Create Agent

```python
model = LitellmModel(
    model=MODEL,
    api_key=GEMINI_API_KEY,
)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model=model,
)
```

### Run Agent

```python
import asyncio

async def main():
    result = await Runner.run(agent, "Hello!")
    print(result.final_output)

asyncio.run(main())
```

### Available Model Prefixes

- `gemini/` - Google Gemini
- `anthropic/` - Anthropic Claude
- `openai/` - OpenAI GPT models
- `cohere/` - Cohere models
- `replicate/` - Replicate models
- [See LiteLLM docs for complete list](https://docs.litellm.ai/docs/providers)

---

## Pattern 4: Per-Run Provider Override (RunConfig)

Switch providers **per request** without recreating agents:

```python
from agents.run import RunConfig

# Setup two providers
gemini_model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=gemini_client)
openrouter_model = OpenAIChatCompletionsModel(model="openai/gpt-4o-mini", openai_client=openrouter_client)

# Create agent with default Gemini
agent = Agent(name="Assistant", instructions="...", model=gemini_model)

# Run with Gemini
result1 = await Runner.run(agent, "Request 1")

# Override to OpenRouter for second request
config = RunConfig(model=openrouter_model, model_provider=openrouter_client, tracing_disabled=True)
result2 = await Runner.run(agent, "Request 2", run_config=config)

# Back to Gemini
result3 = await Runner.run(agent, "Request 3")
```

---

## Best Practices

| Practice | Why |
|----------|-----|
| **Use `load_dotenv()` first** | Ensures env vars are loaded before Agent creation |
| **Never hardcode API keys** | Always use os.getenv("KEY_NAME") |
| **Wrap AsyncOpenAI in OpenAIChatCompletionsModel** | Ensures compatibility with Agent framework |
| **Disable tracing for non-OpenAI providers** | Built-in tracing only works with OpenAI API; use RunConfig(tracing_disabled=True) |
| **Set timeout for external providers** | Optional but recommended: `client = AsyncOpenAI(..., timeout=30)` |
| **Test with cheap model first** | Use gemini-2.5-flash or gpt-4o-mini for prototyping |

---

## Environment Setup

See `.env.example` in this skill's assets for template.

```bash
# Gemini
GEMINI_API_KEY=your_gemini_api_key_here

# OpenRouter
OPENROUTER_API_KEY=your_openrouter_key_here

# OpenAI (if using OpenAI provider)
OPENAI_API_KEY=sk-proj-...
```

Load in Python:

```python
from dotenv import load_dotenv
import os

load_dotenv()  # Loads from .env file

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

---

## Common Issues

### "Invalid API key"
- Check `.env` file exists in project root
- Verify key is not wrapped in quotes: `GEMINI_API_KEY=abc123` (not `"abc123"`)
- Call `load_dotenv()` BEFORE accessing env vars

### "Timeout connecting to provider"
- Verify internet connection
- Check provider status (https://status.openai.com, https://status.google.com)
- Add timeout config: `AsyncOpenAI(..., timeout=Timeout(30))`

### "Tracing failed"
- This is expected for non-OpenAI providers
- Always use: `RunConfig(tracing_disabled=True)` with Gemini/OpenRouter

### "Model not found"
- For Gemini: check model name matches available version
- For OpenRouter: check model ID at https://openrouter.ai/docs/models
