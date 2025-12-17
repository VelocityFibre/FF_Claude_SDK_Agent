# QFieldCloud MOA_Pole_Audit Upload Failure - Urgent Fix

## Issue Summary
- **Date/Time**: December 17, 2025, 9:56 AM - 11:40 AM ongoing
- **Project**: MOA_Pole_Audit (Mohadin)
- **Users Affected**: Hartb, Fransl, JohanS
- **Issue**: All uploads failing with "UNKNOWN" error
- **Job Types Failing**:
  - Process QGIS Project File
  - Delta Apply

## Current Status
- API: ✅ Responding
- Database: ✅ OK
- Storage: ✅ OK
- Worker: ❓ Possible issue

## Immediate Actions to Try

### 1. Via QFieldCloud Web Interface

1. **Check Project Settings**:
   - Login as admin at https://qfield.fibreflow.app/admin/
   - Navigate to MOA_Pole_Audit project
   - Check:
     - Storage quota for user "Jaun"
     - Project permissions for affected users
     - Last successful sync timestamp

2. **Clear Failed Jobs**:
   - Go to Jobs admin panel
   - Filter for MOA_Pole_Audit failed jobs
   - Check error details if available
   - Consider clearing/retrying jobs

3. **Restart Worker via Admin**:
   - If admin panel has service controls
   - Restart worker_wrapper service

### 2. Alternative SSH Access

Since direct root SSH is failing, try:
```bash
# If you have another user account:
ssh qfield@72.61.166.168

# Or via your local QFieldCloud directory:
cd /home/louisdup/VF/Apps/QFieldCloud
./deployment/restart_workers.sh  # If this script exists
```

### 3. Docker Commands (if you can get SSH access)

```bash
# Check worker status
docker ps -a | grep worker

# Restart worker
docker-compose restart worker_wrapper

# Check worker logs
docker-compose logs --tail 100 worker_wrapper | grep ERROR

# Clear stuck jobs
docker-compose exec app python manage.py shell
>>> from qfieldcloud.core.models import Job
>>> Job.objects.filter(project__name='MOA_Pole_Audit', status='failed').delete()
```

### 4. Temporary Workarounds for Field Workers

**Tell field workers to**:
1. **Save work locally** in QField
2. **Try syncing one at a time** (not simultaneously)
3. **Reduce file sizes** if uploading photos
4. **Try again after 30 minutes** (worker might self-recover)

### 5. Check Project File Integrity

Ask project owner (Jaun) to:
1. Download the QGIS project locally
2. Open in QGIS Desktop
3. Check for corruption
4. Re-upload if needed

## Root Cause Analysis

Based on the pattern:
- All jobs failing at same time = systemic issue
- "UNKNOWN" error = worker can't process jobs
- Only affecting one project = likely project-specific

**Most likely causes**:
1. Worker memory exhaustion from large files
2. Corrupted project file blocking processing
3. Database lock on project data
4. Storage quota exceeded

## Contact Information

If above doesn't work:
- QFieldCloud support: tickets.qfield.cloud
- Check status page: https://status.qfield.cloud/
- GitHub issues: https://github.com/opengisch/qfieldcloud/issues

## Prevention

For future:
1. Set up monitoring alerts for failed jobs
2. Implement automatic worker restart on failures
3. Add storage quota warnings
4. Regular project file validation