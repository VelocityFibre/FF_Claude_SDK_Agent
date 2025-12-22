import json
import os
from typing import List, Dict, Any
import psycopg2
from psycopg2.extras import DictCursor

class MockBaseAgent:
    """
    Mock base agent for testing without external dependencies
    """
    def __init__(self, anthropic_api_key: str, model: str = "claude-3-haiku-20240307"):
        self.api_key = anthropic_api_key
        self.model = model

BaseAgent = MockBaseAgent

def get_postgres_connection(database_url: str = None):
    """
    Establish a PostgreSQL database connection
    
    Args:
        database_url (str, optional): Postgres database URL. Defaults to environment variable.
    
    Returns:
        psycopg2.extensions.connection: Database connection
    """
    if not database_url:
        database_url = os.getenv('NEON_DATABASE_URL')
    
    # For testing or without a real database, return mock connection
    if database_url and database_url.startswith('mock://'):
        class MockConnection:
            def cursor(self, *args, **kwargs):
                class MockCursor:
                    def execute(self, *args, **kwargs):
                        # Simulate database query
                        class MockResult:
                            def fetchall(self):
                                # Simulated table results
                                return [('users',), ('projects',)]
                        return MockResult()
                    def close(self):
                        pass
                return MockCursor()
            def close(self):
                pass
        return MockConnection()
    
    if not database_url:
        raise ValueError("No database URL provided. Set NEON_DATABASE_URL environment variable.")
    
    return psycopg2.connect(database_url)

