#!/usr/bin/env python3
"""
Agent Orchestrator - Routes tasks to specialized agents
Acts as the central coordinator for the agent workforce
"""

import json
import os
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path


class AgentOrchestrator:
    """
    Coordinates multiple specialized agents.
    Routes user requests to the appropriate agent based on context.
    """

    def __init__(self, registry_path: str = None):
        """
        Initialize orchestrator with agent registry.

        Args:
            registry_path: Path to registry.json file
        """
        if registry_path is None:
            registry_path = Path(__file__).parent / "registry.json"

        self.registry_path = Path(registry_path)
        self.registry = self._load_registry()
        self.agents = {}  # Cached agent instances

    def _load_registry(self) -> Dict[str, Any]:
        """Load agent registry from JSON file."""
        try:
            with open(self.registry_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Agent registry not found at {self.registry_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid registry JSON: {e}")

    def list_agents(self) -> List[Dict[str, Any]]:
        """
        Get list of all registered agents.

        Returns:
            List of agent information dictionaries
        """
        return self.registry.get("agents", [])

    def get_agent_by_id(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Get agent information by ID.

        Args:
            agent_id: Agent identifier (e.g., 'vps-monitor')

        Returns:
            Agent info dict or None if not found
        """
        for agent in self.registry.get("agents", []):
            if agent["id"] == agent_id:
                return agent
        return None

    def find_agent_for_task(self, task_description: str) -> List[Dict[str, str]]:
        """
        Find best agent(s) for a given task based on keywords.

        Args:
            task_description: User's task/question description

        Returns:
            List of matching agents with confidence scores
        """
        task_lower = task_description.lower()
        matches = []

        for agent in self.registry.get("agents", []):
            score = 0
            matched_triggers = []

            # Check trigger keywords
            for trigger in agent.get("triggers", []):
                if trigger.lower() in task_lower:
                    score += 1
                    matched_triggers.append(trigger)

            if score > 0:
                matches.append({
                    "agent_id": agent["id"],
                    "agent_name": agent["name"],
                    "confidence": score,
                    "matched_keywords": matched_triggers,
                    "description": agent["description"],
                    "path": agent["path"]
                })

        # Sort by confidence (highest first)
        matches.sort(key=lambda x: x["confidence"], reverse=True)

        return matches

    def route_task(self, task_description: str, auto_select: bool = False) -> Dict[str, Any]:
        """
        Route a task to the appropriate agent.

        Args:
            task_description: User's task description
            auto_select: If True, automatically select best agent. If False, return options.

        Returns:
            Routing decision with agent info and confidence
        """
        matches = self.find_agent_for_task(task_description)

        if not matches:
            return {
                "status": "no_match",
                "message": "No specialized agent found for this task",
                "suggestion": "Consider handling with general capabilities or creating new agent"
            }

        if auto_select or len(matches) == 1:
            return {
                "status": "routed",
                "agent": matches[0],
                "alternatives": matches[1:] if len(matches) > 1 else []
            }

        return {
            "status": "multiple_matches",
            "message": "Multiple agents can handle this task",
            "options": matches
        }

    def get_agent_stats(self) -> Dict[str, Any]:
        """Get statistics about the agent workforce."""
        total = self.registry.get("total_agents", 0)
        categories = self.registry.get("agent_categories", {})

        stats = {
            "total_agents": total,
            "active_agents": len([a for a in self.list_agents() if a.get("status") == "active"]),
            "categories": {cat: len(agents) for cat, agents in categories.items()},
            "agent_types": {}
        }

        # Count by type
        for agent in self.list_agents():
            agent_type = agent.get("type", "unknown")
            stats["agent_types"][agent_type] = stats["agent_types"].get(agent_type, 0) + 1

        return stats

    def explain_capabilities(self, agent_id: str) -> str:
        """
        Generate human-readable explanation of agent capabilities.

        Args:
            agent_id: Agent identifier

        Returns:
            Formatted explanation string
        """
        agent = self.get_agent_by_id(agent_id)
        if not agent:
            return f"Agent '{agent_id}' not found"

        explanation = f"""
╔══════════════════════════════════════════════════════════════════╗
║  {agent['name'].center(64)}  ║
╚══════════════════════════════════════════════════════════════════╝

📋 Description:
   {agent['description']}

🎯 What it can do:
"""

        capabilities = agent.get("capabilities", {})
        for category, items in capabilities.items():
            explanation += f"\n   {category.replace('_', ' ').title()}:\n"
            for item in items:
                explanation += f"   • {item}\n"

        explanation += f"""
🔑 Key triggers:
   {', '.join(agent.get('triggers', [])[:10])}

⚡ Performance:
   Model: {agent.get('model', 'N/A')}
   Avg Response: {agent.get('avg_response_time', 'N/A')}
   Cost per query: {agent.get('cost_per_query', 'N/A')}

📁 Location: {agent.get('path', 'N/A')}
"""

        return explanation


def main():
    """Demo the orchestrator."""
    print("🤖 Agent Orchestrator - Demo\n")

    orchestrator = AgentOrchestrator()

    # Show stats
    print("=" * 80)
    print("AGENT WORKFORCE STATISTICS")
    print("=" * 80)
    stats = orchestrator.get_agent_stats()
    print(json.dumps(stats, indent=2))

    # List all agents
    print("\n" + "=" * 80)
    print("REGISTERED AGENTS")
    print("=" * 80)
    for agent in orchestrator.list_agents():
        print(f"\n✓ {agent['name']} ({agent['id']})")
        print(f"  Type: {agent['type']}")
        print(f"  Status: {agent['status']}")
        print(f"  {agent['description'][:80]}...")

    # Test routing
    print("\n" + "=" * 80)
    print("TASK ROUTING EXAMPLES")
    print("=" * 80)

    test_tasks = [
        "What's the CPU usage on the VPS?",
        "Query the Neon database for active contractors",
        "Show me task statistics in Convex",
        "Check if nginx is running",
        "This doesn't match any agent"
    ]

    for task in test_tasks:
        print(f"\n📝 Task: \"{task}\"")
        result = orchestrator.route_task(task)
        print(f"   Status: {result['status']}")

        if result['status'] == 'routed':
            print(f"   → Routed to: {result['agent']['agent_name']}")
            print(f"   → Confidence: {result['agent']['confidence']} keyword matches")
            print(f"   → Matched: {', '.join(result['agent']['matched_keywords'])}")
        elif result['status'] == 'multiple_matches':
            print(f"   → {len(result['options'])} agents available:")
            for opt in result['options']:
                print(f"      • {opt['agent_name']} (score: {opt['confidence']})")
        else:
            print(f"   → {result['message']}")

    # Show capabilities
    print("\n" + "=" * 80)
    print("AGENT CAPABILITIES")
    print("=" * 80)
    print(orchestrator.explain_capabilities("vps-monitor"))


if __name__ == "__main__":
    main()
