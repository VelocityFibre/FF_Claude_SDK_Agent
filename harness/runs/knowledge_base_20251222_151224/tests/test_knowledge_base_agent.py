import os
import pytest
import json
from agents.knowledge_base.agent import KnowledgeBaseAgent

@pytest.fixture
def agent():
    """Create agent instance for testing"""
    api_key = os.getenv('ANTHROPIC_API_KEY', 'test-key')
    return KnowledgeBaseAgent(api_key)

def test_agent_initialization(agent):
    """Test that agent initializes correctly"""
    assert agent is not None
    assert hasattr(agent, 'define_tools')
    assert hasattr(agent, 'execute_tool')
    assert hasattr(agent, 'get_system_prompt')

@pytest.mark.unit
def test_define_tools(agent):
    """Verify tools are defined correctly"""
    tools = agent.define_tools()
    assert isinstance(tools, list)
    assert len(tools) > 0
    
    tool_names = [tool.get('name') for tool in tools]
    assert 'list_documents' in tool_names
    assert 'add_document' in tool_names

@pytest.mark.integration
def test_add_and_list_documents(agent):
    """Test adding and listing documents"""
    # Add document
    add_result = json.loads(
        agent.execute_tool('add_document', {
            'filename': 'test_doc.txt', 
            'content': 'Test document content', 
            'category': 'test'
        })
    )
    assert add_result['status'] == 'success'
    assert 'filepath' in add_result
    assert add_result['filename'] == 'test_doc.txt'

    # List documents
    list_result = json.loads(
        agent.execute_tool('list_documents', {'category': 'test'})
    )
    assert 'documents' in list_result
    assert 'test_test_doc.txt' in list_result['documents']

@pytest.mark.unit
def test_system_prompt(agent):
    """Verify system prompt generation"""
    prompt = agent.get_system_prompt()
    assert isinstance(prompt, str)
    assert len(prompt) > 0
    assert 'Knowledge Base Agent' in prompt

def test_base_agent_inheritance(agent):
    """Confirm inheritance from BaseAgent"""
    assert hasattr(agent, 'anthropic_api_key')
    assert hasattr(agent, 'model')
    assert agent.model == 'claude-3-haiku-20240307'