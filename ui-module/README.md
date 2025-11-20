# Database AI Agent - UI Module

**⌘K Command Palette for Natural Language Database Queries**

Ready-to-integrate module for your Next.js fiber deployment app.

---

## 🎯 What This Is

A **complete, production-ready** command palette that lets users ask questions about your Neon PostgreSQL database using natural language.

**Press ⌘K → Ask "How many active contractors?" → Get instant answer**

---

## 📦 What's Included

| File | Purpose | Copy To |
|------|---------|---------|
| `CommandPalette.tsx` | React component (⌘K UI) | `VF/Apps/FF_React/components/agent/` |
| `route.ts` | Next.js API route | `VF/Apps/FF_React/app/api/agent/chat/` |
| `agent_api.py` | Python FastAPI backend | Deploy to Railway |
| `requirements.txt` | Python dependencies | Backend folder |
| `railway.json` | Railway config | Backend folder |
| `Procfile` | Alternative hosting | Backend folder |
| `.env.backend.example` | Backend variables | Copy to `.env` |
| `.env.frontend.example` | Frontend variables | Copy to `.env.local` |
| `INTEGRATION_GUIDE.md` | **START HERE** | Read first! |

---

## ⚡ Quick Start (3 Steps)

### 1. Deploy Backend (30 min)

```bash
# Sign up at railway.app
# Create new project
# Upload: agent_api.py, neon_agent.py, requirements.txt, railway.json

# Set environment variables in Railway:
ANTHROPIC_API_KEY=your-key
NEON_DATABASE_URL=your-connection-string
ALLOWED_ORIGINS=http://localhost:3000

# Railway auto-deploys → Copy URL
```

### 2. Add to Next.js (30 min)

```bash
cd VF/Apps/FF_React

# Install dependency
npm install lucide-react

# Copy files:
# - CommandPalette.tsx → components/agent/
# - route.ts → app/api/agent/chat/

# Add to .env.local:
AGENT_BACKEND_URL=https://your-app.railway.app
```

Add to your layout:

```typescript
// app/layout.tsx
import { CommandPalette } from '@/components/agent/CommandPalette';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <CommandPalette />
      </body>
    </html>
  );
}
```

### 3. Test It! (5 min)

```bash
npm run dev
```

1. Open http://localhost:3000
2. Press `⌘K`
3. Type: "How many projects do we have?"
4. 🎉 See the magic!

---

## 📖 Full Documentation

**For step-by-step integration:**
👉 **Read `INTEGRATION_GUIDE.md`**

**For technical details:**
- `../NEON_AGENT_GUIDE.md` - Agent documentation
- `../NEON_AGENT_UI_RECOMMENDATIONS.md` - UI patterns & design
- `../PROJECT_SUMMARY.md` - Complete project overview

---

## ✨ Features

### Command Palette
- ⌘K (Mac) or Ctrl+K (Windows) to open
- Natural language queries
- Context-aware suggestions
- Conversation history
- Error handling
- Loading states

### Contextual Intelligence
```typescript
// On project page
<CommandPalette context={{ page: 'project', projectId: '123' }} />

// Suggestions adapt:
// - "Show BOQ status for this project"
// - "What contractors are assigned?"
```

### Example Queries

**General:**
- "How many active projects?"
- "Show me top performing contractors"
- "Which projects are over budget?"

**Analysis:**
- "Compare Q3 vs Q4 costs"
- "Show contractors with red RAG status"
- "Generate a project status report"

**Specific:**
- "What's the safety score for contractor XYZ?"
- "Show me BOQs pending approval"
- "List all suppliers for fiber cable"

---

## 🎨 Customization

### Brand Colors

```typescript
// CommandPalette.tsx line ~120
className="bg-blue-600"  // Your brand color
```

### Custom Suggestions

```typescript
// CommandPalette.tsx line ~200
function getSuggestions(context) {
  if (context.page === 'dashboard') {
    return [
      'Your custom query 1',
      'Your custom query 2',
    ];
  }
}
```

### Keyboard Shortcut

```typescript
// CommandPalette.tsx line ~32
if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
  // Change 'k' to another key
}
```

---

## 🔒 Security

### Set API Key (Recommended)

```bash
# Generate
openssl rand -hex 32

# Add to backend .env
AGENT_API_KEY=generated-key

# Add to frontend .env.local
AGENT_API_KEY=same-generated-key
```

### Restrict CORS

```bash
# In Railway, set specific domain
ALLOWED_ORIGINS=https://your-production-app.vercel.app
```

### Add Rate Limiting

See `INTEGRATION_GUIDE.md` section "Security Best Practices"

---

## 💰 Costs

**Monthly estimate:**
- Railway hosting: $5-20/month
- Anthropic API (1000 queries): $3-5/month
- **Total: $10-25/month**

Scale:
- 5000 queries: ~$20-40/month
- 10000 queries: ~$35-70/month

---

## 🐛 Troubleshooting

### Backend not responding

```bash
# Check health
curl https://your-app.railway.app/health

# View logs
Railway dashboard → Deployments → View Logs
```

### ⌘K doesn't open

- Check component is in layout
- Check browser console for errors
- Try clicking "Ask AI" button instead

