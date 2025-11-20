# Hostinger VPS Deployment Guide

**Deploy your Neon Agent API to Hostinger VPS**

---

## 🎯 What You'll Get

- Backend running on your Hostinger VPS
- Nginx reverse proxy
- SSL certificate (HTTPS)
- Systemd service (auto-restart)
- Full control over your infrastructure

---

## 📋 Prerequisites

### On Hostinger VPS:
- Ubuntu 20.04 or 22.04 (or similar)
- Root or sudo access
- At least 1GB RAM
- Python 3.8+

### DNS Setup:
- Domain pointed to your VPS IP (A record)
- Example: `api.yourcompany.com` → `your.vps.ip`

### Files to Upload:
- `agent_api.py`
- `neon_agent.py`
- `requirements.txt`
- `.env` (with your keys)
- `hostinger-deploy.sh` (deployment script)

---

## 🚀 Quick Deployment (Automated)

### Step 1: Upload Files to VPS

```bash
# On your local machine
cd /home/louisdup/Agents/claude/ui-module

# Create deployment package
tar -czf neon-agent.tar.gz \
    agent_api.py \
    neon_agent.py \
    requirements.txt \
    .env \
    hostinger-deploy.sh

# Upload to VPS (replace with your details)
scp neon-agent.tar.gz root@your-vps-ip:/tmp/

# SSH into VPS
ssh root@your-vps-ip
```

### Step 2: Extract and Deploy

```bash
# On VPS
cd /tmp
tar -xzf neon-agent.tar.gz -C /tmp/neon-agent

# Update deployment script with your domain
nano /tmp/neon-agent/hostinger-deploy.sh
# Change: DOMAIN="your-domain.com"

# Run deployment
chmod +x /tmp/neon-agent/hostinger-deploy.sh
sudo bash /tmp/neon-agent/hostinger-deploy.sh
```

The script will:
1. Install dependencies
2. Create virtual environment
3. Set up systemd service
4. Configure Nginx
5. Install SSL certificate
6. Start the service

### Step 3: Test It

```bash
# Check service status
systemctl status neon-agent

# Test health endpoint
curl http://localhost:8000/health

# Test from outside
curl https://api.yourcompany.com/health
```

---

## 🛠️ Manual Deployment (Step-by-Step)

If you prefer to understand each step:

### 1. Install System Dependencies

```bash
sudo apt-get update
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    nginx \
    certbot \
    python3-certbot-nginx \
    postgresql-client
```

### 2. Create Application Directory

```bash
sudo mkdir -p /var/www/neon-agent
cd /var/www/neon-agent
```

### 3. Upload Your Files

```bash
# Option A: SCP (from local machine)
scp agent_api.py neon_agent.py requirements.txt .env root@your-vps:/var/www/neon-agent/

# Option B: Git
git clone your-private-repo .

# Option C: Manual upload via SFTP
# Use FileZilla or similar
```

### 4. Create Virtual Environment

```bash
cd /var/www/neon-agent
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Environment Variables

```bash
nano .env
```

Add:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-xxx...
NEON_DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
ALLOWED_ORIGINS=https://your-frontend.com
PORT=8000
DEBUG=False
AGENT_API_KEY=your-random-secret-key
```

### 6. Test Locally First

```bash
# Activate venv
source venv/bin/activate

# Run server
uvicorn agent_api:app --host 127.0.0.1 --port 8000

# In another terminal, test
curl http://localhost:8000/health

# If works, stop with Ctrl+C
```

### 7. Create Systemd Service

```bash
sudo nano /etc/systemd/system/neon-agent.service
```

Paste:
```ini
[Unit]
Description=Neon Database AI Agent API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/neon-agent
Environment="PATH=/var/www/neon-agent/venv/bin"
EnvironmentFile=/var/www/neon-agent/.env
ExecStart=/var/www/neon-agent/venv/bin/uvicorn agent_api:app --host 127.0.0.1 --port 8000 --workers 2
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable neon-agent
sudo systemctl start neon-agent
sudo systemctl status neon-agent
```

### 8. Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/neon-agent
```

Paste (replace `api.yourcompany.com`):
```nginx
server {
    listen 80;
    server_name api.yourcompany.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # CORS
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization' always;

        # Timeouts for AI
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/neon-agent /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 9. Set Up SSL Certificate

```bash
sudo certbot --nginx -d api.yourcompany.com
```

Follow prompts to install certificate.

### 10. Verify Deployment

```bash
# Check service
systemctl status neon-agent

# Check logs
journalctl -u neon-agent -f

# Test externally
curl https://api.yourcompany.com/health

# Should return:
# {"status":"healthy","database":"connected","agent":"ready",...}
```

---

## 🔒 Security Hardening

### 1. Set Up Firewall

```bash
# Allow SSH, HTTP, HTTPS
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 2. Restrict CORS

Update `.env`:
```bash
ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-domain.com
```

Restart:
```bash
sudo systemctl restart neon-agent
```

### 3. Enable API Key Auth

Generate key:
```bash
openssl rand -hex 32
```

Add to `.env`:
```bash
AGENT_API_KEY=generated-key-here
```

Add same key to Next.js frontend `.env.local`.

### 4. Set Up Log Rotation

```bash
sudo nano /etc/logrotate.d/neon-agent
```

```
/var/log/neon-agent/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload neon-agent > /dev/null 2>&1 || true
    endscript
}
```

---

## 📊 Monitoring

### View Logs

```bash
# Real-time logs
journalctl -u neon-agent -f

