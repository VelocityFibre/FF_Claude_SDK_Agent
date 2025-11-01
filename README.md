# FibreFlow Agent - AI Database Assistant

AI-powered natural language interface for querying the FibreFlow PostgreSQL database using Claude's Agent SDK.

![FibreFlow Agent](ui-module/vf-logo.svg)

## Overview

FibreFlow Agent enables team members to query the database using plain English instead of SQL. Built with:
- **Claude Agent SDK** - AI framework with tool-calling capabilities
- **Claude Sonnet 4.5** - Latest AI model (upgraded from Haiku for better performance)
- **FastAPI** - Production-ready Python API backend
- **PostgreSQL (Neon)** - Serverless database with 104 tables

## Live Demo

🌐 **Production**: http://72.60.17.245/

Try asking:
- "Show me all active contractors"
- "How many projects do we have?"
- "List recent installations by date"
- "What's the status of fiber deployment in [area]?"

## Architecture

```
┌─────────────────┐
│   Web Chat UI   │  Beautiful gradient interface (chat.html)
│  (Port 80/443)  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  FastAPI Backend│  REST API wrapper (agent_api.py)
│   (Port 8000)   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Claude Agent   │  AI engine with tool calling (neon_agent.py)
│  (Sonnet 4.5)   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Neon Postgres  │  Production database (104 tables)
│   (Azure GWC)   │
└─────────────────┘
```

## Core Files

| File | Purpose | Location |
|------|---------|----------|
| `ui-module/neon_agent.py` | Main agent logic - connects Claude to database | Core |
| `ui-module/agent_api.py` | FastAPI wrapper for production deployment | Core |
| `ui-module/chat.html` | Web interface with markdown support | UI |
| `ui-module/vf-logo.svg` | FibreFlow branding | UI |
| `ui-module/requirements.txt` | Python dependencies | Deploy |
| `ui-module/.env.example` | Environment template (copy to .env) | Config |

## Quick Start (Local Development)

### 1. Clone and Setup

```bash
git clone https://github.com/VelocityFibre/FF_Claude_SDK_Agent.git
cd FF_Claude_SDK_Agent/ui-module
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your credentials
nano .env
```

### 3. Run Locally

```bash
python agent_api.py
# Opens on http://localhost:8000
# Web interface: http://localhost:8000
```

## Environment Variables

Create `.env` file (never commit this!):

```bash
ANTHROPIC_API_KEY=sk-ant-api03-...your-key...
NEON_DATABASE_URL=postgresql://username:password@host/dbname?sslmode=require
ALLOWED_ORIGINS=*
PORT=8000
DEBUG=False
```

## Current Status

### ✅ Working Features
- Natural language database queries
- Markdown-formatted responses (lists, tables, code blocks)
- Context-aware conversations
- Auto-reconnect to database
- Production deployment on Hostinger VPS
- Health monitoring endpoint (`/health`)
- API documentation (`/docs`)

### 🎯 Known Improvements Needed
**Please add your suggestions here!**

1. **Performance**
   - [ ] Query caching for common requests
   - [ ] Connection pooling optimization
   - [ ] Response time monitoring

2. **Features**
   - [ ] Multi-turn conversation history
   - [ ] Export results (CSV, JSON)
   - [ ] Scheduled reports
   - [ ] Query templates/shortcuts

3. **UI/UX**
   - [ ] Dark mode toggle
   - [ ] Query history sidebar
   - [ ] Real-time typing indicator improvements
   - [ ] Mobile responsive design

4. **Security**
   - [ ] User authentication
   - [ ] Role-based access control
   - [ ] Query audit logging
   - [ ] Rate limiting

5. **Integrations**
   - [ ] Slack bot interface
   - [ ] Email alerts for specific queries
   - [ ] Export to Google Sheets
   - [ ] Webhook support for automation

## Adding Improvement Suggestions

### For Teammates:

1. **Quick suggestions**: Add to the checklist above
2. **Detailed proposals**: Create GitHub Issues with:
   - Problem description
   - Proposed solution
   - Use case / benefit
   - Priority (Low/Medium/High)

3. **Code improvements**: Create Pull Requests with:
   - Clear description of changes
   - Test cases if applicable
   - Screenshots for UI changes

## Deployment

Currently deployed on:
- **Server**: Hostinger VPS (72.60.17.245)
- **OS**: Ubuntu 24.04 LTS
- **Location**: Lithuania
- **Web Server**: Nginx (reverse proxy)
- **Process Manager**: Systemd (auto-restart)

See `ui-module/DEPLOY_NOW.md` for deployment instructions.

## Tech Stack Details

- **Python 3.13**
- **Claude SDK** (`anthropic` package)
- **FastAPI** (async web framework)
- **psycopg2** (PostgreSQL driver)
- **Uvicorn** (ASGI server)
- **Marked.js** (markdown rendering)

## Model Evolution

- **Started with**: Claude 3 Haiku (fast, cheap, but conservative)
- **Upgraded to**: Claude Sonnet 4.5 (better reasoning, confident responses)
- **Cost impact**: ~$20-30/month vs $5/month for 1000 queries
- **Result**: 10x better at showing actual data vs refusing with false warnings

## Database Context

The agent has access to **104 tables** including:
- Contractors (20 total, 9 active)
- Projects (fiber deployment tracking)
- Installations and maintenance
- Equipment inventory
- Customer data
- Geographic/location data

## API Endpoints

- `GET /` - Web chat interface
- `POST /agent/chat` - Send message to agent
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation
- `GET /redoc` - Alternative API docs

## Development Notes

### Why Claude Agent SDK?

Traditional chatbots require hardcoded query patterns. Claude Agent SDK uses **tool calling**:
1. User asks natural language question
2. Claude decides which database function to call
3. Function executes SQL query
4. Claude formats results for user

This means adding new capabilities only requires adding new Python functions - no retraining needed!

### System Prompt Strategy

The agent has a system prompt instructing it to:
- Always show actual data when tools succeed
- Never claim connection issues when queries work
- Format results clearly with markdown
- Be confident when presenting data

This was crucial after Haiku would execute queries successfully but refuse to show results.

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Test your changes locally
4. Commit with clear messages
5. Push to your fork
6. Open Pull Request

## Questions / Support

- **Issues**: GitHub Issues tab
- **PM**: Review NEON_AGENT_UI_RECOMMENDATIONS.md for full integration options
- **Live Demo**: http://72.60.17.245/

## License

Internal project - VelocityFibre/FibreFlow team only.

---

**Built by**: Louis Du Preez + Claude
**Last Updated**: November 2025
**Status**: ✅ Production Ready
