# WA Monitor Complete Deployment Guide

## 🎯 Overview

This guide deploys the complete WA DR monitoring system with:
1. `/api/foto/evaluations` endpoint for listing evaluations
2. Updated React components for foto-reviews page
3. WhatsApp integration for sending feedback

## ✅ Current Status

### What's Working:
- ✅ VLM (Qwen/Qwen3-VL-8B-Instruct) - Analyzing images with real scores
- ✅ `/api/foto/evaluate` - Evaluating DRs successfully
- ✅ `/api/foto/evaluation/{dr_number}` - Getting evaluation results
- ✅ `/api/foto/feedback` - Marking feedback as sent
- ✅ `/api/foto/photos` - Listing all DRs
- ✅ WhatsApp Sender service - Running on port 8081

### What Needs Fixing:
- ⚠️ WhatsApp phone NOT paired (connected: false)
- ⚠️ `/api/foto/evaluations` endpoint doesn't exist yet
- ⚠️ React components show "0" - need to fetch real data

## 📦 Deployment Files

### 1. API Endpoint: `/api/foto/evaluations`

**File**: `api_evaluations_route.ts`
**Deploy to**: `/home/louis/apps/fibreflow/app/api/foto/evaluations/route.ts`

This endpoint returns all evaluations with filtering:
- `?feedback_sent=false` - Only pending feedback
- `?status=FAIL` - Only failed evaluations
- `?limit=50&offset=0` - Pagination

### 2. React Component: Foto Reviews Dashboard

**File**: `FotoReviewsDashboard.tsx`
**Deploy to**: `/home/louis/apps/fibreflow/src/modules/foto-reviews/components/FotoReviewsDashboard.tsx`

Features:
- Real-time data from `/api/foto/evaluations`
- Edit feedback messages before sending
- Send to WhatsApp via `/api/foto/feedback`
- Filter and search evaluations

### 3. WhatsApp Integration

**Service**: WhatsApp Sender (Go binary)
**Location**: `~/whatsapp-sender/whatsapp-sender`
**Port**: 8081
**Status**: ✅ Running but ⚠️ Phone not paired

## 🚨 CRITICAL: WhatsApp Phone Pairing Required

The WhatsApp Sender service is running but **phone +27 71 155 8396 is NOT paired**.

### Check Status:
```bash
curl http://100.96.203.105:8081/health
# Response: {"connected": false, "service": "whatsapp-sender", "status": "ok"}
```

### To Pair Phone:

1. **On VF Server**, access the WhatsApp Sender service:
```bash
ssh louis@100.96.203.105
# OR if on server already:
curl http://localhost:8081/qr
```

2. **On Phone +27 71 155 8396**:
   - Open WhatsApp
   - Go to Settings → Linked Devices
   - Tap "Link a Device"
   - Scan the QR code from step 1

3. **Verify Pairing**:
```bash
curl http://localhost:8081/health
# Should show: {"connected": true, ...}
```

4. **Session Persistence**:
   - Session stored in `~/whatsapp-sender/store/whatsapp.db`
   - **NEVER DELETE THIS FILE** - it contains the pairing info
   - Backup regularly: `cp ~/whatsapp-sender/store/whatsapp.db ~/whatsapp-sender/store/whatsapp.db.backup`

## 📝 Step-by-Step Deployment

### Step 1: Deploy API Endpoint

```bash
# On VF server
ssh louis@100.96.203.105

# Create the evaluations endpoint
mkdir -p /home/louis/apps/fibreflow/app/api/foto/evaluations

# Copy the route.ts file
cat > /home/louis/apps/fibreflow/app/api/foto/evaluations/route.ts << 'EOF'
[Paste content of api_evaluations_route.ts]
EOF
```

### Step 2: Deploy React Component

```bash
# Update the FotoReviewsDashboard component
cat > /home/louis/apps/fibreflow/src/modules/foto-reviews/components/FotoReviewsDashboard.tsx << 'EOF'
[Paste content of FotoReviewsDashboard.tsx]
EOF
```

### Step 3: Rebuild Next.js

```bash
# Rebuild the app
cd /home/louis/apps/fibreflow
npm run build

# Restart Next.js
pkill -f "next-server"
sleep 3
npm run start &
```

### Step 4: Pair WhatsApp Phone

```bash
# Get QR code for pairing
curl http://localhost:8081/qr

# Follow pairing instructions above
# Verify: curl http://localhost:8081/health
```

### Step 5: Test End-to-End

1. **Open foto-reviews page**:
```
https://app.fibreflow.app/foto-reviews
```

2. **Verify evaluations load** - Should show pending evaluations with real data

