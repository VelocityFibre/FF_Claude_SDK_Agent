# Database AI Agent - Integration Guide

**Get your command palette working in 3 days**

---

## 📦 What You're Installing

A **⌘K command palette** that lets users ask questions about your database in natural language.

**Example:**
- User presses `⌘K`
- Types: "How many active contractors?"
- Gets instant answer from your Neon database

---

## 🗂️ Files Included

```
ui-module/
├── CommandPalette.tsx          # React component (⌘K interface)
├── route.ts                    # Next.js API route
├── agent_api.py                # Python backend (FastAPI)
├── requirements.txt            # Python dependencies
├── railway.json                # Railway deployment config
├── Procfile                    # Alternative deployment config
├── .env.backend.example        # Backend environment variables
├── .env.frontend.example       # Frontend environment variables
└── INTEGRATION_GUIDE.md        # This file
```

---

## ⚡ Quick Start (3 Days)

### Day 1: Deploy Backend (2-3 hours)

#### Step 1.1: Prepare Backend Files

Create a new folder for the backend:

```bash
mkdir neon-agent-backend
cd neon-agent-backend
```

Copy these files into it:
- `agent_api.py`
- `neon_agent.py` (from main project)
- `requirements.txt`
- `railway.json`
- `Procfile`

#### Step 1.2: Deploy to Railway

1. **Sign up for Railway:**
   - Go to https://railway.app
   - Sign up with GitHub (free tier available)

2. **Create new project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo" (or "Empty Project")

3. **Upload files:**
   - If using GitHub: Push your backend folder
   - If using UI: Drag and drop the folder

4. **Set environment variables:**

   In Railway dashboard → Variables → Add these:

   ```
   ANTHROPIC_API_KEY=sk-ant-api03-xxx...
   NEON_DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
   ALLOWED_ORIGINS=http://localhost:3000,https://your-app.vercel.app
   ```

   Optional (for security):
   ```
   AGENT_API_KEY=your-random-secret-key-here
   ```

5. **Deploy:**
   - Railway auto-detects Python and deploys
   - Wait ~2 minutes for build
   - Copy the deployment URL (e.g., `https://your-app.railway.app`)

6. **Test it:**

   ```bash
   # Health check
   curl https://your-app.railway.app/health

   # Should return:
   # {"status":"healthy","database":"connected","agent":"ready",...}
   ```

---

### Day 2: Integrate Frontend (2-3 hours)

#### Step 2.1: Install Dependencies

In your Next.js project (`VF/Apps/FF_React`):

```bash
npm install lucide-react
```

#### Step 2.2: Copy Component

Copy `CommandPalette.tsx` to:

```
VF/Apps/FF_React/
└── components/
    └── agent/
        └── CommandPalette.tsx    # Paste here
```

#### Step 2.3: Copy API Route

Copy `route.ts` to:

```
VF/Apps/FF_React/
└── app/
    └── api/
        └── agent/
            └── chat/
                └── route.ts    # Paste here
```

#### Step 2.4: Set Environment Variables

Add to `VF/Apps/FF_React/.env.local`:

```bash
# Your Railway deployment URL
AGENT_BACKEND_URL=https://your-app.railway.app

# Optional: If you set AGENT_API_KEY in backend
AGENT_API_KEY=your-random-secret-key-here
```

#### Step 2.5: Add to Your App

Edit your root layout or any page:

```typescript
// app/layout.tsx or app/page.tsx
import { CommandPalette } from '@/components/agent/CommandPalette';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}

        {/* Add command palette */}
        <CommandPalette />
      </body>
    </html>
  );
}
```

#### Step 2.6: Test Locally

```bash
npm run dev
```

1. Open http://localhost:3000
2. Press `⌘K` (Mac) or `Ctrl+K` (Windows)
3. Type: "How many projects do we have?"
4. See the result! 🎉

---

### Day 3: Polish & Deploy (1-2 hours)

#### Step 3.1: Add Contextual Suggestions

For project pages, add context:

