# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**FibreFlow Agent Workforce** - Multi-agent AI system for fiber optic infrastructure operations using Claude Agent SDK. Features specialized AI agents coordinated by an orchestrator, dual database backends (Neon PostgreSQL + Convex), and advanced memory systems.

**Production URL**: http://72.60.17.245/
**Deployment**: Hostinger VPS (srv1092611.hstgr.cloud, Lithuania)

## Commands

### Testing
```bash
# Run all tests
./venv/bin/pytest tests/ -v

# Run specific agent tests
./venv/bin/pytest tests/test_vps_monitor.py -v
./venv/bin/pytest tests/test_orchestrator.py -v

# Test Neon database agent
./venv/bin/python3 test_neon.py

# Test Convex backend agent
./venv/bin/python3 test_convex.py

# Test agent orchestration
./venv/bin/python3 orchestrator/orchestrator.py
```

### Development
```bash
# Activate virtual environment (always required)
source venv/bin/activate

# Run Neon agent demo (interactive)
./venv/bin/python3 demo_neon_agent.py

# Run VPS monitor agent
cd agents/vps-monitor && ../../venv/bin/python3 demo.py

# Sync Neon data to Convex
./venv/bin/python3 sync_neon_to_convex.py

# View agent workforce structure
./venv/bin/python3 orchestrator/organigram.py
cat AGENT_ORGANIGRAM.txt
```

### Convex Backend
```bash
# Deploy Convex functions
npx convex deploy

# Dev mode with auto-reload
npx convex dev

# Test deployed functions
./venv/bin/python3 test_convex_deployed_functions.py
```

### Production Deployment
```bash
# Deploy Superior Agent Brain API
cd deploy && ./deploy_brain.sh

# Run FastAPI agent server
./venv/bin/python3 ui-module/agent_api.py
```

### Development & Deployment Workflow

**Recommended Approach**: Local Development → GitHub → VPS Deployment

**Why NOT develop directly on server**:
- No rollback capability if something breaks
- Risk of breaking production while editing
- No version history or blame tracking
- Difficult to collaborate with team
- No staging/testing environment

**Current Best Practice Workflow**:
```bash
# 1. Develop locally
git add .
git commit -m "feat: Add new capability"

# 2. Push to GitHub (version control + backup)
git push origin main

# 3. Deploy to VPS
ssh louisdup@72.60.17.245
cd /home/louisdup/agents
git pull origin main
./venv/bin/pip install -r requirements.txt  # If deps changed
sudo systemctl restart fibreflow-api        # Restart service
```

**Automated Deployment (Recommended)**:
```bash
# Set up GitHub Actions for auto-deploy on push
# See .github/workflows/deploy.yml for example
```

**Quick Sync Script** (`deploy/sync.sh`):
```bash
#!/bin/bash
# One-command deployment from local to production
rsync -avz --exclude='.env' --exclude='venv/' \
  ./ louisdup@72.60.17.245:/home/louisdup/agents/
ssh louisdup@72.60.17.245 "cd /home/louisdup/agents && \
  source venv/bin/activate && \
  pip install -r requirements.txt && \
  sudo systemctl restart fibreflow-api"
```

**For detailed deployment strategies, see `docs/guides/DEPLOYMENT_WORKFLOW.md`**

### Monitoring & Performance
```bash
# View metrics and performance
./venv/bin/python3 -m metrics.collector  # Test metrics collection
./venv/bin/python3 -m benchmarks.performance_suite  # Run benchmarks

# Check skill versions
./venv/bin/python3 .claude/skills/skill_version_manager.py

# View logs
tail -f logs/fibreflow.log
tail -f logs/fibreflow_errors.log

# Generate performance report
./venv/bin/python3 -c "from metrics.collector import get_collector; \
  print(get_collector().generate_report())"
```

**Logging**:
- Structured logging with JSON format for production
- Colored console output for development
- Automatic request tracking and performance metrics
- Error aggregation in separate log file

**Metrics Collection**:
- Agent performance (response time, success rate)
- Skill usage and effectiveness
- Token consumption tracking
- System health monitoring

**Performance Targets** (from `.claude/config.yaml`):
- Skill response time: <100ms
- Context usage: <1000 tokens
- Success rate: >95%

**Benchmarking**:
- Comprehensive performance suite in `benchmarks/`
- Skills vs Agents comparison
- Database query performance
- Memory footprint analysis

## Architecture

### Skills-Based Architecture (Primary Approach)

**Status**: ✅ Production (as of 2025-12-09)

FibreFlow uses **Claude Code Skills** with progressive disclosure for database operations and other capabilities. This provides:
- **99% faster queries**: 23ms average (vs 2.3s without optimization)
- **84% less context**: 930 tokens per query (vs 4,500 with agents)
- **Native Claude Code integration**: Auto-discovery and progressive disclosure

**Skills Location**: `.claude/skills/`

