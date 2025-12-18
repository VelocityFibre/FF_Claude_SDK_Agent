# Hostinger VPS Details

**Purpose**: Public-facing FibreFlow API and web interface
**Note**: This is separate from VF Server (100.96.203.105) used for internal operations. See `.claude/skills/vf-server/README.md` for VF Server details.

**Server Information**

```
Hostname: srv1092611.hstgr.cloud
IP Address: 72.60.17.245
Location: Lithuania - Vilnius
OS: Ubuntu 24.04 LTS
SSH User: root
```

**Specs**

```
Plan: KVM 2
CPU: 2 cores
Memory: 8 GB
Disk: 100 GB
Bandwidth: 8 TB/month
```

**Current Usage**

```
CPU: 51%
Memory: 8%
Disk: 9 GB / 100 GB
Uptime: 19 hours
```

**Access**

```
SSH: root@72.60.17.245
SSH: root@srv1092611.hstgr.cloud
Public Key: ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILCItJmcpN+6+T4gasnuQlnAIRgNC3c7QrHPOZuD5pXD qfield-vps-deployment
```

**Deployment Target**

```
API will be accessible at:
- http://72.60.17.245
- http://srv1092611.hstgr.cloud

Recommended: Point a domain to this IP
Example: api.yourcompany.com → 72.60.17.245
```