### CORS errors

- Update `ALLOWED_ORIGINS` in Railway
- Include your frontend URL
- Redeploy backend

**More help:** See `INTEGRATION_GUIDE.md` → Troubleshooting

---

## 📊 What Users Can Ask

### Your Fiber Deployment Business

Based on your 104 database tables:

**Projects:**
- "Show active projects"
- "Which projects are delayed?"
- "What's the budget utilization?"

**Contractors:**
- "List contractors by performance score"
- "Who has the best safety rating?"
- "Show contractors available this week"

**BOQs:**
- "What BOQs need approval?"
- "Show unmapped BOQ items"
- "Compare estimated vs actual costs"

**Materials:**
- "How much fiber cable in stock?"
- "Show cable drum locations"
- "What equipment is at Project Phoenix?"

**Reports:**
- "Generate project status report"
- "Summarize contractor performance"
- "Show financial overview"

---

## 🚀 Deployment Checklist

### Before Launch
- [ ] Backend deployed to Railway
- [ ] Environment variables set
- [ ] Health check returns "healthy"
- [ ] Frontend component added
- [ ] ⌘K works in development
- [ ] Test 10+ example queries
- [ ] CORS configured for production

### Launch
- [ ] Deploy to Vercel production
- [ ] Test on production URL
- [ ] Share with 5 pilot users
- [ ] Monitor logs for errors

### First Week
- [ ] Collect user feedback
- [ ] Check most common queries
- [ ] Optimize slow queries
- [ ] Add missing suggestions

---

## 📈 Success Metrics

Track these to measure adoption:

- **Daily active users** - How many use ⌘K?
- **Queries per user** - Average usage
- **Most common queries** - What do people ask?
- **Response time** - Avg time to answer
- **User satisfaction** - Thumbs up/down (add later)

---

## 🔄 Next Steps

### Phase 1 (Current)
✅ Command palette working
✅ Natural language queries
✅ Deployed to production

### Phase 2 (Optional)
- [ ] Add sidebar on detail pages
- [ ] Dashboard insight cards
- [ ] Export results to CSV
- [ ] Voice input support

### Phase 3 (Advanced)
- [ ] Query caching
- [ ] User feedback (👍 👎)
- [ ] Scheduled reports
- [ ] Slack integration

See `../NEON_AGENT_UI_RECOMMENDATIONS.md` for detailed Phase 2-3 plans.

---

## 🎓 Architecture

```
User presses ⌘K
       ↓
CommandPalette.tsx (React)
       ↓
/api/agent/chat (Next.js API Route)
       ↓
agent_api.py (FastAPI on Railway)
       ↓
neon_agent.py (Claude Agent)
       ↓
Claude AI (Anthropic)
       ↓
Neon PostgreSQL Database
       ↓
Result returned to user
```

---

## 📚 Additional Resources

**Documentation:**
- `INTEGRATION_GUIDE.md` - Step-by-step setup
- `../NEON_AGENT_GUIDE.md` - Complete agent docs
- `../PROJECT_SUMMARY.md` - Project overview
- `../QUICK_REFERENCE.md` - Developer cheat sheet

**Examples:**
- `../test_neon_advanced.py` - See agent in action
- `../demo_neon_agent.py` - Interactive demo

**API:**
- https://docs.anthropic.com - Claude docs
- https://docs.railway.app - Deployment docs

---

## ✅ Integration Checklist

Copy this into your project management tool:

```markdown
## Database AI Agent Integration

### Day 1: Backend Deployment
- [ ] Sign up for Railway
- [ ] Create new project
- [ ] Upload backend files
- [ ] Set environment variables
- [ ] Verify health endpoint
- [ ] Copy deployment URL

### Day 2: Frontend Integration
- [ ] Install lucide-react
- [ ] Copy CommandPalette.tsx
- [ ] Copy route.ts
- [ ] Set AGENT_BACKEND_URL
- [ ] Add to layout
- [ ] Test locally with ⌘K
- [ ] Verify queries work

### Day 3: Polish & Deploy
- [ ] Add context to specific pages
- [ ] Test all example queries
- [ ] Update CORS for production
- [ ] Deploy to Vercel
- [ ] Test on production
- [ ] Share with pilot users
- [ ] Monitor usage

### Week 2: Iterate
- [ ] Review analytics
- [ ] Gather user feedback
- [ ] Fix edge cases
- [ ] Optimize slow queries
- [ ] Expand to more pages
```

---

## 💡 Tips for Success

1. **Start small:** Deploy to 5-10 pilot users first
2. **Gather queries:** See what people actually ask
3. **Iterate quickly:** Add suggestions based on usage
4. **Monitor costs:** Check Anthropic dashboard weekly
5. **Celebrate wins:** Share success stories with team

---

## 🎉 You're Ready!

Everything you need is in this folder. Start with `INTEGRATION_GUIDE.md` and you'll have a working command palette in 3 days.

**Questions?** Check the troubleshooting sections in the guides.

**Ready for more?** See `NEON_AGENT_UI_RECOMMENDATIONS.md` for next features.

---

*Built with Claude Agent SDK • Last updated: 2025-10-31*
