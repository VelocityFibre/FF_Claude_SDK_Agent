# External Agent Access Guide
## Complete Reference for AI Agents Accessing This System

**Version:** 1.0
**Purpose:** Enable external AI agents to discover, access, and integrate with this system
**Last Updated:** 2025-11-19

---

## 🌐 System Location & Access

### Base Directory
```
Absolute Path: /home/louisdup/Agents/claude
```

### Repository Information
```yaml
type: git_repository
path: /home/louisdup/Agents/claude
branch: main
status: active
```

---

## 📍 Complete File Manifest with Absolute Paths

### Documentation Hub

```yaml
documentation_hub:
  base_path: /home/louisdup/Agents/claude/docs

  navigation:
    readme: /home/louisdup/Agents/claude/docs/README.md
    master_index: /home/louisdup/Agents/claude/docs/MASTER_INDEX.md

  architecture:
    complete: /home/louisdup/Agents/claude/docs/COMPLETE_BRAIN_ARCHITECTURE.md
    original: /home/louisdup/Agents/claude/AI_AGENT_BRAIN_ARCHITECTURE.md
    summary: /home/louisdup/Agents/claude/docs/COMPLETE_FRAMEWORK_SUMMARY.md

  implementation_guides:
    documents: /home/louisdup/Agents/claude/docs/DOCUMENT_INTEGRATION_GUIDE.md
    ui: /home/louisdup/Agents/claude/docs/UI_INTEGRATION_GUIDE.md
    external_access: /home/louisdup/Agents/claude/docs/EXTERNAL_AGENT_ACCESS_GUIDE.md

  setup_guides:
    quickstart: /home/louisdup/Agents/claude/SUPERIOR_BRAIN_QUICKSTART.md
    detailed: /home/louisdup/Agents/claude/SUPERIOR_BRAIN_SETUP.md
```

### Core Brain Implementation

```yaml
core_brain:
  main: /home/louisdup/Agents/claude/superior_agent_brain.py

  class: SuperiorAgentBrain

  entry_points:
    - method: chat(message, user_id)
    - method: process_query(query, user_id, use_memory)
    - method: save_session(summary)
    - method: sleep(conversation_days, performance_days)
    - method: get_brain_status()

  imports:
    - from superior_agent_brain import SuperiorAgentBrain
```

### Memory Systems

```yaml
memory_systems:
  base_path: /home/louisdup/Agents/claude/memory

  vector_memory:
    path: /home/louisdup/Agents/claude/memory/vector_memory.py
    class: VectorMemory
    purpose: Episodic/semantic memory using Qdrant
    database: qdrant
    collection: agent_memory

  persistent_memory:
    path: /home/louisdup/Agents/claude/memory/persistent_memory.py
    class: PersistentMemory
    purpose: Long-term conversation storage
    database: neon_postgresql
    tables:
      - conversations
      - messages
      - agent_actions

  meta_learner:
    path: /home/louisdup/Agents/claude/memory/meta_learner.py
    class: MetaLearner
    purpose: Performance tracking and learning
    database: neon_postgresql
    tables:
      - agent_performance
      - routing_history
      - learning_insights

  knowledge_graph:
    path: /home/louisdup/Agents/claude/memory/knowledge_graph.py
    class: KnowledgeGraph
    purpose: Cross-agent shared learning
    database: neon_postgresql
    tables:
      - knowledge_nodes
      - knowledge_edges
      - agent_contributions

  consolidation:
    path: /home/louisdup/Agents/claude/memory/consolidation.py
    class: MemoryConsolidation
    purpose: Memory optimization (like sleep)
    database: neon_postgresql
    tables:
      - consolidated_memories
      - consolidation_runs

  module_init:
    path: /home/louisdup/Agents/claude/memory/__init__.py
```

### Orchestration

```yaml
orchestration:
  base_path: /home/louisdup/Agents/claude/orchestrator

  orchestrator:
    path: /home/louisdup/Agents/claude/orchestrator/orchestrator.py
    class: AgentOrchestrator
    purpose: Route tasks to specialized agents

  registry:
    path: /home/louisdup/Agents/claude/orchestrator/registry.json
    format: json
    content: List of registered agents

  organigram:
    path: /home/louisdup/Agents/claude/orchestrator/organigram.py
    purpose: Workforce visualization
```

### Specialized Agents

