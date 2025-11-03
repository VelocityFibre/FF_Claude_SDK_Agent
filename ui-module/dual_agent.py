#!/usr/bin/env python3
"""
Dual Database Agent - Supports both Neon PostgreSQL and Convex
Allows switching between databases for comparison and testing
"""

import os
import json
import requests
from typing import List, Dict, Any, Optional, Literal
from anthropic import Anthropic
import psycopg2
from psycopg2.extras import RealDictCursor


# ============================================================================
# PostgreSQL (Neon) Client
# ============================================================================

class PostgresClient:
    """PostgreSQL database client for Neon."""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None

    def connect(self):
        """Establish database connection."""
        if not self.connection or self.connection.closed:
            self.connection = psycopg2.connect(self.connection_string)
        return self.connection

    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute a SQL query and return results."""
        conn = self.connect()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            try:
                results = cursor.fetchall()
                return [dict(row) for row in results]
            except psycopg2.ProgrammingError:
                conn.commit()
                return [{"status": "success", "message": "Query executed"}]

    def close(self):
        """Close database connection."""
        if self.connection and not self.connection.closed:
            self.connection.close()


# ============================================================================
# Convex Client
# ============================================================================

class ConvexClient:
    """Client for Convex database."""

    def __init__(self, convex_url: str, auth_key: Optional[str] = None):
        self.convex_url = convex_url.rstrip('/')
        self.auth_key = auth_key
        self.headers = {"Content-Type": "application/json"}

    def call_function(self, function_path: str, args: Dict[str, Any] = None) -> Dict[str, Any]:
        """Call a Convex function."""
        function_name = function_path.replace("/", ":")
        payload = {"path": function_name, "args": args or {}}

        try:
            # Try query endpoint
            response = requests.post(
                f"{self.convex_url}/api/query",
                json=payload,
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("value", result)

            # Try mutation endpoint
            response = requests.post(
                f"{self.convex_url}/api/mutation",
                json=payload,
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("value", result)

            return {
                "error": f"Convex API error: {response.status_code}",
                "status": "failed"
            }

        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status": "failed"}


# ============================================================================
# Unified Dual Agent
# ============================================================================

class DualDatabaseAgent:
    """
    Unified agent that can query both Neon PostgreSQL and Convex databases.
    Allows switching between databases for comparison.
    """

    def __init__(
        self,
        model: str = "claude-sonnet-4-5-20250929",
        neon_url: Optional[str] = None,
        convex_url: Optional[str] = None,
        convex_auth_key: Optional[str] = None,
        default_db: Literal["neon", "convex"] = "neon"
    ):
        """
        Initialize dual database agent.

        Args:
            model: Claude model to use
            neon_url: Neon PostgreSQL connection string
            convex_url: Convex deployment URL
            convex_auth_key: Convex authentication key
            default_db: Default database to use
        """
        # Load API key
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")

        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.conversation_history: List[Dict[str, Any]] = []
        self.max_tokens = 4096

        # Load database configs
        self.neon_url = neon_url or os.environ.get("NEON_DATABASE_URL")
        self.convex_url = convex_url or os.environ.get("CONVEX_URL")
        self.convex_auth_key = convex_auth_key or os.environ.get("CONVEX_AUTH_KEY")

        # Initialize clients
        self.neon_db = PostgresClient(self.neon_url) if self.neon_url else None
        self.convex_db = ConvexClient(self.convex_url, self.convex_auth_key) if self.convex_url else None

        # Set active database
        self.active_db = default_db

        print(f"✅ Dual Database Agent initialized")
        print(f"   Model: {model}")
        print(f"   Neon: {'✓' if self.neon_db else '✗'}")
        print(f"   Convex: {'✓' if self.convex_db else '✗'}")
        print(f"   Active: {self.active_db}")

    def set_database(self, db_type: Literal["neon", "convex"]):
        """Switch active database."""
        if db_type == "neon" and not self.neon_db:
            raise ValueError("Neon database not configured")
        if db_type == "convex" and not self.convex_db:
            raise ValueError("Convex database not configured")

        self.active_db = db_type
        print(f"🔄 Switched to {db_type.upper()} database")

    def define_neon_tools(self) -> List[Dict[str, Any]]:
        """Define tools for Neon PostgreSQL database."""
        return [
            {
                "name": "execute_sql",
                "description": "Execute a SQL query on the Neon PostgreSQL database. Returns results as JSON.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The SQL query to execute"
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "list_tables",
                "description": "List all tables in the database with their row counts.",
                "input_schema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "describe_table",
                "description": "Get the schema/structure of a specific table.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "table_name": {
                            "type": "string",
                            "description": "The table name to describe"
                        }
                    },
                    "required": ["table_name"]
                }
            }
        ]

    def define_convex_tools(self) -> List[Dict[str, Any]]:
        """Define tools for Convex database."""
        return [
            {
                "name": "convex_list_contractors",
                "description": "List all contractors from Convex database.",
                "input_schema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "convex_list_projects",
                "description": "List all projects from Convex database.",
                "input_schema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "convex_search",
                "description": "Search Convex database by keyword.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query"
                        }
                    },
                    "required": ["query"]
                }
            }
        ]

    def execute_neon_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """Execute Neon PostgreSQL tool."""
        try:
            if tool_name == "execute_sql":
                results = self.neon_db.execute_query(tool_input["query"])
                return json.dumps(results, indent=2, default=str)

            elif tool_name == "list_tables":
                query = """
                    SELECT table_name,
                           (SELECT COUNT(*) FROM information_schema.columns
                            WHERE table_name = t.table_name) as column_count
                    FROM information_schema.tables t
                    WHERE table_schema = 'public'
                    ORDER BY table_name
                """
                results = self.neon_db.execute_query(query)
                return json.dumps(results, indent=2)

            elif tool_name == "describe_table":
                query = """
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_name = %s
                    ORDER BY ordinal_position
                """
                results = self.neon_db.execute_query(query, (tool_input["table_name"],))
                return json.dumps(results, indent=2)

            return json.dumps({"error": f"Unknown tool: {tool_name}"})

        except Exception as e:
            return json.dumps({"error": str(e), "tool": tool_name})

    def execute_convex_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """Execute Convex database tool."""
        try:
            # Map tool names to Convex functions
            function_map = {
                "convex_list_contractors": "contractors/list",
                "convex_list_projects": "projects/list",
                "convex_search": "search/query"
            }

            if tool_name not in function_map:
                return json.dumps({"error": f"Unknown tool: {tool_name}"})

            function_path = function_map[tool_name]
            result = self.convex_db.call_function(function_path, tool_input)

            return json.dumps(result, indent=2, default=str)

        except Exception as e:
            return json.dumps({"error": str(e), "tool": tool_name})

    def chat(self, user_message: str, database: Optional[Literal["neon", "convex"]] = None) -> str:
        """
        Chat with the agent. Can optionally specify which database to use.

        Args:
            user_message: User's message
            database: Which database to use (overrides active_db for this query)

        Returns:
            Agent's response
        """
        # Determine which database to use
        db_to_use = database if database else self.active_db

        # Select appropriate tools
        if db_to_use == "neon":
            tools = self.define_neon_tools()
            system_prompt = f"""You are a helpful database assistant with access to a Neon PostgreSQL database.
