# WhatsApp Feedback Fix - Deployment Guide

## Issue Summary
The WhatsApp feedback button on https://app.fibreflow.app/wa-monitor was failing because the frontend was using mock API calls instead of real ones.

## Changes Made

### 1. **wa_approval_interface.html** - Fixed JavaScript API Integration

#### Before (Mock Implementation):
- `callEvaluateAPI()` - Used setTimeout to simulate API calls
- `approveFeedback()` - Only simulated sending with setTimeout
- No real HTTP requests were being made

#### After (Real Implementation):
- Added dynamic API base URL detection (localhost vs production)
- `callEvaluateAPI()` - Makes real POST to `/api/foto/evaluate`
- `approveFeedback()` - Makes real POST to `/api/foto/feedback` with WhatsApp message
- `refreshEvaluations()` - Fetches pending evaluations from server
- Proper error handling and user feedback

## Deployment Steps

### 1. Test Locally First
```bash
# Test API endpoints
python3 test_wa_feedback_api.py

# Open HTML file locally and test
open wa_approval_interface.html
```

### 2. Deploy to Production Server

#### Option A: Direct Server Update
```bash
# SSH to VF server
ssh louis@100.96.203.105  # or use Tailscale IP

# Navigate to web directory
cd /path/to/web/app

# Backup existing file
cp wa_approval_interface.html wa_approval_interface.html.backup

# Upload new file
# From local machine:
scp wa_approval_interface.html louis@100.96.203.105:/path/to/web/app/
```

#### Option B: Via Git Repository
```bash
# Commit changes
git add wa_approval_interface.html test_wa_feedback_api.py
git commit -m "fix: Fix WhatsApp feedback API integration - replace mock with real API calls"
git push origin main

# On server
ssh louis@100.96.203.105
cd /path/to/app
git pull origin main
```

### 3. Verify API Endpoints

Ensure the following endpoints are available on production:
- `POST https://app.fibreflow.app/api/foto/evaluate`
- `POST https://app.fibreflow.app/api/foto/feedback`
- `GET https://app.fibreflow.app/api/foto/evaluations`

### 4. Test Production
```bash
# Test production API from local
python3 test_wa_feedback_api.py --prod DR1730550

# Or test directly on server
curl -X POST https://app.fibreflow.app/api/foto/feedback \
  -H "Content-Type: application/json" \
  -d '{"dr_number": "DR1730550", "message": "Test message"}'
```

### 5. Browser Testing

1. Open https://app.fibreflow.app/wa-monitor
2. Enter a DR number (e.g., DR1730550)
3. Click "Evaluate"
4. Edit the feedback message if needed
5. Click "Approve & Send"
6. Verify WhatsApp message is sent

## 🚨 CRITICAL PREREQUISITE: WhatsApp Service

**Before deploying or testing, ensure:**

1. **WhatsApp Sender service is running** on VF server (100.96.203.105:8081)
2. **Phone +27 71 155 8396 is paired** via WhatsApp "Linked Devices"
3. **Session is active** (check `curl http://localhost:8081/health` on server)

**If feedback fails with error "the store doesn't contain a device JID":**
- The phone is not paired to the WhatsApp service
- Follow pairing instructions in `WA_MONITOR_SETUP.md`

**Quick Check**:
```bash
# On VF server
curl http://localhost:8081/health
# Should return: {"status":"ok","service":"whatsapp-sender","connected":true}
```

## Backend Requirements

The backend API at `https://app.fibreflow.app/api/foto/feedback` must:

1. Accept POST requests with JSON payload:
```json
{
  "dr_number": "DR1730550",
  "message": "WhatsApp formatted message",
  "evaluation": { /* evaluation data */ }
}
```

2. Send the WhatsApp message using the configured WhatsApp Business API

3. Return success response:
```json
{
  "success": true,
  "message": "Feedback sent successfully"
}
```

## CORS Configuration

Ensure the backend allows CORS from the frontend domain:
```python
# In FastAPI or similar
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://app.fibreflow.app",
        "http://localhost:*"
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"]
)
```

## Troubleshooting

### If feedback still fails:

1. **Check browser console** (F12 → Console):
   - Look for network errors
   - Check CORS issues
   - Verify API response

2. **Check network tab** (F12 → Network):
   - Verify request is being sent
   - Check response status code
   - Review request/response payloads

3. **Test API directly**:
```bash
# From server
curl -I https://app.fibreflow.app/api/foto/feedback

# Should return 200 OK or 405 Method Not Allowed (not 404)
```

4. **Check server logs**:
```bash
# On VF server
sudo journalctl -u fibreflow-api -f
# or
tail -f /var/log/fibreflow/api.log
```

## Rollback Plan

If issues occur after deployment:
```bash
# On server
mv wa_approval_interface.html wa_approval_interface.html.broken
mv wa_approval_interface.html.backup wa_approval_interface.html
```

## Success Criteria

✅ Feedback button makes real API call (visible in browser Network tab)
✅ API returns success response
✅ WhatsApp message is actually sent to recipients
✅ UI updates to show "WhatsApp feedback sent successfully"
✅ No console errors in browser

## Contact

For backend API issues or WhatsApp Business API configuration, contact the backend team or check the API documentation at `/api/docs`.