```typescript
// app/projects/[id]/page.tsx
import { CommandPalette } from '@/components/agent/CommandPalette';

export default function ProjectPage({ params }) {
  return (
    <div>
      {/* Your existing content */}

      {/* Context-aware command palette */}
      <CommandPalette
        context={{
          page: 'project',
          projectId: params.id
        }}
      />
    </div>
  );
}
```

Now when users press ⌘K on a project page, they get relevant suggestions:
- "Show me the BOQ status for this project"
- "What contractors are assigned?"

#### Step 3.2: Add Trigger Button (Optional)

For users who don't know about ⌘K:

```typescript
import { CommandPaletteShortcut } from '@/components/agent/CommandPalette';

// In your header/navbar:
<CommandPaletteShortcut />
// Renders: "Ask AI ⌘K" button
```

#### Step 3.3: Update CORS for Production

In Railway dashboard → Variables → Update:

```
ALLOWED_ORIGINS=https://your-production-app.vercel.app
```

#### Step 3.4: Deploy to Vercel

```bash
# In VF/Apps/FF_React
vercel deploy --prod
```

Update `AGENT_BACKEND_URL` in Vercel environment variables if needed.

---

## 🎯 Testing Checklist

- [ ] Backend health check returns "healthy"
- [ ] ⌘K opens the command palette
- [ ] Can type and submit a query
- [ ] Gets response from database
- [ ] Suggestions appear on empty state
- [ ] Context works on specific pages
- [ ] Escape closes the palette
- [ ] Works on production deployment

---

## 🎨 Customization

### Change Styling

Edit `CommandPalette.tsx`:

```typescript
// Change colors (line ~120)
className="bg-blue-600"  // Change to your brand color

// Change size (line ~87)
className="max-w-2xl"    // Change to max-w-3xl for wider
```

### Change Keyboard Shortcut

```typescript
// In CommandPalette.tsx, line ~32
if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
  // Change 'k' to another key
}
```

### Add Custom Suggestions

Edit `getSuggestions()` function (line ~200):

```typescript
function getSuggestions(context: Record<string, any>): string[] {
  // Add your own suggestions
  if (context.page === 'custom-page') {
    return [
      'Your custom query 1',
      'Your custom query 2',
    ];
  }
  // ...
}
```

---

## 🔒 Security Best Practices

### 1. Set API Key

Generate a random key:

```bash
openssl rand -hex 32
```

Add to both backend and frontend `.env`:

```
AGENT_API_KEY=your-generated-key
```

### 2. Restrict CORS

In Railway, set specific origins:

```
ALLOWED_ORIGINS=https://your-app.vercel.app
```

### 3. Add Rate Limiting (Optional)

Install in backend:

```bash
pip install slowapi
```

Update `agent_api.py`:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/agent/chat")
@limiter.limit("20/hour")  # 20 queries per hour per IP
async def chat(...):
    # ...
```

### 4. Add Authentication (Optional)

If you have Next.js auth:

```typescript
// route.ts
import { getServerSession } from 'next-auth';

export async function POST(req: NextRequest) {
  const session = await getServerSession();

  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // Continue with request...
}
```

---

## 🐛 Troubleshooting

### Backend Issues

**"Connection failed"**

```bash
# Check if backend is running
curl https://your-app.railway.app/health

