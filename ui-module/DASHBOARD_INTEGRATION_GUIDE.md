# FibreFlow Dashboard Integration Guide

**Add real-time FibreFlow monitoring to your FF_React app in 10 minutes**

## Quick Start

### 1. Install Dependencies

```bash
# Navigate to your FF_React app
cd ~/VF/Apps/FF_React

# Install required packages
npm install recharts axios

# Or with yarn
yarn add recharts axios
```

### 2. Copy Dashboard Files

```bash
# Copy React component to your app
cp ~/Agents/claude/ui-module/FibreFlowDashboard.tsx src/components/

# Copy API server to your project (optional - can run from Agents/claude)
cp ~/Agents/claude/ui-module/fibreflow-dashboard-api.py src/api/
```

### 3. Start the Dashboard API

```bash
# Terminal 1: Start Dashboard API
cd ~/Agents/claude
source venv/bin/activate
python ui-module/fibreflow-dashboard-api.py

# API will be available at http://localhost:8001
# Swagger docs at http://localhost:8001/docs
```

### 4. Add Route to Your React App

**Option A: React Router v6**

```typescript
// src/App.tsx or src/routes.tsx
import FibreFlowDashboard from './components/FibreFlowDashboard';

// Add to your routes
<Route path="/fibreflow" element={<FibreFlowDashboard />} />
```

**Option B: Add to Navigation**

```typescript
// src/components/Navigation.tsx (or wherever your nav is)
<NavLink to="/fibreflow">
  FibreFlow Dashboard
</NavLink>
```

### 5. Access Dashboard

```bash
# Start your React app
npm run dev

# Navigate to
http://localhost:3000/fibreflow
```

---

## API Endpoints

The Dashboard API provides these endpoints:

```
GET /api/dashboard/overview           - System overview (all metrics)
GET /api/dashboard/convergence/latest - Latest convergence results
GET /api/dashboard/consequences/latest - Latest consequence analysis
GET /api/dashboard/patterns            - Pattern learning statistics
GET /api/dashboard/knowledge           - Knowledge graph data
GET /api/dashboard/workload            - Team workload distribution
GET /api/dashboard/conflicts           - Active conflict predictions
GET /api/dashboard/tasks               - Proactivity queue status
GET /api/health                        - Health check
```

**Swagger Docs**: http://localhost:8001/docs

---

## Dashboard Features

### 📊 Overview Cards
- **Task Queue**: Total tasks, confidence distribution
- **Pattern Learning**: Feedback stats, approval/rejection rates
- **Team Status**: Active developers, overloaded count, avg workload

### 🎯 Consequence Analysis
- Overall impact level (none/low/medium/high/critical)
- Deployment risk assessment
- Category breakdown (API, Database, Performance, User)
- Blast radius calculation
- Actionable recommendations

### 👥 Team Workload
- Pie chart distribution (overloaded/busy/available/light)
- Individual developer workload bars
- Real-time capacity tracking

### 📈 Pattern Confidence Weights
- Bar chart of all pattern types
- Shows learning progress over time
- Identifies which patterns are improving/degrading

---

## Customization

### Change API URL

```typescript
// In FibreFlowDashboard.tsx
const API_BASE = 'http://your-api-server:8001/api/dashboard';
```

### Adjust Auto-Refresh Interval

```typescript
// In FibreFlowDashboard.tsx (line ~125)
const interval = setInterval(fetchDashboardData, 30000); // 30 seconds

// Change to 60 seconds
const interval = setInterval(fetchDashboardData, 60000);
```

### Modify Color Scheme

```typescript
// In FibreFlowDashboard.tsx
const COLORS = {
  primary: '#3b82f6',   // Change to your brand color
  success: '#10b981',
  warning: '#f59e0b',
  danger: '#ef4444',
  info: '#06b6d4',
  gray: '#6b7280'
};
```

---

## Production Deployment

### Option 1: Separate API Server

```bash
# Install uvicorn and dependencies
pip install fastapi uvicorn python-multipart

# Run with gunicorn for production
gunicorn fibreflow-dashboard-api:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8001
```

### Option 2: Proxy Through Your React App

```typescript
// vite.config.ts (if using Vite)
export default {
  server: {
    proxy: {
      '/api/dashboard': {
        target: 'http://localhost:8001',
        changeOrigin: true
      }
    }
  }
}
```

```typescript
// Then change API_BASE in FibreFlowDashboard.tsx
const API_BASE = '/api/dashboard';
```

### Option 3: Deploy API to VPS

