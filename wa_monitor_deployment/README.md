# WA Monitor Deployment Package

## 📦 Complete deployment package for FibreFlow WA DR Monitoring System

This package contains everything needed to deploy the complete WA monitor evaluation and feedback system.

## ✅ What This Deploys

1. **API Endpoint**: `/api/foto/evaluations` - Lists all evaluations with filtering
2. **React Component**: Updated `FotoReviewsDashboard` - Displays real evaluation data
3. **WhatsApp Integration**: Verified WhatsApp Sender service configuration

## 🚀 Quick Deploy (Recommended)

```bash
# Run the automated deployment script
./deploy.sh
```

This will:
- ✅ Deploy the `/api/foto/evaluations` API endpoint
- ✅ Rebuild Next.js application
- ✅ Restart the server
- ✅ Test the API endpoint
- ✅ Check WhatsApp Sender status

**Time**: ~5-10 minutes (includes rebuild)

## 📋 What's Included

### Files in This Package:

1. **`deploy.sh`** - One-command automated deployment script
2. **`DEPLOYMENT_GUIDE.md`** - Complete step-by-step deployment guide
3. **`api_evaluations_route.ts`** - API endpoint source code
4. **`FotoReviewsDashboard.tsx`** - React component source code

### Current System Status:

✅ **Working**:
- VLM Service (Qwen/Qwen3-VL-8B-Instruct) on port 8100
- Image evaluation with real quality scores
- Existing API endpoints (/evaluate, /evaluation, /feedback, /photos)
- WhatsApp Sender service on port 8081

⚠️ **Needs Attention**:
- WhatsApp phone +27 71 155 8396 NOT paired (`"connected": false`)
- `/api/foto/evaluations` endpoint doesn't exist (yet)
- React components not fetching real data (yet)

## 🔧 Manual Deployment

If you prefer manual deployment, follow `DEPLOYMENT_GUIDE.md`:

1. Deploy API endpoint
2. Deploy React component
3. Rebuild Next.js
4. Restart server
5. Pair WhatsApp phone

## 🚨 CRITICAL: WhatsApp Phone Pairing

**The feedback feature will NOT work until phone is paired!**

### To Pair:

```bash
# 1. SSH to server
ssh louis@100.96.203.105

# 2. Get QR code
curl http://localhost:8081/qr

# 3. On phone +27 71 155 8396:
#    - Open WhatsApp
#    - Settings → Linked Devices
#    - Link a Device
#    - Scan QR code

# 4. Verify pairing
curl http://localhost:8081/health
# Should show: {"connected": true, ...}
```

## 📊 Testing After Deployment

### Test 1: Check API Endpoint

```bash
curl "http://100.96.203.105:3005/api/foto/evaluations?limit=5" | jq
```

Expected: List of evaluations with success=true

### Test 2: Check Web Interface

Open: https://app.fibreflow.app/foto-reviews

Expected: Shows pending evaluations with real counts

### Test 3: Test Feedback Workflow

1. Click "Review Feedback" on an evaluation
2. Edit message if needed
3. Click "Send to WhatsApp"
4. Verify message arrives (requires phone paired)

## 🎯 Expected Results

After deployment:

- **foto-reviews** page shows real evaluation data
- **Pending** count shows actual pending evaluations
- **Review Feedback** opens detailed view
- **Send to WhatsApp** works (if phone paired)

## 📱 Production URLs

- Foto Reviews: https://app.fibreflow.app/foto-reviews
- WA Monitor: https://app.fibreflow.app/wa-monitor
- Standalone: http://100.96.203.105:3005/wa-monitor.html

## 🆘 Troubleshooting

### Deployment Fails

1. Check Next.js is running: `ps aux | grep next-server`
2. Check build logs: `tail -100 /tmp/nextjs_restart.log`
3. Verify API files deployed: `ls /home/louis/apps/fibreflow/app/api/foto/evaluations/`

### API Returns 404

1. Rebuild application: `cd ~/apps/fibreflow && npm run build`
2. Restart server: `pkill -f next-server && npm run start &`
3. Wait 30 seconds for server to start

### WhatsApp Fails

1. Check service: `curl http://100.96.203.105:8081/health`
2. If `"connected": false` → Phone not paired, follow pairing steps
3. If service not running: See `WA_MONITOR_SETUP.md`

## 📚 Related Documentation

- `DEPLOYMENT_GUIDE.md` - Complete deployment guide in this package
- `../WA_MONITOR_SETUP.md` - WhatsApp Sender service setup
- `../WA_DR_QUICKSTART.md` - Quick start for DR monitoring
- `../CLAUDE.md` - Main project documentation

## 🎉 Quick Start

```bash
# One-command deployment:
./deploy.sh

# Then pair phone if needed:
ssh louis@100.96.203.105
curl http://localhost:8081/qr
# Scan with phone +27 71 155 8396

# Test:
firefox https://app.fibreflow.app/foto-reviews
```

That's it! The complete system will be deployed and ready to use.
