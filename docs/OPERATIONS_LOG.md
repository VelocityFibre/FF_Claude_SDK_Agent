# Operations Log

This log tracks operational changes, deployments, migrations, incidents, and system modifications to FibreFlow infrastructure.

**Purpose**: Historical record of who did what, when, and why. Critical for:
- Incident investigation and root cause analysis
- Change tracking and rollback procedures
- Knowledge transfer and onboarding
- Compliance and audit trails

**Format**: Newest entries first (reverse chronological)

---

## 2025-12-18

### 12:18 UTC - VF Server: Cloudflare Tunnel Setup for Public APK Downloads

**Type**: Infrastructure Setup / Public Access Enablement
**Severity**: Low (additive change, no downtime)
**Status**: ✅ Complete (pending DNS propagation 1-4 hours)
**Operator**: Claude Code + Louis

**Change**:
Set up Cloudflare Tunnel to enable public access to VF server download page without port forwarding or VPN requirements.

**Problem Statement**:
- VF Server (100.96.203.105) behind NAT router, port 80/443 not accessible from internet
- Field agents needed simple public URL to download Image Eval APK
- Tailscale VPN required for current access (too complex for field users)
- Port forwarding would expose server directly to internet (security concern)

**Solution**:
Implemented Cloudflare Tunnel (Zero Trust architecture) to create secure public access without opening router ports.

**Procedure**:

1. **Installed cloudflared on VF server**:
   ```bash
   wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
   chmod +x cloudflared
   mv cloudflared ~/cloudflared
   ```

2. **Migrated domain to Cloudflare**:
   - Added `fibreflow.app` to Cloudflare account
   - Updated nameservers at Xneelo registrar:
     - Old: `ns1.host-h.net`, `ns2.dns-h.com`
     - New: `anton.ns.cloudflare.com`, `haley.ns.cloudflare.com`

3. **Authenticated cloudflared**:
   ```bash
   ~/cloudflared tunnel login
   # Authorized via browser at dash.cloudflare.com
   ```

4. **Created named tunnel**:
   ```bash
   ~/cloudflared tunnel create vf-downloads
   # Tunnel ID: 0bf9e4fa-f650-498c-bd23-def05abe5aaf
   # Credentials: ~/.cloudflared/0bf9e4fa-f650-498c-bd23-def05abe5aaf.json
   ```

5. **Configured tunnel routing**:
   ```yaml
   # ~/.cloudflared/config.yml
   tunnel: 0bf9e4fa-f650-498c-bd23-def05abe5aaf
   credentials-file: /home/louis/.cloudflared/0bf9e4fa-f650-498c-bd23-def05abe5aaf.json
   ingress:
     - hostname: vf.fibreflow.app
       service: http://localhost:80
     - service: http_status:404
   ```

6. **Set up DNS routing**:
   ```bash
   ~/cloudflared tunnel route dns vf-downloads vf.fibreflow.app
   # Created CNAME: vf.fibreflow.app → 0bf9e4fa-f650-498c-bd23-def05abe5aaf.cfargotunnel.com
   ```

7. **Updated nginx configuration**:
   ```nginx
   # /etc/nginx/sites-available/vf-fibreflow
   server {
       listen 80;
       server_name _;  # Accept all hostnames (was: vf.fibreflow.app)
       location / {
           proxy_pass http://localhost:3005;
           # ... proxy headers
       }
   }
   ```

8. **Started tunnel**:
   ```bash
   nohup ~/cloudflared tunnel run vf-downloads > /tmp/cloudflared-named.log 2>&1 &
   # Registered 4 tunnel connections (dur01, cpt02 locations)
   ```

**DNS Records Added to Cloudflare**:
- `app.fibreflow.app` → 72.60.17.245 (Hostinger VPS)
- `fibreflow.app` → 216.150.1.1 (Root domain)
- `vf.fibreflow.app` → 0bf9e4fa-f650-498c-bd23-def05abe5aaf.cfargotunnel.com (Tunnel CNAME)