**Current Skills**:
- `database-operations/` - Neon PostgreSQL interface with connection pooling
- `vf-server/` - VF Velocity server operations via SSH (Tailscale: 100.96.203.105)

**How It Works**:
```
User Query → Claude Code discovers skill (50 tokens metadata)
          → Loads full skill on-demand (600 tokens)
          → Executes script from filesystem (0 context cost)
          → Returns result (280 tokens)
= 930 tokens total, 23ms execution
```

**Key Innovation**: Scripts execute from filesystem, not loaded into context. Only results enter context.

**Using Skills**:
```bash
# Skills auto-discovered by Claude Code
# Just ask natural language questions:
"How many contractors are in the database?"
"Show me the projects table schema"
"Query active contractors with phone numbers"
```

**Performance**:
- First query: ~26ms (cold - initializes connection pool)
- Subsequent queries: ~22ms (pooled connections)
- Session of 10 queries: ~224ms total (0.2 seconds)

**Adding New Skills**:
1. Create `skill-name/` directory in `.claude/skills/`
2. Add `skill.md` with YAML frontmatter (metadata)
3. Create `scripts/` with executable tools
4. Claude Code auto-discovers on next session

**See**: `experiments/skills-vs-agents/FINAL_RESULTS.md` for complete performance analysis

### Multi-Agent Workforce System (Legacy/Fallback)

**Note**: Skills-based approach is now primary. Agents maintained for reference and complex fallback scenarios.

The system previously used **agent specialization** with intelligent routing:

```
User Request → Orchestrator (Claude Code) → Specialized Agent → Response
                      ↓
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
  VPS Monitor    Neon Database  Convex Backend
```

**Key Concept**: Each agent is an expert in a single domain. The orchestrator (`orchestrator/orchestrator.py`) uses keyword matching from `orchestrator/registry.json` to route tasks to the right agent.

**Adding a New Agent**:
1. Create directory: `agents/agent-name/`
2. Implement: `agents/agent-name/agent.py` (use `shared/base_agent.py` as template)
3. Register in: `orchestrator/registry.json` with triggers and capabilities
4. Document: `agents/agent-name/README.md`

### Database Architecture

**Dual Database Strategy**:
- **Neon PostgreSQL**: Production data (104 tables) for contractors, projects, BOQs, RFQs, clients, etc.
- **Convex**: Real-time task management backend with HTTP API

**Sync Flow**: Neon (source of truth) → `sync_neon_to_convex.py` → Convex (operational data)

**Important**: Convex functions are in `convex/` (TypeScript), Python agents call them via HTTP API.

### Memory Systems

**Core Principle**: *"The magic is in the memory. The agent is a policy that transforms one consistent memory state into another."*

FibreFlow implements **two distinct memory systems**:

#### 1. Domain Memory (Task-Level State)

**Purpose**: Track progress within a single long-running task or agent build

**Artifacts**:
- `feature_list.json` - Machine-readable backlog with pass/fail status (single source of truth)
- `claude_progress.md` - Human-readable session summaries
- Git commits - Atomic state snapshots
- Test results - Validation of "is it working?"

**Use when**: Building agents via harness, implementing multi-step features, ensuring task completion

**Key insight**: Each agent session is **stateless** (LLMs have no memory). Domain memory provides the scaffolding so agents know "where we are in the world."

**See**: `DOMAIN_MEMORY_GUIDE.md` for complete patterns and schemas

#### 2. Superior Agent Brain (Cross-Session Learning)

**Purpose**: Agents learn patterns, share knowledge, improve over time across different tasks

**Components** (`superior_agent_brain.py` and `memory/`):
- **Vector Memory**: Qdrant for semantic/episodic recall
- **Persistent Memory**: Neon for cross-session storage
- **Meta-Learning**: Performance tracking and improvement
- **Knowledge Graph**: Shared learning across agents
- **Memory Consolidation**: Background optimization

**Use when**: Need semantic search, meta-learning, knowledge sharing across agents

**Warning**: This is advanced "complete brain" architecture. Don't use for simple task tracking (overkill).

### Agent Types

**Infrastructure Agents**:
- `agents/vps-monitor/` - SSH-based VPS health monitoring (CPU, RAM, disk, processes)

**Database Agents**:
- `agents/neon-database/` - Natural language SQL interface for Neon PostgreSQL
- `agents/convex-database/` - Task management via Convex backend

**Skills** (in `skills/`):
- `codebase-documenter/` - Code documentation generation
- `tech-debt-analyzer/` - Technical debt analysis
- `test-specialist/` - Test generation and analysis
- `context-engineering/` - Context optimization
- `source-validation/` - Source validation

### Key Files

**Core Agents**:
- `neon_agent.py` - Neon PostgreSQL agent (main agent for database queries)
- `convex_agent.py` - Convex backend agent
- `orchestrator/orchestrator.py` - Task routing orchestrator
- `orchestrator/registry.json` - Agent catalog (source of truth)

