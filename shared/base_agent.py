#!/usr/bin/env python3
"""
Base Agent Class - Shared functionality for all Claude agents

This module provides the BaseAgent class that eliminates code duplication
across all agent implementations. It handles:
- Claude API initialization
- Conversation history management
- Tool-calling loop logic
- Domain memory management (persistent state)
- Common agent patterns

All specialized agents (VPS Monitor, Database, etc.) should inherit from this class.

Domain Memory Philosophy:
"The magic is in the memory. The agent is a policy that transforms one
consistent memory state into another."

Each agent can optionally implement persistent state that survives across
sessions. This prevents agents from being "amnesiacs with tool belts."

Resolves: DEBT-003 (Duplicate Agent Pattern Code)
"""

from typing import List, Dict, Any, Optional
from anthropic import Anthropic
from abc import ABC, abstractmethod
import json
import os
from pathlib import Path


class BaseAgent(ABC):
    """
    Abstract base class for all Claude-powered agents.

    Provides common functionality:
    - Anthropic client initialization
    - Conversation history management
    - Tool execution loop
    - Response handling

    Subclasses must implement:
    - define_tools(): Return list of available tools
    - execute_tool(): Execute a specific tool
    - get_system_prompt(): Return agent-specific system prompt
    """

    def __init__(
        self,
        anthropic_api_key: str,
        model: str = "claude-3-haiku-20240307",
        max_tokens: int = 4096,
        state_file: Optional[str] = None
    ):
        """
        Initialize the base agent.

        Args:
            anthropic_api_key: Anthropic API key for Claude
            model: Claude model to use (default: claude-3-haiku-20240307)
            max_tokens: Maximum tokens per response (default: 4096)
            state_file: Optional path to persistent state JSON file (for domain memory)
        """
        self.anthropic = Anthropic(api_key=anthropic_api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.conversation_history: List[Dict[str, Any]] = []

        # Domain memory (persistent state)
        self.state_file = state_file
        self.state: Dict[str, Any] = {}
        if state_file:
            self.load_state()

    @abstractmethod
    def define_tools(self) -> List[Dict[str, Any]]:
        """
        Define tools available to this agent.

        Each tool is a dictionary with:
        - name: Tool identifier
        - description: What the tool does
        - input_schema: JSON schema for tool parameters

        Returns:
            List of tool definitions

        Example:
            [
                {
                    "name": "get_data",
                    "description": "Retrieve data from source",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"}
                        },
                        "required": ["id"]
                    }
                }
            ]
        """
        raise NotImplementedError("Subclasses must implement define_tools()")

    @abstractmethod
    def execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """
        Execute a specific tool.

        Args:
            tool_name: Name of the tool to execute
            tool_input: Tool parameters

        Returns:
            JSON-serialized result string

        Example:
            if tool_name == "get_data":
                result = fetch_data(tool_input["id"])
                return json.dumps(result)
        """
        raise NotImplementedError("Subclasses must implement execute_tool()")

    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Get agent-specific system prompt.

        Returns:
            System prompt describing agent's role and capabilities

        Example:
            return "You are a VPS monitoring assistant..."
        """
        raise NotImplementedError("Subclasses must implement get_system_prompt()")

    def chat(self, user_message: str, max_turns: int = 10) -> str:
        """
        Process user message and return agent response.

        This method handles the complete tool-calling loop:
        1. Add user message to history
        2. Call Claude with tools
        3. If tool_use: execute tools and continue
        4. If end_turn: return final response

        Args:
            user_message: User's question or command
            max_turns: Maximum conversation turns (default: 10)

        Returns:
            Agent's final response text
        """
        # Add user message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        system_prompt = self.get_system_prompt()
        tools = self.define_tools()

        turn_count = 0
        while turn_count < max_turns:
            turn_count += 1

            # Call Claude API
            response = self.anthropic.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_prompt,
                tools=tools,
                messages=self.conversation_history
            )

            # Handle response based on stop reason
            if response.stop_reason == "end_turn":
                # Extract text response
                final_text = ""
                for block in response.content:
                    if block.type == "text":
                        final_text += block.text

                # Add to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response.content
                })

                return final_text

            elif response.stop_reason == "tool_use":
                # Collect tool use blocks and execute them
                assistant_content = []
                tool_results = []

                for block in response.content:
                    assistant_content.append(block)

                    if block.type == "tool_use":
                        # Execute the tool
                        tool_result = self.execute_tool(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": tool_result
                        })

                # Add assistant's tool use to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": assistant_content
                })

                # Add tool results to history
                self.conversation_history.append({
                    "role": "user",
                    "content": tool_results
                })

                # Continue loop to get next response

            else:
                # Unexpected stop reason
                return f"Unexpected stop reason: {response.stop_reason}"

        return "Maximum conversation turns reached."

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []

    def reset_conversation(self):
        """
        Reset conversation (alias for clear_history).

        Some agents use clear_history(), others use reset_conversation().
        This provides both for compatibility.
        """
        self.clear_history()

    def get_history_length(self) -> int:
        """
        Get number of messages in conversation history.

        Returns:
            Number of messages
        """
        return len(self.conversation_history)

    def get_last_message(self) -> Optional[Dict[str, Any]]:
        """
        Get the most recent message in conversation history.

        Returns:
            Last message dictionary, or None if history is empty
        """
        return self.conversation_history[-1] if self.conversation_history else None

    # Domain Memory Management Methods

    def load_state(self) -> None:
        """
        Load persistent state from disk (domain memory).

        This implements the "bootup ritual" - reading where we are in the world.

        If state_file doesn't exist, initializes empty state.
        Subclasses can override to add custom state initialization.
        """
        if not self.state_file:
            return

        state_path = Path(self.state_file)
        if state_path.exists():
            try:
                with open(state_path, 'r') as f:
                    self.state = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Warning: Could not load state from {self.state_file}: {e}")
                self.state = {}
        else:
            # Initialize empty state
            self.state = self.initialize_state()
            self.save_state()

    def save_state(self) -> None:
        """
        Save persistent state to disk (domain memory).

        Called after each interaction to persist agent's understanding of
        "where we are" for the next session.

        Creates parent directories if they don't exist.
        """
        if not self.state_file:
            return

        state_path = Path(self.state_file)
        state_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(state_path, 'w') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save state to {self.state_file}: {e}")

    def initialize_state(self) -> Dict[str, Any]:
        """
        Initialize empty state structure.

        Subclasses should override this to define domain-specific state schema.

        Returns:
            Dictionary with initial state structure

        Example:
            For a research agent:
            {
                "hypotheses": [],
                "experiments": [],
                "decision_journal": []
            }

            For a project management agent:
            {
                "milestones": [],
                "risks": [],
                "blockers": []
            }
        """
        return {}

    def get_state(self, key: str, default: Any = None) -> Any:
        """
        Get value from persistent state.

        Args:
            key: State key
            default: Default value if key doesn't exist

        Returns:
            State value or default
        """
        return self.state.get(key, default)

    def set_state(self, key: str, value: Any) -> None:
        """
        Set value in persistent state.

        Does NOT automatically save to disk. Call save_state() to persist.

        Args:
            key: State key
            value: State value
        """
        self.state[key] = value

    def update_state(self, updates: Dict[str, Any]) -> None:
        """
        Update multiple state values at once.

        Does NOT automatically save to disk. Call save_state() to persist.

        Args:
            updates: Dictionary of key-value pairs to update
        """
        self.state.update(updates)

    def clear_state(self) -> None:
        """
        Clear all persistent state.

        Resets to initial state structure and saves to disk.
        """
        self.state = self.initialize_state()
        self.save_state()
