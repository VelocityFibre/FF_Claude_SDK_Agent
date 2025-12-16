#!/usr/bin/env python3
"""
Claude Agent SDK Example - Python
Demonstrates agentic workflows with continuous conversations, tool use, and streaming.
"""

import os
from anthropic import Anthropic
from typing import List, Dict, Any
import json


class ClaudeAgent:
    """
    A wrapper class for Claude's agent capabilities.
    Manages continuous conversations with context persistence.
    """

    def __init__(self, model: str = "claude-3-haiku-20240307"):
        """
        Initialize the Claude agent.

        Args:
            model: The Claude model to use (default: Sonnet 3.5)
                   Available models:
                   - claude-3-5-sonnet-20241022 (latest)
                   - claude-3-5-sonnet-20240620
                   - claude-3-haiku-20240307 (fastest, cheapest)
                   - claude-3-opus-20240229 (most capable)
        """
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.conversation_history: List[Dict[str, Any]] = []
        self.max_tokens = 4096

    def define_tools(self) -> List[Dict[str, Any]]:
        """
        Define custom tools for the agent to use.
        This is where you can integrate external APIs, databases, etc.
        """
        return [
            {
                "name": "get_weather",
                "description": "Get the current weather in a given location. Returns temperature and conditions.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "The unit of temperature"
                        }
                    },
                    "required": ["location"]
                }
            },
            {
                "name": "search_database",
                "description": "Search a database for information. Simulates a database query.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query"
                        },
                        "table": {
                            "type": "string",
                            "description": "The table to search in"
                        }
                    },
                    "required": ["query", "table"]
                }
            },
            {
                "name": "execute_code",
                "description": "Execute Python code and return the result. Use for calculations or data processing.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "The Python code to execute"
                        }
                    },
                    "required": ["code"]
                }
            }
        ]

    def execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """
        Execute a tool call. This is where you implement the actual tool logic.
        In production, you'd connect to real APIs, databases, etc.
        """
        if tool_name == "get_weather":
            location = tool_input.get("location", "Unknown")
            unit = tool_input.get("unit", "fahrenheit")
            # Simulated response
            return json.dumps({
                "location": location,
                "temperature": 72 if unit == "fahrenheit" else 22,
                "unit": unit,
                "conditions": "Partly cloudy"
            })

        elif tool_name == "search_database":
            query = tool_input.get("query", "")
            table = tool_input.get("table", "")
            # Simulated response
            return json.dumps({
                "results": [
                    {"id": 1, "name": "Example Item", "query": query, "table": table}
                ],
                "count": 1
            })

        elif tool_name == "execute_code":
            code = tool_input.get("code", "")
            try:
                # WARNING: In production, use a sandboxed environment!
                result = eval(code)
                return json.dumps({"result": result, "success": True})
            except Exception as e:
                return json.dumps({"error": str(e), "success": False})

        return json.dumps({"error": f"Unknown tool: {tool_name}"})

    def chat(self, user_message: str, stream: bool = False) -> str:
        """
        Send a message to the agent and get a response.
        Maintains conversation context automatically.

        Args:
            user_message: The user's message
            stream: Whether to stream the response

        Returns:
            The agent's response
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        tools = self.define_tools()

        # Continue the conversation with tool use
        while True:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=self.conversation_history,
                tools=tools
            )

            # Add assistant's response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response.content
            })

            # Check if Claude wants to use a tool
            if response.stop_reason == "tool_use":
                # Find tool use blocks
                tool_uses = [block for block in response.content if block.type == "tool_use"]

                if not tool_uses:
                    break

                # Execute each tool
                tool_results = []
                for tool_use in tool_uses:
                    print(f"🔧 Tool called: {tool_use.name}")
                    print(f"   Input: {tool_use.input}")

                    result = self.execute_tool(tool_use.name, tool_use.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": result
                    })
                    print(f"   Result: {result}\n")

                # Add tool results to history
                self.conversation_history.append({
                    "role": "user",
                    "content": tool_results
                })

                # Continue conversation with tool results
                continue

            # Extract text response
            text_blocks = [block.text for block in response.content if hasattr(block, 'text')]
            return "\n".join(text_blocks)

    def reset_conversation(self):
        """Clear the conversation history."""
        self.conversation_history = []


def example_basic_agent():
    """Example 1: Basic agent with tool use"""
    print("=" * 60)
    print("Example 1: Basic Agent with Tool Use")
    print("=" * 60 + "\n")

    agent = ClaudeAgent()

    # Simple question that might trigger tool use
    response = agent.chat("What's the weather like in San Francisco? Also, calculate 15 * 23 for me.")
    print(f"Agent: {response}\n")


def example_continuous_conversation():
    """Example 2: Continuous conversation with context"""
    print("=" * 60)
    print("Example 2: Continuous Conversation")
    print("=" * 60 + "\n")

    agent = ClaudeAgent()

    # Multi-turn conversation
    response1 = agent.chat("I'm planning a trip to New York. Can you help me?")
    print(f"Agent: {response1}\n")

    response2 = agent.chat("What's the weather like there?")
    print(f"Agent: {response2}\n")

    response3 = agent.chat("Based on that, what should I pack?")
    print(f"Agent: {response3}\n")


def example_research_agent():
    """Example 3: Research agent that uses multiple tools"""
    print("=" * 60)
    print("Example 3: Research Agent")
    print("=" * 60 + "\n")

    agent = ClaudeAgent()

    response = agent.chat(
        "I need to research the best practices for API design. "
        "Search the database for 'REST API' in the 'documentation' table, "
        "and help me understand the results."
    )
    print(f"Agent: {response}\n")


def main():
    """Run all examples"""
    print("\n🤖 Claude Agent SDK - Python Examples\n")

    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("Please set it with: export ANTHROPIC_API_KEY='your-api-key-here'")
        return

    print("Running examples...\n")

    try:
        example_basic_agent()
        example_continuous_conversation()
        example_research_agent()

        print("=" * 60)
        print("✅ All examples completed!")
        print("=" * 60)

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