**Deployment**:
- `deploy/brain_api.py` - FastAPI wrapper for Superior Agent Brain
- `deploy/deploy_brain.sh` - Deployment script
- `ui-module/agent_api.py` - Production FastAPI server
- `ui-module/chat.html` - Web interface

**Configuration**:
- `.env` - Environment variables (never commit!)
- `.env.example` - Template with all required variables
- `convex.json` - Convex deployment config
- `pytest.ini` - Pytest configuration

## MCP (Model Context Protocol) Configuration

FibreFlow uses MCPs for enhanced capabilities. Configuration is in `.claude/settings.local.json`.

### Current Setup (Profile-Based)

Since Docker Desktop MCP Gateway is not available (requires Docker Desktop, we use Docker Engine), we use **task-based profile switching**:

**Active MCPs**:
- `context7` - Always enabled (Python, FastAPI, PostgreSQL, pytest docs)

**Profile-Based MCPs** (enable as needed):
- `postgres-mcp` - Enable for database queries (profile: database)
- `github` - Enable for deployments/repo management (profile: deployment)
- `playwright-mcp` - Enable for UI testing (profile: testing)

**See**: `.claude/mcp-profiles.md` for profile switching guide

### Docker MCP Gateway (Not Available)

Docker's dynamic MCP Gateway requires **Docker Desktop** with beta features enabled. Our setup uses **Docker Engine** (CLI-only), which doesn't support the MCP Gateway feature.

**To use Docker MCP Gateway**, you would need:
1. Install Docker Desktop for Linux
2. Enable "Docker MCP Toolkit" in Settings → Beta features
3. Update MCP config to single `docker` connection

**Current Alternative**: Use profile-based MCP switching (simpler, no Docker Desktop required)

### Adding New MCPs

1. Add to `.claude/settings.local.json`:
```json
{
  "mcpServers": {
    "new-mcp-name": {
      "command": "npx",
      "args": ["-y", "@scope/mcp-package"],
      "description": "What this MCP does",
      "disabled": true,
      "profile": "category"
    }
  }
}
```

2. Enable when needed by removing `"disabled": true`
3. Restart Claude Code session to load MCP

### MCP Best Practices

- **Start with disabled**: Only enable MCPs when actually needed
- **Context efficiency**: Each active MCP adds tool definitions to context window
- **Environment variables**: Use `${VAR_NAME}` syntax for secrets (loads from `.env`)
- **Profiles**: Group MCPs by task type (database, testing, deployment)

## Environment Variables

Required in `.env`:
```bash
# All agents
ANTHROPIC_API_KEY=sk-ant-api03-...

# VPS Monitor
VPS_HOSTNAME=srv1092611.hstgr.cloud

# Neon Database
NEON_DATABASE_URL=postgresql://...

# Convex Backend
CONVEX_URL=https://quixotic-crow-802.convex.cloud

# VF Server Access (SSH key auth preferred)
VF_SERVER_HOST=100.96.203.105
VF_SERVER_USER=louis
# VF_SERVER_PASSWORD=<password>  # Optional - leave unset for SSH key auth
```

See `.env.example` for complete list with documentation.

## Database Context

**Neon PostgreSQL (104 tables)**:
- Fiber optic infrastructure deployment business
- Main entities: contractors (20 total, 9 active), projects (2), BOQs, RFQs, suppliers, clients
- Complex schema with performance tracking, approval workflows, material tracking
- Access via `neon_agent.py` or direct psycopg2 connection

**Convex Tables**:
- `tasks` - Task management
- `contractors` - Synced from Neon
- `projects` - Synced from Neon
- `syncRecords` - Sync operation tracking

## Testing Strategy

**Test Structure**:
- `tests/` - Pytest tests (unit + integration)
- `test_*.py` (root) - Agent-specific integration tests
- `demo_*.py` - Interactive demos for manual testing

**Test Markers** (in `pytest.ini`):
- `@pytest.mark.unit` - Fast, isolated tests
- `@pytest.mark.integration` - Slower, external resources
- `@pytest.mark.vps` - VPS Monitor agent tests
- `@pytest.mark.database` - Database agent tests
- `@pytest.mark.orchestrator` - Orchestrator tests

**Run specific categories**:
```bash
./venv/bin/pytest -m unit        # Fast tests only
./venv/bin/pytest -m integration # Integration tests
```

## Model Selection

**Current Strategy**:
- **Claude 3.5 Haiku**: Fast, cheap ($0.001/query) for simple queries
- **Claude Sonnet 4.5**: Better reasoning, used for production web interface
- **Cost**: ~$20-30/month for 1000 queries (Sonnet) vs $5/month (Haiku)

**Choosing Models**:
- VPS monitoring → Haiku (fast health checks)
- Complex business intelligence → Sonnet (better analysis)
- Production web interface → Sonnet (user-facing, quality matters)

