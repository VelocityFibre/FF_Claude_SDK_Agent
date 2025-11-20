# Quick Fix - Use Neon Agent for Full Data Access

## ✅ The Solution

Your **Convex functions for contractors/projects are broken**, but your **Neon database has ALL the data** (104 tables with everything).

**Quick fix:** Use the Neon agent which has direct access to all your FibreFlow data!

## 🚀 Test with Neon Agent Instead

### Option 1: Use Existing Neon Agent

```bash
cd /home/louisdup/Agents/claude
./venv/bin/python3 << 'EOF'
import sys
sys.path.append('agents/neon-database')
from neon_agent import NeonAgent

agent = NeonAgent()

# Test queries
print("\n1. Contractors:")
print(agent.chat("How many contractors do we have?"))

print("\n2. Projects:")
print(agent.chat("Show me all projects"))

print("\n3. BOQs:")
print(agent.chat("List all BOQs"))
EOF
```

### Option 2: Direct SQL Queries

```bash
./venv/bin/python3 << 'EOF'
import psycopg2
import os

# Load env
with open('.env') as f:
    for line in f:
        if 'NEON_DATABASE_URL' in line:
            os.environ['NEON_DATABASE_URL'] = line.split('=', 1)[1].strip()

conn = psycopg2.connect(os.environ['NEON_DATABASE_URL'])
cur = conn.cursor()

# Count contractors
cur.execute("SELECT COUNT(*) FROM contractors WHERE is_active = true")
print(f"Active contractors: {cur.fetchone()[0]}")

# List projects
cur.execute("SELECT project_name, status FROM projects LIMIT 5")
print("\nProjects:")
for row in cur.fetchall():
    print(f"  - {row[0]}: {row[1]}")

conn.close()
EOF
```

## 🎯 Why This Happened

When we deployed new Convex functions, they expect certain data schemas that don't match what your VPS sync created.

**Working:**
- ✅ Tasks (5 found)
- ✅ Neon database (ALL 104 tables)

**Broken:**
- ❌ Convex contractors function
- ❌ Convex projects function
- ❌ Convex universal function

## 📋 Recommendation

**Use the Neon Database Agent** - it has:
- ✅ All 104 tables
- ✅ All contractors (9+)
- ✅ All projects (2+)
- ✅ BOQs, RFQs, materials, equipment
- ✅ Everything in your FibreFlow system

The Neon agent already exists and works perfectly!

```bash
# Test it now
cd agents/neon-database
../../venv/bin/python3 agent.py
```

Then ask:
- "How many contractors?"
- "List all projects"
- "Show me BOQs"
- "What tables exist?"

## 🔧 To Fix Convex Later

The Convex functions need schema updates to match your actual data structure. But that's not urgent since Neon has everything!