When tools return data:
- ALWAYS show the actual data returned
- Format results clearly with markdown
- Be confident when presenting data
- Never claim connection issues when tools succeed

Current database: NEON (PostgreSQL)"""
        else:
            tools = self.define_convex_tools()
            system_prompt = f"""You are a helpful database assistant with access to a Convex database.
When tools return data:
- ALWAYS show the actual data returned
- Format results clearly with markdown
- Be confident when presenting data

Current database: CONVEX"""

        # Add user message
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Agent loop
        while True:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_prompt,
                messages=self.conversation_history,
                tools=tools
            )

            # Add response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response.content
            })

            # Check for tool use
            if response.stop_reason == "tool_use":
                tool_uses = [block for block in response.content if block.type == "tool_use"]

                if not tool_uses:
                    break

                # Execute tools
                tool_results = []
                for tool_use in tool_uses:
                    print(f"🔧 [{db_to_use.upper()}] {tool_use.name}")

                    if db_to_use == "neon":
                        result = self.execute_neon_tool(tool_use.name, tool_use.input)
                    else:
                        result = self.execute_convex_tool(tool_use.name, tool_use.input)

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": result
                    })

                # Add tool results
                self.conversation_history.append({
                    "role": "user",
                    "content": tool_results
                })

                continue

            # Extract text response
            text_blocks = [block.text for block in response.content if hasattr(block, 'text')]
            return "\n".join(text_blocks)

    def reset_conversation(self):
        """Clear conversation history."""
        self.conversation_history = []

    def close(self):
        """Close database connections."""
        if self.neon_db:
            self.neon_db.close()


def load_env():
    """Load environment variables from .env file."""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value


if __name__ == "__main__":
    load_env()

    agent = DualDatabaseAgent()

    print("\n" + "="*60)
    print("Testing Neon Database")
    print("="*60)
    response = agent.chat("List all active contractors", database="neon")
    print(response)

    print("\n" + "="*60)
    print("Testing Convex Database")
    print("="*60)
    response = agent.chat("Show me all contractors", database="convex")
    print(response)