## Agent SDK Patterns

**Standard Agent Structure**:
1. Define tools in `define_tools()` method
2. Implement tool execution in `execute_tool()`
3. Chat loop with tool calling in `chat()` method
4. Maintain conversation history for context

**Tool Calling Flow**:
```
User query → Agent (Claude) → Decides which tool(s) to call → Execute tool(s) → Format response
```

**See**: `shared/base_agent.py` for base class implementation.

## Agent Harness (Autonomous Agent Builder)

**Long-Running Agent Development System** - Build complete agents autonomously via overnight execution using multiple Claude Code sessions.

### What is the Agent Harness?

The Agent Harness is a **meta-development tool** that orchestrates 50-100 Claude Code sessions to build sophisticated agents while you sleep:

```
App Spec (Requirements) → Initializer Agent → Coding Agent #1 → Coding Agent #2 → ... → Complete Agent
                          (Feature List)      (Fresh Context)   (Fresh Context)       (50-100 sessions)
```

**Key Innovation**: Each session gets a **fresh context window** (no context bloat), while maintaining continuity through:
- `feature_list.json` - 50-100 granular test cases
- `claude_progress.md` - Session-to-session summaries
- Git history - All previous commits and patterns
- App spec - Original requirements (single source of truth)

**Location**: `harness/` directory

### Why Use the Harness?

| Manual Development | Harness Development |
|-------------------|-------------------|
| 2-4 days per agent | Overnight (4-24 hrs) |
| Inconsistent patterns | BaseAgent enforced |
| Often incomplete tests | 100% test coverage |
| Docs get outdated | Auto-generated & current |
| Context window struggles | Fresh context per feature |
| Manual regression testing | Built-in validation |
| **Human time**: Hours | **Human time**: Review only |

### Quick Start

**1. Create App Spec** (define what to build):
```bash
nano harness/specs/my_agent_spec.md
```

Use `harness/specs/sharepoint_spec.md` as reference template. Required sections:
- Purpose (what problem does it solve?)
- Capabilities (3-6 major features)
- Tools (detailed parameter specifications)
- Integration Requirements (env vars, dependencies)
- Success Criteria (what "done" means)

**2. Run Harness**:
```bash
# Using slash command (recommended)
/agents/build my_agent

# OR: Direct invocation
./harness/runner.py --agent my_agent --model haiku
```

**3. Let it Run Overnight** (4-24 hours)

**4. Review Output**:
- `agents/my_agent/agent.py` - Complete BaseAgent implementation
- `tests/test_my_agent.py` - Full test coverage
- `demo_my_agent.py` - Interactive demo script
- `agents/my_agent/README.md` - Comprehensive documentation
- `orchestrator/registry.json` - Auto-registered with triggers

### Architecture

```
harness/
├── config.json                  # FibreFlow-specific configuration
├── runner.py                    # Orchestration engine
├── README.md                    # Complete documentation
│
├── prompts/                     # Claude Code session prompts
│   ├── initializer.md          # Session 1: Generate features, setup
│   └── coding_agent.md         # Sessions 2+: Implement one feature
│
├── specs/                       # Agent specifications (PRDs)
│   ├── sharepoint_spec.md      # Example: Moderate complexity agent
│   └── [agent]_spec.md         # Your agent specs
│
└── runs/                        # Execution runs
    ├── latest/                  # Symlink to most recent run
    └── [agent]_[timestamp]/     # Run-specific artifacts
        ├── feature_list.json    # All test cases
        ├── claude_progress.md   # Progress tracking
        ├── init_agent.sh        # Environment setup
        ├── sessions/            # Per-session logs
        └── HARNESS_REPORT.md    # Final summary
```

### How It Works

#### Session 1: Initializer Agent (10-20 min)

**Input**: App spec (`harness/specs/[agent]_spec.md`)

**Process**:
1. Reads app spec to understand requirements
2. Generates 50-100 granular test cases (feature_list.json)
3. Creates agents/[agent]/ directory with BaseAgent skeleton
4. Sets up init_agent.sh for environment validation
5. Makes initial git commit
6. Writes claude_progress.md summary

**Output**: Project foundation ready for coding agents

#### Sessions 2+: Coding Agents (5-30 min each)

Each coding agent (fresh context window):

1. **Prime** - Read claude_progress.md, feature_list.json, git log
2. **Initialize** - Run init_agent.sh to verify environment
3. **Regression Test** - Validate recent features still work
4. **Choose Feature** - Select next incomplete from feature_list.json
5. **Implement** - Write code following BaseAgent patterns
6. **Validate** - Run ALL validation steps from feature
7. **Update** - Mark feature complete in feature_list.json
8. **Commit** - Git commit with descriptive message
9. **Progress** - Update claude_progress.md
10. **End Session** - Harness automatically starts next agent

