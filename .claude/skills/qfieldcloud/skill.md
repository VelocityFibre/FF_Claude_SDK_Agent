---
name: qfieldcloud
version: 1.0.0
description: Complete management suite for QFieldCloud GIS synchronization platform
author: FibreFlow Team
category: application
tags: [django, docker, postgresql, gis, qfield, qgis, deployment]
created: 2024-12-17
---

# QFieldCloud Management Skill

Comprehensive skill for managing QFieldCloud - a Django-based service for synchronizing QGIS projects and field data between desktop and mobile devices.

## Features

- **Docker Container Management**: Control docker-compose services (app, nginx, db, redis, worker)
- **Deployment Operations**: Deploy updates from GitHub, manage migrations
- **Service Monitoring**: Check container health, API status, database connectivity
- **Log Analysis**: View and search Docker container logs
- **Database Operations**: Backup/restore operations, migrations
- **User Management**: Create users, manage projects, check quotas
- **SSL Certificate Management**: Let's Encrypt certificate renewal

## Quick Usage

```bash
# Check all services status
./scripts/status.py

# Deploy latest updates
./scripts/deploy.py --branch master

# View application logs
./scripts/logs.py --service app --lines 100

# Check database status
./scripts/database.py --action status

# Monitor API health
./scripts/health.py
```

## Infrastructure Configuration

- **Production Server**: srv1083126.hstgr.cloud (72.61.166.168)
- **Public URL**: https://qfield.fibreflow.app
- **Local Development**: /home/louisdup/VF/Apps/QFieldCloud/
- **GitHub**: opengisch/QFieldCloud (fork)

## Services Architecture

QFieldCloud runs multiple Docker containers:

| Service | Purpose | Port |
|---------|---------|------|
| `nginx` | Reverse proxy, SSL termination | 80, 443 |
| `app` | Django application (gunicorn) | 8011 |
| `db` | PostgreSQL with PostGIS | 5432 |
| `redis` | Cache and queue broker | 6379 |
| `worker_wrapper` | Background task processing | - |
| `minio` | Object storage (S3 compatible) | 9000 |
| `ofelia` | Cron job scheduler | - |

## Environment Variables

Required environment variables (stored in .env):
- `QFIELDCLOUD_HOST`: Server hostname
- `QFIELDCLOUD_VPS_HOST`: VPS IP address (72.61.166.168)
- `QFIELDCLOUD_VPS_USER`: SSH username
- `QFIELDCLOUD_VPS_PASSWORD`: SSH password (optional if using key)
- `QFIELDCLOUD_PROJECT_PATH`: Remote project path

## Scripts Available

| Script | Purpose | Usage |
|--------|---------|-------|
| `status.py` | Check Docker services | No args |
| `deploy.py` | Deploy from GitHub | `--branch [master\|develop]` |
| `logs.py` | View container logs | `--service NAME --lines N` |
| `database.py` | Database operations | `--action [status\|backup\|migrate]` |
| `health.py` | API health checks | `--verbose` |
| `users.py` | User management | `--action [list\|create\|quota]` |
| `docker.py` | Docker operations | `--action [restart\|rebuild\|prune]` |

## Common Operations

### Check Service Status
```bash
./scripts/status.py
```
Shows:
- Docker container status
- Memory and CPU usage
- Container health
- Uptime information

### Deploy Updates
```bash
# Deploy from master branch
./scripts/deploy.py --branch master

# Deploy with migrations
./scripts/deploy.py --branch master --migrate

# Deploy and collect static files
./scripts/deploy.py --branch master --collectstatic
```

### View Logs
```bash
# View app logs
./scripts/logs.py --service app --lines 100

# Follow nginx logs
./scripts/logs.py --service nginx --follow

# Search for errors
./scripts/logs.py --service all --grep "ERROR"
```

### Database Management
```bash
# Check database status
./scripts/database.py --action status

# Create backup
./scripts/database.py --action backup

# Run migrations
./scripts/database.py --action migrate

# Access database shell
./scripts/database.py --action shell
```

### Health Monitoring
```bash
# Quick health check
./scripts/health.py

# Verbose health check with response times
./scripts/health.py --verbose

# Check specific endpoint
./scripts/health.py --endpoint /api/v1/status/
```

### User Management
```bash
# List users
./scripts/users.py --action list

# Create superuser
./scripts/users.py --action create --username admin --email admin@example.com

# Check user quota
./scripts/users.py --action quota --username john
```

## Troubleshooting

### Common Issues

1. **Containers not starting**: Check docker-compose logs
   ```bash
   ./scripts/logs.py --service all --lines 200
   ```

2. **Database connection issues**: Verify PostgreSQL is running
   ```bash
   ./scripts/database.py --action status
   ```

3. **SSL certificate issues**: Renew Let's Encrypt certificate
   ```bash
   ./scripts/ssl.py --action renew
   ```

4. **Storage issues**: Check MinIO/S3 connectivity
   ```bash
   ./scripts/health.py --verbose
   ```

### Emergency Commands

