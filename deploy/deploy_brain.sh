#!/bin/bash
#
# Deploy Superior Brain Agent to Hostinger VPS
# Runs alongside Dual Agent on port 8001
#
# Usage: bash deploy_brain.sh
#

set -e

echo "🧠 Deploying Superior Brain Agent to VPS..."

# Configuration
VPS_IP="72.60.17.245"
VPS_USER="root"
VPS_PASS="VeloF@2025@@"
APP_DIR="/var/www/superior-brain"
DOMAIN="app.fibreflow.app"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_step() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC}  $1"
}

# Step 1: Create deployment package
print_step "Creating deployment package..."
cd /home/louisdup/Agents/claude

tar -czf /tmp/superior-brain-deploy.tar.gz \
    superior_agent_brain.py \
    memory/ \
    orchestrator/ \
    shared/ \
    deploy/brain_api.py \
    deploy/requirements_brain.txt \
    .env

print_success "Package created"

# Step 2: Upload to VPS
print_step "Uploading to VPS..."
sshpass -p "$VPS_PASS" scp -o StrictHostKeyChecking=no \
    /tmp/superior-brain-deploy.tar.gz \
    $VPS_USER@$VPS_IP:/tmp/

print_success "Upload complete"

# Step 3: Deploy on VPS
print_step "Deploying on VPS..."
sshpass -p "$VPS_PASS" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_IP << 'ENDSSH'

# Create directory
mkdir -p /var/www/superior-brain
cd /var/www/superior-brain

# Extract files
tar -xzf /tmp/superior-brain-deploy.tar.gz

# Move API to root
mv deploy/brain_api.py ./
mv deploy/requirements_brain.txt ./requirements.txt

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Set permissions
chown -R www-data:www-data /var/www/superior-brain
chmod -R 755 /var/www/superior-brain

echo "✅ Files deployed"

ENDSSH

print_success "Deployment complete"

# Step 4: Install Qdrant (if not already running)
print_step "Checking Qdrant..."
sshpass -p "$VPS_PASS" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_IP << 'ENDSSH'

if ! docker ps | grep -q qdrant; then
    echo "Installing Qdrant vector database..."
    docker run -d \
        --name qdrant \
        -p 6333:6333 \
        -p 6334:6334 \
        -v /var/lib/qdrant:/qdrant/storage \
        --restart unless-stopped \
        qdrant/qdrant

    echo "✅ Qdrant installed"
else
    echo "✅ Qdrant already running"
fi

ENDSSH

# Step 5: Create systemd service
print_step "Creating systemd service..."
sshpass -p "$VPS_PASS" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_IP << 'ENDSSH'

cat > /etc/systemd/system/superior-brain.service <<EOF
[Unit]
Description=Superior Brain AI Agent API
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/superior-brain
Environment="PATH=/var/www/superior-brain/venv/bin"
EnvironmentFile=/var/www/superior-brain/.env
ExecStart=/var/www/superior-brain/venv/bin/uvicorn brain_api:app --host 127.0.0.1 --port 8001 --workers 2
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
systemctl daemon-reload
systemctl enable superior-brain
systemctl start superior-brain

sleep 3

# Check status
systemctl status superior-brain --no-pager | head -15

ENDSSH

print_success "Service created and started"

# Step 6: Configure Nginx
print_step "Configuring Nginx routing..."
sshpass -p "$VPS_PASS" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_IP << 'ENDSSH'

# Backup existing config
cp /etc/nginx/sites-available/fibreflow /etc/nginx/sites-available/fibreflow.bak

# Add agent routes to Nginx config (before the main location block)
sed -i '/location \/ {/i\
    # Superior Brain Agent (Smart Mode)\
    location /api/agent/brain {\
        proxy_pass http://127.0.0.1:8001;\
        proxy_http_version 1.1;\
        proxy_set_header Upgrade $http_upgrade;\
        proxy_set_header Connection "upgrade";\
        proxy_set_header Host $host;\
        proxy_set_header X-Real-IP $remote_addr;\
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\
        proxy_set_header X-Forwarded-Proto $scheme;\
        proxy_connect_timeout 90s;\
        proxy_send_timeout 90s;\
        proxy_read_timeout 90s;\
\
        # CORS\
        add_header "Access-Control-Allow-Origin" "*" always;\
        add_header "Access-Control-Allow-Methods" "GET, POST, OPTIONS" always;\
        add_header "Access-Control-Allow-Headers" "*" always;\
    }\
\
    # Dual Database Agent (Quick Mode)\
    location /api/agent/quick {\
        proxy_pass http://127.0.0.1:8000;\
        proxy_http_version 1.1;\
        proxy_set_header Upgrade $http_upgrade;\
        proxy_set_header Connection "upgrade";\
        proxy_set_header Host $host;\
        proxy_set_header X-Real-IP $remote_addr;\
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\
        proxy_set_header X-Forwarded-Proto $scheme;\
        proxy_connect_timeout 60s;\
        proxy_send_timeout 60s;\
        proxy_read_timeout 60s;\
\
        # CORS\
        add_header "Access-Control-Allow-Origin" "*" always;\
        add_header "Access-Control-Allow-Methods" "GET, POST, OPTIONS" always;\
        add_header "Access-Control-Allow-Headers" "*" always;\
    }\
\
' /etc/nginx/sites-available/fibreflow

# Test and reload
nginx -t && systemctl reload nginx

echo "✅ Nginx configured"

ENDSSH

print_success "Nginx routing configured"

# Step 7: Test deployment
print_step "Testing deployment..."

echo ""
echo "Testing Dual Agent (Quick Mode):"
sshpass -p "$VPS_PASS" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_IP \
    "curl -s http://localhost:8000/health | head -5"

echo ""
echo "Testing Superior Brain (Smart Mode):"
sshpass -p "$VPS_PASS" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_IP \
    "curl -s http://localhost:8001/health | head -5"

echo ""
print_success "Deployment complete!"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🎉 Superior Brain Deployed Successfully!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📍 API Endpoints:"
echo "   Quick Mode:  https://$DOMAIN/api/agent/quick"
echo "   Brain Mode:  https://$DOMAIN/api/agent/brain"
echo ""
echo "🔍 Service Management:"
echo "   Dual Agent:     systemctl status neon-agent"
echo "   Superior Brain: systemctl status superior-brain"
echo "   Qdrant:         docker ps | grep qdrant"
echo ""
echo "📊 Test endpoints:"
echo "   curl https://$DOMAIN/api/agent/quick/health"
echo "   curl https://$DOMAIN/api/agent/brain/health"
echo ""
echo "📝 View logs:"
echo "   journalctl -u superior-brain -f"
echo ""