**Continues until**: All features in feature_list.json have `"passes": true`

### Core Artifacts

#### 1. Feature List (feature_list.json)

Test-driven roadmap with validation:

```json
{
  "agent_name": "sharepoint",
  "total_features": 75,
  "completed": 15,
  "features": [
    {
      "id": 15,
      "category": "3_tools",
      "description": "Implement upload_file_to_sharepoint tool",
      "validation_steps": [
        "Check tool in define_tools()",
        "Test tool execution",
        "Verify OAuth2 authentication",
        "Run integration test"
      ],
      "passes": true,
      "files_involved": ["agents/sharepoint/agent.py"],
      "dependencies": [12, 13]
    }
  ]
}
```

**Categories** (execution order):
1. Scaffolding (directory structure, BaseAgent skeleton)
2. Base Implementation (required methods)
3. Tools (define_tools, execute_tool implementations)
4. Testing (pytest unit + integration tests)
5. Documentation (README, docstrings)
6. Integration (orchestrator registration, demo script)

#### 2. Progress File (claude_progress.md)

Session-to-session communication:

```markdown
# Session 15: Coding Agent

## Previous Session
Session 14 implemented execute_tool() method with error handling

## This Session - Feature #15
Implemented upload_file_to_sharepoint tool
- Added tool definition with parameters
- OAuth2 token acquisition working
- Tested with real SharePoint site
- All validation steps passed ✅

## Current Progress
15/75 features complete (20%)

## Next Steps
Session 16: Implement download_file_from_sharepoint tool
```

#### 3. Configuration (config.json)

```json
{
  "max_features": 100,
  "session_timeout_minutes": 30,
  "model": {
    "initializer": "claude-sonnet-4.5",
    "coding_agent": "claude-3-5-haiku"
  },
  "fibreflow_patterns": {
    "base_agent_class": "shared.base_agent.BaseAgent",
    "orchestrator_registry": "orchestrator/registry.json",
    "required_methods": ["define_tools()", "execute_tool()", "get_system_prompt()"]
  }
}
```

### Cost Estimates

| Complexity | Features | Time | Cost (Haiku) | Cost (Sonnet) |
|-----------|----------|------|--------------|---------------|
| Simple    | 20-40    | 4-8h | $3-5         | $15-25        |
| Moderate  | 40-75    | 8-16h| $10-15       | $40-70        |
| Complex   | 75-100+  | 16-24h| $20-30      | $90-140       |

**Recommendation**: Use **Haiku** for coding agents (fast, cheap iterations) and **Sonnet** for initializer (better planning).

**Alternative**: Use Claude subscription ($20/month unlimited) via `CLAUDE_TOKEN` instead of API key.

### FibreFlow Patterns Enforced

The harness prompts ensure all agents follow standards:

✅ **BaseAgent Inheritance**:
```python
from shared.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self, anthropic_api_key: str, model: str = "claude-3-haiku-20240307"):
        super().__init__(anthropic_api_key, model)
```

✅ **Tool Structure**:
```python
{
    "name": "snake_case_tool_name",
    "description": "Clear description of what tool does",
    "input_schema": {
        "type": "object",
        "properties": {
            "param": {"type": "string", "description": "Parameter purpose"}
        },
        "required": ["param"]
    }
}
```

✅ **Test Markers**:
```python
@pytest.mark.unit
@pytest.mark.agent_name
def test_feature(agent):
    # Test implementation
```

✅ **Orchestrator Registration**: Auto-updates `orchestrator/registry.json` with triggers and capabilities

✅ **Error Handling**: Comprehensive try/except with JSON error returns

✅ **Documentation**: README.md, docstrings, usage examples

### Monitoring Progress

While harness runs:

```bash
# Watch progress
watch -n 60 'cat harness/runs/latest/claude_progress.md | tail -30'

# Check completion percentage
cat harness/runs/latest/feature_list.json | jq '{total: .total_features, done: .completed, pct: (.completed/.total_features*100)}'

# View recent commits
git log --oneline -20

# Check test results
./venv/bin/pytest tests/test_[agent].py -v
```

### Integration with Anthropic's Harness

The `runner.py` is a **demonstration**. For production:

**Option 1: Use Anthropic's Harness** (Recommended)
```bash
# Clone official harness
git clone https://github.com/anthropics/anthropic-harness

# Copy FibreFlow prompts
cp harness/prompts/* anthropic-harness/prompts/

# Run with your spec
cd anthropic-harness
python run_autonomous_agent.py \
  --app-spec ../harness/specs/my_agent_spec.md \
  --project-dir ../agents/my_agent
```

**Option 2: Integrate Claude Agent SDK**
```bash
pip install anthropic-agent-sdk
```

Then update `harness/runner.py` with real SDK calls (see comments in file).

### Example: SharePoint Agent

A complete moderate-complexity example is included:

