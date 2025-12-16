#!/bin/bash
# setup_github.sh - Quick GitHub integration setup for FibreFlow

set -e  # Exit on any error

echo "🚀 FibreFlow GitHub Integration Setup"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git is not installed. Please install git first.${NC}"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "CLAUDE.md" ]; then
    echo -e "${RED}❌ Please run this script from the FibreFlow root directory${NC}"
    exit 1
fi

# Get GitHub details
echo -e "${YELLOW}📝 Please provide your GitHub details:${NC}"
read -p "GitHub username: " GITHUB_USER
read -p "Repository name (default: fibreflow-agents): " REPO_NAME
REPO_NAME=${REPO_NAME:-fibreflow-agents}

echo ""
echo -e "${GREEN}Setting up Git repository...${NC}"

# Initialize git if not already initialized
if [ ! -d .git ]; then
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Create comprehensive .gitignore if it doesn't exist
if [ ! -f .gitignore ]; then
    cat > .gitignore << 'EOF'
# Environment files
.env
.env.*
!.env.example

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
venv/
env/
.Python
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Logs
*.log
logs/
*.pid

# Secrets
*.pem
*.key
*.crt
credentials/
secrets/

# Database
*.db
*.sqlite
*.sqlite3

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# Node (for Convex)
node_modules/
npm-debug.log
yarn-error.log

# Convex
.convex/

# Deployment
deploy/*.tar.gz
deploy/backup/

# Memory systems
memory/*.db
memory/backups/
EOF
    echo "✅ Created .gitignore"
else
    echo "✅ .gitignore already exists"
fi

# Check for sensitive files
echo -e "${YELLOW}🔍 Checking for sensitive files...${NC}"
if [ -f .env ]; then
    if grep -q "ANTHROPIC_API_KEY\|DATABASE_URL\|NEON_DATABASE_URL" .env 2>/dev/null; then
        echo -e "${YELLOW}⚠️  Found .env with sensitive data - this will NOT be committed${NC}"
    fi
fi

# Create initial commit if no commits exist
if ! git log -1 &> /dev/null; then
    echo -e "${GREEN}📦 Creating initial commit...${NC}"
    git add .
    git commit -m "Initial commit: FibreFlow Agent Workforce System" || true
    echo "✅ Initial commit created"
else
    echo "✅ Repository already has commits"
fi

# Setup remote
echo -e "${GREEN}🔗 Setting up GitHub remote...${NC}"
if git remote | grep -q origin; then
    echo "Remote 'origin' already exists. Current URL:"
    git remote get-url origin
    read -p "Do you want to update it? (y/n): " UPDATE_REMOTE
    if [ "$UPDATE_REMOTE" = "y" ]; then
        git remote set-url origin "https://github.com/${GITHUB_USER}/${REPO_NAME}.git"
        echo "✅ Remote updated"
    fi
else
    git remote add origin "https://github.com/${GITHUB_USER}/${REPO_NAME}.git"
    echo "✅ Remote added"
fi

# Create deployment script
echo -e "${GREEN}📝 Creating deployment script...${NC}"
cat > deploy.sh << 'EOF'
#!/bin/bash
# deploy.sh - Deploy FibreFlow to production VPS

set -e

# Configuration
VPS_HOST="72.60.17.245"
VPS_USER="louisdup"
VPS_PATH="/home/louisdup/agents"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "🚀 Deploying FibreFlow to production..."

# Check if message provided
if [ -z "$1" ]; then
    echo -e "${RED}❌ Please provide a commit message${NC}"
    echo "Usage: ./deploy.sh 'your commit message'"
    exit 1
fi

# Run tests
echo "📋 Running tests..."
if [ -d venv ]; then
    source venv/bin/activate
fi
pytest tests/ -q || {
    echo -e "${RED}❌ Tests failed! Fix them before deploying.${NC}"
    exit 1
}

# Commit and push
echo "📤 Pushing to GitHub..."
git add .
git commit -m "$1" || echo "No changes to commit"
git push origin main || {
    echo -e "${RED}❌ Failed to push. Check your GitHub setup.${NC}"
    exit 1
}

# Deploy to VPS
echo "🔄 Deploying to VPS..."
ssh ${VPS_USER}@${VPS_HOST} << 'ENDSSH'
cd /home/louisdup/agents
git pull origin main
source venv/bin/activate
pip install -r requirements.txt --quiet
sudo systemctl restart fibreflow-api || echo "Service restart failed - may need manual intervention"
echo "✅ Deployment complete on VPS!"
ENDSSH

# Verify deployment
echo "🔍 Verifying deployment..."
sleep 2
curl -s http://${VPS_HOST}/health || echo "Health check failed - service may still be starting"

echo -e "${GREEN}✅ Deployment complete!${NC}"
EOF
chmod +x deploy.sh
echo "✅ Created deploy.sh"

# Create rollback script
cat > rollback.sh << 'EOF'
#!/bin/bash
# rollback.sh - Quick rollback to previous version

VPS_HOST="72.60.17.245"
VPS_USER="louisdup"

echo "🔄 Rolling back to previous version..."

ssh ${VPS_USER}@${VPS_HOST} << 'ENDSSH'
cd /home/louisdup/agents
echo "Current version:"
git log -1 --oneline
echo ""
echo "Rolling back..."
git reset --hard HEAD~1
sudo systemctl restart fibreflow-api
echo "Rolled back to:"
git log -1 --oneline
ENDSSH

echo "✅ Rollback complete!"
EOF
chmod +x rollback.sh
echo "✅ Created rollback.sh"

# Setup VPS instructions
echo ""
echo -e "${GREEN}✨ Local setup complete!${NC}"
echo ""
echo -e "${YELLOW}📋 Next steps:${NC}"
echo ""
echo "1. Create repository on GitHub:"
echo "   ${GREEN}https://github.com/new${NC}"
echo "   Repository name: ${REPO_NAME}"
echo "   Make it private if it contains sensitive business logic"
echo ""
echo "2. Push to GitHub:"
echo "   ${GREEN}git branch -M main${NC}"
echo "   ${GREEN}git push -u origin main${NC}"
echo ""
echo "3. Setup VPS for pulling (run these commands on VPS):"
echo "   ${GREEN}ssh ${VPS_USER}@72.60.17.245${NC}"
echo "   ${GREEN}cd /home/${VPS_USER}${NC}"
echo "   ${GREEN}mv agents agents_backup  # Backup current${NC}"
echo "   ${GREEN}git clone https://github.com/${GITHUB_USER}/${REPO_NAME}.git agents${NC}"
echo "   ${GREEN}cd agents${NC}"
echo "   ${GREEN}python3 -m venv venv${NC}"
echo "   ${GREEN}source venv/bin/activate${NC}"
echo "   ${GREEN}pip install -r requirements.txt${NC}"
echo "   ${GREEN}cp ../agents_backup/.env .env  # Restore env${NC}"
echo ""
echo "4. Test deployment:"
echo "   ${GREEN}./deploy.sh 'test: Initial deployment'${NC}"
echo ""
echo -e "${GREEN}🎉 Setup complete! You now have:${NC}"
echo "   ✅ Version control with Git"
echo "   ✅ GitHub backup and collaboration"
echo "   ✅ One-command deployment (./deploy.sh)"
echo "   ✅ Quick rollback capability (./rollback.sh)"
echo "   ✅ Professional development workflow"