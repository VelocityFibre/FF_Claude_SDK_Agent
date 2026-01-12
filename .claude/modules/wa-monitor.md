# Module: WA Monitor (WhatsApp Photo Review)

**Type**: agent
**Location**: `agents/wa-monitor/` (in FibreFlow Next.js app)
**Deployment**: VF Server port 3005 (dev), http://100.96.203.105:3005/foto-reviews
**Isolation**: fully_isolated
**Developers**: louis
**Last Updated**: 2026-01-12

---

## Overview

AI-powered photo review system that receives installation photos via WhatsApp, analyzes them using a Vision Language Model (VLM), detects DR (Distribution Room) compliance issues, and stores reviews in the database. Fully autonomous - zero human intervention required.

**Critical Context**: Fully isolated agent. No dependencies on core FibreFlow modules. WhatsApp phone +27 71 155 8396 MUST remain paired.

## Dependencies

### External Dependencies
- **WhatsApp Sender Service**: Port 8081, Go + whatsmeow library
  - Phone: +27 71 155 8396 (CRITICAL - session stored in ~/whatsapp-sender/store/)
  - Location: `/opt/whatsapp-sender/` on VF Server (planned migration from Hostinger)
  - Supports pairing codes (NOT QR codes)
- **VLM (Qwen3-VL-8B)**: Port 8100 on VF Server
  - Model: Qwen/Qwen2-VL-7B-Instruct
  - Response time: 2-5 seconds per image
  - GPU: NVIDIA (recommended) or CPU (slower)
- **Neon PostgreSQL**: `foto_ai_reviews` table
  - Source of truth for all reviews
  - No Convex sync (isolated data)

### Internal Dependencies
- **None** - Standalone monitoring system

## Database Schema

### Tables Owned
| Table | Description | Key Columns |
|-------|-------------|-------------|
| foto_ai_reviews | AI photo reviews | id, whatsapp_number, image_url, feedback, ai_model, created_at |
| whatsapp_messages | Message log (optional) | id, phone_number, message_body, direction, timestamp |

**Database Queries**:
```sql
-- Get recent reviews
SELECT * FROM foto_ai_reviews ORDER BY created_at DESC LIMIT 20;

-- Count reviews by phone
SELECT whatsapp_number, COUNT(*)
FROM foto_ai_reviews
GROUP BY whatsapp_number;

-- Find reviews with issues
SELECT * FROM foto_ai_reviews
WHERE feedback LIKE '%issue%' OR feedback LIKE '%problem%';
```

### Tables Referenced
None - fully isolated data

## API Endpoints

| Endpoint | Method | Purpose | Auth Required |
|----------|--------|---------|---------------|
| /api/whatsapp/webhook | POST | Receive WhatsApp messages | No (webhook) |
| /foto-reviews | GET | View review dashboard | No (dev only) |
| /api/foto-reviews | GET | Fetch reviews (JSON) | No (internal) |
| /api/vlm/analyze | POST | Trigger VLM analysis | No (internal) |

**Webhook Flow**:
1. WhatsApp Sender receives image → POST to /api/whatsapp/webhook
2. Webhook downloads image, sends to VLM (port 8100)
3. VLM analyzes image, returns feedback
4. Webhook stores review in `foto_ai_reviews` table
5. Optional: Send response back via WhatsApp

## Services/Methods

### Core Services
- **VLM Analysis Service** - `/api/vlm/analyze` endpoint
  - Accepts: Base64 image or image URL
  - Returns: JSON with feedback, confidence, detected_issues
  - Model: Qwen3-VL-8B (2-5 sec latency)

- **WhatsApp Webhook Handler** - `/api/whatsapp/webhook`
  - Validates sender (contractors only)
  - Downloads attached images
  - Triggers VLM analysis
  - Stores results in database

- **Review Dashboard** - `/foto-reviews`
  - Real-time view of all reviews
  - Filter by phone number, date range
  - Display images + AI feedback

## File Structure

