# Superior Agent Brain - Setup Guide

## Overview

The Superior Agent Brain is a complete AI cognitive system that mimics human brain architecture. It integrates multiple memory systems, learning capabilities, and specialized processing units.

## Architecture

```
Superior Agent Brain
├── CPU (Processing)         → Claude Sonnet 4.5
├── RAM (Working Memory)     → 200K context window
├── Memory Systems
│   ├── Vector Memory        → Qdrant (episodic/semantic)
│   ├── Persistent Memory    → Neon PostgreSQL (long-term)
│   ├── Meta-Learner         → Performance tracking
│   ├── Knowledge Graph      → Shared learning
│   └── Consolidation        → Memory optimization
├── Executive Function       → Orchestrator
└── Specialized Agents       → Domain experts
```

## Prerequisites

### 1. Required Services

**Qdrant Vector Database**
```bash
# Option 1: Docker
docker pull qdrant/qdrant
docker run -p 6333:6333 qdrant/qdrant

# Option 2: Cloud (Qdrant Cloud)
# Sign up at https://cloud.qdrant.io
```

**Neon PostgreSQL**
- Already configured (NEON_DATABASE_URL in .env)

**Anthropic API**
- Already configured (ANTHROPIC_API_KEY in .env)

### 2. Python Dependencies

```bash
# Install new dependencies
pip install qdrant-client numpy psycopg2-binary anthropic
```

Add to `requirements.txt`:
```
qdrant-client>=1.7.0
numpy>=1.24.0
psycopg2-binary>=2.9.9
anthropic>=0.18.0
```

### 3. Environment Variables

Add to `.env`:
```bash
# Existing
ANTHROPIC_API_KEY=your_key_here
NEON_DATABASE_URL=postgresql://...

# New for Superior Brain
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=  # Optional, for cloud
```

## Installation

### Step 1: Install Qdrant

**Using Docker (Recommended for local development):**
```bash
# Pull and run Qdrant
docker run -d -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage:z \
  qdrant/qdrant

# Verify it's running
curl http://localhost:6333/
```

**Using Qdrant Cloud:**
1. Sign up at https://cloud.qdrant.io
2. Create a cluster
3. Get your API key and URL
4. Add to `.env`:
   ```bash
   QDRANT_URL=https://your-cluster.qdrant.io
   QDRANT_API_KEY=your_api_key
   ```

### Step 2: Install Python Dependencies

```bash
# Install required packages
pip install qdrant-client numpy

# Verify installations
python -c "import qdrant_client; print('Qdrant client installed')"
python -c "import numpy; print('NumPy installed')"
```

### Step 3: Initialize Database Schema

The brain will automatically create necessary tables on first run, but you can manually initialize:

```bash
# Initialize all memory systems
python -c "
from memory import PersistentMemory, MetaLearner, KnowledgeGraph
from memory.consolidation import MemoryConsolidation

# This will create all required tables
PersistentMemory()
MetaLearner()
KnowledgeGraph()
MemoryConsolidation()

print('✅ All schemas initialized')
"
```

### Step 4: Test Individual Components

**Test Vector Memory:**
```bash
python memory/vector_memory.py
```

**Test Persistent Memory:**
```bash
python memory/persistent_memory.py
```

**Test Meta-Learner:**
```bash
python memory/meta_learner.py
```

**Test Knowledge Graph:**
```bash
python memory/knowledge_graph.py
```

**Test Consolidation:**
```bash
python memory/consolidation.py
```

### Step 5: Run Complete Brain

```bash
python superior_agent_brain.py
```

## Usage

### Basic Usage

```python
from superior_agent_brain import SuperiorAgentBrain

# Initialize brain
brain = SuperiorAgentBrain()

# Ask a question
response = brain.chat("What contractors are in the system?")
print(response)

# Save session
brain.save_session(summary="Queried contractor data")

# Cleanup
brain.close()
```

### Advanced Usage

