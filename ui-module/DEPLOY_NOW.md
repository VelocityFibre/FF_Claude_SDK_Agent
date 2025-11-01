# Deploy to Your Hostinger VPS NOW

**One-command deployment for srv1092611.hstgr.cloud**

---

## 🚀 Super Quick Deploy (5 Minutes)

### Step 1: Package Everything (On This Machine)

```bash
cd /home/louisdup/Agents/claude

# Create deployment package
tar -czf neon-agent-deploy.tar.gz \
    ui-module/agent_api.py \
    ui-module/neon_agent.py \
    ui-module/requirements.txt \
    ui-module/.env \
    ui-module/hostinger-deploy.sh \
    ui-module/Procfile

# Package created!
ls -lh neon-agent-deploy.tar.gz
```

### Step 2: Upload to VPS

```bash
# Upload the package
scp neon-agent-deploy.tar.gz root@72.60.17.245:/tmp/

# Should take ~5 seconds (files are small)
```

### Step 3: SSH and Deploy

```bash
# SSH into your VPS
ssh root@72.60.17.245

# Once connected, run these commands:
cd /tmp
mkdir -p neon-agent
tar -xzf neon-agent-deploy.tar.gz -C neon-agent --strip-components=1

# Edit deployment script with your domain (or use IP)
nano neon-agent/hostinger-deploy.sh
# Change line 17: DOMAIN="72.60.17.245"  # or your domain

# Run deployment
chmod +x neon-agent/hostinger-deploy.sh
sudo bash neon-agent/hostinger-deploy.sh
```

**That's it!** The script will:
- Install Python, Nginx, SSL tools
- Create systemd service
- Configure Nginx
- Start the API
- Set up auto-restart

### Step 4: Test It

```bash
# While still SSH'd into VPS
curl http://localhost:8000/health

# From your local machine
curl http://72.60.17.245/health

# Should return:
# {"status":"healthy","database":"connected","agent":"ready",...}
```

---

## 🎯 Alternative: Copy-Paste Deployment

If you don't want to use the automated script, here are the exact commands:

### On Your VPS:

```bash
# 1. Install dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv nginx

# 2. Create app directory
sudo mkdir -p /var/www/neon-agent
cd /var/www/neon-agent

# 3. Upload files (you'll do this via SCP)
# Files needed: agent_api.py, neon_agent.py, requirements.txt, .env

# 4. Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Test it works
uvicorn agent_api:app --host 127.0.0.1 --port 8000 &
curl http://localhost:8000/health
# Kill test server: pkill -f uvicorn

# 6. Create systemd service
sudo nano /etc/systemd/system/neon-agent.service
```

Paste this:
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

Save and continue:
```bash
# 7. Set permissions
sudo chown -R www-data:www-data /var/www/neon-agent

# 8. Start service
sudo systemctl daemon-reload
sudo systemctl enable neon-agent
sudo systemctl start neon-agent
sudo systemctl status neon-agent

# 9. Configure Nginx
sudo nano /etc/nginx/sites-available/neon-agent
```

Paste this:
```nginx
server {
    listen 80;
    server_name 72.60.17.245 srv1092611.hstgr.cloud;

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

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

Save and continue:
```bash
# 10. Enable site and restart Nginx
sudo ln -s /etc/nginx/sites-available/neon-agent /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 11. Open firewall
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 12. Test from outside
curl http://72.60.17.245/health
```

---

## 📦 What to Upload

Make sure these files are in `/var/www/neon-agent`:

```
/var/www/neon-agent/
├── agent_api.py
├── neon_agent.py
├── requirements.txt
└── .env
```

Your `.env` file should contain:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
NEON_DATABASE_URL=postgresql://username:password@host/dbname?sslmode=require&channel_binding=require
ALLOWED_ORIGINS=*
PORT=8000
DEBUG=False
```

> **Note**: Get actual credentials from team lead or .env file backup

---

## 🎯 After Deployment

Your API will be accessible at:
```
http://72.60.17.245/
http://72.60.17.245/health
http://72.60.17.245/docs
http://srv1092611.hstgr.cloud/
```

Update your Next.js frontend:
```bash
# In VF/Apps/FF_React/.env.local
AGENT_BACKEND_URL=http://72.60.17.245
```

---

## 🔒 Optional: Add Domain and SSL

If you have a domain (e.g., `api.yourcompany.com`):

```bash
# 1. Point domain to VPS
# In your DNS: api.yourcompany.com → A record → 72.60.17.245

# 2. Install SSL certificate
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d api.yourcompany.com

# 3. Update frontend
AGENT_BACKEND_URL=https://api.yourcompany.com
```

---

## 🐛 Troubleshooting

**Check service status:**
```bash
sudo systemctl status neon-agent
```

**View logs:**
```bash
sudo journalctl -u neon-agent -f
```

**Restart service:**
```bash
sudo systemctl restart neon-agent
```

**Check if port is listening:**
```bash
sudo lsof -i :8000
```

**Test database connection from VPS:**
```bash
psql "postgresql://neondb_owner:npg_aRNLhZc1G2CD@ep-dry-night-a9qyh4sj-pooler.gwc.azure.neon.tech/neondb?sslmode=require"
```

---

## ✅ Success Checklist

- [ ] Package created: `neon-agent-deploy.tar.gz`
- [ ] Uploaded to VPS: `/tmp/neon-agent-deploy.tar.gz`
- [ ] Extracted files: `/var/www/neon-agent/`
- [ ] Virtual env created: `venv/`
- [ ] Dependencies installed: `requirements.txt`
- [ ] Service running: `systemctl status neon-agent`
- [ ] Nginx configured: `/etc/nginx/sites-available/neon-agent`
- [ ] Health check works: `curl http://72.60.17.245/health`
- [ ] Frontend updated: `AGENT_BACKEND_URL`

---

**Ready to deploy?** Follow Step 1-3 above!

Need help? I'm here to troubleshoot any issues.
