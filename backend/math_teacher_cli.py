#!/usr/bin/env python
"""
Simple CLI to test the Math Teacher Agent.

Usage:
    python math_teacher_cli.py
    > What is addition?
    > How do I multiply large numbers?
    > Explain division
    > exit

Requirements:
    - OPENROUTER_API_KEY environment variable set
    - openai-agents package installed
"""

import asyncio
import sys
from src.agents import explain_math


async def main():
    """Interactive CLI for the math teacher agent."""
    print("=" * 60)
    print("🎓 Math Teacher Agent - Interactive CLI")
    print("=" * 60)
    print("\nType your math questions below. Type 'exit' to quit.\n")

    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit", "q"):
                print("Goodbye! Keep learning math! 👋")
                break

            # Ask the math teacher
            print("\n🤔 Math Teacher is thinking...\n")
            result = await explain_math(user_input)

            # Display the response
            print("-" * 60)
            print(f"📚 Concept: {result.concept}")
            print(f"\n📖 Explanation:\n{result.explanation}")
            print(f"\n✨ Example:\n{result.example}")
            print(f"\n💡 Tip:\n{result.tip}")
            print("-" * 60)
            print()

        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye! 👋")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print("\nMake sure OPENROUTER_API_KEY is set in your .env file")
            print("Get a free key at: https://openrouter.ai\n")


if __name__ == "__main__":
    asyncio.run(main())
