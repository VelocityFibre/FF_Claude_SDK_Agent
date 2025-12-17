# WA DR Monitoring & Evaluation System - Quick Start Guide

## 🚀 Quick Setup

The system is ready to monitor new DR submissions from the wa-monitor workflow, evaluate images, and provide WhatsApp feedback.

## System Components

### 1. **Monitoring Script** (`wa_dr_monitor.py`)
- Polls for new DR submissions every 30 seconds
- Automatically evaluates new DRs
- Prepares WhatsApp feedback messages
- Logs all activity

### 2. **Direct Evaluation Script** (`evaluate_dr.py`)
- Evaluate specific DR numbers on demand
- Get formatted WhatsApp feedback
- Save results to JSON

### 3. **Human Approval Interface** (`wa_approval_interface.html`)
- Web interface for reviewing evaluations
- Edit feedback messages before sending
- Approve/reject evaluations

## 🔴 IMPORTANT: Current Issue

The VLM (Vision Language Model) API is timing out when evaluating images. This needs to be resolved on the server side. The evaluation endpoint exists but the image processing service appears to be down or misconfigured.

## How to Use

### Option 1: Monitor for New DRs (Automated)

```bash
# Start the monitoring service
./venv/bin/python3 wa_dr_monitor.py
```

This will:
- Check for new DRs every 30 seconds
- Evaluate any new submissions
- Generate WhatsApp feedback
- Log everything to `wa_dr_monitor.log`

### Option 2: Evaluate Specific DR (Manual)

```bash
# Evaluate a specific DR number
./venv/bin/python3 evaluate_dr.py DR1730550
```

This will:
- Evaluate the specified DR
- Display results in terminal
- Save to `evaluation_DR1730550.json`

### Option 3: Web Interface (Human Review)

```bash
# Open the approval interface
firefox wa_approval_interface.html
# or
google-chrome wa_approval_interface.html
```

Then:
1. Enter DR number in the input field
2. Click "Evaluate"
3. Review the evaluation results
4. Edit the WhatsApp message if needed
5. Click "Approve & Send" to send feedback

## API Endpoints (VF Server)

The system uses these endpoints on the velo-server (100.96.203.105:3005):

- `POST /api/foto/evaluate` - Evaluate a DR's images
- `GET /api/foto/evaluation/{dr_number}` - Get evaluation results
- `POST /api/foto/feedback` - Mark feedback as sent
- `GET /api/foto/photos` - Get all DRs with photos

**Note**: These APIs work locally on the server but external access appears restricted.

## Sample WhatsApp Feedback Format

```
✅ *QA PASSED*
DR: DR1730550

📊 Overall Score: 8/10
✔️ Steps Passed: 14/16

*Detailed Results:*
✓ Site Preparation: 9/10
✓ Cable Installation: 8/10
✗ Termination Quality: 5/10
  ↳ Poor cable management
  ↳ Labels missing
✓ Testing Results: 7/10

*Recommendations:*
⚠️ Please review and address the noted issues.
```

## Troubleshooting

### Issue: VLM API Timeout
**Problem**: "VLM API request timed out after 3 minutes"
**Solution**: The image evaluation service needs to be running on the VF server. Contact server admin to restart the VLM service.

### Issue: Cannot Connect to Server
**Problem**: Connection refused or timeout
**Solution**:
1. Check VPN/Tailscale connection
2. Verify server is running: `ping 100.96.203.105`
3. Check credentials in `.env` file

### Issue: API Returns 404
**Problem**: API endpoints not found
**Solution**: APIs only work locally on server. Use the provided scripts that execute via SSH.

## Environment Variables

Ensure these are set in your `.env` file:

```bash
VF_SERVER_HOST=100.96.203.105
VF_SERVER_USER=louis
VF_SERVER_PASSWORD=VeloAdmin2025!
```

## Next Steps

1. **Fix VLM Service**: The image evaluation service needs to be operational on the server
2. **WhatsApp Integration**: Connect to actual WhatsApp Business API for sending feedback
3. **Database Integration**: Store evaluations in database for historical tracking
4. **Auto-Approval Rules**: Set thresholds for automatic approval of high-scoring evaluations

## Support

For issues or questions:
- Check logs: `tail -f wa_dr_monitor.log`
- Test connectivity: `ping 100.96.203.105`
- Verify API: `./venv/bin/python3 evaluate_dr.py DR1730550`

## Architecture Diagram

```
WhatsApp Submissions → wa-monitor → New DR
                                      ↓
                              wa_dr_monitor.py
                                      ↓
                            Evaluation API (foto/evaluate)
                                      ↓
                              Image Analysis (VLM)
                                      ↓
                           Human Review (wa_approval_interface.html)
                                      ↓
                            WhatsApp Feedback
```

## Quick Test

To quickly test if everything is working:

```bash
# Test evaluation (will show VLM timeout currently)
./venv/bin/python3 evaluate_dr.py DR1730550

# Start monitoring
./venv/bin/python3 wa_dr_monitor.py

# Open web interface
firefox wa_approval_interface.html
```

The system is ready but needs the VLM service to be operational for actual image evaluation.