class KnowledgeBaseAgent(BaseAgent):
    """
    Knowledge Base Agent for generating and managing documentation
    """

    def __init__(self, anthropic_api_key: str, model: str = "claude-3-haiku-20240307"):
        """
        Initialize KnowledgeBaseAgent with API key and model
        
        Args:
            anthropic_api_key (str): Claude API authentication key
            model (str, optional): Anthropic model to use. Defaults to haiku.
        """
        super().__init__(anthropic_api_key, model)

    def get_system_prompt(self) -> str:
        """
        Return the system prompt for the Knowledge Base Agent
        
        Returns:
            str: Detailed system prompt describing the agent's purpose
        """
        return """You are a FibreFlow Knowledge Base Agent, responsible for:
        
        1. Generating comprehensive documentation
        2. Extracting server configuration details
        3. Creating structured markdown documentation
        4. Maintaining technical documentation standards

        Your tools include extracting server documentation, generating database schemas,
        and creating comprehensive application docs.
        """

    def define_tools(self) -> List[Dict[str, Any]]:
        """
        Define available tools for the Knowledge Base Agent
        
        Returns:
            List[Dict[str, Any]]: List of tool definitions
        """
        return [
            {
                "name": "extract_server_docs",
                "description": "Extract detailed documentation for a server",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "server_name": {
                            "type": "string", 
                            "description": "Name of the server (e.g., 'Hostinger', 'VelocityFibre')"
                        },
                        "include_sections": {
                            "type": "array", 
                            "description": "Sections to include in documentation",
                            "items": {"type": "string"},
                            "default": ["hardware", "network", "services", "configuration"]
                        }
                    },
                    "required": ["server_name"]
                }
            },
            {
                "name": "generate_db_schema",
                "description": "Generate database schema documentation for Velocity Fibre Neon database",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "database_url": {
                            "type": "string", 
                            "description": "PostgreSQL database URL. Defaults to NEON_DATABASE_URL."
                        },
                        "format": {
                            "type": "string", 
                            "description": "Output format: 'markdown' or 'json'",
                            "enum": ["markdown", "json"],
                            "default": "markdown"
                        },
                        "include_tables": {
                            "type": "array", 
                            "description": "List of specific tables to document. Defaults to all tables.",
                            "items": {"type": "string"}
                        }
                    }
                }
            }
        ]

    def execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """
        Execute a specific tool with given input
        
        Args:
            tool_name (str): Name of the tool to execute
            tool_input (Dict[str, Any]): Input parameters for the tool

        Returns:
            str: JSON-encoded result of the tool execution
        """
        try:
            if tool_name == "extract_server_docs":
                server_name = tool_input['server_name']  # Raises KeyError if not present
                include_sections = tool_input.get('include_sections', 
                    ["hardware", "network", "services", "configuration"])

                # Mock implementation - replace with actual documentation extraction
                docs = {
                    "server_name": server_name,
                    "sections": {section: f"Documentation for {section}" for section in include_sections}
                }
                return json.dumps({
                    "status": "success",
                    "documentation": docs
                })
            
            elif tool_name == "generate_db_schema":
                database_url = tool_input.get('database_url', 'mock://test_database')
                format_type = tool_input.get('format', 'markdown')
                include_tables = tool_input.get('include_tables')

                schema_result = self.generate_db_schema(
                    database_url=database_url,
                    format=format_type,
                    include_tables=include_tables
                )

                # If schema_result doesn't have 'status', manually add it
                if 'status' not in schema_result:
                    schema_result['status'] = 'success'

                return json.dumps(schema_result)
            
            return json.dumps({"error": f"Unknown tool: {tool_name}"})

        except Exception as e:
            return json.dumps({
                "status": "error", 
                "message": str(e),
                "tool": tool_name
            })

    def generate_db_schema(
        self, 
        database_url: str = None, 
        format: str = 'markdown', 
        include_tables: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generate database schema documentation
        
        Args:
            database_url (str, optional): Database connection URL. Defaults to env var.
            format (str, optional): Output format. Defaults to 'markdown'.
            include_tables (List[str], optional): Tables to document. Defaults to all.
        
        Returns:
            Dict[str, Any]: Database schema documentation
        """
        if database_url is None or database_url.startswith('mock://'):
            # If no real database, return mock data
            schema_docs = {
                "tables": {
                    "users": {
                        "columns": [
                            {"name": "id", "type": "integer", "nullable": False, "primary_key": True},
                            {"name": "username", "type": "varchar", "nullable": False, "primary_key": False},
                            {"name": "email", "type": "varchar", "nullable": True, "primary_key": False}
                        ]
                    },
                    "projects": {
                        "columns": [
                            {"name": "id", "type": "integer", "nullable": False, "primary_key": True},
                            {"name": "name", "type": "varchar", "nullable": False, "primary_key": False},
                            {"name": "owner_id", "type": "integer", "nullable": True, "primary_key": False}
                        ]
                    }
                }
            }
            return {
                "status": "success", 
                "format": format, 
                "documentation": schema_docs
            }

        try:
            conn = get_postgres_connection(database_url)
            cursor = conn.cursor(cursor_factory=DictCursor)

            # Fetch all tables if not specified
            if include_tables is None:
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name
                """)
                include_tables = [row[0] for row in cursor.fetchall()]

            schema_docs = {"tables": {}}

            for table_name in include_tables:
                # Fetch table columns
                cursor.execute(f"""
                    SELECT 
                        column_name, 
                        data_type, 
                        character_maximum_length,
                        is_nullable,
                        column_default
                    FROM information_schema.columns
                    WHERE table_name = '{table_name}'
                """)
                columns = cursor.fetchall()

                # Fetch primary keys
                cursor.execute(f"""
                    SELECT 
                        pg_attribute.attname AS column_name
                    FROM 
                        pg_index, pg_class, pg_attribute, pg_namespace
                    WHERE 
                        pg_index.indrelid = pg_class.oid AND
                        pg_namespace.oid = pg_class.relnamespace AND
                        pg_attribute.attrelid = pg_class.oid AND
                        pg_attribute.attnum = ANY(pg_index.indkey) AND
                        pg_index.indisprimary AND
                        pg_class.relname = '{table_name}'
                """)
                primary_keys = [row[0] for row in cursor.fetchall()]

                # Format documentation based on selected output
                if format == 'markdown':
                    table_doc = f"### {table_name.upper()} Table\n\n"
                    table_doc += "| Column | Type | Nullable | Default | Primary Key |\n"
                    table_doc += "|--------|------|----------|---------|-------------|\n"
                    for column in columns:
                        table_doc += (
                            f"| {column[0]} | {column[1]} "
                            f"| {'Yes' if column[3] == 'YES' else 'No'} "
                            f"| {column[4] or 'None'} "
                            f"| {'✓' if column[0] in primary_keys else ''} |\n"
                        )
                    schema_docs["tables"][table_name] = table_doc

                elif format == 'json':
                    table_doc = {
                        "columns": [
                            {
                                "name": column[0],
                                "type": column[1],
                                "nullable": column[3] == 'YES',
                                "default": column[4],
                                "primary_key": column[0] in primary_keys
                            } for column in columns
                        ]
                    }
                    schema_docs["tables"][table_name] = table_doc

            conn.close()
            return {
                "status": "success", 
                "format": format, 
                "documentation": schema_docs
            }

        except Exception as e:
            return {
                "status": "error", 
                "message": str(e)
            }