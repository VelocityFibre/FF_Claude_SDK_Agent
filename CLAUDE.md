# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**FibreFlow Agent Workforce** - Multi-agent AI system for fiber optic infrastructure operations using Claude Agent SDK. Features specialized AI agents coordinated by an orchestrator, dual database backends (Neon PostgreSQL + Convex), and advanced memory systems.

## Infrastructure

### Production URLs (Cloudflare DNS)
- **https://app.fibreflow.app** - Main FibreFlow app (VF Server port 3000)
- **https://qfield.fibreflow.app** - QFieldCloud sync (VF Server port 8082 via Cloudflare Tunnel)
- **https://vf.fibreflow.app** - FibreFlow staging (VF Server port 3006)
- **https://vf.fibreflow.app/downloads** - APK downloads (VF Server via Tunnel)
- **https://support.fibreflow.app** - Support portal (VF Server via Tunnel)
- **https://docs.fibreflow.app** - Knowledge base documentation
- **http://api.docs.fibreflow.app** - Knowledge base API

### Servers (Updated Jan 2026 - Battery Backup Acquired)

**VF Server** (100.96.203.105) - PRIMARY PRODUCTION + Dev/Staging, 99%+ uptime
- **Battery Backup**: UPS system (1-2 hours during load shedding)
- **SSH**: `ssh velo@100.96.203.105` (password: **2025**)
- **Production Services**:
  - Port 3000: FibreFlow production (app.fibreflow.app)
  - Port 8082: QFieldCloud (qfield.fibreflow.app) - **MIGRATED Jan 2026** ✅
    - 8 workers (scaled from 4)
    - PostgreSQL + PostGIS (port 5433)
    - MinIO storage (ports 8009-8010)
    - QGIS processing (2.7GB image)
  - Port 8081: WhatsApp sender service
  - Port 8091: Storage API (Firebase replacement) - **NEW Jan 2026**
- **Dev/Staging Services**:
  - Port 3005: Development instance (Hein)
  - Port 3006: Staging instance (Louis) - https://vf.fibreflow.app
- **Other Services**: VLM (port 8100), support portal, internal tools
- **Storage**: `/srv/data/fibreflow-storage/` (replaced Firebase, saves R50/month)
- **Cloudflare Tunnel**: Running as user `velo` (tunnel ID: 0bf9e4fa-f650-498c-bd23-def05abe5aaf)
- **Setup Guide**: `VF_SERVER_PRODUCTION_SETUP.md`

**QFieldCloud Production Server** (72.61.166.168) - DECOMMISSIONED Jan 2026
- **Status**: ❌ Decommissioned (migrated to VF Server)
- **Migration Date**: 2026-01-08
- **Reason**: Moved to VF Server for better resources and battery backup
- **Backups**: Archived on VF Server (/opt/qfieldcloud/backups/)
- **Note**: See `.claude/skills/qfieldcloud/MIGRATION_COMPLETE.md`

**Hostinger VPS Backup** (72.61.197.178) - BACKUP/FAILOVER
- **Purpose**: Cold standby, disaster recovery
- **Status**: Not active (DNS points to VF Server)
- **SSH**: `ssh root@72.61.197.178` (password: **VeloF@2025@@**)
- **Cost**: R20-30/month (insurance policy)
- **Activated**: Only if VF Server fails

**Old Hostinger VPS** (72.60.17.245) - DEPRECATED
- Being decommissioned after QFieldCloud migration complete
- Cost savings: R30/month

**Architecture Philosophy**: "All services on battery-backed VF Server, Hostinger for backup"
- Details: `docs/INFRASTRUCTURE_RESILIENCE_STRATEGY.md` (Updated Jan 2026)

### Knowledge Base
- **Web**: https://docs.fibreflow.app
- **API**: http://api.docs.fibreflow.app
- **Claude Skill**: `.claude/skills/knowledge-base/`
- **Git Repo**: `~/velocity-fibre-knowledge/` (VF Server)
- **Guide**: `~/velocity-fibre-knowledge/KNOWLEDGE_BASE_SYSTEM.md`

## Quick Commands