**Spec**: `harness/specs/sharepoint_spec.md`

**Features**:
- 6 tools (upload, download, list, create, search, metadata)
- OAuth2 authentication with Azure AD
- Error handling for network/auth/permissions
- Chunked uploads for large files
- Full integration test coverage

**Estimates**:
- **Test Cases**: 60-80 features
- **Build Time**: 10-14 hours
- **Cost**: $12-18 with Haiku
- **Result**: Production-ready SharePoint integration agent

### Troubleshooting

**Session Fails or Times Out**:
```bash
# Check session log
cat harness/runs/latest/sessions/session_NNN.log

# Resume from next session
./harness/runner.py --agent my_agent --resume
```

**Tests Keep Failing**:
```bash
# Find failing feature
cat harness/runs/latest/feature_list.json | jq '.features[] | select(.passes == false) | .id' | head -1

# Option 1: Simplify validation steps
nano harness/runs/latest/feature_list.json

# Option 2: Fix manually and resume
nano agents/my_agent/agent.py
# Fix issue, then:
./harness/runner.py --agent my_agent --resume
```

**Harness Loops on Same Feature**:
```bash
# Stop harness (Ctrl+C)

# Mark problematic feature complete manually
nano harness/runs/latest/feature_list.json
# Change "passes": false → "passes": true

# Resume
./harness/runner.py --agent my_agent --resume
```

### When to Use Harness

✅ **USE for**:
- Building new specialized agents (VPS monitoring, API integrations, etc.)
- Complex agents with 6+ tools and extensive logic
- Agents requiring comprehensive test coverage
- Learning agent architecture through generated examples
- Prototyping multiple agent concepts quickly

❌ **DON'T USE for**:
- Simple one-off scripts
- Extending existing agents (manual edit faster)
- Emergency fixes or hotfixes
- Agents with unclear requirements (write spec first)

### Post-Completion Workflow

After harness completes:

1. **Review Generated Code** - Always human-review before production
   ```bash
   cat agents/my_agent/agent.py
   ```

2. **Run Tests**
   ```bash
   ./venv/bin/pytest tests/test_my_agent.py -v
   ```

3. **Try Demo**
   ```bash
   ./venv/bin/python3 demo_my_agent.py
   ```

4. **Test via Orchestrator**
   ```bash
   ./venv/bin/python3 orchestrator/orchestrator.py
   # Query with trigger keywords
   ```

5. **Deploy to Production**
   ```bash
   /deployment/deploy my_agent
   ```

### Documentation

- **Complete Guide**: `harness/README.md` - Architecture, usage, troubleshooting
- **Slash Command**: `.claude/commands/agents/build.md` - Quick reference
- **Example Spec**: `harness/specs/sharepoint_spec.md` - Template for writing specs
- **Initializer Prompt**: `harness/prompts/initializer.md` - How features are generated
- **Coding Prompt**: `harness/prompts/coding_agent.md` - How features are implemented

### Harness vs Agent OS

**Agent Harness** = Autonomous code generation (builds the agent)
**Agent OS** = Development-time guidance (how to build agents)
**Orchestrator** = Runtime routing (which agent to use)

All three work together:
```
Agent OS (Specs) → Agent Harness (Builds) → Orchestrator (Routes) → Production
```

Use Agent Harness when you want FibreFlow to build the agent overnight. Use Agent OS when you're building manually and need structured context.

## Spec-Driven Development (Agent OS)

