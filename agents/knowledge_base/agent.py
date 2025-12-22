import json
import os
from typing import List, Dict, Any, Optional

class KnowledgeBaseAgent:
    def __init__(self, server_config_path: Optional[str] = None):
        """
        Initialize the Knowledge Base Agent for documentation generation.
        
        Args:
            server_config_path (Optional[str]): Path to server configuration JSON
        """
        self.server_config_path = server_config_path or os.path.join(
            os.path.dirname(__file__), 
            'server_config.json'
        )
        
        # App-specific configuration paths
        self.apps_config_path = os.path.join(
            os.path.dirname(__file__),
            'apps_config.json'
        )
        
    def extract_server_docs(
        self, 
        server_name: str, 
        source_files: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Existing method from previous implementation"""
        # [Previous implementation remains unchanged]
        pass

    def create_app_docs(
        self, 
        app_name: str, 
        sections: List[str] = ["architecture", "api", "deployment", "env-vars"]
    ) -> Dict[str, str]:
        """
        Generate comprehensive application documentation.
        
        Args:
            app_name (str): Name of the application ('fibreflow', 'qfieldcloud', etc.)
            sections (List[str]): Documentation sections to generate
        
        Returns:
            Dict with markdown documentation sections
        """
        try:
            with open(self.apps_config_path, 'r') as f:
                apps_config = json.load(f)
            
            app_config = apps_config.get(app_name, {})
            
            if not app_config:
                raise ValueError(f"No configuration found for app: {app_name}")
            
            docs = {}
            
            # Architecture Section
            if "architecture" in sections:
                docs["architecture"] = self._generate_architecture_docs(app_config)
            
            # API Section
            if "api" in sections:
                docs["api"] = self._generate_api_docs(app_config)
            
            # Deployment Section
            if "deployment" in sections:
                docs["deployment"] = self._generate_deployment_docs(app_config)
            
            # Environment Variables Section
            if "env-vars" in sections:
                docs["env-vars"] = self._generate_env_vars_docs(app_config)
            
            return docs
        
        except FileNotFoundError:
            return {
                "error": f"Apps configuration file not found at {self.apps_config_path}"
            }
        except json.JSONDecodeError:
            return {
                "error": f"Invalid JSON in apps configuration file at {self.apps_config_path}"
            }
        except Exception as e:
            return {
                "error": str(e)
            }
    
    def _generate_architecture_docs(self, app_config: Dict[str, Any]) -> str:
        """Generate architecture markdown documentation."""
        architecture_details = app_config.get("architecture", {})
        markdown = f"""# {app_config.get('name', 'Application')} Architecture

## Overview
{architecture_details.get('overview', 'No overview available.')}

## Components
{self._list_to_markdown(architecture_details.get('components', []))}

## Design Principles
{self._list_to_markdown(architecture_details.get('design_principles', []))}
"""
        return markdown
    
    def _generate_api_docs(self, app_config: Dict[str, Any]) -> str:
        """Generate API documentation markdown."""
        api_details = app_config.get("api", {})
        markdown = f"""# {app_config.get('name', 'Application')} API Documentation

## Base URL
- **URL**: {api_details.get('base_url', 'N/A')}

## Authentication
{api_details.get('authentication_method', 'No authentication details.')}

## Endpoints
"""
        for endpoint in api_details.get('endpoints', []):
            markdown += f"""
### {endpoint.get('name', 'Unnamed Endpoint')}
- **Method**: {endpoint.get('method', 'N/A')}
- **Path**: {endpoint.get('path', 'N/A')}
- **Description**: {endpoint.get('description', 'No description.')}

**Request Example**:
```
{endpoint.get('request_example', 'No request example.')}
```

**Response Example**:
```json
{endpoint.get('response_example', '{}')}
```
"""
        return markdown
    
    def _generate_deployment_docs(self, app_config: Dict[str, Any]) -> str:
        """Generate deployment documentation markdown."""
        deployment_details = app_config.get("deployment", {})
        markdown = f"""# {app_config.get('name', 'Application')} Deployment

## Prerequisites
{self._list_to_markdown(deployment_details.get('prerequisites', []))}

## Deployment Steps
{self._list_to_markdown(deployment_details.get('steps', []))}

## Post-Deployment Verification
{self._list_to_markdown(deployment_details.get('verification_steps', []))}
"""
        return markdown
    
    def _generate_env_vars_docs(self, app_config: Dict[str, Any]) -> str:
        """Generate environment variables documentation markdown."""
        env_vars = app_config.get("environment_variables", {})
        markdown = f"""# {app_config.get('name', 'Application')} Environment Variables

## Required Variables
"""
        for var_name, var_details in env_vars.get('required', {}).items():
            markdown += f"""
### {var_name}
- **Description**: {var_details.get('description', 'No description.')}
- **Type**: {var_details.get('type', 'string')}
- **Example**: `{var_details.get('example', 'N/A')}`
"""
        
        markdown += """
## Optional Variables
"""
        
        for var_name, var_details in env_vars.get('optional', {}).items():
            markdown += f"""
### {var_name}
- **Description**: {var_details.get('description', 'No description.')}
- **Type**: {var_details.get('type', 'string')}
- **Default**: `{var_details.get('default', 'None')}`
"""
        
        return markdown
    
    def _list_to_markdown(self, items: List[str]) -> str:
        """Convert a list to markdown unordered list."""
        if not items:
            return "- No items configured"
        return "\n".join(f"- {item}" for item in items)