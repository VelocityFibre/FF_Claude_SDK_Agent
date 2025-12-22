import os
import sys

# Explicit path to shared directory
SHARED_DIR = '/home/louisdup/Agents/claude/harness/shared'
if SHARED_DIR not in sys.path:
    sys.path.insert(0, SHARED_DIR)

from base_agent import BaseAgent
from typing import List, Dict, Any
import json

class KnowledgeBaseAgent(BaseAgent):
    """
    Knowledge Base Agent specialized for managing and querying information repositories
    
    Inherits from BaseAgent with specialized knowledge management capabilities
    """

    def __init__(self, anthropic_api_key: str, model: str = "claude-3-haiku-20240307"):
        """
        Initialize KnowledgeBaseAgent with base agent initialization
        
        :param anthropic_api_key: Anthropic API key for Claude interactions
        :param model: Claude model to use, defaults to haiku
        """
        super().__init__(anthropic_api_key, model)
        
        # Agent-specific initialization for knowledge base
        self._documents_directory = os.path.join(
            os.path.expanduser('~/velocity-fibre-knowledge'), 
            'documents'
        )
        os.makedirs(self._documents_directory, exist_ok=True)

    def define_tools(self) -> List[Dict[str, Any]]:
        """
        Define tools specific to knowledge base management
        
        :return: List of tool definitions for knowledge base operations
        """
        return [
            {
                "name": "list_documents",
                "description": "List all documents in the knowledge base",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string", 
                            "description": "Optional category to filter documents"
                        }
                    }
                }
            },
            {
                "name": "add_document",
                "description": "Add a new document to the knowledge base",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string"},
                        "category": {"type": "string"},
                        "content": {"type": "string"}
                    },
                    "required": ["filename", "content"]
                }
            }
        ]

    def execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """
        Execute knowledge base specific tools
        
        :param tool_name: Name of the tool to execute
        :param tool_input: Input parameters for the tool
        :return: JSON string with execution result
        """
        try:
            if tool_name == "list_documents":
                category = tool_input.get("category")
                documents = os.listdir(self._documents_directory)
                if category:
                    documents = [doc for doc in documents if category in doc]
                return json.dumps({"documents": documents})
            
            elif tool_name == "add_document":
                filename = tool_input.get("filename")
                content = tool_input.get("content")
                category = tool_input.get("category", "uncategorized")
                
                filepath = os.path.join(self._documents_directory, 
                                        f"{category}_{os.path.basename(filename)}")
                
                with open(filepath, 'w') as f:
                    f.write(content)
                
                return json.dumps({
                    "status": "success", 
                    "filepath": filepath,
                    "filename": os.path.basename(filename)
                })
            
            else:
                return json.dumps({"error": f"Unknown tool: {tool_name}"})
        
        except Exception as e:
            return json.dumps({"error": str(e)})

    def get_system_prompt(self) -> str:
        """
        Generate system prompt for knowledge base interactions
        
        :return: System prompt tailored to knowledge base agent
        """
        return """You are a FibreFlow Knowledge Base Agent.

Your primary responsibilities:
- Manage and organize documents
- Retrieve and list documents
- Add new documents to the knowledge base
- Categorize and tag documents efficiently

Available tools:
- list_documents: List documents, optionally filtered by category
- add_document: Add a new document to the knowledge base

Use these tools to help users manage and interact with their knowledge repository.
"""