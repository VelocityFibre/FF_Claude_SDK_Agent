# QFieldCloud Incident Log

## Purpose
Track all QFieldCloud service incidents, resolutions, and preventive measures. This log serves as:
- Quick reference for troubleshooting recurring issues
- Knowledge base for support team
- Post-mortem analysis resource
- Service improvement guide

## Format
- **Newest entries first** (reverse chronological)
- **Severity Levels**: 🔴 Critical | 🟡 Major | 🔵 Minor
- **Status**: ⚠️ Active | ✅ Resolved | 🔄 Monitoring

---

## 2026-01-12

### 🔴 CRITICAL: Complete Service Failure - Missing QGIS Docker Image

**Time**: 09:00-11:45 SAST
**Status**: ✅ Resolved
**Impact Duration**: Unknown (possibly since migration on 2026-01-08)
**Affected Users**: All QFieldCloud users (Luke, Juan, others)
**Operator**: Claude Code + Louis

#### Symptoms Reported
1. Luke: Authentication error "HTTP/401 not_authenticated" for job `314d08af-bdd3-4ca8-998f`
2. Luke: Projects not showing after server URL update
3. Juan & Luke: "Failed" errors when saving/syncing projects
4. Juan: Permission differences (sees "Owner" option, others don't)
5. Web UI: No CSS styling (plain text only)
6. Juan & Luke (11:56): Download errors in QField after initial fixes

#### Root Causes Identified
1. **PRIMARY**: QGIS Docker processing image (`qfieldcloud-qgis:latest`) was missing
   - Workers couldn't process any project files
   - All sync operations failed with "ImageNotFound" errors
2. **SECONDARY**: Static files not served correctly after migration
   - CSS/JS served at `/staticfiles/` instead of `/static/`
3. **TERTIARY**: Stale authentication tokens after migration
4. **QUATERNARY**: Missing MinIO storage configuration in app container
   - Storage environment variables not set
   - Downloads failed with `/storage-download/` 404 errors

#### Resolution Steps
1. ✅ Built missing QGIS Docker image (2.6GB)
   ```bash
   cd /opt/qfieldcloud/docker-qgis
   docker build -t qfieldcloud-qgis:latest .
   ```
2. ✅ Restarted all 8 workers
3. ✅ Fixed static file serving (collected static files, adjusted nginx)
4. ✅ Cleared authentication tokens for affected users
5. ✅ Fixed storage backend configuration
   ```bash
   # Added to docker-compose.override.yml app environment:
   STORAGE_ENDPOINT_URL: http://minio:9000
   STORAGE_ACCESS_KEY_ID: minioadmin
   STORAGE_SECRET_ACCESS_KEY: minioadmin
   STORAGE_BUCKET_NAME: qfieldcloud-prod
   ```

#### Preventive Measures
- [ ] Add Docker image check to migration checklist
- [ ] Create health monitoring script for critical components
- [ ] Document all required Docker images
- [ ] Add automated backup of Docker images before migrations
- [ ] Verify storage backend configuration in migration checklist
- [ ] Test download functionality as part of post-migration verification

#### Reference
See detailed analysis: [INCIDENT_REF_2026-01-12.md](./incidents/INCIDENT_REF_2026-01-12.md)

---

## 2026-01-08

### 🟡 MAJOR: QFieldCloud Migration to VF Server

**Time**: Full day operation
**Status**: ✅ Completed (with issues discovered 2026-01-12)
**Impact**: Service moved from Hostinger (72.61.166.168) to VF Server (100.96.203.105)
**Operator**: Team

#### Changes
- Migrated for battery backup (UPS system)
- Scaled from 4 to 8 workers
- Database on port 5433
- MinIO storage on ports 8009-8010
- Service on port 8082

#### Issues (discovered later)
- QGIS Docker image not transferred
- Static file configuration needed adjustment
- Some user tokens became invalid

---

## Template for New Incidents

### 🔴/🟡/🔵 [SEVERITY]: [Brief Description]

**Time**: HH:MM-HH:MM SAST
**Status**: ⚠️/✅/🔄
**Impact Duration**:
**Affected Users**:
**Operator**:

#### Symptoms Reported
-

#### Root Causes Identified
-

#### Resolution Steps
1.

#### Preventive Measures
- [ ]

#### Reference
See: [link to detailed doc]