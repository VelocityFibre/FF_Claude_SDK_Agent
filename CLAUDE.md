# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**FibreFlow Agent Workforce** - Multi-agent AI system for fiber optic infrastructure operations using Claude Agent SDK. Features specialized AI agents coordinated by an orchestrator, dual database backends (Neon PostgreSQL + Convex), and advanced memory systems.

**Production URLs** (All via Cloudflare DNS):
- **https://app.fibreflow.app** - Main FibreFlow app (Hostinger VPS)
- **https://vf.fibreflow.app/downloads** - APK downloads (VF Server via Tunnel)
- **https://support.fibreflow.app** - Support portal (VF Server via Tunnel)
- **https://docs.fibreflow.app** - Knowledge base documentation (VF Server via Tunnel)
- **http://api.docs.fibreflow.app** - Knowledge base API (VF Server via Tunnel)

**Knowledge Base** (Centralized Documentation):
- **Web UI**: https://docs.fibreflow.app - Searchable documentation with Material theme
- **API**: http://api.docs.fibreflow.app - Programmatic access for scripts/agents
- **Git Repo**: ~/velocity-fibre-knowledge/ - Direct file access (VF Server)
- **Claude Skill**: `.claude/skills/knowledge-base/` - Auto-discovered by Claude Code
- **Contents**: Server docs, database schema (133 tables), SQL queries (50+), deployment procedures
- **Complete Guide**: ~/velocity-fibre-knowledge/KNOWLEDGE_BASE_SYSTEM.md

**Development Tools** (VF Server):
- **http://100.96.203.105:3005/shadcn-enhanced-v2-demo.html** - shadcn/ui Interactive Playground
  - Visual design system configurator for shadcn/ui components
  - Test 28+ interactive components (dialogs, dropdowns, forms, tabs, etc.)
  - Customize themes, fonts, spacing, shadows, animations in real-time
  - Export CSS configuration for production use
  - File: `/srv/data/apps/fibreflow/public/shadcn-enhanced-v2-demo.html`

**Direct Access** (for troubleshooting):
- Hostinger VPS: 72.60.17.245 (srv1092611.hstgr.cloud, Lithuania)
- VF Server: 100.96.203.105:3005 (velo-server via Tailscale)

**Deployment Targets**:
- **Hostinger VPS** (72.60.17.245): Public-facing FibreFlow API/UI
  - PM2 Process: `fibreflow-prod` on port 3005
  - Nginx: SSL/TLS with Let's Encrypt, proxies to port 3005
  - DNS: A record via Cloudflare (Full SSL/TLS mode)
  - SSH: `ssh root@72.60.17.245` (password: VeloF@2025@@)

- **VF Server** (100.96.203.105): Internal operations, BOSS integration, QField sync
  - **FibreFlow Location**: `/srv/data/apps/fibreflow/` (NVMe storage)
  - **Port**: 3005 (Next.js v14.2.18)
  - **Cloudflare Tunnel**: `vf-downloads` (ID: 0bf9e4fa-f650-498c-bd23-def05abe5aaf)
  - **Tunnel Config**: `~/.cloudflared/config.yml`
  - **Tunnel Process**: Running in background, logs at `/tmp/cloudflared.log`
  - SSH: `ssh louis@100.96.203.105` (via Tailscale or LAN)

