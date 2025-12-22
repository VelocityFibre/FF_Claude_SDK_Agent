import os
import pytest
from agents.knowledge_base.agent import KnowledgeBaseAgent


@pytest.fixture
def knowledge_base_agent():
    """Fixture to create a KnowledgeBaseAgent for testing"""
    api_key = os.getenv('ANTHROPIC_API_KEY', 'test-key')
    return KnowledgeBaseAgent(api_key)


@pytest.mark.unit
@pytest.mark.knowledge_base
def test_create_app_docs_all_sections(knowledge_base_agent):
    """Test creating app docs with all sections"""
    docs = knowledge_base_agent.create_app_docs()
    
    # Test docs dictionary
    assert isinstance(docs, dict)
    assert len(docs) == 4  # architecture, api, deployment, env-vars
    
    # Check each section
    for section in ["architecture", "api", "deployment", "env-vars"]:
        assert section in docs
        assert isinstance(docs[section], str)
        assert len(docs[section]) > 100  # Ensure meaningful content

    # Verify documents were added
    tool_result = knowledge_base_agent.execute_tool("list_documents", {"category": "apps"})
    added_docs = knowledge_base_agent.execute_tool("list_documents", {"category": "apps"})
    assert "fibreflow_architecture.md" in added_docs
    assert "fibreflow_api.md" in added_docs


@pytest.mark.unit
@pytest.mark.knowledge_base
def test_create_app_docs_specific_sections(knowledge_base_agent):
    """Test creating app docs with specific sections"""
    docs = knowledge_base_agent.create_app_docs(
        app_name="testapp", 
        sections=["architecture", "deployment"]
    )
    
    # Test docs dictionary
    assert isinstance(docs, dict)
    assert len(docs) == 2  # Only architecture and deployment

    # Check specific sections
    assert "architecture" in docs
    assert "deployment" in docs
    assert "api" not in docs

    # Verify documents were added
    added_docs = knowledge_base_agent.execute_tool("list_documents", {"category": "apps"})
    assert "testapp_architecture.md" in added_docs
    assert "testapp_deployment.md" in added_docs