```yaml
agents:
  database_agents:
    neon:
      path: /home/louisdup/Agents/claude/neon_agent.py
      class: NeonAgent
      purpose: PostgreSQL/Neon database queries

    convex:
      path: /home/louisdup/Agents/claude/convex_agent.py
      class: ConvexAgent
      purpose: Convex real-time database

    universal_convex:
      path: /home/louisdup/Agents/claude/universal_convex_agent.py
      class: UniversalConvexAgent
      purpose: Dynamic Convex table access

    dual:
      path: /home/louisdup/Agents/claude/ui-module/dual_agent.py
      class: DualDatabaseAgent
      purpose: Dual Neon + Convex support
```

### UI Layer

```yaml
ui_layer:
  base_path: /home/louisdup/Agents/claude/ui-module

  backend:
    current:
      path: /home/louisdup/Agents/claude/ui-module/unified_agent_api.py
      framework: FastAPI/Flask
      port: 8000

    enhanced:
      path: /home/louisdup/Agents/claude/ui-module/enhanced_agent_api.py
      status: implementation_ready
      features:
        - full_brain_integration
        - document_rag
        - memory_recall
        - websocket_support

  frontend:
    current:
      path: /home/louisdup/Agents/claude/ui-module/unified_chat.html
      type: web_interface

    enhanced:
      path: /home/louisdup/Agents/claude/ui-module/enhanced_chat.html
      status: implementation_ready
      features:
        - memory_indicators
        - source_citations
        - similar_queries
        - agent_display
```

### Document RAG System

```yaml
document_rag:
  base_path: /home/louisdup/Agents/claude/document_rag
  status: implementation_ready

  components:
    ingestion:
      path: /home/louisdup/Agents/claude/document_rag/document_ingestion.py
      status: design_complete

    embeddings:
      path: /home/louisdup/Agents/claude/document_rag/document_embeddings.py
      status: design_complete

    search:
      path: /home/louisdup/Agents/claude/document_rag/document_search.py
      status: design_complete

    organizer:
      path: /home/louisdup/Agents/claude/document_rag/document_organizer.py
      status: design_complete

    pipeline:
      path: /home/louisdup/Agents/claude/document_rag/rag_pipeline.py
      status: design_complete
      class: RAGPipeline
```

### Skills

```yaml
skills:
  base_path: /home/louisdup/Agents/claude/skills

  codebase_documenter:
    path: /home/louisdup/Agents/claude/skills/codebase-documenter
    purpose: Automated documentation generation

  test_specialist:
    path: /home/louisdup/Agents/claude/skills/test-specialist
    purpose: Test execution and analysis

  tech_debt_analyzer:
    path: /home/louisdup/Agents/claude/skills/tech-debt-analyzer
    purpose: Code quality analysis

  context_engineering:
    path: /home/louisdup/Agents/claude/skills/context-engineering
    purpose: Context optimization
```

### Configuration Files

```yaml
configuration:
  environment:
    path: /home/louisdup/Agents/claude/.env
    format: key=value
    required_variables:
      - ANTHROPIC_API_KEY
      - NEON_DATABASE_URL
      - CONVEX_URL
      - QDRANT_URL (optional)
      - QDRANT_API_KEY (optional)

  requirements:
    superior_brain:
      path: /home/louisdup/Agents/claude/requirements_superior_brain.txt
      dependencies:
        - qdrant-client>=1.7.0
        - numpy>=1.24.0
        - psycopg2-binary>=2.9.9
        - anthropic>=0.18.0
```

---

## 🔌 API Access Points

### HTTP API (Current)

```yaml
api:
  base_url: http://localhost:8000

  endpoints:
    chat:
      method: POST
      path: /chat
      request:
        message: string
        user_id: string (optional)
      response:
        response: string
        metadata: object

    status:
      method: GET
      path: /status
      response:
        session_id: string
        components: object
        features: object
```

### Enhanced API (Implementation Ready)

```yaml
enhanced_api:
  implementation: /home/louisdup/Agents/claude/ui-module/enhanced_agent_api.py
  base_url: http://localhost:8000

  endpoints:
    chat:
      method: POST
      path: /chat
      request:
        message: string
        user_id: string
        use_memory: boolean
        use_documents: boolean
      response:
        response: string
        metadata: object
        sources: array
        similar_queries: array

    status:
      method: GET
      path: /status

    save_session:
      method: POST
      path: /save_session

    reset_conversation:
      method: POST
      path: /reset_conversation

    consolidate_memory:
      method: POST
      path: /consolidate_memory

    list_agents:
      method: GET
      path: /agents

    reindex_documents:
      method: POST
      path: /reindex_documents

    websocket:
      protocol: WebSocket
      path: /ws/chat
```

---

## 💻 Python Integration for External Agents