```bash
# On your VPS
sudo systemctl create fibreflow-api.service

[Unit]
Description=FibreFlow Dashboard API
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/Agents/claude
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/uvicorn ui-module.fibreflow-dashboard-api:app --host 0.0.0.0 --port 8001

[Install]
WantedBy=multi-user.target
```

---

## Troubleshooting

### Issue: CORS Error

**Solution**: The API already includes CORS middleware for localhost:3000 and localhost:5173. If using a different port:

```python
# In fibreflow-dashboard-api.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://your-custom-port"  # Add your port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: API Not Found

**Check**:
1. API server is running: `curl http://localhost:8001/api/health`
2. FibreFlow databases exist: `ls memory/*.db`
3. Python environment activated: `source venv/bin/activate`

### Issue: No Data Showing

**Check**:
1. Run convergence analysis first: `./venv/bin/python3 orchestrator/convergence.py`
2. Check proactivity queue: `cat shared/proactivity_queue.json`
3. Verify git history exists: `git log --oneline | head`

### Issue: React Import Error

**Solution**: Add to `tsconfig.json`:

```json
{
  "compilerOptions": {
    "types": ["recharts"]
  }
}
```

---

## Optional Enhancements

### 1. Add Authentication

```python
# In fibreflow-dashboard-api.py
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.get("/api/dashboard/overview")
async def get_overview(credentials: HTTPBearer = Depends(security)):
    # Verify token
    # ...
```

### 2. WebSocket for Real-Time Updates

```python
# Add WebSocket endpoint
from fastapi import WebSocket

@app.websocket("/ws/dashboard")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = get_dashboard_data()
        await websocket.send_json(data)
        await asyncio.sleep(10)
```

### 3. Export Dashboard Data

```typescript
// Add export button in dashboard
const exportData = () => {
  const data = {
    overview,
    consequences,
    patterns,
    workload
  };

  const blob = new Blob([JSON.stringify(data, null, 2)], {
    type: 'application/json'
  });

  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `fibreflow-${Date.now()}.json`;
  a.click();
};
```

---

## Dashboard Screenshots

### Overview (What You'll See)

```
┌─────────────────────────────────────────────────────────────┐
│ FibreFlow Dashboard                      Last Updated: 14:30 │
│ Proactive AI System Monitoring                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐ ┌───────────────┐ ┌────────────────┐     │
│  │ Task Queue   │ │ Pattern Learn │ │ Team Status    │     │
│  │ 365 Total    │ │ 50 Feedback   │ │ 3 Developers   │     │
│  │ ■ 328 High   │ │ 42% Approval  │ │ 0 Overloaded   │     │
│  │ ■ 37 Medium  │ │ 16% Rejection │ │ 65% Avg Load   │     │
│  └──────────────┘ └───────────────┘ └────────────────┘     │
│                                                               │
│  ┌──────────────────────────┐ ┌──────────────────────────┐ │
│  │ Latest Commit Impact     │ │ Team Workload            │ │
│  │ Overall: HIGH            │ │ [Pie Chart]              │ │
│  │ Risk: HIGH               │ │ Developer A: ████░░ 80%  │ │
│  │                          │ │ Developer B: ██░░░░ 40%  │ │
│  │ ■ API: LOW               │ │ Developer C: ███░░░ 60%  │ │
│  │ ■ Database: NONE         │ │                          │ │
│  │ ■ Performance: HIGH      │ │                          │ │
│  │ ■ User: HIGH             │ │                          │ │
│  │                          │ │                          │ │
│  │ Recommendations:         │ │                          │ │
│  │ • Deploy during low      │ │                          │ │
│  │   traffic period         │ │                          │ │
│  └──────────────────────────┘ └──────────────────────────┘ │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Pattern Confidence Weights [Bar Chart]                  ││
│  │ unused_import    ████████░░ 0.90                        ││
│  │ n+1_query        ████░░░░░░ 0.46                        ││
│  │ trailing_space   ████████░░ 0.87                        ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

---

## Support & Next Steps

### Need Help?
1. Check API health: `curl http://localhost:8001/api/health`
2. View API logs in terminal
3. Check browser console for React errors
4. Review `CLAUDE.md` for FibreFlow documentation

### Extend the Dashboard
1. Add conflict prediction visualization
2. Add knowledge graph network diagram
3. Add task timeline view
4. Add developer activity heatmap
5. Add notification center

---

**You now have a production-ready dashboard integrated into your React app!** 🎉

Access it at: `http://localhost:3000/fibreflow`

The dashboard auto-refreshes every 30 seconds and provides real-time visibility into your FibreFlow proactive system.