```python
from superior_agent_brain import SuperiorAgentBrain

# Initialize with specific configuration
brain = SuperiorAgentBrain(
    model="claude-sonnet-4-5-20250929",
    enable_vector_memory=True,
    enable_persistent_memory=True,
    enable_meta_learning=True,
    enable_knowledge_graph=True,
    enable_orchestration=True
)

# Process query with full pipeline
result = brain.process_query(
    query="How many active projects do we have?",
    user_id="user_123",
    use_memory=True
)

print(f"Response: {result['response']}")
print(f"Time: {result['metadata']['execution_time_seconds']}s")
print(f"Agent: {result['metadata']['selected_agent']}")
print(f"Similar experiences: {result['metadata']['similar_experiences_found']}")

# Run memory consolidation (like sleep)
brain.sleep(conversation_days=30, performance_days=60)

# Get brain status
status = brain.get_brain_status()
print(json.dumps(status, indent=2))

# Cleanup
brain.close()
```

### Memory Management

```python
from superior_agent_brain import SuperiorAgentBrain

brain = SuperiorAgentBrain()

# Regular conversation
brain.chat("Query 1")
brain.chat("Query 2")
brain.chat("Query 3")

# Save session
brain.save_session(summary="Discussion about projects")

# Clear working memory (keep long-term intact)
brain.reset_conversation()

# Run consolidation to optimize stored memories
brain.sleep(conversation_days=7)

brain.close()
```

## Component Details

### 1. Vector Memory (Qdrant)

**Purpose:** Episodic and semantic memory - remembers similar past experiences

**Features:**
- Stores conversation embeddings
- Finds similar past queries
- Enables "I've seen this before" reasoning

**Usage:**
```python
from memory import VectorMemory

memory = VectorMemory(collection_name="my_agent")

# Store interaction
memory.store_interaction(
    query="How do I fix database errors?",
    response="Check connection string and network access",
    agent_id="database-agent",
    success=True
)

# Recall similar
similar = memory.recall_similar(
    query="Database won't connect",
    limit=5
)

for mem in similar:
    print(f"Similar (score: {mem['score']:.2f}): {mem['query']}")
```

### 2. Persistent Memory (Neon + Qdrant)

**Purpose:** Cross-session conversation storage

**Features:**
- Stores full conversations in PostgreSQL
- Creates searchable summaries in Qdrant
- Enables context continuity across sessions

**Usage:**
```python
from memory import PersistentMemory

memory = PersistentMemory()

# Save conversation
messages = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! How can I help?"}
]

conv_id = memory.save_conversation(
    user_id="user_123",
    session_id="session_001",
    messages=messages,
    summary="Greeting exchange"
)

# Load later
conversation = memory.load_conversation(conv_id)
```

### 3. Meta-Learner

**Purpose:** Performance tracking and continuous improvement

**Features:**
- Tracks agent success rates
- Identifies best agent for each task type
- Extracts learning insights over time

**Usage:**
```python
from memory import MetaLearner

learner = MetaLearner()

# Track outcome
learner.track_outcome(
    agent_id="neon-agent",
    task_type="database_query",
    query="List contractors",
    success=True,
    execution_time_ms=150
)

# Get success rate
stats = learner.get_agent_success_rate("neon-agent")
print(f"Success rate: {stats['success_rate']:.1%}")

# Get best agent for task
best = learner.get_best_agent_for_task("database_query")
print(f"Best agent: {best['agent_id']} ({best['success_rate']:.1%})")
```

### 4. Knowledge Graph

**Purpose:** Cross-agent learning and relationship mapping

**Features:**
- Agents share learnings with each other
- Maps relationships between concepts
- Finds solution paths for problems

**Usage:**
```python
from memory import KnowledgeGraph

kg = KnowledgeGraph()

# Agent learns a solution
kg.learn_from_success(
    problem_description="Database timeout errors",
    solution_description="Increase connection pool to 20",
    agent_id="database-agent",
    confidence=0.95
)

# Find solutions
problem = kg.find_node("problem", "Database timeout errors")
solutions = kg.find_solution_path(problem['id'])

for sol in solutions:
    print(f"Solution: {sol['name']} (confidence: {sol['confidence']:.1%})")
```

### 5. Memory Consolidation

**Purpose:** Optimize and compress old memories (like sleep)

**Features:**
- Compresses old conversations into summaries
- Aggregates performance data
- Archives low-value data
- Maintains memory quality

**Usage:**
```python
from memory.consolidation import MemoryConsolidation

consolidator = MemoryConsolidation()

# Run full consolidation
results = consolidator.run_full_consolidation(
    conversation_days=30,  # Consolidate conversations older than 30 days
    performance_days=60    # Consolidate performance data older than 60 days
)

print(f"Consolidated: {results['conversations']['conversations_consolidated']} conversations")
print(f"Created: {results['performance']['aggregates_created']} performance aggregates")
```