**Preferred Tool**: [Agent OS](https://github.com/buildermethods/agent-os) - Free, open-source spec-driven development framework for AI coding agents.

### What is Agent OS?

Agent OS is a structured context system that transforms AI coding from reactive guesswork to proactive specification-driven development. It provides a 3-layer context architecture that ensures consistent, standards-compliant code across all agents.

### 3-Layer Context System

**1. Standards Layer**
- Coding standards and conventions
- Agent creation patterns
- Testing requirements
- Documentation templates
- Security and performance guidelines

**2. Product Layer**
- Project vision and roadmap
- Database schema specifications
- API contracts and interfaces
- Deployment architecture
- Business domain knowledge

**3. Specs Layer**
- Feature-specific implementation details
- Agent capability definitions
- Tool and integration specifications
- Use cases and workflows

### Agent OS Workflow Commands

**Phase 1: Planning**
- `/plan-product` - Interactive roadmap definition via Q&A
- `/shape-spec` - Scope MVP requirements through targeted questions
- `/write-spec` - Generate formal spec.md from Q&A session

**Phase 2: Implementation**
- `/create-tasks` - Break spec into prioritized task groups in tasks.md
- `/implement-tasks` - Sequential execution (faster, simpler)
- `/orchestrate-tasks` - Generate orchestration.yml for multi-agent control

**Quick fixes**: For simple bugs/tweaks, skip Agent OS commands and prompt Claude directly.

### Integration with FibreFlow

Agent OS **complements** (not replaces) FibreFlow's existing orchestrator system:

```
Agent OS (Standards/Product/Specs)
        ↓
Claude Code (AI Assistant)
        ↓
Orchestrator (Task Routing)
        ↓
Specialized Agents (Execution)
```

**Key Benefits**:
- **Context Efficiency**: Sub-agents see only relevant code (no context pollution)
- **Standards Enforcement**: Only framework natively using Claude Code skills
- **Team Consistency**: Shared configuration across developers

**When to Use Agent OS**:
- Creating new specialized agents (define specs first)
- Building greenfield projects (full workflow shines here)
- Onboarding team members (standards documentation)
- Adding major features (product/feature specs)
- Establishing coding standards (standards layer)

**When NOT to Use**:
- Quick bug fixes or color changes (overhead > value)
- Simple one-off queries
- Emergency production issues (use direct agent access)

### Configuration

Agent OS v2.1.1 supports Claude Code integration:
- **Claude Code Commands**: Enabled
- **Claude Code Subagents**: Enabled
- **Multi-agent Support**: Compatible with FibreFlow's orchestrator

**Repository**: https://github.com/buildermethods/agent-os
**Documentation**: https://buildermethods.com/agent-os

### Known Limitations (v2.1.1)

**Sub-agent Skills Bug**: Agent OS doesn't auto-inject the `skill` property into generated agent definitions. You must manually add:
```yaml
skills:
  - standards
```
to each agent's markdown file in `.claude/agents/`.

**Maintenance Velocity**: Single-maintainer project with monthly release cycles (slower than daily-shipping tools).

**Bug Fix Overhead**: No dedicated `/fix-bug` command - full workflow is overkill for typos/minor tweaks.

### Agent OS vs. Orchestrator

**Agent OS** = Development-time guidance (how to build agents)
**Orchestrator** = Runtime routing (which agent to use)

Both systems work together - Agent OS ensures agents are built consistently, while the orchestrator ensures they're used correctly.

### Development Philosophy

**Model Intelligence > Methodology Choice**

Agent OS (like BMAD, Spec Kit, etc.) was invented to solve context limits and model stupidity. With Claude Opus 4.5 and 200K+ context windows, these limits are disappearing.

**Focus on platform primitives**:
- How agents work (`.claude/agents/`)
- How MCP works (Model Context Protocol)
- How skills and hooks function
- How tools integrate

Master the fundamental tools, and you can bend any framework to your will. **The final application is the product** - don't let the process become the product.

## Development Principles

### Working with AI Assistants

**Prompt Engineering**:
- **Clear Prompts = Clear Thinking**: If you can't write a clear prompt, you don't know what you want yet
- **Be Specific**: "Fix the database query" → "Optimize the contractor query in neon_agent.py:156 to reduce execution time"
- **Provide Context**: Reference specific files, line numbers, error messages
- **Break Down Complex Tasks**: Use plan mode for multi-step features

**Plan Mode Usage**:
Use plan mode when:
- Requirements are unclear or vague
- Multiple approaches possible
- Need to explore trade-offs
- Complex multi-step implementation

**Code Review Standards**:
AI generates code, but humans own it. Before production:
1. **Security Review**: SQL injection, API key exposure, input validation
2. **Performance Review**: Query optimization, memory usage, async patterns
3. **Error Handling**: Proper exceptions, logging, user-friendly messages
4. **Testing**: Unit tests, integration tests, edge cases covered
5. **Documentation**: Docstrings, README updates, inline comments for complex logic

**Quality Over Speed**:
- Speed without quality = technical debt
- Always review AI code before pushing
- Run tests before deployment
- Monitor production for issues

### Agent Development Guidelines

**When to Create New Agent**:
- Distinct domain expertise (VPS monitoring, database queries, etc.)
- Requires specialized tools
- Independent from other agents
- Reusable across multiple use cases

**When NOT to Create New Agent**:
- One-off task (use sub-agent instead)
- Overlaps with existing agent (extend instead)
- Too generic (role-based agents don't work well - use task-based specialization)

**Agent Testing Requirements**:
- Unit tests for tool execution
- Integration tests with real dependencies
- Error handling tests
- Demo script for manual testing
- Documentation with usage examples

### Deployment Safety

**Pre-Deployment Checklist**:
Use `/deploy` command or deployment-checker sub-agent:
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Security review completed
- [ ] Documentation updated

**Post-Deployment Validation**:
- Monitor logs for errors
- Run smoke tests
- Check health endpoints
- Verify agent responses

### Cost Management

**Model Selection**:
- **Haiku**: Quick queries, health checks, simple data retrieval ($0.001/query)
- **Sonnet**: Complex analysis, business intelligence, production UI ($0.020/query)

**Context Optimization**:
- Use sub-agents to reduce main context pollution
- Clear conversation history when switching tasks
- Use slash commands for repetitive operations (saves tokens)

### Documentation Standards

**Required Documentation**:
- Agent README.md with usage examples
- Update CLAUDE.md for architectural changes
- Document environment variables in .env.example
- Add entries to orchestrator/registry.json

**Documentation Reviews**:
- Update docs with code changes
- Keep examples current
- Document common issues
- Add troubleshooting guides

### Custom Commands

FibreFlow includes custom slash commands in `.claude/commands/`:

**Agent Commands**:
- `/agents/build [agent-name]` - Build complete agent via autonomous harness (overnight)
- `/agents/test [agent-name]` - Run tests for specific agent
- `/agents/new [name] [capabilities]` - Scaffold new agent with templates
- `/agents/document [agent-name]` - Generate/update agent documentation

**Database Commands**:
- `/db-query [natural-language]` - Execute natural language database query
- `/db-sync` - Sync Neon data to Convex backend

**Deployment Commands**:
- `/vps-health` - Check VPS status (CPU, RAM, disk)
- `/deploy [agent-name]` - Deploy agent to production with validation

**Testing Commands**:
- `/test-all` - Run complete test suite with summary
- `/code-review` - Security and performance review of recent changes
- `/eval [content]` - Evaluate external content against sources of truth

### Sub-Agents

Task-based sub-agents in `.claude/agents/`:
- **code-reviewer** - Security, performance, error handling analysis
- **test-generator** - Generate pytest tests following FibreFlow patterns
- **doc-writer** - Generate agent README.md documentation
- **deployment-checker** - Pre-deployment validation checklist
- **ui-tester** - Automated web interface testing (requires Playwright MCP)

Invoke with `@agent-name` or natural language.

## Production Architecture

**Current Deployment**:
```
Nginx (Port 80/443) → FastAPI (Port 8000) → Agent (Claude) → Databases
                                                 ↓
                                        Neon PostgreSQL
                                        Convex Backend
                                        VPS (via SSH)
```

**Web Interface**: `ui-module/chat.html` - Markdown rendering, gradient UI, VF branding

## Common Pitfalls

1. **Always activate venv**: Use `./venv/bin/python3`, not `python3`
2. **Agent routing**: Check `orchestrator/registry.json` triggers if agent not selected
3. **Convex functions**: Deploy with `npx convex deploy` before testing
4. **SSH keys**: VPS Monitor and VF Server skills use SSH keys in `~/.ssh/` (never commit keys to repo)
5. **Context limits**: Superior Agent Brain uses 200K token context window
6. **Neon sync**: Run `sync_neon_to_convex.py` after Neon schema changes

## Documentation Structure

**Quick References**:
- `PROJECT_SUMMARY.md` - Overall project overview
- `QUICK_REFERENCE.md` - One-page developer cheat sheet
- `QUICK_START.md` - Getting started guide

**Agent Guides**:
- `NEON_AGENT_GUIDE.md` - Complete Neon agent documentation
- `CONVEX_AGENT_GUIDE.md` - Convex agent documentation
- `agents/vps-monitor/README.md` - VPS monitoring guide

**Architecture**:
- `DOMAIN_MEMORY_GUIDE.md` - **Domain memory patterns and philosophy** (read this first!)
- `AGENT_WORKFORCE_GUIDE.md` - Multi-agent system guide
- `AI_AGENT_BRAIN_ARCHITECTURE.md` - Memory systems architecture
- `SUPERIOR_BRAIN_QUICKSTART.md` - Superior brain setup
- `harness/README.md` - Agent Harness complete guide

**System Organization**:
- `AGENT_ORGANIGRAM.txt` - Visual agent structure (generated by `orchestrator/organigram.py`)
- `orchestrator/registry.json` - Source of truth for all agents
- `harness/specs/` - Agent specifications for autonomous building

## Special Notes

- **Domain Memory First**: **"The magic is in the memory."** Every long-running agent needs persistent state (feature_list.json, progress.md, git commits). Without domain memory, agents are amnesiacs. See `DOMAIN_MEMORY_GUIDE.md`.
- **Agent Workforce**: This is a **multi-agent** system. Don't create monolithic agents - create specialized agents and register them.
- **Agent Harness**: For complex agents (6+ tools), use the autonomous harness (`/agents/build`) instead of manual development. It builds complete agents overnight with 100% test coverage.
- **Two Memory Systems**: Domain Memory (task state via feature_list.json) vs Superior Agent Brain (cross-session learning via vector DB). Use the right one for the job.
- **Dual Databases**: Neon is source of truth for business data. Convex is for operational/real-time data. Keep them synced.
- **SSH Access**: VPS Monitor and VF Server skills use SSH keys for authentication. Keys stored in `~/.ssh/`, never in repo. VF Server (100.96.203.105) verified working with key auth.
- **Convex Deployment**: Always deploy Convex functions before testing agents that use them.