**DNS & Cloudflare Setup**:
- **Domain**: fibreflow.app (registered with Xneelo)
- **Nameservers**: anton.ns.cloudflare.com, haley.ns.cloudflare.com (migrated 2025-12-19)
- **SSL/TLS Mode**: Full (origin has Let's Encrypt certificates)
- **Tunnel Management**:
  - Config: `~/.cloudflared/config.yml` on VF server
  - Add new apps: Edit config → `~/cloudflared tunnel route dns vf-downloads HOSTNAME` → restart tunnel
  - Restart: `pkill cloudflared && nohup ~/cloudflared tunnel run vf-downloads > /tmp/cloudflared.log 2>&1 &`
- **Troubleshooting**: If `app.fibreflow.app` doesn't work, check Cloudflare SSL/TLS mode is "Full" (not Flexible)

## Server Architecture Philosophy

**Dual-Server Strategy for Load Shedding Resilience** (South African context)

FibreFlow uses a **dual-server architecture** optimized for South African load shedding:

**Hostinger VPS** (Production - 99.9% uptime required):
- **Role**: Customer-facing storefront (always open)
- **Services**: app.fibreflow.app (main app), qfield.fibreflow.app (GIS sync - MISSION-CRITICAL)
- **Uptime SLA**: 99.9% (datacenter with generators, multiple ISPs)
- **Cost**: R40-60/month (both VPS combined)
- **Purpose**: Services that field workers and customers depend on

**VF Server** (Development/Processing - 85-95% uptime acceptable):
- **Role**: Development workshop and processing powerhouse
- **Services**: VLM evaluations, training image storage, dev/testing, internal tools, automation
- **Uptime**: 85-95% (acceptable - affected by load shedding)
- **Cost**: R0/month (you own hardware) + electricity (~R200/month)
- **Value**: R2,700-R6,800/month savings vs cloud GPU/storage equivalents
- **Purpose**: Heavy compute, development, internal tools that can tolerate downtime

**Design Principle**: **"Customer-critical on datacenter, compute-heavy on-premises"**

### Why This Architecture?

**QFieldCloud = Crown Jewel**:
- Field workers synchronize project data (MOA Pole Audit, etc.)
- Without sync, work stops → revenue stops
- **Already protected on Hostinger VPS #2** (72.61.166.168)
- Load shedding has ZERO impact on field operations

**VF Server Value** (even with load shedding):
- Free GPU/CPU for VLM evaluations (vs R2,000-R5,000/month cloud)
- Free 500GB+ storage for training images (vs R500-R1,000/month cloud)
- Free dev/staging environment (vs R200-R500/month cloud VPS)
- Learning platform for Docker, agents, automation
- **Total savings: R2,700-R6,800/month** vs cloud equivalents

**Graceful Degradation**:
- VF Server down → Jobs queue for later processing (not blocked)
- Critical services continue (Hostinger + Neon database)
- Users see: "Evaluation queued - results in 2-4 hours"
- No hard failures, just temporary delays on non-critical features

**Documentation**:
- Complete strategy: `docs/INFRASTRUCTURE_RESILIENCE_STRATEGY.md`
- Implementation guide: `docs/GRACEFUL_DEGRADATION_GUIDE.md`
- Monitoring: VF Server health checks run every 5 minutes from Hostinger

**Decision**: Never move app.fibreflow.app or qfield.fibreflow.app to VF Server. Failover complexity (20-40 hours development) costs more than R20-40/month hosting. Keep production on datacenter, processing on-premises.

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

### Knowledge Base Access
```bash
# Ask Claude Code (natural language)
# "What services run on VF Server?"
# "Show me SQL queries for contractors"
# "How do I deploy FibreFlow?"

# Search documentation via skill
./.claude/skills/knowledge-base/scripts/search.py --query "deployment" --category servers

# Get server documentation
./.claude/skills/knowledge-base/scripts/get_server_docs.py --server vf-server

# Get SQL query library
./.claude/skills/knowledge-base/scripts/get_queries.py

# Get database schema
./.claude/skills/knowledge-base/scripts/get_schema.py

# Read files directly (VF Server)
cat ~/velocity-fibre-knowledge/servers/vf-server.md
cat ~/velocity-fibre-knowledge/databases/common-queries.sql

# Access via API
curl "http://api.docs.fibreflow.app/api/v1/search?q=FibreFlow"
curl "http://api.docs.fibreflow.app/api/v1/servers/vf-server"
curl "http://api.docs.fibreflow.app/api/v1/database/queries"

# Web browser
open https://docs.fibreflow.app
```

### QFieldCloud Local Development
```bash
# Start all services for sync capability
cd /home/louisdup/VF/Apps/QFieldCloud
docker-compose up -d app db memcached worker_wrapper ofelia

# Check sync readiness
.claude/skills/qfieldcloud/scripts/sync_diagnostic.py

# Monitor sync operations
docker logs -f qfieldcloud-worker

# CRITICAL: Worker service MUST be running for sync to work
# Build time: ~15 minutes due to geospatial dependencies (GDAL, GEOS)
```

### QFieldCloud Monitoring Dashboard
```bash
# Start monitoring dashboard (local QFieldCloud)
cd .claude/skills/qfieldcloud/dashboard
./monitor_server.py
# Visit: http://localhost:8888

# OR: Monitor remote QFieldCloud on Hostinger VPS
./monitor_server_hostinger.py
# Visit: http://localhost:8888

# Safe testing without affecting services
xdg-open test_dashboard.html

# Run automated functionality tests
./test_functionality.py

# Features:
# - Real-time service status (Worker, DB, Cache, API, Monitor)
# - Manual restart buttons (only visible when services fail)
# - Auto-refresh every 30 seconds
# - Activity log with color-coded messages
# - Queue metrics and worker health stats

# Systemd Services (auto-start on boot):
# - qfield-worker-monitor.service - Background health checks (60s intervals)
# - Auto-restarts worker after 3 consecutive failures
# - Logs: /var/log/qfield_worker_monitor.log

# Dashboard Documentation:
# - .claude/skills/qfieldcloud/dashboard/RESTART_FUNCTIONALITY.md
```

### Development
```bash
# Activate virtual environment (always required)
source venv/bin/activate

# Run Neon agent demo (interactive)
./venv/bin/python3 tests/demos/demo_neon_agent.py

# Run VPS monitor agent
cd agents/vps-monitor && ../../venv/bin/python3 demo.py

# Sync Neon data to Convex
./venv/bin/python3 sync_neon_to_convex.py

# View agent workforce structure
./venv/bin/python3 orchestrator/organigram.py
cat AGENT_ORGANIGRAM.txt
```

### Claude Code Session Management
```bash
# Resume past sessions (preserves context)
claude --res                     # List all past sessions for this project
                                 # Select session to resume conversation

# Name sessions for better organization (recommended for parallel work)
/rename vf-server-operations     # When working on VF server tasks
/rename hostinger-deployment     # When deploying to Hostinger
/rename qfield-diagnostics       # When fixing QField issues
/rename foto-reviews-vlm         # When working on VLM integration
/rename harness-build-[agent]    # When building agents via harness

# Advanced features
Ctrl+S                           # Stash current prompt (saves it for later)
Double Escape                    # Rewind conversation (undo recent changes)
                                 # Then select checkpoint to restore code + conversation
```

**Session Management Strategy**:
- **Day-to-day work**: Use `claude --res` to resume conversations with context intact
- **Parallel development**: Open multiple sessions, name each with `/rename` for clarity
- **Agent builds**: Use harness system (separate session management in `harness/runs/`)
- **Quick experiments**: Use Double Escape to rewind mistakes without git history pollution

**When to Name Sessions**:
- Working across different servers (VF Server, Hostinger, QFieldCloud)
- Different feature contexts (wa-monitor, foto-reviews, autonomous ticketing)
- Long-running tasks where you'll come back later
- Any time you have 2+ Claude Code windows open simultaneously
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
cd deployment && ./deploy_brain.sh

# Run FastAPI agent server
./venv/bin/python3 ui-module/agent_api.py
```

### Automated Sync to Production Servers

**Quick Sync Commands**:
```bash
# Sync docs to both servers (safe, fast)
./sync-to-hostinger              # Hostinger VPS (app.fibreflow.app)
scp CLAUDE.md louis@100.96.203.105:/srv/data/apps/fibreflow/  # VF Server

# Full deployment to Hostinger (with code)
./sync-to-hostinger --code --restart  # Sync everything + restart PM2

# Check production status
.claude/skills/hostinger-vps/scripts/check_status.py  # Hostinger status
sudo systemctl status fibreflow                       # VF Server status (via SSH)
```

**Hostinger VPS Management** (via `.claude/skills/hostinger-vps/`):
- **sync_all.py**: Sync docs/code with options (--code, --restart)
- **check_status.py**: Check PM2, ports, disk, memory
- **execute.py**: Run any command on Hostinger
- **Location**: `/var/www/fibreflow/`
- **Process**: PM2 `fibreflow-prod`

**VF Server Management** (via `.claude/skills/vf-server/`):
- **execute.py**: Run commands on VF Server
- **Location**: `/srv/data/apps/fibreflow/`
- **Process**: systemd `fibreflow.service`

### Voice Agent (Grok Realtime)
```bash
# Validate voice agent setup
./venv/bin/python3 test_voice_agent_setup.py

# Run Grok voice agent (requires xAI API key + LiveKit)
./venv/bin/python3 voice_agent_grok.py

# Get API keys:
# - xAI: https://x.ai/api
# - LiveKit: https://cloud.livekit.io (free tier available)

# Add to .env:
# XAI_API_KEY=xai-your-key
# LIVEKIT_URL=wss://your-project.livekit.cloud
# LIVEKIT_API_KEY=your-key
# LIVEKIT_API_SECRET=your-secret
```

**See `docs/deployment/VOICE_AGENT_SETUP.md` for complete setup guide.**

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

# Claude Code built-in monitoring (NEW)
/stats                           # View token usage, model distribution, streaks
/context                         # Visualize what's consuming context window
                                 # If degraded performance, check if messages/tools
                                 # are bloating context, then use /clear

# Check skill versions
./venv/bin/python3 .claude/skills/skill_version_manager.py

# View logs
tail -f logs/fibreflow.log
tail -f logs/fibreflow_errors.log

# Generate performance report
./venv/bin/python3 -c "from metrics.collector import get_collector; \
  print(get_collector().generate_report())"

# View work log (git-based activity tracking)
./scripts/work-log               # Terminal view - last 7 days
./scripts/work-log 1             # Today only
./scripts/work-log 30            # Last month

# Work Log Web UI
./scripts/start-work-log-ui      # Start web UI server on port 8001
# Then visit: http://localhost:8001/work-log
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

### Work Log System

**Git-Based Activity Tracking** - Automatic work logging from git commits with zero maintenance.

**Components**:
- `scripts/work-log` - Terminal-based viewer with color coding
- `scripts/work-log-json` - JSON output for API consumption
- `api/work_log_api.py` - FastAPI server for web UI
- `public/work-log.html` - Clean black/white web interface
- `scripts/start-work-log-ui` - One-command startup script

**Usage**:
```bash
# Terminal view (instant, no server needed)
./scripts/work-log         # Last 7 days
./scripts/work-log 1       # Today only
./scripts/work-log 30      # Last month

# Web UI (better for team viewing)
./scripts/start-work-log-ui
# Visit: http://localhost:8001/work-log
```

**Features**:
- **Automatic Module Detection**: Categorizes work by analyzing changed files
- **Zero Maintenance**: Reads git history directly, no manual logging
- **Multiple Views**: TODAY, 3 DAYS, WEEK, MONTH filters
- **Auto-Refresh**: Optional 30-second updates in web UI
- **Color Coding**: Visual distinction between modules
- **Commit Type Highlighting**: feat/fix/docs/perf prefixes

**Module Categories** (auto-detected):
- `NEON-AGENT`, `CONVEX-AGENT`, `VPS-MONITOR` - Agent work
- `VF-SERVER`, `WA-MONITOR` - Server modules
- `QFIELD` - QFieldCloud sync operations
- `DOCS` - Documentation updates
- `TESTS` - Test additions/modifications
- `DEPLOYMENT` - Deploy scripts and configs
- `CORE` - General codebase changes

**Why It Works**: Leverages existing git commit discipline (enforced by hooks) to generate meaningful work summaries without additional overhead.

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
  - Production paths: `/srv/data/apps/`, `/srv/scripts/cron/`
  - FibreFlow deployment: `/srv/data/apps/fibreflow/` (NVMe storage, migrated 2025-12-17)
  - See `.claude/skills/vf-server/README.md` for complete installation structure

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
  - Hostinger VPS (72.60.17.245): Public-facing FibreFlow deployment
  - VF Server (100.96.203.105): Internal operations via Tailscale
    - Production paths: `/srv/data/apps/`, `/srv/scripts/cron/`

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
- `deployment/brain_api.py` - FastAPI wrapper for Superior Agent Brain
- `deployment/deploy_brain.sh` - Deployment script
- `ui-module/agent_api.py` - Production FastAPI server
- `ui-module/chat.html` - Web interface

**Voice Agent**:
- `voice_agent_grok.py` - Grok realtime voice agent (speech-to-speech)
- `docs/deployment/VOICE_AGENT_SETUP.md` - Complete setup guide with API keys
- `test_voice_agent_setup.py` - Validation script for voice agent configuration

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

# VPS Monitor (Hostinger - public FibreFlow)
VPS_HOSTNAME=srv1092611.hstgr.cloud

# Neon Database
NEON_DATABASE_URL=postgresql://...

# Convex Backend
CONVEX_URL=https://quixotic-crow-802.convex.cloud

# VF Server Access (Internal operations - Tailscale)
VF_SERVER_HOST=100.96.203.105  # or velo-server
VF_SERVER_USER=louis
# VF_SERVER_PASSWORD=<password>  # Optional - leave unset for SSH key auth

# WhatsApp Sender Service (for wa-monitor module)
# CRITICAL: Phone +27 71 155 8396 must be paired to WhatsApp service
# See docs/deployment/WA_MONITOR_SETUP.md for pairing instructions

# Voice Agent (Grok Realtime via LiveKit)
XAI_API_KEY=xai-...                        # Get from: https://x.ai/api
LIVEKIT_URL=wss://project.livekit.cloud   # Get from: https://cloud.livekit.io
LIVEKIT_API_KEY=...                        # LiveKit API credentials
LIVEKIT_API_SECRET=...                     # LiveKit API secret
```

**Server Installation Paths** (VF Server: 100.96.203.105):
- FibreFlow production: `/srv/data/apps/fibreflow/` (NVMe storage, migrated 2025-12-18)
- Backup location: `/home/louis/apps/fibreflow.BACKUP_20251218` (old location, kept for reference)
- Cron scripts: `/srv/scripts/cron/`
- See `.claude/skills/vf-server/README.md` for complete structure

See `.env.example` for complete list with documentation.

### WhatsApp Service Dependencies

**CRITICAL FOR wa-monitor MODULE**: The feedback feature at https://app.fibreflow.app/wa-monitor **requires** the WhatsApp Sender service to be running on the VF server with phone +27 71 155 8396 paired.

- **Service**: WhatsApp Sender (Go binary at `~/whatsapp-sender/`)
- **Port**: 8081
- **Phone**: +27 71 155 8396 (must be paired via WhatsApp Linked Devices)
- **Session**: Stored in `~/whatsapp-sender/store/whatsapp.db`
- **Documentation**: See `docs/deployment/WA_MONITOR_MODULE_DOCUMENTATION.md` for complete module guide

### WA Monitor (Foto Reviews) Module - PRODUCTION READY ✅

**Status**: Fully operational with VLM integration (2025-12-19)
**URL**: http://100.96.203.105:3005/foto-reviews
**Last Updated**: 2025-12-19 - Removed Antigravity API, all endpoints now use direct Neon queries

**Components**:
- **VLM Service**: Qwen/Qwen3-VL-8B-Instruct on port 8100 (16K context)
- **Database**: Neon PostgreSQL `foto_ai_reviews` table (27+ evaluations)
- **API Endpoints** (All use direct Neon database queries):
  - `GET /api/foto-reviews/pending` - List pending reviews
  - `GET /api/foto-reviews/{dr_number}` - Get review details
  - `GET /api/foto-reviews/{dr_number}/history` - Get review history (stub)
  - `POST /api/foto/evaluate` - Trigger VLM evaluation
  - `POST /api/foto/feedback` - Send WhatsApp feedback
- **WhatsApp**: Service on port 8081 with phone paired

**Quick Test**:
```bash
# Check system status
.claude/skills/wa-monitor/scripts/check_status.py

# Trigger evaluation
.claude/skills/wa-monitor/scripts/trigger_evaluation.py DR1234567

# View pending reviews
curl "http://100.96.203.105:3005/api/foto-reviews/pending?limit=5"

# Get specific review
curl "http://100.96.203.105:3005/api/foto-reviews/DR1733758"
```

**Note**: Antigravity API has been completely removed. All endpoints now query Neon database directly.

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

**Role in FibreFlow**: Agent OS is for **PLANNING** (defining what to build), while FibreFlow Harness is for **EXECUTION** (building it autonomously).

```
Agent OS (Planning)     →  FibreFlow Harness (Building)  →  Production
/plan-product              ./harness/runner.py               Deployed Agent
/shape-spec                --parallel 6 (4-6x faster)
/write-spec → spec.md      Auto-Claude Phases 1+2+3
```

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

**Note**: Agent OS `/implement-tasks` is for manual development. For autonomous overnight builds, use FibreFlow Harness instead (see decision tree below).

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

### When to Use What: Decision Tree

**Starting a new development task?** Follow this decision tree:

```
Need to build something?
    ↓
┌──────────────────────────────────────────────┐
│ 1. Is the requirement well-defined?         │
└──────────────────────────────────────────────┘
    ↓
    ├─ NO → Use Agent OS for Planning
    │        ├─ /plan-product (define vision)
    │        ├─ /shape-spec (scope MVP via Q&A)
    │        └─ /write-spec (generate harness/specs/agent_spec.md)
    │        ↓
    │        Spec created → Continue below ↓
    │
    └─ YES → Have a formal spec?
               ↓
               ├─ NO → Write spec first
               │        (Use Agent OS or write manually)
               │        ↓
               │        Spec created → Continue below ↓
               │
               └─ YES → How many features?
                          ↓
                          ├─ 10+ features → Use FibreFlow Harness
                          │                 ./harness/runner.py --agent name --parallel 6
                          │                 (Auto-Claude Phases 1+2+3: Safe + Quality + Speed)
                          │                 Expected: Overnight autonomous build
                          │
                          ├─ 3-9 features → Consider FibreFlow Harness
                          │                 OR implement directly (faster for small scope)
                          │
                          └─ 1-2 features → Implement directly
                                            (Harness overhead not worth it)
```

**Quick Reference Table**:

| Scenario | Tool | Reason |
|----------|------|--------|
| **"I want a SharePoint agent"** (vague) | Agent OS | Need structured planning |
| **Have spec, 50 features** | FibreFlow Harness | Autonomous build overnight |
| **Have spec, 2 features** | Direct development | Faster than harness setup |
| **Bug fix** | Direct development | 30 seconds vs 30 minutes |
| **Emergency hotfix** | Direct development | Speed > process |
| **New major feature** | Agent OS → Harness | Plan first, build second |

**When to Use Agent OS** (Planning Phase):
- ✅ Creating new specialized agents (define specs first)
- ✅ Building greenfield projects (full workflow shines here)
- ✅ Onboarding team members (standards documentation)
- ✅ Adding major features (product/feature specs)
- ✅ Requirement is vague or unclear
- ✅ Need to scope MVP interactively

**When to Use FibreFlow Harness** (Execution Phase):
- ✅ Have a well-defined spec (harness/specs/agent_spec.md)
- ✅ Building complete agent (10+ features)
- ✅ Want overnight autonomous build
- ✅ Want 4-6x speedup (Phase 3 parallel execution)
- ✅ Want safety (Phase 1 worktrees) + quality (Phase 2 self-healing)

**When to Use Direct Development** (No Tools):
- ✅ Quick bug fixes or typos
- ✅ Color/style changes
- ✅ Emergency production issues
- ✅ 1-2 simple features
- ✅ Exploring/prototyping (spec would slow discovery)

### Complete Workflow Example

**Scenario**: Building a new Microsoft Teams agent for deployment notifications

**Step 1: Planning (Agent OS) - 30 minutes**

```bash
# Initial request (too vague for harness)
# "I need something that posts to Teams"

# Use Agent OS to define requirements
/plan-product
# Interactive Q&A clarifies:
# - Posts deployment notifications to specific channels
# - Supports channel selection
# - Handles auth with OAuth2

/shape-spec
# Interactive Q&A scopes MVP:
# - 3 core tools: post_message, list_channels, authenticate
# - OAuth2 flow with token refresh
# - Rate limit handling
# - Success: Message posted with confirmation

/write-spec
# Output: specs/teams_spec.md (formal specification)
```

**Step 2: Copy Spec to FibreFlow**

```bash
# If using standalone Agent OS
cp ~/agent-os/specs/teams_spec.md harness/specs/teams_spec.md

# If using Agent OS within FibreFlow (recommended)
# Spec already in harness/specs/
```

**Step 3: Execution (FibreFlow Harness) - Overnight**

```bash
# Start autonomous build with Auto-Claude phases
./harness/runner.py --agent teams --parallel 6

# What happens overnight:
# - Phase 1 (Worktrees): All work in isolated .worktrees/
# - Phase 2 (Self-Healing): Auto-fixes syntax/import/logic errors
# - Phase 3 (Parallel): 6 features developed simultaneously
# - Result: 90% completion rate, 4-6x faster than sequential

# Wake up to:
# ✅ agents/teams/agent.py (complete implementation)
# ✅ tests/test_teams.py (full test coverage)
# ✅ demo_teams.py (working demonstration)
# ✅ agents/teams/README.md (documentation)
# ✅ orchestrator/registry.json (auto-registered)
```

**Step 4: Test and Deploy**

```bash
# Test the agent
./venv/bin/pytest tests/test_teams.py -v
./venv/bin/python3 demo_teams.py

# Register environment variables
echo "TEAMS_TENANT_ID=..." >> .env
echo "TEAMS_CLIENT_ID=..." >> .env

# Deploy to production
/deployment/deploy teams

# Or use orchestrator
./venv/bin/python3 orchestrator/orchestrator.py
# Query: "Post deployment notification to Teams"
```

**Time Investment vs Value**:
- Agent OS planning: 30 minutes
- FibreFlow build: Overnight (unattended)
- Testing/deployment: 30 minutes
- **Total hands-on time: 1 hour**
- **Result: Production-ready agent with tests and docs**

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

### Agent OS vs. Harness vs. Orchestrator

Three distinct systems work together in the FibreFlow lifecycle:

**Agent OS** = **Planning** (What to build)
- Interactive Q&A to define requirements
- Generates formal specifications
- Used BEFORE building
- Output: harness/specs/agent_spec.md

**FibreFlow Harness** = **Building** (How to build it)
- Autonomous overnight execution
- Auto-Claude Phases 1+2+3 (Safe + Quality + Speed)
- Used AFTER planning
- Input: specs/agent_spec.md → Output: Complete agent

**Orchestrator** = **Routing** (Which agent to use)
- Runtime task routing to specialized agents
- Keyword-based agent selection
- Used IN PRODUCTION
- Input: User query → Output: Routed to correct agent

**Complete Lifecycle**:
```
Agent OS        →  FibreFlow Harness    →  Orchestrator       →  Production
(Planning)         (Building)              (Routing)             (Usage)
────────────────────────────────────────────────────────────────────────────
/plan-product      ./harness/runner.py     orchestrator.py       User queries
/shape-spec        --parallel 6            registry.json         Auto-routing
/write-spec        Phases 1+2+3            Keyword matching      Agent execution

Output:            Output:                 Output:               Output:
spec.md            Complete agent          Selected agent        Results
```

All three work together - Agent OS plans, Harness builds, Orchestrator routes.

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
- **Ultrathink for Complex Tasks**: Add "Ultrathink about this" to prompts requiring deep reasoning

**Advanced Prompting Techniques**:

*Ultrathink* - Force Claude to think harder on complex problems:
```
When to use Ultrathink:
✅ Complex agent builds via harness (initializer phase)
✅ Architectural decisions (DECISION_LOG.md entries)
✅ Difficult VLM prompt engineering (foto-reviews)
✅ Critical production deployment decisions
✅ Complex bug diagnosis with multiple potential causes

❌ Simple database queries (skills already optimized)
❌ Routine VPS health checks
❌ Documentation updates

Examples:
"Ultrathink about the optimal tool structure for the SharePoint agent spec"
"The QFieldCloud worker keeps failing. Ultrathink about root causes and solutions."
"Ultrathink about the best approach for autonomous GitHub ticketing remediation"
```

*Custom Memories* - Project-specific context Claude remembers:
```
# Create custom memory (one-time, lasts entire project)
# add to memory
Always use skills-based approach over agent-based for database operations (99% faster)

# Recommended FibreFlow memories:
# add to memory
VF Server is at 100.96.203.105, production path is /srv/data/apps/fibreflow/, use SSH key auth

# add to memory
Never commit .env files, use .env.example template instead

# add to memory
Always activate venv with ./venv/bin/python3, never use system python3

# add to memory
Always update CHANGELOG.md with feature changes using ./scripts/add-changelog-entry.sh

# add to memory
For VF Server operations, use .claude/skills/vf-server/scripts/execute.py wrapper

When to use custom memories vs CLAUDE.md:
- Memories: Temporary project context, preferences, current workflow focus
- CLAUDE.md: Permanent architecture, infrastructure, standards
```

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

### Autonomous GitHub Ticketing System

**Status**: ✅ **PRODUCTION - AUTO-TRIGGER ENABLED** (2025-12-23)
**Repository**: https://github.com/VelocityFibre/ticketing
**Execution**: GitHub Actions (cloud) → QFieldCloud VPS (72.61.166.168)
**Test Results**: 100% success rate (issues #6, #8)

A **fully autonomous** support system that resolves QFieldCloud issues end-to-end in 25-30 seconds with **zero human intervention**.

**Architecture** (Hybrid Cloud + On-Premise):
```
GitHub Cloud (Free Tier)          QFieldCloud VPS (72.61.166.168)
┌─────────────────────┐          ┌──────────────────────────┐
│ Issue Created       │          │                          │
│        ↓            │   SSH    │  13 Docker Services:     │
│ Actions Runner      │ ───────→ │  - app, db, nginx        │
│ (Ubuntu VM)         │          │  - worker_wrapper        │
│   - Install deps    │          │  - memcached, minio      │
│   - Setup SSH key   │          │  - certbot, ofelia       │
│   - Run diagnostics │ ←─────── │  - Returns status        │
│        ↓            │  Results │                          │
│ Post Report         │          │  Auto-fixes:             │
│        ↓            │   API    │  - Worker restart        │
│ Close Issue         │ ───────→ │  - Queue cleanup         │
└─────────────────────┘          │  - DB restart            │
                                 └──────────────────────────┘
```

**Trigger Methods** (3 ways):
1. **Automatic** ✅ - Runs when issues are `opened` or `reopened` in VelocityFibre/ticketing
2. **Manual** - Via "Run workflow" button: https://github.com/VelocityFibre/ticketing/actions
3. **API** - Via `/qfield:support <issue-number>` slash command (local execution)

**Execution Flow**:
```bash
User creates issue → GitHub Actions auto-triggers in <3 seconds
                  ↓
         GitHub Runner (cloud VM):
         1. Install Python deps (anthropic, psycopg2, python-dotenv)
         2. Decode base64 SSH key → ~/.ssh/qfield_vps
         3. SSH to 72.61.166.168
                  ↓
         QFieldCloud VPS diagnostics:
         4. Check 13 Docker containers (docker compose ps)
         5. Query job queue (PostgreSQL)
         6. Check disk usage (df -h)
                  ↓
         AI Analysis + Auto-Fix:
         7. Detect issues (worker down, queue stuck, etc.)
         8. Execute fixes (restart services, clean queue)
         9. Verify resolution (re-run diagnostics)
                  ↓
         GitHub Report:
         10. Post comprehensive comment with emojis
         11. Auto-close issue (if resolved)
         12. Upload diagnostics artifact (if failed)

Total time: 25-30 seconds | Cost: $0 (free tier)
```

**Capabilities**:
- **Auto-fixes** ~80% of issues: worker down, database issues, stuck queues, disk space, memory limits
- **Auto-escalates** ~20%: SSL certs, code bugs, permissions (with clear explanations)
- **Resolution time**: 5-25 seconds vs hours/days manually
- **Zero human intervention** for routine issues
- **24/7 availability** (GitHub Actions always-on)

**Key Files**:
- **Workflow**: `.github/workflows/autonomous-support.yml` (in VelocityFibre/ticketing repo)
- **Resolution Script**: `.github/workflows/scripts/auto_resolve.py` (Python, 300+ lines)
- **Remediation Engine**: `.claude/skills/qfieldcloud/scripts/remediate.py` (local, for manual use)
- **Diagnostic Scripts**: `status.py`, `prevention.py`, `logs.py` (local health monitoring)

**GitHub Secrets Required**:
- `ANTHROPIC_API_KEY` - For AI analysis (Claude)
- `QFIELD_VPS_SSH_KEY` - Base64-encoded SSH private key for VPS access

**Authentication**:
- **SSH Key**: Ed25519 key at `~/.ssh/qfield_vps` (local) or base64-decoded in workflow
- **Host**: 72.61.166.168 (QFieldCloud VPS on Hostinger #2)
- **User**: root
- **Fallback**: StrictHostKeyChecking=no (if ssh-keyscan times out)

**Diagnostic Report Example**: https://github.com/VelocityFibre/ticketing/issues/8

**Documentation**:
- Complete guide: `docs/guides/AUTONOMOUS_GITHUB_TICKETING.md`
- Testing guide: `docs/guides/AUTONOMOUS_TICKETING_TESTING.md`
- Session summary: `docs/SESSION_SUMMARY_AUTONOMOUS_TICKETING.md`
- Workflow setup: `.github/workflows/SETUP.md` (in ticketing repo)

**Where It Runs**:
- ☁️ **Execution**: GitHub's cloud infrastructure (free Ubuntu runners)
- 🖥️ **Target**: Your QFieldCloud VPS (72.61.166.168)
- 💰 **Cost**: $0/month (GitHub Actions free tier: 2,000 minutes/month)
- ⚡ **Speed**: ~30 seconds including dependency installation

**Test It**:
```bash
# Create test issue (auto-triggers workflow):
gh issue create --repo VelocityFibre/ticketing \
  --title "QField status check" \
  --body "Please verify all services are running"

# Watch execution:
# https://github.com/VelocityFibre/ticketing/actions

# View result:
gh issue view <number> --repo VelocityFibre/ticketing
```

**Success Metrics**:
- Issue #6: Health check → 18 seconds → Closed ✅
- Issue #8: Sync check → 5 seconds → Closed ✅
- First auto-trigger: Failed (SSH timeout) → Fixed → Success ✅

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

**WA Monitor Module** (https://app.fibreflow.app/wa-monitor):
```
Frontend → Next.js API (/api/wa-monitor-send-feedback) → WhatsApp Sender (Port 8081)
                                                                ↓
                                                   WhatsApp Web API (whatsmeow)
                                                                ↓
                                                   Phone +27 71 155 8396 (MUST BE PAIRED)
                                                                ↓
                                                   WhatsApp Groups (by project)
```

**CRITICAL**: The WhatsApp Sender service requires phone +27 71 155 8396 to be paired via WhatsApp "Linked Devices" feature. See `docs/deployment/WA_MONITOR_SETUP.md` for pairing instructions.

## Common Pitfalls

1. **Always activate venv**: Use `./venv/bin/python3`, not `python3`
2. **Agent routing**: Check `orchestrator/registry.json` triggers if agent not selected
3. **Convex functions**: Deploy with `npx convex deploy` before testing
4. **SSH keys**: VPS Monitor and VF Server skills use SSH keys in `~/.ssh/` (never commit keys to repo)
5. **Context limits**: Superior Agent Brain uses 200K token context window
6. **Neon sync**: Run `sync_neon_to_convex.py` after Neon schema changes
7. **WhatsApp feedback failing**: Check that WhatsApp Sender service is running and phone +27 71 155 8396 is paired. Error "the store doesn't contain a device JID" means phone is not paired. See `docs/deployment/WA_MONITOR_SETUP.md`

## Documentation Structure

**Operational Documentation** (Infrastructure & Decisions):
- `CHANGELOG.md` - Feature releases, version history, what changed
- `docs/OPERATIONS_LOG.md` - Server changes, deployments, migrations, incidents
- `docs/DECISION_LOG.md` - Architectural decisions (ADRs), why we chose this approach
- `docs/DOCUMENTATION_FRAMEWORK.md` - How to decide what/where to document
- `docs/DOCUMENTATION_AUTOMATION.md` - **How automation ensures docs are maintained**
- `docs/DOCUMENTATION_README.md` - **Quick start guide for documentation system**

**Quick References**:
- `PROJECT_SUMMARY.md` - Overall project overview
- `QUICK_REFERENCE.md` - One-page developer cheat sheet
- `QUICK_START.md` - Getting started guide

**Agent Guides**:
- `NEON_AGENT_GUIDE.md` - Complete Neon agent documentation
- `CONVEX_AGENT_GUIDE.md` - Convex agent documentation
- `agents/vps-monitor/README.md` - VPS monitoring guide
- `docs/deployment/VOICE_AGENT_SETUP.md` - **Voice agent with Grok realtime API setup guide**
- `docs/deployment/WA_MONITOR_SETUP.md` - **WhatsApp Sender service setup and phone pairing guide (CRITICAL for wa-monitor)**
- `docs/deployment/WA_DR_QUICKSTART.md` - WA DR monitoring system quickstart
- `docs/deployment/WA_FEEDBACK_FIX_DEPLOYMENT.md` - WhatsApp feedback fix deployment

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

## Documentation Automation System

**Status**: ✅ Active (4-layer automation enforces documentation)

FibreFlow uses a **self-enforcing documentation system** that ensures docs are actually maintained through automation, not discipline.

### Quick Start

```bash
# One-time setup (install git hooks)
./scripts/install-git-hooks.sh

# Daily use - add CHANGELOG entry (30 seconds)
./scripts/add-changelog-entry.sh

# Daily use - document deployment (2 minutes)
./scripts/add-operations-entry.sh
```

### The Four Layers

**Layer 1: Git Hooks** (Local enforcement)
- `.git/hooks/commit-msg` - Validates conventional commit format (blocks bad commits)
- `.git/hooks/pre-push` - Warns if documentation not updated before push
- Install: `./scripts/install-git-hooks.sh`

**Layer 2: Helper Scripts** (Make it easy)
- `scripts/add-changelog-entry.sh` - Interactive CHANGELOG entry (30 sec)
- `scripts/add-operations-entry.sh` - Pre-filled OPS_LOG template (2 min)

**Layer 3: CI/CD** (Remote validation)
- `.github/workflows/documentation-check.yml` - GitHub Actions validates docs
- Comments on PRs with warnings if docs missing
- Checks conventional commit format

**Layer 4: Culture** (Embedded process)
- Definition of Done checklists
- PR templates with docs section
- Quarterly reviews and metrics

### Documentation Decision Tree

```
Is this important to remember?
│
├─ NO → Git commit is enough
│
└─ YES → What type?
          ├─ Feature/fix? → CHANGELOG.md (./scripts/add-changelog-entry.sh)
          ├─ Deployment? → docs/OPERATIONS_LOG.md (./scripts/add-operations-entry.sh)
          └─ Architecture? → docs/DECISION_LOG.md (copy template, edit)
```

### Why It Works

- **Automation > Discipline**: Hooks catch mistakes before they enter git history
- **Easy > Forced**: Helper scripts make docs faster than skipping (30 sec)
- **Visible > Silent**: CI comments on PRs create peer accountability
- **Self-sustaining**: System enforces itself, no human oversight needed

### Success Metrics

**Targets** (measure quarterly):
- ✅ 100% conventional commit compliance (enforced by hooks)
- ✅ 90%+ features documented in CHANGELOG (warned by hooks/CI)
- ✅ 100% deployments documented in OPERATIONS_LOG (required)
- ✅ <1 minute to add docs (helper scripts)

### Documentation

**Start here**: `docs/DOCUMENTATION_README.md` (5 min read)
**Deep dive**: `docs/DOCUMENTATION_AUTOMATION.md` (complete guide)
**Decision guide**: `docs/DOCUMENTATION_FRAMEWORK.md` (when/what to document)

## Special Notes

- **Domain Memory First**: **"The magic is in the memory."** Every long-running agent needs persistent state (feature_list.json, progress.md, git commits). Without domain memory, agents are amnesiacs. See `DOMAIN_MEMORY_GUIDE.md`.
- **Agent Workforce**: This is a **multi-agent** system. Don't create monolithic agents - create specialized agents and register them.
- **Agent Harness**: For complex agents (6+ tools), use the autonomous harness (`/agents/build`) instead of manual development. It builds complete agents overnight with 100% test coverage.
- **Two Memory Systems**: Domain Memory (task state via feature_list.json) vs Superior Agent Brain (cross-session learning via vector DB). Use the right one for the job.
- **Dual Databases**: Neon is source of truth for business data. Convex is for operational/real-time data. Keep them synced.
- **SSH Access**: VPS Monitor and VF Server skills use SSH keys for authentication. Keys stored in `~/.ssh/`, never in repo. VF Server (100.96.203.105) verified working with key auth.
- **VF Server Paths**: Production apps deployed to `/srv/data/apps/` (NVMe storage). FibreFlow at `/srv/data/apps/fibreflow/` (migrated 2025-12-17). See `docs/OPERATIONS_LOG.md` for procedures.
- **Convex Deployment**: Always deploy Convex functions before testing agents that use them.
- **Documentation**: Important changes documented in CHANGELOG.md (what), docs/OPERATIONS_LOG.md (how), and docs/DECISION_LOG.md (why). See `docs/DOCUMENTATION_FRAMEWORK.md` for guidelines.
- **WhatsApp Service**: **CRITICAL** - The wa-monitor feedback feature (https://app.fibreflow.app/wa-monitor) requires WhatsApp Sender service running on VF server with phone +27 71 155 8396 paired. Service runs on port 8081. Session stored in `~/whatsapp-sender/store/whatsapp.db` - **NEVER DELETE**. See `docs/deployment/WA_MONITOR_SETUP.md` for complete setup and troubleshooting.