### Method 1: Direct Import

```python
import sys
sys.path.insert(0, '/home/louisdup/Agents/claude')

from superior_agent_brain import SuperiorAgentBrain

# Initialize
brain = SuperiorAgentBrain(
    enable_vector_memory=True,
    enable_persistent_memory=True,
    enable_meta_learning=True,
    enable_knowledge_graph=True,
    enable_orchestration=True
)

# Use
response = brain.chat("Your query here", user_id="external_agent_1")
print(response)

# Get status
status = brain.get_brain_status()

# Cleanup
brain.close()
```

### Method 2: HTTP API

```python
import requests

API_BASE = "http://localhost:8000"

# Chat
response = requests.post(f"{API_BASE}/chat", json={
    "message": "Your query here",
    "user_id": "external_agent_1",
    "use_memory": True,
    "use_documents": True
})

data = response.json()
print(data['response'])
print(f"Sources: {data.get('sources', [])}")
print(f"Similar queries: {data.get('similar_queries', [])}")
```

### Method 3: WebSocket (Real-time)

```python
import websocket
import json

ws = websocket.WebSocket()
ws.connect("ws://localhost:8000/ws/chat")

# Send message
ws.send(json.dumps({
    "message": "Your query here",
    "user_id": "external_agent_1",
    "use_memory": True,
    "use_documents": True
}))

# Receive response
response = json.loads(ws.recv())
print(response['response'])

ws.close()
```

---

## 🗄️ Database Access

### Qdrant Vector Database

```yaml
qdrant:
  host: localhost
  port: 6333
  protocol: http

  collections:
    agent_memory:
      dimension: 1024
      distance: cosine
      purpose: Episodic/semantic memory

    document_embeddings:
      dimension: 1024
      distance: cosine
      purpose: Document RAG

    conversation_memory:
      dimension: 1024
      distance: cosine
      purpose: Persistent conversation embeddings

  access:
    url: http://localhost:6333
    api_key: optional

  python_client:
    code: |
      from qdrant_client import QdrantClient

      client = QdrantClient(
          url="http://localhost:6333",
          api_key=None  # or your API key
      )

      # Search
      results = client.search(
          collection_name="agent_memory",
          query_vector=[...],  # Your embedding
          limit=5
      )
```

### Neon PostgreSQL

```yaml
neon:
  connection_string: ${NEON_DATABASE_URL}

  schemas:
    conversations:
      table: conversations
      columns:
        - id (SERIAL PRIMARY KEY)
        - user_id (VARCHAR)
        - session_id (VARCHAR)
        - summary (TEXT)
        - created_at (TIMESTAMP)
        - metadata (JSONB)

    messages:
      table: messages
      columns:
        - id (SERIAL PRIMARY KEY)
        - conversation_id (INTEGER)
        - role (VARCHAR)
        - content (TEXT)
        - timestamp (TIMESTAMP)

    agent_performance:
      table: agent_performance
      columns:
        - id (SERIAL PRIMARY KEY)
        - agent_id (VARCHAR)
        - task_type (VARCHAR)
        - success (BOOLEAN)
        - execution_time_ms (INTEGER)
        - timestamp (TIMESTAMP)

    knowledge_nodes:
      table: knowledge_nodes
      columns:
        - id (SERIAL PRIMARY KEY)
        - node_type (VARCHAR)
        - name (VARCHAR)
        - description (TEXT)
        - confidence (FLOAT)
        - source_agent (VARCHAR)

  access:
    python_code: |
      import os
      import psycopg2
      from psycopg2.extras import RealDictCursor

      conn = psycopg2.connect(
          os.environ['NEON_DATABASE_URL'],
          cursor_factory=RealDictCursor
      )

      with conn.cursor() as cursor:
          cursor.execute("SELECT * FROM conversations LIMIT 10")
          results = cursor.fetchall()
```

### Convex

```yaml
convex:
  url: ${CONVEX_URL}

  tables:
    - tasks
    - contractors
    - projects
    - boqs
    - rfqs
    - quotes
    - (35+ total tables)

  access:
    http_api:
      query_endpoint: ${CONVEX_URL}/api/query
      mutation_endpoint: ${CONVEX_URL}/api/mutation

    python_code: |
      import requests
      import os

      CONVEX_URL = os.environ['CONVEX_URL']

      # Query
      response = requests.post(
          f"{CONVEX_URL}/api/query",
          json={
              "path": "contractors:list",
              "args": {"limit": 10}
          }
      )

      data = response.json()
```

---

## 📋 System Capabilities Manifest

