import json
import os
from typing import List, Dict, Any
import psycopg2
from psycopg2.extras import DictCursor
import yaml

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

def create_repo_structure(base_path: str = 'velocity-fibre-knowledge') -> Dict[str, str]:
    """
    Create the velocity-fibre-knowledge repository structure.
    
    Args:
        base_path (str, optional): Base directory path. Defaults to 'velocity-fibre-knowledge'.
    
    Returns:
        Dict[str, str]: Paths of created directories and files
    """
    os.makedirs(base_path, exist_ok=True)
    
    # Create subdirectories
    subdirs = [
        'docs/servers', 
        'docs/apps', 
        'docs/databases', 
        'docs/skills', 
        'docs/procedures', 
        'scripts'
    ]
    for subdir in subdirs:
        os.makedirs(os.path.join(base_path, subdir), exist_ok=True)
    
    # Create mkdocs.yml
    mkdocs_config = {
        'site_name': 'Velocity Fibre Knowledge Base',
        'site_url': 'https://docs.fibreflow.app',
        'theme': {'name': 'material'},
        'nav': [
            {'Servers': 'servers/index.md'},
            {'Applications': 'apps/index.md'},
            {'Databases': 'databases/index.md'},
            {'Skills': 'skills/index.md'},
            {'Procedures': 'procedures/index.md'}
        ]
    }
    with open(os.path.join(base_path, 'mkdocs.yml'), 'w') as f:
        yaml.safe_dump(mkdocs_config, f, default_flow_style=False)
    
    # Create README
    readme_content = """# Velocity Fibre Knowledge Base

Centralized documentation for Velocity Fibre operations.

## Structure

- `/docs/servers`: Server infrastructure documentation
- `/docs/apps`: Application documentation
- `/docs/databases`: Database schema and ERD
- `/docs/skills`: Claude AI skills usage
- `/docs/procedures`: Deployment and maintenance guides

## Generation

Automatically generated and deployed via FibreFlow Knowledge Base Agent.
"""
    with open(os.path.join(base_path, 'README.md'), 'w') as f:
        f.write(readme_content)
    
    # Create index files for each section
    index_template = """# {section_name}

Welcome to the {section_name} documentation section.

More details coming soon.
"""
    
    sections = ['servers', 'apps', 'databases', 'skills', 'procedures']
    for section in sections:
        with open(os.path.join(base_path, f'docs/{section}/index.md'), 'w') as f:
            f.write(index_template.format(section_name=section.capitalize()))
    
    # Return paths of created resources
    return {
        'base_path': base_path,
        'mkdocs_config': os.path.join(base_path, 'mkdocs.yml'),
        'readme': os.path.join(base_path, 'README.md'),
        'docs_path': os.path.join(base_path, 'docs'),
        'scripts_path': os.path.join(base_path, 'scripts')
    }

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
                "name": "create_repo_structure",
                "description": "Create repository structure for knowledge base",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "base_path": {
                            "type": "string", 
                            "description": "Base directory path for knowledge base repository",
                            "default": "velocity-fibre-knowledge"
                        }
                    },
                    "required": []
                }
            },
            {
                "name": "generate_db_schema",
                "description": "Generate database schema documentation",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "database_url": {
                            "type": "string", 
                            "description": "Database connection URL"
                        },
                        "format": {
                            "type": "string",
                            "enum": ["markdown", "json"],
                            "default": "markdown"
                        },
                        "include_tables": {
                            "type": "array",
                            "description": "List of tables to include",
                            "items": {"type": "string"}
                        }
                    }
                }
            },
            {
                "name": "setup_mkdocs",
                "description": "Configure MkDocs for documentation site",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "site_name": {
                            "type": "string",
                            "default": "Velocity Fibre Knowledge Base"
                        },
                        "site_url": {
                            "type": "string",
                            "default": "https://docs.fibreflow.app"
                        },
                        "theme": {
                            "type": "string",
                            "default": "material"
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
            if tool_name == "create_repo_structure":
                base_path = tool_input.get('base_path', 'velocity-fibre-knowledge')
                repo_result = create_repo_structure(base_path)
                return json.dumps({
                    "status": "success",
                    "base_path": repo_result['base_path'],
                    "docs_path": repo_result['docs_path'],
                    "mkdocs_config": repo_result['mkdocs_config'],
                    "readme_path": repo_result['readme']
                })
            
            elif tool_name == "generate_db_schema":
                # Simulated DB schema generation
                database_url = tool_input.get('database_url', 'mock://test_database')
                format_type = tool_input.get('format', 'markdown')
                include_tables = tool_input.get('include_tables')

                mock_schema = {
                    "status": "success", 
                    "format": format_type,
                    "documentation": {
                        "tables": {
                            "users": {
                                "columns": [
                                    {"name": "id", "type": "integer"},
                                    {"name": "username", "type": "varchar"}
                                ]
                            },
                            "projects": {
                                "columns": [
                                    {"name": "id", "type": "integer"},
                                    {"name": "name", "type": "varchar"}
                                ]
                            }
                        }
                    }
                }

                if include_tables:
                    mock_schema['documentation']['tables'] = {
                        table: mock_schema['documentation']['tables'][table]
                        for table in include_tables
                        if table in mock_schema['documentation']['tables']
                    }

                return json.dumps(mock_schema)
            
            elif tool_name == "setup_mkdocs":
                site_name = tool_input.get('site_name', 'Velocity Fibre Knowledge Base')
                site_url = tool_input.get('site_url', 'https://docs.fibreflow.app')
                theme = tool_input.get('theme', 'material')
                
                home_path = os.environ.get('HOME', '/tmp')
                base_path = os.path.join(home_path, 'velocity-fibre-knowledge')

                os.makedirs(base_path, exist_ok=True)
                docs_path = os.path.join(base_path, 'docs')
                os.makedirs(docs_path, exist_ok=True)

                # Create index files for sections
                sections = ['servers', 'apps', 'databases', 'skills', 'procedures']
                for section in sections:
                    section_path = os.path.join(docs_path, section)
                    os.makedirs(section_path, exist_ok=True)
                    with open(os.path.join(section_path, 'index.md'), 'w') as f:
                        f.write(f"# {section.capitalize()} Documentation")

                mkdocs_path = os.path.join(base_path, 'mkdocs.yml')
                
                # Create index.md file
                index_path = os.path.join(docs_path, 'index.md')
                with open(index_path, 'w') as f:
                    f.write(f"# {site_name}\n\nWelcome to the documentation site.")

                mkdocs_config = {
                    'site_name': site_name,
                    'site_url': site_url,
                    'theme': {'name': theme},
                    'nav': [{'Home': 'index.md'}] + 
                           [{'Servers': 'servers/index.md'}] +
                           [{'Applications': 'apps/index.md'}] +
                           [{'Databases': 'databases/index.md'}] +
                           [{'Skills': 'skills/index.md'}] +
                           [{'Procedures': 'procedures/index.md'}],
                    'markdown_extensions': [
                        'tables',
                        'codehilite',
                        'admonition',
                        'pymdownx.details',
                        'pymdownx.superfences'
                    ]
                }

                with open(mkdocs_path, 'w') as f:
                    yaml.safe_dump(mkdocs_config, f)

                return json.dumps({
                    "status": "success",
                    "mkdocs_config_path": mkdocs_path,
                    "docs_path": docs_path
                })
            
            return json.dumps({"error": f"Unknown tool: {tool_name}"})

        except Exception as e:
            return json.dumps({
                "status": "error", 
                "message": str(e),
                "tool": tool_name
            })