```
agents/wa-monitor/              # Main agent directory
├── README.md                  # Setup guide
├── routes/
│   └── api/
│       └── whatsapp/
│           └── webhook.ts     # WhatsApp message handler
├── services/
│   └── vlm_analysis.ts       # VLM integration
└── components/
    └── foto-reviews/
        └── dashboard.tsx     # Review UI

/opt/whatsapp-sender/          # WhatsApp service (VF Server)
├── whatsapp-sender           # Go binary
├── store/                    # Session storage (NEVER DELETE)
└── sender.log               # Service logs
```

## Configuration

### Environment Variables (VF Server)
```bash
# WhatsApp Sender
WHATSAPP_SENDER_URL=http://100.96.203.105:8081
WHATSAPP_PHONE=+27711558396

# VLM Service
VLM_URL=http://100.96.203.105:8100
VLM_MODEL=Qwen/Qwen2-VL-7B-Instruct

# Database
NEON_DATABASE_URL=postgresql://...
```

### Config Files
- `.env` - Environment variables
- `docs/deployment/WA_MONITOR_SETUP.md` - Complete setup guide
- `WHATSAPP_PAIRING_CRITICAL.md` - WhatsApp pairing instructions

## Common Operations

### Development
```bash
# Start local dev server (port 3005)
cd /path/to/fibreflow-app
npm run dev -- --port 3005

# View dashboard
open http://localhost:3005/foto-reviews

# Test webhook
curl -X POST http://localhost:3005/api/whatsapp/webhook \
  -H 'Content-Type: application/json' \
  -d '{"phone": "+27711558396", "image_url": "https://example.com/photo.jpg"}'
```

### Deployment
```bash
# Deploy to VF Server dev instance (port 3005)
ssh velo@100.96.203.105
cd /srv/data/apps/fibreflow-dev
git pull origin develop
npm ci
npm run build
pm2 restart fibreflow-dev
```

### WhatsApp Service Management
```bash
# Check WhatsApp service status
ssh velo@100.96.203.105
ps aux | grep whatsapp-sender

# View WhatsApp logs
tail -f /opt/whatsapp-sender/sender.log

# Re-pair phone (if session lost)
# CRITICAL: Follow WHATSAPP_PAIRING_CRITICAL.md
systemctl stop whatsapp-sender.service
cd /opt/whatsapp-sender
rm -rf store/*
./whatsapp-sender
# Enter phone number +27711558396 when prompted
# Enter pairing code from phone
```

## Known Gotchas

### Issue 1: WhatsApp Session Lost (CRITICAL)
**Problem**: Messages not being received, webhook not firing
**Root Cause**: WhatsApp session expired or phone unpaired
**Solution**:
```bash
# Check session status
ssh velo@100.96.203.105
ls -la /opt/whatsapp-sender/store/whatsapp.db
# If file missing, session lost

# Re-pair (CRITICAL: Phone must be accessible)
cd /opt/whatsapp-sender
systemctl stop whatsapp-sender.service
rm -rf store/*
./whatsapp-sender
# Follow pairing prompts
```
**Reference**: `WHATSAPP_PAIRING_CRITICAL.md`
**Prevention**: NEVER delete `/opt/whatsapp-sender/store/` directory

### Issue 2: VLM Service Not Responding
**Problem**: Webhook times out, no AI feedback generated
**Root Cause**: VLM service crashed or model not loaded
**Solution**:
```bash
# Check VLM status
curl http://100.96.203.105:8100/health
# Expected: {"status": "ok", "model": "Qwen/Qwen2-VL-7B-Instruct"}

# Restart VLM if down
ssh velo@100.96.203.105
pm2 restart vlm-server
# Or manually:
cd /path/to/vlm-server
./venv/bin/python server.py --port 8100
```
**Reference**: `docs/deployment/WA_MONITOR_SETUP.md`

