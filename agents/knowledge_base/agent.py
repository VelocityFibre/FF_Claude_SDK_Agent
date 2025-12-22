#!/usr/bin/env python3
"""
KnowledgeBase Agent - FibreFlow Specialized Agent
"""
import os
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from shared.base_agent import BaseAgent


class KnowledgeBaseAgent(BaseAgent):
    """Knowledge Base Agent for documentation management."""

    def __init__(self, anthropic_api_key: str, model: str = "claude-3-haiku-20240307"):
        """Initialize with API key and model."""
        super().__init__(anthropic_api_key, model)
        self.knowledge_base_path = os.path.expanduser("~/velocity-fibre-knowledge")
        
    def define_tools(self) -> List[Dict[str, Any]]:
        """Define tools for git repository initialization."""
        return [
            {
                "name": "initialize_git_repo",
                "description": "Initialize git repository for knowledge base",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "base_path": {
                            "type": "string",
                            "description": "Path to initialize repository",
                            "default": "~/velocity-fibre-knowledge"
                        },
                        "remote_url": {
                            "type": "string", 
                            "description": "Optional git remote repository URL",
                            "default": ""
                        }
                    },
                    "required": ["base_path"]
                }
            }
        ]

    def execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """Execute tools for git repository initialization."""
        if tool_name == "initialize_git_repo":
            base_path = os.path.expanduser(tool_input.get("base_path", "~/velocity-fibre-knowledge"))
            remote_url = tool_input.get("remote_url", "")
            
            try:
                # Ensure base path exists
                os.makedirs(base_path, exist_ok=True)
                
                # Change to base path
                original_dir = os.getcwd()
                os.chdir(base_path)
                
                # Initialize git repository
                subprocess.run(["git", "init"], check=True)
                
                # Create initial README.md
                with open("README.md", "w") as f:
                    f.write("# Velocity Fibre Knowledge Base\n\nCentral developer documentation for Velocity Fibre ecosystem.")
                
                # Stage initial files
                subprocess.run(["git", "add", "README.md"], check=True)
                
                # Create initial commit
                subprocess.run(["git", "commit", "-m", "Initial commit: Set up knowledge base repository"], check=True)
                
                # Set up remote origin if provided
                if remote_url:
                    subprocess.run(["git", "remote", "add", "origin", remote_url], check=True)
                
                # Change back to original directory
                os.chdir(original_dir)
                
                return json.dumps({
                    "status": "success",
                    "base_path": base_path,
                    "message": "Git repository initialized successfully"
                })
            
            except subprocess.CalledProcessError as e:
                return json.dumps({
                    "status": "error",
                    "message": f"Git command failed: {str(e)}"
                })
            except Exception as e:
                return json.dumps({
                    "status": "error",
                    "message": f"Unexpected error: {str(e)}"
                })

        return json.dumps({"error": f"Unknown tool: {tool_name}"})

    def get_system_prompt(self) -> str:
        """Return system prompt for knowledge base agent."""
        return """You are a Knowledge Base Agent responsible for 
        creating and maintaining comprehensive developer documentation 
        for the Velocity Fibre ecosystem.

        Your primary tasks:
        1. Initialize git repository
        2. Set up documentation structure
        3. Create initial documentation files
        4. Prepare for future content generation

        Available tools:
        - initialize_git_repo: Set up git repository
        """