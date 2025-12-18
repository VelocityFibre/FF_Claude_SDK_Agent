# Changelog

All notable changes to the FibreFlow Agent Workforce project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastructure
- VF Server: Set up Cloudflare Tunnel for public APK downloads (2025-12-18)
  - Enabled: `https://vf.fibreflow.app/downloads` for field agent access
  - Method: Cloudflare Tunnel (no port forwarding required)
  - Domain: Migrated fibreflow.app nameservers to Cloudflare
  - Tunnel: Named tunnel `vf-downloads` (ID: 0bf9e4fa-f650-498c-bd23-def05abe5aaf)
  - Temporary URL: Available via Tailscale at `http://velo-server.tailce437e.ts.net/downloads`
- VF Server: Moved FibreFlow application from `/home/louis/apps/fibreflow/` to `/srv/data/apps/fibreflow/` (2025-12-17)
  - Reason: Utilize faster NVMe storage and standardize production paths
  - Impact: Requires rebuild of Next.js application, updated ecosystem.config.js
  - Rollback: Old directory backed up as `fibreflow.OLD_20251217`

## [1.0.0] - 2025-12-17

### Added
- Complete repository reorganization to A+ professional standards
- Skills-based architecture with progressive disclosure (99% faster queries)
- VF Server skill for remote operations via SSH/Tailscale
- Database operations skill with connection pooling
- Git operations skill for direct repository management
- Comprehensive testing suite with pytest
- Performance benchmarking system
- Metrics collection and reporting

### Changed
- Migrated from agent-heavy architecture to skills-first approach
- Reduced context usage by 84% (930 tokens vs 4,500)
- Optimized database queries from 2.3s to 23ms average
- Restructured documentation into guides/ and architecture/ directories

### Fixed
- WhatsApp feedback API integration (replaced mocks with real API calls)
- Removed hardcoded Azure AD secrets (moved to environment variables)
- Fixed agent orchestration routing logic

### Security
- Moved all secrets to environment variables
- Implemented SSH key authentication for VF Server
- Removed credentials from codebase

## [0.9.0] - 2025-12-16

### Added
- Agent Harness for autonomous agent building
- Domain Memory system with feature_list.json tracking
- Superior Agent Brain with vector memory (Qdrant)
- Dual database architecture (Neon + Convex)
- VPS monitoring agent
- Neon database agent
- Convex backend agent

### Infrastructure
- Hostinger VPS deployment (72.60.17.245)
- VF Server deployment (100.96.203.105 via Tailscale)
- FastAPI production server
- Nginx reverse proxy configuration

## Format Guidelines

### Version Numbers
- **Major**: Breaking changes, architecture shifts
- **Minor**: New features, agents, or skills
- **Patch**: Bug fixes, documentation updates

### Categories
- **Added**: New features, files, agents, skills
- **Changed**: Modifications to existing functionality
- **Deprecated**: Features to be removed
- **Removed**: Deleted features
- **Fixed**: Bug fixes
- **Security**: Security improvements
- **Infrastructure**: Server, deployment, configuration changes

### Entry Format
```markdown
### Category
- Brief description (YYYY-MM-DD)
  - Reason: Why this change was made
  - Impact: What it affects
  - Rollback: How to undo if needed (for risky changes)
```

---

**Note**: For detailed operational changes (server migrations, configuration updates, incident responses), see `docs/OPERATIONS_LOG.md`.
For architectural decisions and trade-offs, see `docs/DECISION_LOG.md`.