### Issue 3: Wrong WhatsApp Service (QR Codes Only)
**Problem**: Trying to get pairing code but only seeing QR code
**Root Cause**: Using wrong service - `/var/www/lifeos-agents` (Node.js) instead of `/opt/whatsapp-sender` (Go)
**Solution**:
```bash
# Verify you're using the CORRECT service
ssh velo@100.96.203.105
which whatsapp-sender
# Should show: /opt/whatsapp-sender/whatsapp-sender

# If using wrong service, switch to correct one
cd /opt/whatsapp-sender
./whatsapp-sender  # Supports pairing codes
```
**Reference**: `WHATSAPP_PAIRING_CRITICAL.md:9-17`

### Issue 4: Webhook Returns 500 (Database Connection Failed)
**Problem**: Webhook fires but can't store review
**Root Cause**: Neon connection string missing or incorrect
**Solution**:
```bash
# Verify database connection
echo $NEON_DATABASE_URL
# Should start with: postgresql://

# Test connection
psql $NEON_DATABASE_URL -c "SELECT COUNT(*) FROM foto_ai_reviews;"
```

## Testing Strategy

### Unit Tests
- Location: `tests/unit/wa-monitor/`
- Coverage requirement: 80%+
- Key areas:
  - Webhook validation (phone number format, message types)
  - VLM integration (API calls, response parsing)
  - Database operations (insert reviews, query filters)

### Integration Tests
- Location: `tests/integration/wa-monitor/`
- External dependencies: Mock VLM responses, test database
- Key scenarios:
  - End-to-end webhook → VLM → database flow
  - WhatsApp message parsing (images, text, errors)
  - Database storage and retrieval

### E2E Tests
- Location: Manual testing with real WhatsApp account
- Tool: WhatsApp mobile app + test phone number
- Critical user flows:
  1. Send photo to +27 71 155 8396
  2. Verify webhook receives message
  3. Confirm VLM analysis completes
  4. Check review appears in dashboard
  5. Verify response sent back to WhatsApp (optional)

## Monitoring & Alerts

### Health Checks
- Endpoint: `/api/whatsapp/webhook` (should return 405 for GET)
- Expected response: Method Not Allowed (GET not supported)
- WhatsApp Service: `curl http://100.96.203.105:8081/status`
- VLM Service: `curl http://100.96.203.105:8100/health`

### Key Metrics
- **Reviews per hour**: `SELECT COUNT(*) FROM foto_ai_reviews WHERE created_at > NOW() - INTERVAL '1 hour';`
- **VLM response time**: Target <5 seconds
- **Webhook success rate**: >95% (check logs for 500 errors)
- **WhatsApp session uptime**: 99%+ (monitor pairing status)

### Logs
- Location: PM2 logs on VF Server
  - `pm2 logs fibreflow-dev | grep whatsapp`
  - `tail -f /opt/whatsapp-sender/sender.log`
- Key log patterns:
  - `Received WhatsApp message` - Webhook triggered
  - `VLM analysis completed` - Image processed
  - `Stored review in database` - Success
  - `ERROR: VLM timeout` - VLM service issue
  - `ERROR: Database connection failed` - Neon issue

## Breaking Changes History

| Date | Change | Migration Required | Reference |
|------|--------|-------------------|-----------|
| 2025-12-XX | Initial implementation | Yes - Create foto_ai_reviews table | WA_MONITOR_SETUP.md |
| 2026-01-XX | VLM integration (Qwen3-VL-8B) | Yes - Deploy VLM service | OPERATIONS_LOG.md |

## Related Documentation

- [WA Monitor Setup Guide](docs/deployment/WA_MONITOR_SETUP.md)
- [WhatsApp Pairing Guide](WHATSAPP_PAIRING_CRITICAL.md)
- [VLM Server Setup](docs/deployment/VLM_SERVER_SETUP.md) (if exists)

## Contact

**Primary Owner**: Louis
**Team**: FibreFlow AI/Automation
**Deployment**: VF Server port 3005 (dev), port 8081 (WhatsApp), port 8100 (VLM)