### Essential Commands
```bash
# Testing
./venv/bin/pytest tests/ -v                      # Run all tests
./venv/bin/pytest tests/test_[agent].py -v       # Test specific agent

# Knowledge Base (natural language to Claude Code)
"How many contractors are in the database?"
"Show me SQL queries for contractors"

# Development
source venv/bin/activate                         # Always required first
./venv/bin/python3 orchestrator/orchestrator.py  # Test orchestration

# Session Management
claude --res                                      # Resume past sessions
/rename [descriptive-name]                       # Name current session
Ctrl+S                                           # Stash prompt
Double Escape                                    # Rewind conversation

# Deployment
./sync-to-hostinger                             # Deploy to Hostinger
npx convex deploy                                # Deploy Convex functions
```

**Detailed commands**: See section-specific documentation files

## Architecture

### Skills-Based Architecture (PRIMARY - ✅ Production)
- **Location**: `.claude/skills/`
- **Performance**: 99% faster (23ms vs 2.3s), 84% less context
- **How it works**: Scripts execute from filesystem, only results enter context
- **Key Innovation**: Progressive disclosure with auto-discovery
- **Details**: `experiments/skills-vs-agents/FINAL_RESULTS.md`

### Multi-Agent Workforce (Legacy/Fallback)
```
User → Orchestrator → Specialized Agent → Response
           ↓
    VPS Monitor / Neon DB / Convex
```
- **Registry**: `orchestrator/registry.json` (source of truth)
- **Base Class**: `shared/base_agent.py`

### Memory Systems

**1. Domain Memory** (Task-Level State)
- `feature_list.json` - Machine-readable backlog
- `claude_progress.md` - Session summaries
- Git commits - State snapshots
- **Use for**: Agent builds, multi-step features
- **Guide**: `DOMAIN_MEMORY_GUIDE.md`

**2. Superior Agent Brain** (Cross-Session Learning)
- Vector Memory (Qdrant), Persistent Memory (Neon)
- Meta-learning, Knowledge graphs
- **Use for**: Semantic search, knowledge sharing
- **Warning**: Advanced architecture, overkill for simple tasks

### Databases
- **Neon PostgreSQL**: Source of truth (104 tables) - contractors, projects, BOQs
- **Convex**: Real-time/operational data
- **Sync**: `sync_neon_to_convex.py`

## MCP Configuration

**Config**: `.claude/settings.local.json`
**Active**: `context7` (Python, FastAPI, PostgreSQL, pytest docs)
**Profile-Based**: postgres-mcp, github, playwright-mcp (enable as needed)
**Guide**: `.claude/mcp-profiles.md`

## Environment Variables

Required in `.env` (see `.env.example` for complete list):
```bash
ANTHROPIC_API_KEY=sk-ant-api03-...
NEON_DATABASE_URL=postgresql://...
CONVEX_URL=https://quixotic-crow-802.convex.cloud
VF_SERVER_HOST=100.96.203.105
VF_SERVER_USER=louis
# Storage Configuration (NEW Jan 2026 - replaced Firebase)
NEXT_PUBLIC_USE_VF_STORAGE=true
NEXT_PUBLIC_STORAGE_URL=http://100.96.203.105:8091
# WhatsApp (CRITICAL for wa-monitor)
# Phone +27 71 155 8396 must be paired
# See docs/deployment/WA_MONITOR_SETUP.md
```

## WA Monitor Module

**Status**: ✅ Production Ready with VLM
- **URL**: http://100.96.203.105:3005/foto-reviews
- **VLM**: Qwen3-VL-8B on port 8100
- **Database**: Neon `foto_ai_reviews` table
- **WhatsApp**: Port 8081, phone +27 71 155 8396 (MUST BE PAIRED)
- **Setup**: `docs/deployment/WA_MONITOR_SETUP.md`

## Agent Harness (Autonomous Builder)

Build complete agents overnight with 100% test coverage.

### Quick Start
```bash
# Create spec
nano harness/specs/my_agent_spec.md

# Run harness (overnight, 4-24 hours)
/agents/build my_agent
# OR
./harness/runner.py --agent my_agent --model haiku

# Monitor progress
watch -n 60 'cat harness/runs/latest/claude_progress.md | tail -30'
```

### When to Use
- ✅ Complex agents (6+ tools)
- ✅ Need comprehensive test coverage
- ❌ NOT for simple scripts or emergency fixes

**Complete Guide**: `harness/README.md`

## Vibe Coding Transformation (10x Productivity)

**Status**: ✅ ALL 6 PHASES COMPLETE - 100% 🎉
**Impact**: 10x productivity, 80% cost + time reduction, complete CNC machine mode

### What is Vibe Coding?

