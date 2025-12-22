import json
import os
from typing import List, Dict, Any, Optional

class KnowledgeBaseAgent:
    def __init__(self, server_config_path: Optional[str] = None):
        """
        Initialize the Knowledge Base Agent for server documentation extraction.
        
        Args:
            server_config_path (Optional[str]): Path to server configuration JSON
        """
        self.server_config_path = server_config_path or os.path.join(
            os.path.dirname(__file__), 
            'server_config.json'
        )
        
    def extract_server_docs(
        self, 
        server_name: str, 
        source_files: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Extract server documentation for a given server.
        
        Args:
            server_name (str): Name of the server (e.g., 'hostinger', 'vf-server')
            source_files (Optional[List[str]]): Optional list of source files to extract from
        
        Returns:
            Dict with server documentation
        """
        try:
            with open(self.server_config_path, 'r') as f:
                server_configs = json.load(f)
            
            server_config = server_configs.get(server_name, {})
            
            if not server_config:
                raise ValueError(f"No configuration found for server: {server_name}")
            
            # Basic documentation extraction
            docs = {
                "name": server_name,
                "hostname": server_config.get("hostname", ""),
                "ip_address": server_config.get("ip_address", ""),
                "services": server_config.get("services", []),
                "ports": server_config.get("ports", {})
            }
            
            return docs
        
        except FileNotFoundError:
            return {
                "error": f"Server configuration file not found at {self.server_config_path}"
            }
        except json.JSONDecodeError:
            return {
                "error": f"Invalid JSON in server configuration file at {self.server_config_path}"
            }
        except Exception as e:
            return {
                "error": str(e)
            }

    def create_markdown_docs(self, server_docs: Dict[str, Any]) -> str:
        """
        Convert server documentation to markdown format.
        
        Args:
            server_docs (Dict[str, Any]): Server documentation dictionary
        
        Returns:
            str: Markdown-formatted documentation
        """
        if "error" in server_docs:
            return f"# Error\n\n{server_docs['error']}"
        
        markdown = f"""# {server_docs['name'].upper()} Server Documentation

## Basic Information
- **Hostname**: {server_docs.get('hostname', 'N/A')}
- **IP Address**: {server_docs.get('ip_address', 'N/A')}

## Services
{self._list_to_markdown(server_docs.get('services', []))}

## Ports
{self._dict_to_markdown(server_docs.get('ports', {}))}
"""
        return markdown
    
    def _list_to_markdown(self, items: List[str]) -> str:
        """Convert a list to markdown unordered list."""
        if not items:
            return "- No services configured"
        return "\n".join(f"- {item}" for item in items)
    
    def _dict_to_markdown(self, dictionary: Dict[str, Any]) -> str:
        """Convert a dictionary to markdown key-value list."""
        if not dictionary:
            return "- No port information"
        return "\n".join(f"- **{k}**: {v}" for k, v in dictionary.items())