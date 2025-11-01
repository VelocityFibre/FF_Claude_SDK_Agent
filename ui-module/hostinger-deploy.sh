#!/bin/bash
#
# Hostinger VPS Deployment Script for Neon Agent API
# Run this script after uploading files to your VPS
#
# Usage: bash hostinger-deploy.sh
#

set -e  # Exit on error

echo "🚀 Deploying Neon Agent API to Hostinger VPS..."

# Configuration
APP_DIR="/var/www/neon-agent"
APP_USER="www-data"
DOMAIN="your-domain.com"  # Update this!

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

# Step 1: Install system dependencies
print_step "Installing system dependencies..."
apt-get update
apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    nginx \
    certbot \
    python3-certbot-nginx \
    postgresql-client
print_success "Dependencies installed"

# Step 2: Create application directory
print_step "Setting up application directory..."
mkdir -p $APP_DIR
cd $APP_DIR

# Copy files (assumes you've uploaded them to /tmp/neon-agent)
if [ -d "/tmp/neon-agent" ]; then
    cp -r /tmp/neon-agent/* $APP_DIR/
    print_success "Files copied"
else
    echo "⚠️  No files found at /tmp/neon-agent"
    echo "Please upload your files first, then rerun this script"
    exit 1
fi

# Step 3: Create Python virtual environment
print_step "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
print_success "Virtual environment created and dependencies installed"

# Step 4: Set permissions
print_step "Setting permissions..."
chown -R $APP_USER:$APP_USER $APP_DIR
chmod -R 755 $APP_DIR
print_success "Permissions set"

# Step 5: Create systemd service
print_step "Creating systemd service..."
cat > /etc/systemd/system/neon-agent.service <<EOF
[Unit]
Description=Neon Database AI Agent API
After=network.target

[Service]
Type=simple
User=$APP_USER
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
EnvironmentFile=$APP_DIR/.env
ExecStart=$APP_DIR/venv/bin/uvicorn agent_api:app --host 127.0.0.1 --port 8000 --workers 2
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable neon-agent
systemctl start neon-agent
print_success "Systemd service created and started"

# Step 6: Configure Nginx
print_step "Configuring Nginx..."
cat > /etc/nginx/sites-available/neon-agent <<EOF
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        # CORS headers
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization' always;

        # Timeouts for AI processing
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
EOF

# Enable site
ln -sf /etc/nginx/sites-available/neon-agent /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
print_success "Nginx configured"

# Step 7: Set up SSL (optional but recommended)
print_step "Setting up SSL with Let's Encrypt..."
echo "⚠️  Make sure your domain points to this server before continuing!"
read -p "Continue with SSL setup? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN
    print_success "SSL certificate installed"
else
    echo "Skipping SSL setup. You can run this later with:"
    echo "  certbot --nginx -d $DOMAIN"
fi

# Step 8: Check status
print_step "Checking deployment status..."
echo ""
systemctl status neon-agent --no-pager | head -10
echo ""

# Test health endpoint
sleep 2
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    print_success "Health check passed!"
else
    echo "⚠️  Health check failed. Check logs:"
    echo "  journalctl -u neon-agent -f"
fi

# Final summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ Deployment Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📍 Your API is running at:"
echo "   http://$DOMAIN/"
echo "   http://$DOMAIN/health"
echo "   http://$DOMAIN/docs"
echo ""
echo "🔍 Useful commands:"
echo "   Check logs:   journalctl -u neon-agent -f"
echo "   Restart:      systemctl restart neon-agent"
echo "   Status:       systemctl status neon-agent"
echo "   Stop:         systemctl stop neon-agent"
echo ""
echo "🔐 Next steps:"
echo "   1. Update ALLOWED_ORIGINS in $APP_DIR/.env"
echo "   2. Set AGENT_API_KEY for security"
echo "   3. Test: curl http://$DOMAIN/health"
echo "   4. Update frontend AGENT_BACKEND_URL"
echo ""
