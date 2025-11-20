# 🚀 Test Unified Convex Agent - Local UI

## ✅ What You're Testing

**ONE unified agent** connected to your Convex database:
- 9 contractors
- 2 projects
- Tasks
- Sync operations

**17 tools in ONE agent** - No multiple agents, no orchestrator, just pure simplicity!

---

## 📋 Step 1: Start the API

```bash
cd /home/louisdup/Agents/claude/ui-module
../venv/bin/python3 unified_agent_api.py
```

**Wait for this message:**
```
✅ Agent ready with 17 tools
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## 📋 Step 2: Open the UI

Open this file in your browser:

```bash
xdg-open /home/louisdup/Agents/claude/ui-module/unified_chat.html
```

Or manually open:
```
file:///home/louisdup/Agents/claude/ui-module/unified_chat.html
```

---

## 📋 Step 3: Ask Questions!

### Try These Queries:

**Contractors:**
```
"Show me all contractors"
"How many contractors do we have?"
"Search for contractors with Fiber in the name"
"Get contractor statistics"
```

**Projects:**
```
"List all projects"
"Show me project details"
"How many projects are there?"
```

**Tasks:**
```
"Show task statistics"
"List all tasks"
"How many tasks do we have?"
```

**Sync:**
```
"Get sync status"
"Show synchronization statistics"
```

**Cross-domain (shows unified power):**
```
"Tell me about our contractors and projects"
"Give me an overview of everything"
```

---

## 🎯 What You'll See

### The UI Shows:
- ✅ **Clean chat interface**
- ✅ **Your questions** on the right (purple bubble)
- ✅ **Agent responses** on the left (white bubble)
- ✅ **Status indicator** - shows "17 tools" connected
- ✅ **Quick examples** - Click to try instantly
- ✅ **Reset button** - Clear conversation anytime

### The Agent Responds With:
- Real data from your Convex database
- Natural language answers
- Maintains conversation context
- Uses appropriate tools automatically

---

## 🔍 How It Works

```
You type: "Show me all contractors"
        ↓
Unified Agent analyzes query
        ↓
Selects: list_contractors tool
        ↓
Calls: contractors:list on Convex
        ↓
Returns: "You have 9 contractors..."
```

**ONE agent, automatic tool selection, maintains context!**

---

## 🎨 UI Features

### Quick Examples (Click to Try):
- 📋 All contractors
- 🔢 Count contractors
- 📁 Projects
- 📊 Task stats
- 🔄 Sync status

### Reset Button:
- Clears conversation history
- Starts fresh
- Agent forgets previous context

### Conversation Memory:
The agent **remembers** your conversation:
```
You: "Show contractors"
Agent: [Shows 9 contractors]

You: "How many are active?"
Agent: [Knows you mean contractors, checks count]
```

---

## 🧪 Test Scenarios

### Test 1: Basic Query
```
Ask: "How many contractors do we have?"
Expect: "You have 9 contractors in total"
```

### Test 2: Detailed Query
```
Ask: "List all contractors"
Expect: [Shows all 9 with details]
```

### Test 3: Cross-Domain
```
Ask: "Show contractors and projects"
Expect: [Shows both - uses multiple tools]
```

### Test 4: Context Memory
```
1. Ask: "Show all contractors"
2. Ask: "How many are there?" (doesn't specify "contractors")
Expect: Agent remembers you're talking about contractors
```

---

## 🐛 Troubleshooting

### Issue: Can't connect to API
**Solution:**
```bash
# Check if API is running
curl http://localhost:8000/health

# If not, start it
cd ui-module
../venv/bin/python3 unified_agent_api.py
```

### Issue: Agent responds slowly
**Normal!** First query takes 2-5 seconds (agent initialization).
Subsequent queries are faster.

### Issue: Browser won't load UI
**Solution:** Make sure you're opening the HTML file, not trying to visit http://localhost

**Correct:**
```
file:///home/louisdup/Agents/claude/ui-module/unified_chat.html
```

---

## 📊 What Data You Have

Your Convex database contains:

| Data Type | Count | Tools Available |
|-----------|-------|-----------------|
| **Contractors** | 9 | list, search, stats, add |
| **Projects** | 2 | list, search, stats, add |
| **Tasks** | 0 | list, add, update, delete, search, stats |
| **Sync Records** | - | get stats, last sync time |

**Total:** 17 tools in ONE agent

---

## 🎯 Key Differences from Before

### Before (Orchestrator with 3 agents):
```
Your query → Orchestrator → Routes to specific agent → Response
```
- More complex
- 3 separate agents
- Routing logic

### Now (Unified Agent):
```
Your query → Unified agent → Auto-selects tool → Response
```
- ✅ Simpler
- ✅ ONE agent
- ✅ Maintains context better
- ✅ Easier to understand

---

## ✅ Success Checklist

- [ ] API started on port 8000
- [ ] UI opened in browser
- [ ] Queried contractors successfully
- [ ] Queried projects successfully
- [ ] Agent maintained conversation context
- [ ] Reset button worked

---

## 📄 Files Created

✅ `unified_agent_api.py` - Simple FastAPI backend
✅ `unified_chat.html` - Clean UI
✅ `START_UNIFIED_UI.md` - This guide

---

**Ready to test!** 🎉

Start the API, open the HTML, and chat with your unified agent!