**Verification**:
```bash
# Tunnel status
ps aux | grep "cloudflared tunnel run"  # ✅ Running (PID 104776)
tail -f /tmp/cloudflared-named.log      # ✅ 4 connections registered

# DNS check (will show Cloudflare IPs after propagation)
dig vf.fibreflow.app +short             # Currently: 100.96.203.105 (old)
dig NS fibreflow.app +short             # Currently: ns1.host-h.net (propagating)

# Test URLs
curl https://vf.fibreflow.app/downloads # Pending nameserver propagation
curl http://velo-server.tailce437e.ts.net/downloads  # ✅ Works via Tailscale
```

**Public URLs** (post-propagation):
- Download page: `https://vf.fibreflow.app/downloads`
- Direct APK: `https://vf.fibreflow.app/veloqa-imageeval-v1.2.0.apk`

**Temporary Access**:
- Tailscale users: `http://velo-server.tailce437e.ts.net/downloads`

**Impact**:
- ✅ Field agents can download APKs via simple HTTPS URL (no VPN needed)
- ✅ Automatic HTTPS with Cloudflare certificate
- ✅ DDoS protection and CDN caching included
- ✅ No router configuration or port forwarding required
- ✅ VF server remains protected behind NAT

**Rollback Procedure**:
```bash
# Stop tunnel
pkill cloudflared

# Revert nameservers at Xneelo to:
ns1.host-h.net, ns2.dns-h.com, ns1.dns-h.com, ns2.host-h.net

# Remove DNS records from Cloudflare
# Remove tunnel: cloudflared tunnel delete vf-downloads
```

**Next Steps**:
- Monitor DNS propagation (check in 2-4 hours)
- Set up systemd service for tunnel auto-start on reboot
- Test public URL from external network once DNS propagates
- Share URL with field agents

**Files Modified**:
- `/etc/nginx/sites-available/vf-fibreflow` - Updated server_name to accept all hosts
- `/home/louis/.cloudflared/config.yml` - Tunnel configuration (new)
- `/home/louis/.cloudflared/*.json` - Tunnel credentials (new)

**Architecture**:
```
Field Agent → Internet → Cloudflare → Tunnel (outbound conn) → VF Server nginx → Next.js
```

---

## 2025-12-17

### 20:40 UTC - VF Server: FibreFlow Application Migration

**Type**: Infrastructure Migration
**Severity**: Medium (requires rebuild, ~30min downtime on dev server)
**Status**: ✅ Complete
**Operator**: Claude Code + Louis

**Change**:
Moved FibreFlow Next.js application from `/home/louis/apps/fibreflow/` to `/srv/data/apps/fibreflow/`

**Reason**:
- Utilize faster NVMe storage (`/srv/data/` on nvme1n1p1 vs root partition)
- Standardize production paths for better organization
- Separate data from home directory

**Procedure**:
1. Stopped services: Next.js (PID 671485), Python proxy (PID 672756)
2. Created target directory: `/srv/data/apps/fibreflow/` with `louis:louis` ownership
3. Copied files: 2.7GB via rsync (157 files/directories)
4. Updated configuration: `ecosystem.config.js` path from old to new location
5. Rebuilt Next.js: Production build from new location (required due to hardcoded paths)
6. Restarted services:
   - Next.js: PID 731865, port 3005, working dir `/srv/data/apps/fibreflow`
   - Python proxy: PID 715099, port 8080, forwarding to 3005
7. Backed up old directory: Renamed to `fibreflow.OLD_20251217`

**Verification**:
```bash
# Service status
ps aux | grep -E "(next-server|simple-proxy)"
# Ports listening
ss -tlnp | grep -E ":(3005|8080)"
# HTTP test
curl http://localhost:3005/  # ✅ FibreFlow homepage
curl http://localhost:8080/  # ✅ Proxy working
# Working directory
pwdx 731865  # /srv/data/apps/fibreflow ✅
```

**Impact**:
- ✅ No production impact (Hostinger VPS unaffected)
- ✅ Dev/internal VF server operational
- ⚠️ ~30 minutes downtime during migration
- ℹ️ Old directory still exists (2.7GB) - can delete after verification period