### What External Agents Can Do

```yaml
capabilities:
  query:
    - Ask questions in natural language
    - Get contextual responses
    - Receive source citations
    - See similar past queries

  memory:
    - Access past conversations
    - Find similar interactions
    - Learn from performance
    - Share knowledge

  documents:
    - Search documentation semantically
    - Get relevant context
    - Cite sources
    - Ingest new documents

  agents:
    - Route to specialists
    - Execute database queries
    - Monitor systems
    - Run tests
    - Generate documentation

  learning:
    - Track performance
    - Identify patterns
    - Improve over time
    - Share learnings
```

---

## 🔐 Authentication & Security

### Current Setup

```yaml
authentication:
  type: environment_variables
  required:
    - ANTHROPIC_API_KEY: For Claude LLM access
    - NEON_DATABASE_URL: For database access

  optional:
    - QDRANT_API_KEY: For Qdrant Cloud
    - CONVEX_AUTH_KEY: For Convex authentication

security:
  level: development
  notes: |
    - No user authentication in current implementation
    - API accessible on localhost only
    - Production deployment requires:
      * User authentication
      * API key management
      * Rate limiting
      * HTTPS/TLS
```

---

## 📡 External Agent Integration Patterns

### Pattern 1: Query & Response

```python
# External agent queries this system
import sys
sys.path.insert(0, '/home/louisdup/Agents/claude')
from superior_agent_brain import SuperiorAgentBrain

brain = SuperiorAgentBrain()
result = brain.process_query(
    query="What contractors are active?",
    user_id="external_agent_alpha"
)

response_data = {
    "answer": result['response'],
    "agent_used": result['metadata']['selected_agent'],
    "execution_time": result['metadata']['execution_time_seconds'],
    "sources": result['metadata'].get('sources', [])
}

brain.close()
```

### Pattern 2: Knowledge Sharing

```python
# External agent contributes knowledge
from memory.knowledge_graph import KnowledgeGraph

kg = KnowledgeGraph()

# Share a learning
kg.learn_from_success(
    problem_description="Connection timeout to API",
    solution_description="Increased retry attempts to 3 with exponential backoff",
    agent_id="external_agent_alpha",
    confidence=0.95
)
```

### Pattern 3: Document Contribution

```python
# External agent adds documents
from document_rag.document_ingestion import DocumentIngestion
from document_rag.document_embeddings import DocumentEmbeddings

ingestion = DocumentIngestion()
embedder = DocumentEmbeddings()

# Add document
doc = {
    "id": "external_doc_1",
    "title": "API Integration Guide",
    "content": "...",
    "source": "external_agent_alpha",
    "metadata": {"type": "guide"}
}

embedder.embed_documents([doc])
```

### Pattern 4: Performance Tracking

```python
# External agent reports performance
from memory.meta_learner import MetaLearner

learner = MetaLearner()

learner.track_outcome(
    agent_id="external_agent_alpha",
    task_type="api_integration",
    query="Connect to external API",
    success=True,
    execution_time_ms=250
)
```

---

## 🗺️ Discovery Endpoints

### For External Agents to Self-Discover

```python
# Get system manifest
def discover_system():
    """External agent discovers this system's capabilities."""
    manifest = {
        "system_name": "Superior Agent Brain",
        "version": "2.0",
        "location": "/home/louisdup/Agents/claude",

        "entry_points": {
            "python": "superior_agent_brain.SuperiorAgentBrain",
            "http": "http://localhost:8000",
            "websocket": "ws://localhost:8000/ws/chat"
        },

        "capabilities": [
            "natural_language_query",
            "memory_recall",
            "document_search",
            "task_routing",
            "performance_learning",
            "knowledge_sharing"
        ],

        "documentation": {
            "master_index": "/home/louisdup/Agents/claude/docs/MASTER_INDEX.md",
            "architecture": "/home/louisdup/Agents/claude/docs/COMPLETE_BRAIN_ARCHITECTURE.md",
            "external_access": "/home/louisdup/Agents/claude/docs/EXTERNAL_AGENT_ACCESS_GUIDE.md"
        },

        "databases": {
            "qdrant": "http://localhost:6333",
            "neon": "postgresql://...",
            "convex": "https://..."
        }
    }

    return manifest
```

### System Status Check

```python
# Check if system is operational
def check_system_health():
    """External agent checks system health."""
    try:
        from superior_agent_brain import SuperiorAgentBrain

        brain = SuperiorAgentBrain()
        status = brain.get_brain_status()

        health = {
            "operational": True,
            "components": status['components'],
            "session_id": status['session_id'],
            "agent_count": status.get('agent_stats', {}).get('total_agents', 0)
        }

        brain.close()
        return health

    except Exception as e:
        return {
            "operational": False,
            "error": str(e)
        }
```