## Maintenance

### Daily Operations

```bash
# No daily maintenance required
# The brain handles memory automatically
```

### Weekly Maintenance

```python
# Run memory consolidation (recommended weekly)
from superior_agent_brain import SuperiorAgentBrain

brain = SuperiorAgentBrain()
brain.sleep(conversation_days=7, performance_days=14)
brain.close()
```

### Monthly Maintenance

```bash
# Check memory statistics
python -c "
from superior_agent_brain import SuperiorAgentBrain
import json

brain = SuperiorAgentBrain()
status = brain.get_brain_status()
print(json.dumps(status, indent=2, default=str))
brain.close()
"
```

### Backup

```bash
# Backup Qdrant collections
docker exec qdrant_container /bin/sh -c \
  "cd /qdrant && tar czf /backup/qdrant-$(date +%Y%m%d).tar.gz storage/"

# Neon is already backed up automatically
```

## Troubleshooting

### Qdrant Connection Issues

```python
# Test Qdrant connection
import requests
response = requests.get("http://localhost:6333/")
print(response.json())  # Should show Qdrant info

# If connection fails:
# 1. Check Docker: docker ps | grep qdrant
# 2. Check port: netstat -an | grep 6333
# 3. Restart: docker restart qdrant_container
```

### Memory Errors

```bash
# If "out of memory" errors occur:
# 1. Run consolidation more frequently
# 2. Reduce conversation history size
# 3. Archive old data
```

### Database Schema Issues

```bash
# Reset schemas (WARNING: deletes all data)
python -c "
import psycopg2
import os

conn = psycopg2.connect(os.environ['NEON_DATABASE_URL'])
cursor = conn.cursor()

# Drop all tables
cursor.execute('DROP TABLE IF EXISTS agent_actions CASCADE')
cursor.execute('DROP TABLE IF EXISTS messages CASCADE')
cursor.execute('DROP TABLE IF EXISTS conversations CASCADE')
cursor.execute('DROP TABLE IF EXISTS agent_performance CASCADE')
cursor.execute('DROP TABLE IF EXISTS routing_history CASCADE')
cursor.execute('DROP TABLE IF EXISTS learning_insights CASCADE')
cursor.execute('DROP TABLE IF EXISTS knowledge_nodes CASCADE')
cursor.execute('DROP TABLE IF EXISTS knowledge_edges CASCADE')
cursor.execute('DROP TABLE IF EXISTS agent_contributions CASCADE')
cursor.execute('DROP TABLE IF EXISTS consolidated_memories CASCADE')
cursor.execute('DROP TABLE IF EXISTS consolidation_runs CASCADE')

conn.commit()
print('✅ All tables dropped')
"

# Then reinitialize
python superior_agent_brain.py
```

## Performance Optimization

### Embedding Performance

For production, use a proper embedding service instead of the simple hash-based approach:

```python
# Install Voyage AI
pip install voyageai

# Update .env
VOYAGE_API_KEY=your_key

# Use in code
from memory.vector_memory import EmbeddingService

embedder = EmbeddingService(provider="voyage")
embedding = embedder.embed("Your text here")
```

### Database Performance

```sql
-- Add indexes for common queries
CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);
CREATE INDEX IF NOT EXISTS idx_agent_perf_timestamp ON agent_performance(timestamp);

-- Vacuum and analyze
VACUUM ANALYZE conversations;
VACUUM ANALYZE messages;
VACUUM ANALYZE agent_performance;
```

## Next Steps

1. **Integrate with UI**: Connect superior brain to `ui-module/unified_agent_api.py`
2. **Add More Agents**: Register specialized agents in orchestrator
3. **Tune Parameters**: Adjust consolidation schedules and memory limits
4. **Monitor Performance**: Track response times and memory usage
5. **Implement Embeddings**: Use Voyage AI or OpenAI for better semantic search

## Support

- Documentation: See `AI_AGENT_BRAIN_ARCHITECTURE.md`
- Issues: Check `TROUBLESHOOTING.md`
- Code: All components in `memory/` directory

---

**Status:** ✅ Complete and operational
**Version:** 1.0
**Last Updated:** 2025-11-19
