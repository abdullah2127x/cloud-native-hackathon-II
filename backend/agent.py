#!/usr/bin/env python3
"""AI Agent for todo management using MCP with Gemini provider."""

import asyncio
import sys

# Windows event loop setup
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Runner,
    set_tracing_disabled,
)
from agents.mcp import MCPServerStreamableHttp

# Import settings from backend config
from src.core.config import settings

set_tracing_disabled(True)

# ── Model Setup (Gemini via OpenAI-compatible API) ──
if not settings.gemini_api_key:
    print("❌ Error: GEMINI_API_KEY not set in .env file")
    print("   Get your API key from: https://aistudio.google.com/apikey")
    sys.exit(1)

# Gemini via OpenAI-compatible endpoint (using OpenRouter or direct Gemini API)
GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta/openai/"
MODEL_ID = "gemini-2.5-flash"

client = AsyncOpenAI(api_key=settings.gemini_api_key, base_url=GEMINI_API_BASE)
model = OpenAIChatCompletionsModel(model=MODEL_ID, openai_client=client)


# ── JWT Token Management ──
# The agent receives the JWT token from the frontend via user input
# It passes this token to the MCP server for authentication
JWT_TOKEN = None  # Will be set from user context or session


def set_jwt_token(token: str):
    """Set the JWT token for MCP server communication."""
    global JWT_TOKEN
    JWT_TOKEN = token
    print(f"🔐 JWT token configured for authenticated MCP calls")


async def main(jwt_token: str = None):
    """Run the todo agent.

    Args:
        jwt_token: JWT Bearer token for authenticated MCP calls.
                   If not provided, agent will use hardcoded token (for testing only).
    """
    import os

    # Set JWT token for MCP authentication
    if jwt_token:
        set_jwt_token(jwt_token)
    else:
        # For testing: use token from environment (NEVER in production!)
        test_token = os.getenv("TEST_JWT_TOKEN")
        if test_token:
            set_jwt_token(test_token)
        else:
            print("⚠️  Warning: No JWT token provided. Using HTTP MCP without auth.")
            print("   In production, JWT token should come from frontend/session.")

    # Create HTTP MCP server connection
    # The MCP HTTP server must be running on port 8001
    mcp_server = MCPServerStreamableHttp(
        # name="todo-mcp-http",
        # params={
        #     "url": "http://localhost:8001",
        #     "headers": {"Authorization": f"Bearer {JWT_TOKEN}" if JWT_TOKEN else ""},
        # } if JWT_TOKEN else {}
        name="todo-mcp-http",
        params={
            "url": "http://localhost:8001",
            "headers": {"Authorization": f"Bearer {JWT_TOKEN}" if JWT_TOKEN else ""},
        },
    )

    print("🔌 Connecting to HTTP MCP server at http://localhost:8001...")

    try:
        async with mcp_server:
            print("✅ Connected to todo MCP HTTP server\n")

            # Create agent
            agent = Agent(
                name="Assistant",
                instructions="Helpful Assistant",
                mcp_servers=[mcp_server],
                model=model,
            )

            print("=" * 60)
            print("📝 TODO ASSISTANT")
            print("=" * 60)
            print("Chat with the assistant to manage your todos.")
            print("Type 'quit' or 'exit' to stop.\n")

            # Main loop
            while True:
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ("quit", "exit"):
                    print("👋 Goodbye!")
                    break

                try:
                    print("\n🤔 Thinking...", end="", flush=True)
                    result = await Runner.run(agent, user_input, max_turns=10)
                    print(
                        "\r" + " " * 20 + "\r", end="", flush=True
                    )  # Clear "Thinking..."
                    print(f"Assistant: {result.final_output}\n")

                except Exception as e:
                    print(f"\n⚠️ Error: {type(e).__name__}: {str(e)}\n")

    except Exception as e:
        print(f"❌ Failed to connect to MCP server: {e}")
        print("Make sure todo_mcp_server.py is accessible and Python is in PATH.")


if __name__ == "__main__":
    import os

    # In production, get JWT token from:
    # 1. Frontend session (passed via API)
    # 2. Environment variable (for testing)
    # 3. Command line argument (for CLI)

    jwt_token = settings.jwt_token

    try:
        asyncio.run(main(jwt_token=jwt_token))
    except KeyboardInterrupt:
        print("\n\n👋 Agent stopped by user")