```bash
# Restart all services
./scripts/docker.py --action restart --all

# Rebuild specific service
./scripts/docker.py --action rebuild --service app

# Clean up Docker resources
./scripts/docker.py --action prune

# Force recreate containers
./scripts/docker.py --action recreate
```

## QFieldCloud Specific Operations

### Project Management
```bash
# List all projects
./scripts/projects.py --action list

# Check project status
./scripts/projects.py --action status --project PROJECT_ID

# Export project data
./scripts/projects.py --action export --project PROJECT_ID
```

### Synchronization Monitoring
```bash
# Check sync queue
./scripts/sync.py --action queue

# View recent syncs
./scripts/sync.py --action recent --hours 24

# Check failed syncs
./scripts/sync.py --action failed
```

## Integration with Other Skills

This skill works with:
- `vf-server`: For server-level operations
- `database-operations`: For complex PostgreSQL queries
- `git-operations`: For repository management
- `ff-react`: Coordinates with main FibreFlow app

## Development Workflow

### Local Development
```bash
# SSH to VPS
ssh user@72.61.166.168

# Navigate to project
cd /path/to/qfieldcloud

# Update from git
git pull origin master

# Rebuild containers
docker-compose build

# Run migrations
docker-compose exec app python manage.py migrate

# Restart services
docker-compose restart
```

### Production Deployment
```bash
# Use deployment script
./scripts/deploy.py --branch master --migrate --collectstatic

# Monitor deployment
./scripts/logs.py --service app --follow
```

## API Endpoints

Key API endpoints to monitor:
- `/api/v1/status/` - Health check
- `/api/v1/auth/login/` - Authentication
- `/api/v1/projects/` - Project listing
- `/api/v1/users/` - User management
- `/swagger/` - API documentation

## Self-Healing Prevention System

QFieldCloud includes a comprehensive automated prevention and monitoring system to prevent upload failures and service degradation.

### Monitor Daemon

**Service**: `qfield-monitor` (systemd)
**Script**: `/home/louisdup/VF/Apps/QFieldCloud/qfield_monitor_daemon.py`
**Logs**: `/var/log/qfield_monitor.log` and `/var/log/qfield_monitor_error.log`

Continuous health monitoring (every 5 minutes) with auto-recovery:
- Detects stuck jobs (queued >10 minutes)
- Monitors worker health and auto-restarts
- Tracks failure rates (alerts if >30%)
- Self-healing with automatic interventions

```bash
# Check monitor status
sudo systemctl status qfield-monitor

# View monitor logs
tail -f /var/log/qfield_monitor.log

# Restart monitor
sudo systemctl restart qfield-monitor
```

### Rate Limiting

**Script**: `qfield_rate_limiter.sh`

Nginx rate limiting to prevent sync overload:
- Global: 10 syncs/minute
- Per-project: 5 syncs/minute
- Throttle individual projects if needed

```bash
# Apply rate limiting
./qfield_rate_limiter.sh --enable

# Throttle specific project
./qfield_rate_limiter.sh --throttle MOA_Pole_Audit
```

### Automated Maintenance

**Cron Jobs** (configured via `qfield_cron_jobs.sh`):

| Frequency | Script | Purpose |
|-----------|--------|---------|
| */5 min | `qfield_quick_check.sh` | Worker and API health |
| */30 min | `qfield_cleanup.sh` | Docker resource cleanup |
| */4 hours | `qfield_scheduled_restart.sh` | Preventive worker restart (if idle) |
| Daily 2am | `qfield_daily_maintenance.sh` | Full maintenance cycle |
| Daily 6am | `qfield_stats.sh` | Usage statistics report |

```bash
# View cron schedule
crontab -l | grep qfield

# Run maintenance manually
./qfield_daily_maintenance.sh
```

### Prevention System Setup

Complete setup in one command:
```bash
cd /home/louisdup/VF/Apps/QFieldCloud
./SETUP_PREVENTION.sh
```

This installs:
- Monitor daemon with systemd service
- Rate limiting configuration
- All automated cron jobs
- Log rotation

### Troubleshooting Prevention System

**Monitor keeps restarting workers:**
```bash
# Check what's triggering it
tail -f /var/log/qfield_monitor.log | grep "CRITICAL\|WARNING"

# Temporarily stop monitor to fix manually
sudo systemctl stop qfield-monitor
# Fix the issue...
sudo systemctl start qfield-monitor
```

**Disk full (100%):**
```bash
# Emergency cleanup
ssh root@72.61.166.168 "docker system prune -a --volumes -f"

# Check disk usage
./scripts/docker.py --action check-disk
```

**Workers missing after cleanup:**
```bash
# Rebuild workers
ssh root@72.61.166.168 "cd /opt/qfieldcloud && docker compose up -d worker_wrapper"
```

## Notes

- Always backup database before major updates
- Monitor disk space on VPS (Docker images can be large) - **automated via cron**
- Regular certificate renewal for Let's Encrypt
- Keep docker-compose.yml in sync with upstream
- Monitor worker queue for stuck jobs - **automated via prevention system**
- Check storage quotas regularly
- Prevention system provides self-healing for common issues