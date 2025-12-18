# WA Monitor Setup Guide - WhatsApp Sender Service

## 🚨 CRITICAL REQUIREMENT

**The wa-monitor module at https://app.fibreflow.app/wa-monitor REQUIRES a paired WhatsApp device to send feedback messages.**

### Phone Number Required: +27 71 155 8396

This phone number must be:
- ✅ Active and able to receive WhatsApp pairing codes
- ✅ Linked to the WhatsApp sender service on VF server (100.96.203.105)
- ✅ Kept active (session expires if phone is offline for 14+ days)

## Architecture Overview

```
wa-monitor Frontend (https://app.fibreflow.app/wa-monitor)
         ↓
Next.js API (/api/wa-monitor-send-feedback)
         ↓
WhatsApp Sender Service (100.96.203.105:8081)
         ↓
WhatsApp Web API (whatsmeow library)
         ↓
Phone +27 71 155 8396 (MUST BE PAIRED)
         ↓
WhatsApp Groups (Velo Test, Lawley, Mohadin, Mamelodi)
```

## Service Components

### 1. WhatsApp Sender Service (Go)
- **Location**: `~/whatsapp-sender/` on VF server
- **Port**: 8081
- **Technology**: Go + whatsmeow library
- **Session Storage**: SQLite database at `~/whatsapp-sender/store/whatsapp.db`
- **Phone**: +27 71 155 8396

### 2. Next.js API Route
- **Location**: `/home/louis/apps/fibreflow/pages/api/wa-monitor-send-feedback.ts`
- **Function**: Formats QA feedback and calls WhatsApp sender service
- **Port**: Calls localhost:8081 (same server)

### 3. Frontend
- **URL**: https://app.fibreflow.app/wa-monitor
- **Function**: QA photo review interface with "Send Feedback" button

## Initial Setup (One-Time)

### Step 1: Install Go on VF Server

```bash
ssh louis@100.96.203.105

# Download and install Go
wget https://go.dev/dl/go1.21.5.linux-amd64.tar.gz -O /tmp/go1.21.5.linux-amd64.tar.gz
rm -rf ~/go
tar -C ~/ -xzf /tmp/go1.21.5.linux-amd64.tar.gz

# Verify installation
~/go/bin/go version
# Should output: go version go1.21.5 linux/amd64
```

### Step 2: Build WhatsApp Sender Service

```bash
# Create directory structure
mkdir -p ~/whatsapp-sender/store

# Copy whatsapp-sender.go source file to ~/whatsapp-sender/
# (Source file location: /home/louis/apps/fibreflow/scripts/wa-monitor/whatsapp-sender.go)

cd ~/whatsapp-sender

# Initialize Go module
export PATH=$PATH:~/go/bin
~/go/bin/go mod init whatsapp-sender
~/go/bin/go mod tidy

# Build binary
~/go/bin/go build -o whatsapp-sender whatsapp-sender.go

# Verify binary
ls -lh whatsapp-sender
# Should show ~23MB executable
```

### Step 3: Start Service and Pair Phone

```bash
cd ~/whatsapp-sender

# Start service in background
nohup ./whatsapp-sender > whatsapp-sender.log 2>&1 &

# View pairing code
tail -20 whatsapp-sender.log
```

**Expected Output**:
```
🔑 PAIRING CODE: XXXX-XXXX
========================================
📱 On phone +27 71 155 8396:
   1. Open WhatsApp
   2. Go to Settings → Linked Devices
   3. Tap 'Link a Device'
   4. Tap 'Link with Phone Number Instead'
   5. Enter code: XXXX-XXXX
========================================
```

### Step 4: Complete Pairing on Phone

**On phone +27 71 155 8396:**
1. Open WhatsApp
2. Tap **Settings** (three dots → Settings)
3. Tap **Linked Devices**
4. Tap **Link a Device**
5. Tap **Link with Phone Number Instead**
6. Enter the pairing code shown in the log

**Verification**:
After entering the code, the log should show:
```
✅ Connected to WhatsApp!
```

## Daily Operations

### Check Service Status

```bash
# Check if service is running
ps aux | grep whatsapp-sender | grep -v grep

# View recent logs
tail -30 ~/whatsapp-sender/whatsapp-sender.log

# Test health endpoint
curl http://localhost:8081/health
```

**Expected Health Response**:
```json
{
  "status": "ok",
  "service": "whatsapp-sender",
  "connected": true
}
```

### Restart Service

```bash
# Stop service
pkill -f whatsapp-sender

# Start service
cd ~/whatsapp-sender
nohup ./whatsapp-sender > whatsapp-sender.log 2>&1 &

# Verify it started
tail -20 whatsapp-sender.log
```

**Note**: If the phone was previously paired, the service will reconnect automatically without needing a new pairing code.

### Re-pair Phone (If Session Expired)

If the log shows **"Device not logged in - generating pairing code"**, the session has expired:

```bash
# Service will automatically generate new pairing code
tail -f ~/whatsapp-sender/whatsapp-sender.log

# Look for new pairing code, then repeat Step 4 above
```

## Troubleshooting

### Issue 1: "the store doesn't contain a device JID"

**Symptom**: Frontend shows error "Failed to send WhatsApp message: the store doesn't contain a device JID"

**Cause**: WhatsApp sender service is not paired or not running

