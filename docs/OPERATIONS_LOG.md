# Operations Log

This log tracks operational changes, deployments, migrations, incidents, and system modifications to FibreFlow infrastructure.

**Purpose**: Historical record of who did what, when, and why. Critical for:
- Incident investigation and root cause analysis
- Change tracking and rollback procedures
- Knowledge transfer and onboarding
- Compliance and audit trails

**Format**: Newest entries first (reverse chronological)

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
