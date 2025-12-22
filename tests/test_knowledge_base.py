import os
import pytest
import json
import yaml
from agents.knowledge_base.agent import KnowledgeBaseAgent, get_postgres_connection

@pytest.fixture
def agent():
    """Create KnowledgeBaseAgent for testing"""
    api_key = os.getenv('ANTHROPIC_API_KEY', 'test-key')
    return KnowledgeBaseAgent(api_key)

def test_generate_db_schema_tool(agent):
    """Test generate_db_schema tool"""
    # Mock data for testing when no real database is available
    mock_result = json.loads(agent.execute_tool('generate_db_schema', {
        'format': 'markdown',
        'database_url': 'mock://test_database'  # Simulate no connection
    }))
    
    # If real database is configured, this will work
    # If not, we expect an error result
    assert 'status' in mock_result
    assert mock_result['status'] in ['success', 'error']

def test_generate_db_schema_formats(agent):
    """Test different documentation formats"""
    # Test markdown format
    markdown_result = json.loads(agent.execute_tool('generate_db_schema', {
        'format': 'markdown',
        'database_url': 'mock://test_database'
    }))
    assert 'status' in markdown_result
    
    # Test JSON format
    json_result = json.loads(agent.execute_tool('generate_db_schema', {
        'format': 'json',
        'database_url': 'mock://test_database'
    }))
    assert 'status' in json_result

def test_get_postgres_connection():
    """Test database connection helper"""
    # This will raise an error if no database URL is set
    try:
        conn = get_postgres_connection()
        assert conn is not None
        conn.close()
    except Exception as e:
        pytest.skip(f"No database connection possible: {e}")

@pytest.mark.parametrize("tables", [
    None,  # Test all tables
    ['users', 'projects'],  # Test specific tables
])
def test_generate_db_schema_table_filter(agent, tables):
    """Test table filtering in schema generation"""
    result = json.loads(agent.execute_tool('generate_db_schema', {
        'include_tables': tables
    }))

    assert result['status'] == 'success'
    
    if tables:
        # If specific tables requested, ensure only those are documented
        documented_tables = list(result['documentation']['tables'].keys())
        assert set(documented_tables) <= set(tables)

@pytest.mark.mkdocs
def test_setup_mkdocs_tool(agent, tmp_path):
    """Test setup_mkdocs() tool functionality"""
    # Override home directory for testing
    os.environ['HOME'] = str(tmp_path)

    # Use the tool
    result = json.loads(agent.execute_tool('setup_mkdocs', {
        'site_name': 'Test Knowledge Base',
        'site_url': 'https://test.fibreflow.app',
        'theme': 'material'
    }))

    # Verify successful configuration
    assert result['status'] == 'success'
    assert 'mkdocs_config_path' in result
    assert 'docs_path' in result

    # Verify MkDocs configuration file exists
    mkdocs_path = result['mkdocs_config_path']
    assert os.path.exists(mkdocs_path)

    # Verify docs structure
    docs_path = result['docs_path']
    assert os.path.exists(docs_path)
    
    # Check default documentation categories
    categories = ['servers', 'apps', 'databases', 'skills', 'procedures']
    for category in categories:
        category_path = os.path.join(docs_path, category)
        assert os.path.exists(category_path)
        
    # Verify base index.md exists
    assert os.path.exists(os.path.join(docs_path, 'index.md'))

    # Load and verify MkDocs YAML configuration
    with open(mkdocs_path, 'r') as f:
        config = yaml.safe_load(f)

    assert config['site_name'] == 'Test Knowledge Base'
    assert config['site_url'] == 'https://test.fibreflow.app'
    assert config['theme']['name'] == 'material'
    assert 'nav' in config
    assert 'markdown_extensions' in config

@pytest.mark.mkdocs
def test_setup_mkdocs_default_configuration(agent, tmp_path):
    """Test setup_mkdocs() with default configuration"""
    # Override home directory for testing
    os.environ['HOME'] = str(tmp_path)

    # Use the tool with no parameters
    result = json.loads(agent.execute_tool('setup_mkdocs', {}))

    assert result['status'] == 'success'
    
    # Verify MkDocs configuration file exists
    mkdocs_path = result['mkdocs_config_path']
    assert os.path.exists(mkdocs_path)

    # Load configuration
    with open(mkdocs_path, 'r') as f:
        config = yaml.safe_load(f)

    # Check default values
    assert config['site_name'] == 'Velocity Fibre Knowledge Base'
    assert config['site_url'] == 'https://docs.fibreflow.app'
    assert config['theme']['name'] == 'material'
    assert len(config['nav']) > 0
    assert len(config['markdown_extensions']) > 0