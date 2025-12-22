# FibreFlow Knowledge Base Agent

## Overview

The Knowledge Base Agent is responsible for generating, managing, and extracting documentation across the FibreFlow ecosystem.

## Capabilities

1. **Server Documentation Extraction**
   - Extract detailed configuration for servers
   - Supports multiple servers (Hostinger, VelocityFibre)
   - Customizable documentation sections

2. **Tool: `extract_server_docs`**
   - Generate comprehensive server documentation
   
   **Input Parameters**:
   - `server_name`: Name of the server
   - `include_sections`: Optional array of sections to document
     - Defaults: hardware, network, services, configuration

## Usage Example

```python
from agents.knowledge_base.agent import KnowledgeBaseAgent

# Initialize agent
agent = KnowledgeBaseAgent(api_key)

# Extract server documentation
result = agent.execute_tool("extract_server_docs", {
    "server_name": "Hostinger",
    "include_sections": ["hardware", "network"]
})
```

## Validation Steps

- Verify server name handling
- Check section inclusion/exclusion
- Test JSON output format
- Validate error handling

## Dependencies

- BaseAgent
- Shared configuration tools
- Access to server configuration databases