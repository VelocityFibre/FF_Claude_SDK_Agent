import os
import pytest
from agents.knowledge_base.agent import KnowledgeBaseAgent

@pytest.fixture
def agent():
    """Create a KnowledgeBaseAgent instance for testing"""
    return KnowledgeBaseAgent()

@pytest.mark.unit
def test_create_app_docs_initialization(agent):
    """Test that create_app_docs method exists and is callable"""
    assert hasattr(agent, 'create_app_docs'), "Method create_app_docs not found"
    assert callable(agent.create_app_docs), "create_app_docs is not callable"

@pytest.mark.unit
def test_create_app_docs_fibreflow(agent):
    """Test documentation generation for FibreFlow application"""
    docs = agent.create_app_docs('fibreflow')
    
    # Check all sections are generated
    assert len(docs) >= 4, "Not enough documentation sections generated"
    
    assert 'architecture' in docs, "Architecture section missing"
    assert 'api' in docs, "API section missing"
    assert 'deployment' in docs, "Deployment section missing"
    assert 'env-vars' in docs, "Environment variables section missing"

@pytest.mark.unit
def test_specific_sections_generation(agent):
    """Test generation of specific documentation sections"""
    docs = agent.create_app_docs('fibreflow', sections=['architecture', 'api'])
    
    assert len(docs) == 2, "Incorrect number of sections generated"
    assert 'architecture' in docs, "Architecture section missing"
    assert 'api' in docs, "API section missing"
    assert 'deployment' not in docs, "Unexpected deployment section"
    assert 'env-vars' not in docs, "Unexpected environment variables section"

@pytest.mark.unit
def test_markdown_generation(agent):
    """Test that generated docs are markdown strings"""
    docs = agent.create_app_docs('fibreflow', sections=['architecture'])
    
    assert isinstance(docs['architecture'], str), "Architecture docs not a string"
    assert docs['architecture'].startswith('# '), "Markdown should start with header"
    assert '## Overview' in docs['architecture'], "Missing markdown subsection"

@pytest.mark.unit
def test_nonexistent_app(agent):
    """Test handling of nonexistent application"""
    result = agent.create_app_docs('nonexistent_app')
    
    assert isinstance(result, dict), "Result should be a dictionary"
    assert 'error' in result, "Error not returned for nonexistent app"
    assert "No configuration found" in result['error'], "Incorrect error message"