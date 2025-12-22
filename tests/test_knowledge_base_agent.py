import pytest
import os
from agents.knowledge_base.agent import KnowledgeBaseAgent

def test_extract_server_docs_success(tmpdir):
    """Test successful extraction of server documentation."""
    agent = KnowledgeBaseAgent(
        server_config_path=os.path.join(
            os.path.dirname(__file__),
            '../agents/knowledge_base/server_config.json'
        )
    )
    
    # Test Hostinger server
    hostinger_docs = agent.extract_server_docs('hostinger')
    assert 'name' in hostinger_docs
    assert hostinger_docs['name'] == 'hostinger'
    assert 'hostname' in hostinger_docs
    assert 'services' in hostinger_docs
    
    # Test VF Server
    vf_server_docs = agent.extract_server_docs('vf-server')
    assert 'name' in vf_server_docs
    assert vf_server_docs['name'] == 'vf-server'

def test_create_markdown_docs():
    """Test markdown documentation generation."""
    agent = KnowledgeBaseAgent()
    
    sample_docs = {
        'name': 'test-server',
        'hostname': 'test.example.com',
        'ip_address': '192.168.1.100',
        'services': ['web', 'database'],
        'ports': {'http': 80, 'https': 443}
    }
    
    markdown = agent.create_markdown_docs(sample_docs)
    
    assert 'TEST-SERVER Server Documentation' in markdown
    assert 'Hostname: test.example.com' in markdown
    assert '- web' in markdown
    assert '- **http**: 80' in markdown

def test_extract_server_docs_not_found():
    """Test handling of non-existent server configuration."""
    agent = KnowledgeBaseAgent()
    result = agent.extract_server_docs('non-existent-server')
    
    assert 'error' in result
    assert 'No configuration found' in result['error']