3. **Test feedback sending**:
   - Click "Review Feedback" on an evaluation
   - Edit message if needed
   - Click "Send to WhatsApp"
   - Verify message arrives on WhatsApp

## 🧪 Testing the System

### Test 1: API Endpoints

```bash
# List all evaluations
curl http://100.96.203.105:3005/api/foto/evaluations | jq

# Get pending only
curl "http://100.96.203.105:3005/api/foto/evaluations?feedback_sent=false" | jq

# Get specific DR
curl http://100.96.203.105:3005/api/foto/evaluation/DR1734014 | jq
```

### Test 2: Evaluation Workflow

```bash
# 1. Evaluate a DR
curl -X POST http://100.96.203.105:3005/api/foto/evaluate \
  -H "Content-Type: application/json" \
  -d '{"dr_number": "DR1734014"}'

# 2. Check it appears in evaluations list
curl "http://100.96.203.105:3005/api/foto/evaluations?feedback_sent=false" | jq

# 3. Send feedback
curl -X POST http://100.96.203.105:3005/api/foto/feedback \
  -H "Content-Type: application/json" \
  -d '{"dr_number": "DR1734014"}'

# 4. Verify feedback_sent = true
curl http://100.96.203.105:3005/api/foto/evaluation/DR1734014 | jq .data.feedback_sent
```

### Test 3: WhatsApp Integration

```bash
# Check WhatsApp service health
curl http://100.96.203.105:8081/health

# Send test message (requires phone paired)
curl -X POST http://100.96.203.105:8081/send \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "27711558396",
    "message": "Test message from WA Monitor"
  }'
```

## 🔧 Troubleshooting

### Issue: Evaluations Don't Load

**Problem**: foto-reviews page shows "0" for all stats

**Solution**:
1. Check API endpoint exists: `curl http://100.96.203.105:3005/api/foto/evaluations`
2. Check database has data: Run evaluation first
3. Check browser console for errors
4. Verify Next.js rebuild completed

### Issue: WhatsApp Feedback Fails

**Problem**: "the store doesn't contain a device JID"

**Solution**: Phone is not paired. Follow pairing instructions in Step 4.

**Problem**: "Failed to send to WhatsApp"

**Solution**:
1. Check WhatsApp Sender is running: `ss -tlnp | grep 8081`
2. Check health: `curl http://localhost:8081/health`
3. Verify phone is paired: `"connected": true`
4. Check session file exists: `ls -la ~/whatsapp-sender/store/whatsapp.db`

### Issue: VLM Still Failing

**Problem**: Evaluations return score 0/10

**Solution**:
1. Check VLM service: `ps aux | grep vllm`
2. Verify model: Should show `Qwen/Qwen3-VL-8B-Instruct`
3. Check context limit: Should show `--max-model-len 16384`
4. Test VLM directly: `curl http://localhost:8100/v1/models`

## 📊 Expected Results

After deployment:

1. **foto-reviews page** (https://app.fibreflow.app/foto-reviews):
   - Shows pending evaluations with real counts
   - Can review and edit feedback messages
   - Can send to WhatsApp (if phone paired)

2. **Evaluation API** (/api/foto/evaluations):
   - Returns list of all evaluations
   - Supports filtering by status and feedback_sent
   - Includes pagination

3. **WhatsApp Integration**:
   - Service running on port 8081
   - Phone paired and connected
   - Messages sent successfully

## 🎯 Quick Deployment Script

```bash
#!/bin/bash
# Quick deployment script

echo "Deploying WA Monitor updates..."

# 1. Deploy API endpoint
mkdir -p /home/louis/apps/fibreflow/app/api/foto/evaluations
cp api_evaluations_route.ts /home/louis/apps/fibreflow/app/api/foto/evaluations/route.ts

# 2. Deploy React component
cp FotoReviewsDashboard.tsx /home/louis/apps/fibreflow/src/modules/foto-reviews/components/

# 3. Rebuild
cd /home/louis/apps/fibreflow
npm run build

# 4. Restart
pkill -f "next-server"
sleep 3
npm run start &

echo "Deployment complete!"
echo "Check https://app.fibreflow.app/foto-reviews"
echo ""
echo "⚠️  Don't forget to pair WhatsApp phone!"
echo "Run: curl http://localhost:8081/qr"
```

## 📚 Related Documentation

- `WA_MONITOR_SETUP.md` - Complete WhatsApp Sender setup guide
- `WA_DR_QUICKSTART.md` - Quick start for DR monitoring
- `CLAUDE.md` - Main project documentation

## 🆘 Support

If deployment fails:
1. Check all services are running (Next.js, VLM, WhatsApp Sender)
2. Review logs: `/tmp/vllm.log`, Next.js console
3. Verify phone pairing status
4. Test each component individually before testing end-to-end