# If fails, check Railway logs:
# Railway dashboard → Deployments → View Logs
```

**"Database connection error"**

- Verify `NEON_DATABASE_URL` in Railway variables
- Check Neon database is running
- Test connection string directly:
  ```bash
  psql "your-connection-string"
  ```

### Frontend Issues

**"⌘K doesn't work"**

- Check browser console for errors
- Verify component is imported in layout
- Try clicking the "Ask AI" button instead

**"Failed to fetch"**

- Check `AGENT_BACKEND_URL` in `.env.local`
- Verify backend is running (health check)
- Check browser network tab for CORS errors

**"Response is slow"**

- First query is slower (cold start)
- Consider upgrading Railway plan
- Or use Haiku model for faster responses

### CORS Errors

In browser console: `CORS policy: No 'Access-Control-Allow-Origin'`

**Fix:**

1. Add your frontend URL to `ALLOWED_ORIGINS` in Railway
2. Redeploy backend
3. Clear browser cache

---

## 📊 Monitoring Usage

### Track Queries (Optional)

Add analytics to `route.ts`:

```typescript
// After successful response
await logAnalytics({
  event: 'agent_query',
  userId: session?.user?.id,
  query: message.substring(0, 100),
  page: context.page,
  timestamp: new Date()
});
```

### Monitor Costs

Check Anthropic usage:
- https://console.anthropic.com/settings/usage

Track:
- Total requests
- Average tokens per request
- Monthly cost

**Typical costs:**
- 1000 queries/month: $3-5
- 5000 queries/month: $15-25

---

## 🚀 Next Steps

### Phase 1 (Done ✅)
- [x] Command palette working
- [x] Connected to database
- [x] Deployed to production

### Phase 2 (Optional Enhancements)

**Add sidebar on detail pages:**
```typescript
// Show persistent sidebar on project pages
<AgentSidebar context={{ projectId }} />
```

**Add dashboard insights:**
```typescript
// Show proactive insights on dashboard
<AgentInsightCard query="What needs attention today?" />
```

**Add voice input:**
```typescript
// Use Web Speech API
navigator.mediaDevices.getUserMedia({ audio: true })
```

### Phase 3 (Advanced)

- [ ] Caching for common queries
- [ ] User feedback system (👍 👎)
- [ ] Query suggestions based on usage
- [ ] Export results to CSV/PDF
- [ ] Scheduled reports

---

## 💬 Support

### Documentation
- **Agent Guide:** `NEON_AGENT_GUIDE.md`
- **UI Recommendations:** `NEON_AGENT_UI_RECOMMENDATIONS.md`
- **Quick Reference:** `QUICK_REFERENCE.md`

### Logs

**Backend logs (Railway):**
```
Railway dashboard → Deployments → View Logs
```

**Frontend logs:**
```
Browser → Console → Network tab
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Slow responses | Use Haiku model, add caching |
| High costs | Add rate limiting, optimize queries |
| Wrong answers | Improve context, reset conversation |
| CORS errors | Update ALLOWED_ORIGINS |

---

## ✅ Success Criteria

Your integration is successful when:

1. ✅ Users can press ⌘K anywhere in app
2. ✅ Natural language queries return correct answers
3. ✅ Response time < 3 seconds
4. ✅ Suggestions are contextually relevant
5. ✅ Works on production deployment
6. ✅ Users are actually using it (check analytics)

---

## 📝 Deployment Checklist

### Before Going Live

- [ ] Test all example queries work
- [ ] CORS configured for production domain
- [ ] API keys set in production environment
- [ ] Rate limiting enabled (optional)
- [ ] Error handling tested
- [ ] Mobile responsive (test ⌘K on mobile)
- [ ] Documentation shared with team
- [ ] Analytics/monitoring set up

### Launch Day

- [ ] Deploy backend to Railway
- [ ] Deploy frontend to Vercel
- [ ] Announce to 5-10 pilot users
- [ ] Monitor logs for errors
- [ ] Collect feedback

### First Week

- [ ] Review usage analytics
- [ ] Check most common queries
- [ ] Identify and fix edge cases
- [ ] Gather user feedback
- [ ] Iterate on suggestions

---

## 🎉 You're Done!

Your database AI agent is now live! Users can:

✨ Press ⌘K to ask questions
✨ Get instant answers from your database
✨ Work faster without writing SQL

**Questions?** Review the documentation files or check the troubleshooting section.

**Ready to expand?** See `NEON_AGENT_UI_RECOMMENDATIONS.md` for next features (sidebar, dashboard insights, etc.)

---

*Built with Claude Agent SDK • Questions? Check NEON_AGENT_GUIDE.md*
