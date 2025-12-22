# FibreFlow Agent Workforce 🚀

**Multi-agent AI system for fiber optic infrastructure operations**

[![Production](https://img.shields.io/badge/Production-Live-green)](http://72.60.17.245/)
[![Claude SDK](https://img.shields.io/badge/Claude-Agent_SDK-blue)](https://github.com/anthropics/anthropic-sdk-python)
[![Architecture](https://img.shields.io/badge/Architecture-Skills--Based-orange)](docs/architecture/)

**Deployment Targets**:
- **Hostinger VPS** (72.60.17.245): Public-facing FibreFlow API and web interface
- **VF Server** (100.96.203.105): Internal operations, BOSS integration, QField sync

## Overview

FibreFlow Agent Workforce is a production-ready AI agent system featuring:
- **Skills-Based Architecture**: 99% faster queries, 84% less context usage
- **Dual Database Strategy**: Neon PostgreSQL + Convex real-time backend
- **Intelligent Orchestration**: Automatic task routing to specialized agents
- **Advanced Memory Systems**: Domain memory + Superior Agent Brain
- **Autonomous Agent Builder**: Overnight agent development via harness

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/VelocityFibre/FibreFlow-Agent-Workforce.git
cd FibreFlow-Agent-Workforce

# Set up environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Test the system
./venv/bin/pytest tests/ -v
```

## 📖 Documentation

### Essential Reading
- **[CLAUDE.md](CLAUDE.md)** - Complete project reference and Claude Code instructions
- **[Repository Improvement Plan](REPOSITORY_IMPROVEMENT_PLAN.md)** - Current reorganization status

### Documentation Hub

#### 🎯 Getting Started
- [Quick Start Guide](docs/guides/QUICK_START.md)
- [Setup Checklist](docs/guides/SETUP_CHECKLIST.md)
- [Troubleshooting](docs/guides/TROUBLESHOOTING.md)
- [Monday Quick Start](docs/guides/MONDAY_QUICK_START.md)

#### 🏗️ Architecture
- [Skills vs Agents Architecture](docs/architecture/AGENT_WORKFORCE_GUIDE.md)
- [Domain Memory Guide](docs/architecture/DOMAIN_MEMORY_GUIDE.md)
- [AI Brain Architecture](docs/architecture/AI_AGENT_BRAIN_ARCHITECTURE.md)
- [Memory Decision Matrix](docs/architecture/MEMORY_DECISION_MATRIX.md)

#### 🛠️ Development Guides
- [Agent SDK Setup](docs/guides/AGENT_SDK_SETUP.md)
- [Agent Skills Guide](docs/guides/AGENT_SKILLS_GUIDE.md)
- [Neon Database Agent](docs/guides/NEON_AGENT_GUIDE.md)
- [Convex Backend Agent](docs/guides/CONVEX_AGENT_GUIDE.md)
- [Claude Code Best Practices](docs/guides/CLAUDE_CODE_BEST_PRACTICES.md)

#### 📚 API Reference
- [Quick Reference](docs/api/QUICK_REFERENCE.md)
- [Command Reference](docs/api/COMMAND_QUICK_REFERENCE.md)
- [Project Summary](docs/api/PROJECT_SUMMARY.md)
- [Agent Organigram](docs/api/AGENT_ORGANIGRAM.txt)

## 🏆 Performance

Latest benchmarks with skills-based architecture:

| Metric | Skills-Based | Agent-Based | Improvement |
|--------|-------------|-------------|-------------|
| Query Time | 23ms | 2,300ms | **99% faster** |
| Context Usage | 930 tokens | 4,500 tokens | **80% less** |
| Success Rate | 95%+ | 100% | Comparable |

See [experiments/skills-vs-agents/FINAL_RESULTS.md](experiments/skills-vs-agents/FINAL_RESULTS.md)

## 🧩 Project Structure

```
.
├── .claude/              # Claude Code configuration
│   ├── skills/          # Production skills (optimized)
│   ├── agents/          # Sub-agents for Claude Code
│   └── commands/        # Slash commands
├── docs/                # All documentation
│   ├── guides/          # How-to guides
│   ├── architecture/    # System design
│   ├── api/            # Reference docs
│   └── archive/        # Old documentation
├── agents/             # Legacy agents (fallback)
├── skills/             # Old skills (being migrated)
├── orchestrator/       # Task routing system
├── harness/           # Autonomous agent builder
├── shared/            # Shared utilities
├── tests/             # Test suite
├── convex/            # Convex backend
├── deploy/            # Deployment scripts
└── ui-module/         # Web interface
```

## 🚀 Production Deployment

**Live URL**: http://72.60.17.245/

```bash
# Deploy to VPS
cd deploy
./deploy_brain.sh

# Check health
curl http://72.60.17.245/health
```

See [Deployment Workflow](docs/guides/DEPLOYMENT_WORKFLOW.md)

## 🔧 Key Commands

### Using Claude Code
```bash
# Database query
/db-query "Show all active contractors"

# Build new agent (overnight)
/agents/build my-agent

# Check VPS health
/vps-health

# Run all tests
/test-all
```

### Direct Python Usage
```bash
# Interactive Neon agent
./venv/bin/python3 demo_neon_agent.py

# Run orchestrator
./venv/bin/python3 orchestrator/orchestrator.py

# Sync databases
./venv/bin/python3 sync_neon_to_convex.py
```

## 🧪 Testing

```bash
# Run all tests
./venv/bin/pytest tests/ -v

# Run specific category
./venv/bin/pytest -m unit        # Fast unit tests
./venv/bin/pytest -m integration # Integration tests
./venv/bin/pytest -m database    # Database tests
```

## 🤝 Contributing

1. Read [CLAUDE.md](CLAUDE.md) for project conventions
2. Check [Repository Improvement Plan](REPOSITORY_IMPROVEMENT_PLAN.md)
3. Follow the skills-based architecture pattern
4. Add tests for new features
5. Update documentation

## 📄 License

Proprietary - Velocity Fibre Internal Use

## 🆘 Support

- **Issues**: Create GitHub issue
- **Internal**: Contact FibreFlow team
- **Documentation**: See [docs/](docs/) directory

---

**Built with Claude Agent SDK** | **Powered by Anthropic Claude**
<\!-- Auto-sync test: 2025-12-22 09:00:04 -->
