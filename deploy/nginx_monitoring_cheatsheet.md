# Nginx Monitoring Cheat Sheet

**Quick reference for monitoring your enhanced Nginx configuration**

---

## 🏥 Health Checks

```bash
# Quick health check (all services)
ssh root@72.60.17.245 'curl -s http://localhost/nginx_status && echo "" && systemctl status neon-agent --no-pager | head -5 && systemctl status superior-brain --no-pager | head -5'

# Individual services
curl http://app.fibreflow.app/api/agent/quick/health
curl http://app.fibreflow.app/api/agent/brain/health
```

---

## 📊 Cache Statistics

```bash
# Cache hit ratio (last 1000 requests)
ssh root@72.60.17.245 'tail -1000 /var/log/nginx/fibreflow_access.log | grep -o "cache:[A-Z]*" | sort | uniq -c'

# Cache directory size
ssh root@72.60.17.245 'du -sh /var/cache/nginx/agent_cache/'

# Cache file count
ssh root@72.60.17.245 'find /var/cache/nginx/agent_cache/ -type f | wc -l'

# Test cache status on specific endpoint
curl -I http://app.fibreflow.app/api/agent/quick/health | grep X-Cache-Status
```

---

## 📝 Log Analysis

```bash
# Real-time access logs
ssh root@72.60.17.245 'tail -f /var/log/nginx/fibreflow_access.log'

# Real-time error logs
ssh root@72.60.17.245 'tail -f /var/log/nginx/fibreflow_error.log'

# Count requests by endpoint (last hour)
ssh root@72.60.17.245 'grep "$(date +%d/%b/%Y:%H)" /var/log/nginx/fibreflow_access.log | cut -d\" -f2 | cut -d" " -f2 | sort | uniq -c | sort -rn'

# Find slow requests (>5s)
ssh root@72.60.17.245 'awk '\''$NF > 5000 {print $0}'\'' /var/log/nginx/fibreflow_access.log | tail -20'
```

---

## 🚦 Rate Limiting

```bash
# View rate limiting events
ssh root@72.60.17.245 'grep "limiting requests" /var/log/nginx/fibreflow_error.log | tail -20'

# Count rate limits by IP
ssh root@72.60.17.245 'grep "limiting requests" /var/log/nginx/fibreflow_error.log | grep -oE "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" | sort | uniq -c | sort -rn'

# Check if you're being rate limited (from local machine)
for i in {1..15}; do curl -s -o /dev/null -w "%{http_code}\n" http://app.fibreflow.app/api/agent/quick/health; done
```

---

## 💰 Cost Estimation

```bash
# Total requests today
ssh root@72.60.17.245 'grep "$(date +%d/%b/%Y)" /var/log/nginx/fibreflow_access.log | wc -l'

# Cache hit ratio (today)
ssh root@72.60.17.245 'grep "$(date +%d/%b/%Y)" /var/log/nginx/fibreflow_access.log | grep -o "cache:[A-Z]*" | sort | uniq -c'

# Calculate saved API calls (if 60% hit rate)
# Formula: total_requests * cache_hit_ratio * api_cost_per_request
# Example: 1000 requests * 0.60 * $0.02 = $12 saved
```

---

## 🔧 Cache Management

```bash
# Clear all cache
ssh root@72.60.17.245 'rm -rf /var/cache/nginx/agent_cache/* && systemctl reload nginx'

# Clear cache for specific endpoint (manual - find cache files)
ssh root@72.60.17.245 'find /var/cache/nginx/agent_cache/ -name "*quick*" -delete'

# Reload Nginx configuration (zero downtime)
ssh root@72.60.17.245 'nginx -t && systemctl reload nginx'

# View cache configuration
ssh root@72.60.17.245 'nginx -T | grep -A 10 proxy_cache_path'
```

---

## 🎯 Performance Metrics

```bash
# Active connections
ssh root@72.60.17.245 'curl -s http://localhost/nginx_status | grep "Active"'

# Request rate (requests per second)
ssh root@72.60.17.245 'tail -1000 /var/log/nginx/fibreflow_access.log | wc -l'
# Divide by time window (rough estimate)

# Average response time (from upstream)
ssh root@72.60.17.245 'tail -1000 /var/log/nginx/fibreflow_access.log | awk '\''{sum+=$NF; count++} END {print "Avg:", sum/count, "ms"}'\''

# Top 10 slowest requests
ssh root@72.60.17.245 'awk '\''$NF ~ /^[0-9]+/ {print $NF, $7}'\'' /var/log/nginx/fibreflow_access.log | sort -rn | head -10'
```

---

## 🚨 Error Tracking

```bash
# Count errors by type
ssh root@72.60.17.245 'grep error /var/log/nginx/fibreflow_error.log | cut -d" " -f4- | cut -d: -f1 | sort | uniq -c | sort -rn'

# Recent 5xx errors
ssh root@72.60.17.245 'grep " 5[0-9][0-9] " /var/log/nginx/fibreflow_access.log | tail -20'

# Backend connection errors
ssh root@72.60.17.245 'grep "upstream" /var/log/nginx/fibreflow_error.log | tail -20'

# Check if backend services are running
ssh root@72.60.17.245 'ss -tlnp | grep -E "8000|8001"'
```