# Last 100 lines
journalctl -u neon-agent -n 100

# Errors only
journalctl -u neon-agent -p err

# Today's logs
journalctl -u neon-agent --since today
```

### Check Resource Usage

```bash
# CPU and memory
htop

# Disk usage
df -h

# Service status
systemctl status neon-agent
```

### Health Monitoring Script

Create `health-check.sh`:
```bash
#!/bin/bash
ENDPOINT="https://api.yourcompany.com/health"

if curl -f $ENDPOINT > /dev/null 2>&1; then
    echo "$(date): OK"
else
    echo "$(date): FAILED - restarting service"
    systemctl restart neon-agent
fi
```

Add to crontab:
```bash
# Run every 5 minutes
*/5 * * * * /root/health-check.sh >> /var/log/health-check.log 2>&1
```

---

## 🐛 Troubleshooting

### Service Won't Start

```bash
# Check logs
journalctl -u neon-agent -n 50

# Common issues:
# 1. Missing .env file
# 2. Wrong Python path
# 3. Port already in use

# Check port
sudo lsof -i :8000
```

### Database Connection Error

```bash
# Test connection from VPS
psql "postgresql://user:pass@host/db"

# If fails:
# 1. Check firewall on Neon
# 2. Verify connection string
# 3. Check SSL mode
```

### Nginx 502 Bad Gateway

```bash
# Check if backend is running
curl http://localhost:8000/health

# If not running:
sudo systemctl start neon-agent

# Check nginx error log
sudo tail -f /var/log/nginx/error.log
```

### SSL Certificate Issues

```bash
# Renew certificate
sudo certbot renew

# Test auto-renewal
sudo certbot renew --dry-run
```

---

## 🔄 Updates and Maintenance

### Update Code

```bash
cd /var/www/neon-agent

# Pull latest code
git pull  # or upload new files

# Restart service
sudo systemctl restart neon-agent
```

### Update Dependencies

```bash
cd /var/www/neon-agent
source venv/bin/activate
pip install --upgrade -r requirements.txt
sudo systemctl restart neon-agent
```

### Backup

```bash
# Backup .env file
cp .env .env.backup

# Backup entire directory
tar -czf neon-agent-backup-$(date +%Y%m%d).tar.gz /var/www/neon-agent
```

---

## 💰 Hostinger VPS Costs

**VPS Plan recommendations:**
- **VPS 1** ($4.99/month): Good for testing
- **VPS 2** ($5.99/month): Recommended for production
- **VPS 3** ($8.99/month): High traffic

**Total monthly cost:**
- VPS hosting: $5-9
- Anthropic API: $3-25 (usage-based)
- **Total: ~$10-35/month**

---

## ✅ Post-Deployment Checklist

- [ ] Service starts automatically: `systemctl is-enabled neon-agent`
- [ ] Health endpoint responds: `curl https://api.yourcompany.com/health`
- [ ] SSL certificate valid: Check in browser
- [ ] Logs are clean: `journalctl -u neon-agent -n 20`
- [ ] CORS configured: Test from frontend
- [ ] API key set: Check `.env`
- [ ] Firewall configured: `sudo ufw status`
- [ ] Auto-renewal enabled: `sudo certbot renew --dry-run`
- [ ] Backups scheduled: Check crontab
- [ ] Monitoring active: Health check running

---

## 🆘 Need Help?

**View logs:**
```bash
journalctl -u neon-agent -f
```

**Restart service:**
```bash
sudo systemctl restart neon-agent
```

**Check configuration:**
```bash
cat /etc/systemd/system/neon-agent.service
cat /etc/nginx/sites-available/neon-agent
cat /var/www/neon-agent/.env
```

---

## 🎉 Success!

Your Neon Agent API is now running on Hostinger VPS!

**API URL:** https://api.yourcompany.com

**Next steps:**
1. Update frontend `AGENT_BACKEND_URL` to your new domain
2. Test queries from your Next.js app
3. Monitor logs for first few hours
4. Set up backups and monitoring

---

*Last updated: 2025-11-01*