**Rollback Procedure** (if needed):
```bash
# Stop services
pkill -f "next-server" && pkill -f "simple-proxy"
# Restore old directory
mv /home/louis/apps/fibreflow.OLD_20251217 /home/louis/apps/fibreflow
# Update config
sed -i 's|/srv/data/apps/fibreflow|/home/louis/apps/fibreflow|g' \
  /home/louis/apps/fibreflow/ecosystem.config.js
# Restart
cd /home/louis/apps/fibreflow
NODE_ENV=production node node_modules/next/dist/bin/next start -p 3005 -H 0.0.0.0 &
cd /home/louis && python3 simple-proxy.py &
```

**Documentation Updated**:
- CHANGELOG.md - Added infrastructure change entry
- CLAUDE.md - Updated VF Server paths (pending)
- .claude/skills/vf-server/README.md - Updated installation paths (pending)

**Lessons Learned**:
- Next.js embeds absolute paths in build artifacts - always rebuild after moving
- Background commands via SSH require proper redirection (`</dev/null >/tmp/log 2>&1 &`)
- Permission issues with `/srv/data/apps/` (root owned) - needed sudo for mkdir

**Related Issues**: None
**Follow-up Actions**:
- [ ] Monitor for 48 hours for any path-related issues
- [ ] Delete old directory after verification: `rm -rf /home/louis/apps/fibreflow.OLD_20251217`
- [ ] Update documentation with new standard paths

---

## 2025-12-16

### 15:00 UTC - Repository Reorganization Complete

**Type**: Code Restructure
**Severity**: Low (no infrastructure changes)
**Status**: ✅ Complete
**Operator**: Claude Code + Louis

**Change**:
- Moved all guides to `docs/guides/`
- Moved architecture docs to `docs/architecture/`
- Created skills in `.claude/skills/`
- Removed hardcoded secrets

**Impact**: Developer experience improvement, no service downtime

**Documentation Updated**:
- README.md
- CLAUDE.md
- NEW_STRUCTURE_GUIDE.md

---

## Template for New Entries

```markdown
## YYYY-MM-DD

### HH:MM UTC - Short Title

**Type**: [Deployment|Migration|Incident|Configuration|Maintenance|Security]
**Severity**: [Critical|High|Medium|Low]
**Status**: [✅ Complete|⚠️ In Progress|❌ Failed|🔄 Rolled Back]
**Operator**: [Who performed this change]

**Change**:
[What was changed - be specific]

**Reason**:
[Why this change was necessary]

**Procedure**:
1. Step 1
2. Step 2
...

**Verification**:
[How you verified it worked]

**Impact**:
- ✅ Expected impact 1
- ⚠️ Known issue or limitation
- ℹ️ Additional notes

**Rollback Procedure** (if applicable):
[Exact steps to undo this change]

**Documentation Updated**:
- File 1 - What changed
- File 2 - What changed

**Lessons Learned**:
[What you learned for next time]

**Related Issues**: [Link to GitHub issues, tickets, etc.]
**Follow-up Actions**:
- [ ] TODO 1
- [ ] TODO 2
```

---

## Operations Log Best Practices

### When to Log

**ALWAYS log**:
- ✅ Infrastructure changes (server moves, disk changes, network config)
- ✅ Deployments to production or staging
- ✅ Security incidents or patches
- ✅ Database migrations or schema changes
- ✅ Service outages or incidents
- ✅ Configuration changes affecting multiple systems
- ✅ Access/permission changes

**Sometimes log** (use judgment):
- ⚠️ Minor bug fixes deployed
- ⚠️ Documentation updates
- ⚠️ Development environment changes

**Don't log**:
- ❌ Code commits (use git log)
- ❌ Feature development (use CHANGELOG.md)
- ❌ Personal dev environment tweaks
- ❌ Test runs

### Severity Levels

- **Critical**: Production down, data loss risk, security breach
- **High**: Production degraded, major feature broken, security vulnerability
- **Medium**: Development/staging changes, non-critical service impact
- **Low**: Documentation, minor config changes, improvements

### Retention Policy

- **Critical/High**: Keep forever (compliance, legal)
- **Medium**: Keep 2 years minimum
- **Low**: Keep 1 year minimum

After retention period, archive to `docs/archive/operations-log-YYYY.md`

---

**See also**:
- `CHANGELOG.md` - Feature changes and version history
- `docs/DECISION_LOG.md` - Architectural decisions and trade-offs
- `git log` - Code-level changes