---

## 🔄 Rollback & Recovery

```bash
# List config backups
ssh root@72.60.17.245 'ls -lh /etc/nginx/sites-available/fibreflow.backup*'

# Rollback to previous config
ssh root@72.60.17.245 'cp /etc/nginx/sites-available/fibreflow.backup.YYYYMMDD_HHMMSS /etc/nginx/sites-available/fibreflow && nginx -t && systemctl reload nginx'

# Restart services if needed
ssh root@72.60.17.245 'systemctl restart neon-agent && systemctl restart superior-brain'

# Nuclear option: restart everything
ssh root@72.60.17.245 'systemctl restart nginx && systemctl restart neon-agent && systemctl restart superior-brain'
```

---

## 📈 Weekly Monitoring Routine

```bash
# Run this weekly to assess cache performance

echo "=== Weekly Nginx Report ===" && \
ssh root@72.60.17.245 '
echo "" && \
echo "📊 Total Requests (last 7 days):" && \
find /var/log/nginx -name "fibreflow_access.log*" -mtime -7 -exec cat {} \; | wc -l && \
echo "" && \
echo "💾 Cache Statistics:" && \
find /var/log/nginx -name "fibreflow_access.log*" -mtime -7 -exec cat {} \; | grep -o "cache:[A-Z]*" | sort | uniq -c && \
echo "" && \
echo "🚦 Rate Limiting Events:" && \
grep "limiting requests" /var/log/nginx/fibreflow_error.log | wc -l && \
echo "" && \
echo "📦 Cache Size:" && \
du -sh /var/cache/nginx/agent_cache/ && \
echo "" && \
echo "❌ Error Count:" && \
grep " 5[0-9][0-9] " /var/log/nginx/fibreflow_access.log | wc -l && \
echo "" && \
echo "✅ Uptime:" && \
uptime
'
```

---

## 🎨 Pretty Dashboard (One-Liner)

```bash
watch -n 5 'ssh root@72.60.17.245 "echo \"🔥 Active Connections:\" && curl -s http://localhost/nginx_status | head -1 && echo \"\" && echo \"📊 Recent Cache Stats (last 100):\" && tail -100 /var/log/nginx/fibreflow_access.log | grep -o \"cache:[A-Z]*\" | sort | uniq -c && echo \"\" && echo \"⚡ Service Status:\" && systemctl is-active neon-agent superior-brain nginx"'
```

---

## 🆘 Quick Troubleshooting

**Problem: High cache miss rate (<30%)**
```bash
# Check if cache directory is writable
ssh root@72.60.17.245 'ls -la /var/cache/nginx/ && df -h /var/cache/nginx/'

# Verify cache configuration
ssh root@72.60.17.245 'nginx -T | grep proxy_cache'
```

**Problem: 502 Bad Gateway**
```bash
# Check backend services
ssh root@72.60.17.245 'systemctl status neon-agent superior-brain && ss -tlnp | grep -E "8000|8001"'

# Check backend logs
ssh root@72.60.17.245 'journalctl -u neon-agent -n 50 && journalctl -u superior-brain -n 50'
```

**Problem: High error rate**
```bash
# Find most common errors
ssh root@72.60.17.245 'tail -500 /var/log/nginx/fibreflow_error.log | cut -d" " -f9- | sort | uniq -c | sort -rn | head -10'
```

---

## 💡 Pro Tips

1. **Set up log rotation** to prevent disk space issues:
```bash
ssh root@72.60.17.245 'ls -lh /var/log/nginx/ | grep fibreflow'
```

2. **Monitor disk space** for cache:
```bash
ssh root@72.60.17.245 'df -h /var/cache/nginx/'
```

3. **Create alerts** for high error rates:
```bash
# Add to crontab on VPS
*/5 * * * * [ $(grep " 5[0-9][0-9] " /var/log/nginx/fibreflow_access.log | tail -100 | wc -l) -gt 10 ] && echo "High error rate!" | mail -s "Nginx Alert" admin@example.com
```

4. **Benchmark cache performance**:
```bash
# Before and after comparison
ab -n 1000 -c 10 http://app.fibreflow.app/api/agent/quick/health
```

---

**Quick Access Commands:**

```bash
# Save these as shell aliases for faster access
alias nginx-status='ssh root@72.60.17.245 "curl -s http://localhost/nginx_status"'
alias nginx-cache='ssh root@72.60.17.245 "tail -100 /var/log/nginx/fibreflow_access.log | grep -o \"cache:[A-Z]*\" | sort | uniq -c"'
alias nginx-logs='ssh root@72.60.17.245 "tail -f /var/log/nginx/fibreflow_access.log"'
alias nginx-errors='ssh root@72.60.17.245 "tail -f /var/log/nginx/fibreflow_error.log"'
alias nginx-reload='ssh root@72.60.17.245 "nginx -t && systemctl reload nginx"'
alias nginx-clear-cache='ssh root@72.60.17.245 "rm -rf /var/cache/nginx/agent_cache/* && systemctl reload nginx"'
```

Add to `~/.bashrc` or `~/.zshrc` and run `source ~/.bashrc`

---

**Last updated:** 2025-11-26
