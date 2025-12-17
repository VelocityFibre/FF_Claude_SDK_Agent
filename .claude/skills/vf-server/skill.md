---
name: vf-server
description: Direct VF Velocity server operations via Tailscale
version: 1.0.0
requires: ssh, sshpass, curl
---

# VF Server Operations Skill

Provides direct access to Velocity Fibre server operations without exploration.

## Available Scripts

- `status.py` - Check server health and services
- `connect.py` - Get connection command (doesn't expose password)
- `service_check.py` - Check status of all web services
- `logs.py` - View recent logs from services
- `execute.py` - Execute commands on server
- `docker_status.py` - Check Docker containers status
- `disk_usage.py` - Check disk space
- `restart_service.py` - Restart specific services

## Services Available

- **Portainer**: Container management (port 9443)
- **Grafana**: Metrics visualization (port 3000)
- **Ollama**: Local LLM service (port 11434)
- **Qdrant**: Vector database (port 6333)
- **FibreFlow API**: Production API (port 80)

## Connection Methods

1. **Tailscale** (Preferred): 100.96.203.105 or velo-server
2. **WireGuard**: Via 10.10.0.1
3. **Local Network**: 192.168.1.150

## Security

All credentials stored in environment variables:
- VF_SERVER_HOST
- VF_SERVER_USER
- VF_SERVER_PASSWORD (encrypted in .env)