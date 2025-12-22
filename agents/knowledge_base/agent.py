import json
from typing import List, Dict, Any

class MockBaseAgent:
    """
    Mock base agent for testing without external dependencies
    """
    def __init__(self, anthropic_api_key: str, model: str = "claude-3-haiku-20240307"):
        self.api_key = anthropic_api_key
        self.model = model

BaseAgent = MockBaseAgent

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
            
            return json.dumps({"error": f"Unknown tool: {tool_name}"})

        except Exception as e:
            return json.dumps({
                "status": "error", 
                "message": str(e),
                "tool": tool_name
            })