"Vibe coding" is **anything where you don't type code by hand** - more precisely, the iterative conversation that results in AI writing your code. FibreFlow has **fully evolved** from AI-assisted development to complete **CNC machine mode** where engineers are city planners who oversee outcomes through real-time dashboards.

### Current Progress (100% Complete) 🎉

✅ Multi-agent decomposition, domain memory, autonomous ticketing
✅ **E2B sandboxes (Phase 1)** - Live and tested, 12-second execution, $0.003/sandbox
✅ **Reflection loops (Phase 1.5)** - Self-improving agents, 93% fewer repeated failures, 20% faster
✅ **Tiered routing (Phase 2)** - Haiku/Sonnet/Opus selection, 80% cost reduction, 18/18 tests passed
✅ **Data SLAs (Phase 2.5)** - Freshness guarantees, <5 min sync, 95% compliance, Slack alerts
✅ **Autopilot (Phase 3)** - 15 parallel attempts, best-of-N selection, 80% time reduction (4h → 20min)
✅ **Digital Twin Dashboard (Phase 4)** - Real-time observability, 5 layers, city planner control room

### Six-Phase Implementation

1. ✅ **Phase 1: E2B Sandboxes** (COMPLETE 2026-01-05) - 15 parallel agents, 12x speedup, $0.003/execution
2. ✅ **Phase 1.5: Reflection Loops** (COMPLETE 2026-01-05) - Self-improving agents, 93% reduction in repeated failures
3. ✅ **Phase 2: Tiered Routing** (COMPLETE 2026-01-05) - Haiku/Sonnet/Opus auto-selection, 80% cost reduction, 18/18 tests passed
4. ✅ **Phase 2.5: Data Layer SLAs** (COMPLETE 2026-01-05) - <5 min sync, 95% compliance, automatic Slack alerts
5. ✅ **Phase 3: Autopilot Mode** (COMPLETE 2026-01-05) - Best-of-N selection, consensus voting, 4h → 20min (80% time saved)
6. ✅ **Phase 4: Digital Twin Dashboard** (COMPLETE 2026-01-05) - City planner control room, 5-layer observability, real-time monitoring

**Roadmap**: `docs/VIBE_CODING_TRANSFORMATION.md`

### 🎉 TRANSFORMATION COMPLETE

FibreFlow has fully transformed from traditional development to vibe coding:
- **Before**: Manual coding, unknown costs, stale data, sequential builds, log debugging
- **After**: Autonomous development, 80% cheaper, fresh data, parallel execution, dashboard monitoring
- **Result**: Engineers are now city planners who validate outcomes through real-time dashboards

**Access Dashboard**: `python dashboard/digital_twin_api.py` → http://localhost:8000

## Agent OS (Spec-Driven Planning)

Structured planning framework for agent development.

### Decision Tree
```
Need to build? → Well-defined requirement?
├─ NO → Use Agent OS (/plan-product, /shape-spec, /write-spec)
└─ YES → How many features?
         ├─ 10+ → Use Harness (overnight build)
         ├─ 3-9 → Consider Harness or direct
         └─ 1-2 → Direct development
```

### Quick Reference
| Scenario | Tool | Reason |
|----------|------|--------|
| Vague requirement | Agent OS | Need planning |
| 50 features + spec | Harness | Autonomous build |
| Bug fix | Direct | 30 seconds vs 30 minutes |
| New major feature | Agent OS → Harness | Plan first, build second |

**Repository**: https://github.com/buildermethods/agent-os

## Development Principles

### Prompt Engineering
- **Clear Prompts**: Specific files, line numbers, error messages
- **Ultrathink**: For complex problems requiring deep reasoning
- **Custom Memories**: Project-specific context (`# add to memory`)
- **Plan Mode**: For unclear requirements or multi-step features

### Advanced Techniques
- **Ultrathink**: Add to prompts for complex agent builds, architectural decisions, VLM engineering
- **Custom Memories**: Temporary project context vs permanent CLAUDE.md
- **Examples**: See `docs/PROMPT_ENGINEERING_GUIDE.md`

### Agent Development
- **When to create**: Distinct domain, specialized tools, reusable
- **When NOT**: One-off tasks, overlaps existing, too generic
- **Testing**: Unit + integration tests, error handling, demo script

### Cost Management
- **Haiku**: $0.001/query - health checks, simple queries
- **Sonnet**: $0.020/query - complex analysis, production UI
- **Context**: Use sub-agents, clear history, slash commands

## Autonomous GitHub Ticketing

