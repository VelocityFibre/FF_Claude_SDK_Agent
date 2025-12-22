import json
import os
import pytest
from agents.knowledge_base.agent import KnowledgeBaseAgent

@pytest.fixture
def agent():
    """Create KnowledgeBaseAgent instance"""
    api_key = os.getenv('ANTHROPIC_API_KEY', 'test_key')
    return KnowledgeBaseAgent(api_key)

@pytest.mark.unit
@pytest.mark.knowledge_base
def test_extract_server_docs(agent):
    """Test extract_server_docs tool"""
    result = agent.execute_tool("extract_server_docs", {
        "server_name": "Hostinger",
        "include_sections": ["hardware", "network"]
    })
    
    # Parse result
    result_json = json.loads(result)
    
    # Validate structure
    assert result_json.get("status") == "success"
    assert "documentation" in result_json
    
    doc = result_json["documentation"]
    assert doc["server_name"] == "Hostinger"
    
    # Check included sections
    assert "hardware" in doc["sections"]
    assert "network" in doc["sections"]
    assert "services" not in doc["sections"]
    assert "configuration" not in doc["sections"]

@pytest.mark.unit
@pytest.mark.knowledge_base
def test_extract_server_docs_default_sections(agent):
    """Test extract_server_docs with default sections"""
    result = agent.execute_tool("extract_server_docs", {
        "server_name": "VelocityFibre"
    })
    
    result_json = json.loads(result)
    
    assert result_json.get("status") == "success"
    doc = result_json["documentation"]
    
    # Check default sections
    default_sections = ["hardware", "network", "services", "configuration"]
    for section in default_sections:
        assert section in doc["sections"]

@pytest.mark.unit
@pytest.mark.knowledge_base
def test_extract_server_docs_error_handling(agent):
    """Test error handling for extract_server_docs"""
    result = agent.execute_tool("extract_server_docs", {})
    result_json = json.loads(result)
    
    assert result_json.get("status") == "error"
    assert "message" in result_json
    assert "server_name" in result_json.get("message", "")  # Missing server_name

@pytest.mark.unit
@pytest.mark.knowledge_base
def test_unknown_tool_handling(agent):
    """Test handling of unknown tools"""
    result = agent.execute_tool("non_existent_tool", {})
    result_json = json.loads(result)
    
    assert result_json.get("error") is not None
    assert "Unknown tool" in result_json.get("error", "")