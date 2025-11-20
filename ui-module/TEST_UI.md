# Testing the Updated UI Locally

## 🎯 What's New

Your UI now uses **orchestrated routing** with your 3 specialized agents:
- **Contractor Agent** - Auto-selected for contractor queries
- **Project Agent** - Auto-selected for project queries
- **Universal Convex Agent** - Access to all 30+ tables & 14k+ records

## 🚀 How to Test Locally

### Step 1: Start the API Server

```bash
cd ui-module
../venv/bin/python3 orchestrated_agent_api.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Initializing Agent Orchestrator...
INFO:     Orchestrator initialized with 5 agents
```

### Step 2: Open the UI

Open `orchestrated_chat.html` in your browser:

```bash
# On Linux
xdg-open orchestrated_chat.html

# Or just open the file directly
# File path: /home/louisdup/Agents/claude/ui-module/orchestrated_chat.html
```

### Step 3: Test Queries

Try these queries and watch which agent gets selected:

**Contractor Queries** (→ Contractor Agent):
- "Show me all contractors"
- "How many contractors do we have?"
- "Search for contractors with Fiber"

**Project Queries** (→ Project Agent):
- "List all projects"
- "Show me project details"
- "How many projects are active?"

**FibreFlow Data Queries** (→ Universal Agent):
- "Show me Lawley activations"
- "How many OneMap poles?"
- "List Nokia exports"
- "Show SOW poles"

## 🎨 What You'll See

### Smart Routing:
```
User: "Show me all contractors"
     ↓
Orchestrator analyzes keywords: ["contractors"]
     ↓
Routes to: CONTRACTOR-AGENT
     ↓
Response: "You have 9 contractors..."
```

### UI Features:
1. **Status indicator** shows which agent is handling your query
2. **Agent badge** on each response (e.g., "CONTRACTOR-AGENT")
3. **Typing indicator** while agent is thinking
4. **Quick examples** you can click to test

## 📊 API Endpoints Available

### `/chat` - Orchestrated routing
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me all contractors", "mode": "orchestrated"}'
```

### `/agents` - List all agents
```bash
curl http://localhost:8000/agents
```

### `/health` - Check status
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "3.0.0",
  "agents_available": 5,
  "tables_accessible": 30,
  "records_accessible": 14173
}
```

## 🔧 Troubleshooting

### Issue: API won't start
**Solution:** Install dependencies
```bash
pip install fastapi uvicorn
```

### Issue: UI can't connect
**Solution:** Check API is running on port 8000
```bash
# In another terminal
curl http://localhost:8000/health
```

### Issue: Agent responses are slow
**Solution:** Normal for first query (agent initialization). Subsequent queries are faster.

## 🎯 How Routing Works

The orchestrator checks your query for keywords:

| Keywords | Routes To | Example |
|----------|-----------|---------|
| contractor, vendor, company | Contractor Agent | "Show contractors" |
| project, site, deployment | Project Agent | "List projects" |
| task, todo | Convex Agent | "Show tasks" |
| lawley, mohadin, poles, activations | Universal Agent | "Lawley activations" |

If no match, falls back to Universal Agent (can access everything).

## 📄 Files Created

✅ `orchestrated_agent_api.py` - FastAPI backend with orchestrator
✅ `orchestrated_chat.html` - Updated UI with agent badges
✅ `TEST_UI.md` - This guide

## 🎉 What You Have Now

✅ **Orchestrated routing** - Auto-selects right agent
✅ **5 agents available** - VPS, Neon, Convex, Contractor, Project
✅ **14,173 records** - Full FibreFlow data access
✅ **30+ tables** - Universal access to all Convex data
✅ **Beautiful UI** - Shows which agent handled each query
✅ **Local testing** - No deployment needed

---

**Ready to test!** Start the API, open the HTML, and ask away! 🚀