---

## 📖 Quick Reference for External Agents

### Essential Paths

```bash
# Main entry point
/home/louisdup/Agents/claude/superior_agent_brain.py

# Documentation hub
/home/louisdup/Agents/claude/docs/MASTER_INDEX.md

# Memory systems
/home/louisdup/Agents/claude/memory/

# Configuration
/home/louisdup/Agents/claude/.env
```

### Essential Imports

```python
# Core brain
from superior_agent_brain import SuperiorAgentBrain

# Memory systems
from memory import (
    VectorMemory,
    PersistentMemory,
    MetaLearner,
    KnowledgeGraph,
    MemoryConsolidation
)

# Orchestration
from orchestrator.orchestrator import AgentOrchestrator

# Document RAG (when implemented)
from document_rag.rag_pipeline import RAGPipeline
```

### Essential Endpoints

```
GET  http://localhost:8000/status
POST http://localhost:8000/chat
WS   ws://localhost:8000/ws/chat
```

---

## 🔄 Data Exchange Format

### Standard Request Format

```json
{
  "message": "User query here",
  "user_id": "external_agent_id",
  "session_id": "optional_session_id",
  "use_memory": true,
  "use_documents": true,
  "metadata": {
    "source": "external_agent",
    "priority": "normal"
  }
}
```

### Standard Response Format

```json
{
  "response": "Generated answer here",
  "metadata": {
    "execution_time_seconds": 1.23,
    "selected_agent": "neon-agent",
    "similar_experiences_found": 2,
    "timestamp": "2025-11-19T12:00:00Z"
  },
  "sources": [
    {
      "title": "Document title",
      "path": "/path/to/doc",
      "relevance": 0.95,
      "excerpt": "..."
    }
  ],
  "similar_queries": [
    {
      "query": "Similar past query",
      "response_preview": "...",
      "similarity": 0.87
    }
  ]
}
```

---

## 🛠️ External Agent Development Kit

### Minimal Integration Example

```python
#!/usr/bin/env python3
"""
Minimal external agent integration with Superior Brain
"""

import sys
import os

# Add Superior Brain to path
sys.path.insert(0, '/home/louisdup/Agents/claude')

# Load environment
from pathlib import Path
env_path = Path('/home/louisdup/Agents/claude/.env')
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

# Import and use
from superior_agent_brain import SuperiorAgentBrain

class ExternalAgent:
    """External agent that integrates with Superior Brain."""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.brain = SuperiorAgentBrain()

    def query(self, message: str) -> dict:
        """Send query to Superior Brain."""
        result = self.brain.process_query(
            query=message,
            user_id=self.agent_id
        )
        return result

    def close(self):
        """Cleanup."""
        self.brain.close()

# Usage
if __name__ == "__main__":
    agent = ExternalAgent("external_agent_demo")

    result = agent.query("What contractors are active?")
    print(f"Response: {result['response']}")
    print(f"Agent used: {result['metadata']['selected_agent']}")

    agent.close()
```

---

## 📞 Support for External Agents

### Documentation
- **Full Reference:** `/home/louisdup/Agents/claude/docs/MASTER_INDEX.md`
- **Architecture:** `/home/louisdup/Agents/claude/docs/COMPLETE_BRAIN_ARCHITECTURE.md`
- **This Guide:** `/home/louisdup/Agents/claude/docs/EXTERNAL_AGENT_ACCESS_GUIDE.md`

### Code Examples
- **Main Brain:** `/home/louisdup/Agents/claude/superior_agent_brain.py`
- **Memory Systems:** `/home/louisdup/Agents/claude/memory/`
- **Agents:** `/home/louisdup/Agents/claude/*_agent.py`

### Contact
- **System Location:** `/home/louisdup/Agents/claude`
- **API:** `http://localhost:8000` (when running)

---

**Document Version:** 1.0
**System Version:** 2.0 - Complete
**Last Updated:** 2025-11-19
**Maintained By:** Superior Agent Brain Team

---

## ✅ Quick Access Checklist for External Agents

```
□ Read this guide
□ Check system health (see "System Status Check")
□ Review capabilities manifest
□ Choose integration pattern (Direct/HTTP/WebSocket)
□ Test connection
□ Start integration
□ Contribute knowledge back to system
```

**Everything an external agent needs to integrate is documented above.**