**Solution**:
```bash
# Check if service is running
ps aux | grep whatsapp-sender

# If not running, start it
cd ~/whatsapp-sender
nohup ./whatsapp-sender > whatsapp-sender.log 2>&1 &

# Check pairing status
tail -30 whatsapp-sender.log

# If it says "Device not logged in", pair the phone (see Step 4)
```

### Issue 2: Service Not Running

**Symptom**: curl http://localhost:8081/health returns connection refused

**Solution**:
```bash
cd ~/whatsapp-sender
nohup ./whatsapp-sender > whatsapp-sender.log 2>&1 &
tail -20 whatsapp-sender.log
```

### Issue 3: Session Expired

**Symptom**: Service was working but stopped sending messages

**Cause**: WhatsApp session expires after 14 days of phone being offline

**Solution**: Re-pair the phone using the new pairing code in the logs

### Issue 4: Port 8081 Already in Use

**Symptom**: Service won't start, log shows "address already in use"

**Solution**:
```bash
# Find process using port 8081
lsof -i :8081

# Kill old process
pkill -f whatsapp-sender

# Start service again
cd ~/whatsapp-sender
nohup ./whatsapp-sender > whatsapp-sender.log 2>&1 &
```

## Project WhatsApp Groups

The service sends to these WhatsApp groups based on project:

| Project | Group Name | Group JID |
|---------|-----------|-----------|
| Velo Test | Velo Test | 120363421664266245@g.us |
| Lawley | Lawley Activation 3 | 120363418298130331@g.us |
| Mohadin | Mohadin Activations 🥳 | 120363421532174586@g.us |
| Mamelodi | Mamelodi POP1 Activations | 120363408849234743@g.us |

**Note**: Group JIDs are configured in `/home/louis/apps/fibreflow/pages/api/wa-monitor-send-feedback.ts`

## Security Notes

1. **Phone Access**: Only authorized personnel should have access to phone +27 71 155 8396
2. **Session Database**: The file `~/whatsapp-sender/store/whatsapp.db` contains the WhatsApp session - **DO NOT DELETE**
3. **Pairing Codes**: Expire after 10 minutes
4. **Service Logs**: Contain sensitive phone numbers - restrict access to logs

## Monitoring Best Practices

1. **Daily Health Check**:
   ```bash
   curl http://localhost:8081/health
   ```

2. **Weekly Log Review**:
   ```bash
   tail -100 ~/whatsapp-sender/whatsapp-sender.log
   ```

3. **Monthly Session Verification**:
   - Ensure phone is online and connected
   - Send test message via wa-monitor interface

## API Endpoints

### WhatsApp Sender Service (Port 8081)

**POST /send-message**
```json
{
  "group_jid": "120363421664266245@g.us",
  "recipient_jid": "27640412391@s.whatsapp.net",
  "message": "Feedback message with @mention"
}
```

**GET /health**
```json
{
  "status": "ok",
  "service": "whatsapp-sender",
  "connected": true
}
```

## Service Architecture

```
┌─────────────────────────────────────────────┐
│  Phone +27 71 155 8396                      │
│  (MUST BE PAIRED - Critical!)               │
└─────────────────┬───────────────────────────┘
                  │ WhatsApp Web Protocol
                  │
┌─────────────────▼───────────────────────────┐
│  WhatsApp Sender Service                    │
│  - Port: 8081                               │
│  - Location: ~/whatsapp-sender/             │
│  - Session: store/whatsapp.db               │
│  - Technology: Go + whatsmeow               │
└─────────────────┬───────────────────────────┘
                  │ HTTP API (localhost only)
                  │
┌─────────────────▼───────────────────────────┐
│  Next.js API Route                          │
│  /api/wa-monitor-send-feedback              │
│  - Formats QA feedback messages             │
│  - Adds @mentions                           │
│  - Maps projects to groups                  │
└─────────────────┬───────────────────────────┘
                  │ HTTPS
                  │
┌─────────────────▼───────────────────────────┐
│  Frontend: app.fibreflow.app/wa-monitor    │
│  - QA photo review interface                │
│  - "Send Feedback" button                   │
└─────────────────────────────────────────────┘
```

## Critical Files

| File | Location | Purpose |
|------|----------|---------|
| Binary | `~/whatsapp-sender/whatsapp-sender` | Compiled Go service |
| Source | `~/whatsapp-sender/whatsapp-sender.go` | Go source code |
| Session DB | `~/whatsapp-sender/store/whatsapp.db` | **CRITICAL** - WhatsApp session (DO NOT DELETE) |
| Logs | `~/whatsapp-sender/whatsapp-sender.log` | Service logs |
| API Route | `/home/louis/apps/fibreflow/pages/api/wa-monitor-send-feedback.ts` | Next.js API |

## Emergency Contacts

**If the service is down and feedback needs to be sent urgently:**
1. Manually send feedback via WhatsApp Business Web
2. Document which DRs need feedback sent
3. Contact server admin to restart WhatsApp sender service
4. Re-pair phone if session expired

## Appendix: Manual Message Format

If sending manually, use this format:

```
@27640412391

DR1234567
APPROVED

[OK] House Photo
[OK] Cable from Pole
[MISSING] Cable Entry Outside
[OK] Cable Entry Inside
...

Additional feedback here.
```

**Note**: The `@27640412391` mention must match the technician's WhatsApp number in the database.