**Status**: ✅ PRODUCTION - AUTO-TRIGGER ENABLED
- **Repo**: https://github.com/VelocityFibre/ticketing
- **Execution**: GitHub Actions → QFieldCloud VPS
- **Resolution**: 25-30 seconds, zero human intervention
- **Capabilities**: Auto-fixes 80% of issues, escalates 20%
- **Guide**: `docs/guides/AUTONOMOUS_GITHUB_TICKETING.md`

## Custom Commands & Sub-Agents

### Slash Commands (`.claude/commands/`)
- `/agents/build [name]` - Build agent via harness
- `/db-query [natural-language]` - Database query
- `/vps-health` - Check VPS status
- `/test-all` - Run test suite
- `/deploy [agent]` - Deploy to production

### Sub-Agents (`.claude/agents/`)
- `code-reviewer`, `test-generator`, `doc-writer`
- `deployment-checker`, `ui-tester`
- Invoke with `@agent-name` or natural language

## 🚨 CRITICAL: WhatsApp Pairing Codes

**THE CORRECT SERVICE**: `/opt/whatsapp-sender/whatsapp-sender` on **HOSTINGER VPS**
- **Technology**: Go + whatsmeow (NOT Node.js)
- **Phone**: +27 71 155 8396
- **Port**: 8081
- **Supports**: ✅ PAIRING CODES (via phone number)

**THE WRONG SERVICE**: `/var/www/lifeos-agents`
- **Technology**: Node.js + whatsapp-web.js
- **Supports**: ❌ QR CODES ONLY (no pairing codes)

**To Get Pairing Code**:
```bash
ssh root@72.60.17.245  # DEPRECATED VPS (password: VeloF@2025@@)
# CRITICAL: Stop systemd auto-restart first!
systemctl stop whatsapp-sender.service && systemctl disable whatsapp-sender.service && pkill -9 -f whatsapp-sender && cd /opt/whatsapp-sender && rm -rf store/* && ./whatsapp-sender > sender.log 2>&1 & sleep 10 && tail -40 sender.log
```

**Note**: This service will be migrated to VF Server after QFieldCloud migration completes.

**Details**: See `WHATSAPP_PAIRING_CRITICAL.md`

## Common Pitfalls

1. **Always activate venv**: Use `./venv/bin/python3`, not `python3`
2. **Agent routing**: Check `orchestrator/registry.json` triggers
3. **Convex functions**: Deploy with `npx convex deploy` first
4. **SSH keys**: Store in `~/.ssh/`, never commit
5. **Context limits**: Superior Agent Brain uses 200K tokens
6. **Neon sync**: Run `sync_neon_to_convex.py` after schema changes
7. **WhatsApp failing**: Use `/opt/whatsapp-sender` NOT lifeos-agents (`WHATSAPP_PAIRING_CRITICAL.md`)
8. **Storage uploads failing**: Check `NEXT_PUBLIC_USE_VF_STORAGE=true` and port 8091 is running (`FIREBASE_STORAGE_MIGRATION_2026-01-09.md`)

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

## Documentation Automation

4-layer system ensures docs stay updated:

1. **Git Hooks**: Validate commits, warn on missing docs
2. **Helper Scripts**: `./scripts/add-changelog-entry.sh` (30 sec)
3. **CI/CD**: GitHub Actions validates documentation
4. **Culture**: Definition of Done, PR templates

**Setup**: `./scripts/install-git-hooks.sh`
**Guide**: `docs/DOCUMENTATION_AUTOMATION.md`

## Special Notes

- **Domain Memory First**: "The magic is in the memory." See `DOMAIN_MEMORY_GUIDE.md`
- **Multi-Agent System**: Create specialized agents, not monolithic ones
- **Agent Harness**: For 6+ tools, use harness instead of manual development
- **Two Memory Systems**: Domain Memory (task state) vs Superior Brain (cross-session)
- **Dual Databases**: Neon (source of truth) + Convex (operational). Keep synced
- **SSH Access**: Keys in `~/.ssh/`, VF Server verified with key auth
- **VF Server Paths**: `/srv/data/apps/fibreflow/` (production on NVMe)
- **WhatsApp Critical**: Phone +27 71 155 8396 must be paired. Session in `~/whatsapp-sender/store/whatsapp.db` - NEVER DELETE

# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless absolutely necessary.
ALWAYS prefer editing existing files.
NEVER proactively create documentation files unless explicitly requested.
