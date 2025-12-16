# Convex Sync Requirements

## 📋 Overview
Sync data from Neon PostgreSQL database to Convex. This is a simpler database-to-database sync that mirrors the 7 tables already being populated by the SharePoint → Neon sync.

**Architecture:**
```
SharePoint Excel Files
         ↓
    [Neon Database] ← Already working, syncs every 4 hours
         ↓
    [Convex Database] ← Mirror Neon tables (this task)
```

---

## 🔐 Connection Details

### Convex
```bash
CONVEX_URL=https://quixotic-crow-802.convex.cloud
DEPLOYMENT=quixotic-crow-802
SYNC_AUTH_KEY=d8a094cd23d5beb878139d7bec04dab866e0825db06925ea021a917439ede3f6
```

### Neon (Source Database)
Connection details already configured in `/root/datahub/.env` on VPS

---

## 📊 Tables to Sync (7 Total)

| # | Neon Table Name | Convex Collection Name | Records | Purpose |
|---|-----------------|------------------------|---------|---------|
| 1 | `sow_poles` | `sow_poles` | ~4,500 | Foundation - Design data for poles |
| 2 | `sow_drops` | `sow_drops` | ~23,700 | Foundation - Home design data |
| 3 | `nokia_exports` | `nokia_exports` | ~1,900 | Activation data from Nokia |
| 4 | `onemap_installations` | `onemap_installations` | ~21,700 | OneMap installation records |
| 5 | `onemap_poles` | `onemap_poles` | ~5,400 | OneMap pole cross-reference |
| 6 | `lawley_activations` | `lawley_activations` | ~1,900 | Photo verification (ongoing) |
| 7 | `mohadin_activations` | `mohadin_activations` | ~400 | Photo verification with Zone/PON |

**Total Records:** ~60,000

---

## 🎯 Requirements for Convex Sync

### 1. Collection Names
Use the exact same names as Neon tables for consistency:
- `sow_poles`
- `sow_drops`
- `nokia_exports`
- `onemap_installations`
- `onemap_poles`
- `lawley_activations`
- `mohadin_activations`

### 2. Sync Strategy
Simple database replication approach:
- **Source:** Read from Neon PostgreSQL tables
- **Destination:** Write to Convex collections
- **Logic:** Upsert (insert new + update existing records)
- **Memory:** Process one table at a time (memory-optimized)
- **Incremental:** Track changes, only sync modified records (optional optimization)

### 3. Automation Schedule
Run after the Neon sync completes:
```bash
# Every 4 hours, 15 minutes after Neon sync (00:15, 04:15, 08:15, 12:15, 16:15, 20:15)
15 */4 * * * cd /root/datahub && npm run sync:convex >> /root/datahub/logs/cron-sync-convex.log 2>&1
```

**Why 15 minutes offset?**
- Neon sync runs at :00 (:00, 04:00, 08:00, etc.)
- Takes ~23 minutes to complete
- Convex sync starts at :15, ensuring fresh data

### 4. Data Source
- **Database:** Neon PostgreSQL (Serverless)
- **Connection:** Use existing Neon client from `/root/datahub/src/database/client.js`
- **Authentication:** Already configured in `.env`

---

## 📁 Implementation Approach

### Simple SQL → Convex Script

```typescript
// Example: src/scripts/sync-neon-to-convex.ts

import { sql } from '../database/client.js';
import { ConvexClient } from 'convex/browser';

const convex = new ConvexClient(process.env.CONVEX_URL!);

async function syncTable(tableName: string) {
  console.log(`📦 Syncing ${tableName}...`);

  // Read from Neon
  const records = await sql`SELECT * FROM ${sql(tableName)}`;

  // Write to Convex (batch upsert)
  await convex.mutation('sync/upsertBatch', {
    table: tableName,
    records: records
  });

  console.log(`✅ ${tableName}: ${records.length} records synced`);
}

// Sync all 7 tables
await syncTable('sow_poles');
await syncTable('sow_drops');
await syncTable('nokia_exports');
await syncTable('onemap_installations');
await syncTable('onemap_poles');
await syncTable('lawley_activations');
await syncTable('mohadin_activations');
```

---

## 📁 Reference Files

Located at: `/root/datahub` on VPS `72.60.17.245`

Key files to reference:
```
/root/datahub/
├── src/
│   ├── database/client.js           # Neon connection (reuse this)
│   ├── scripts/
│   │   ├── sync-all.ts              # Reference for sync patterns
│   │   └── sync-neon-to-convex.ts   # New file to create
│   └── config/
│       └── convex.config.js         # New Convex config
├── .env                             # Database credentials
└── package.json                     # Add npm scripts
```

---

## ✅ Success Criteria

1. All 7 Neon tables syncing to Convex collections successfully
2. Data in Convex matches Neon exactly
3. Cron job running every 4 hours (15 minutes after Neon sync)
4. Error logging and health checks implemented
5. Memory-efficient processing (won't crash on small VPS)
6. Sync completes in < 10 minutes

---

## 🚀 Deployment Location

Same VPS as Neon sync:
```bash
Server: 72.60.17.245
User: root
Working Dir: /root/datahub
```

---

## 📞 Environment Variables

Add to `/root/datahub/.env`:
```bash
# Existing Neon connection (already configured)
DATABASE_URL=postgresql://...

# Add Convex credentials
CONVEX_URL=https://quixotic-crow-802.convex.cloud
CONVEX_DEPLOYMENT=quixotic-crow-802
CONVEX_SYNC_AUTH_KEY=d8a094cd23d5beb878139d7bec04dab866e0825db06925ea021a917439ede3f6
```

---

## 🎯 Benefits of Neon → Convex Approach

✅ **Simpler:** No duplicate SharePoint parsing logic
✅ **Cleaner:** Neon is single source of truth
✅ **Faster:** Just copy structured data between databases
✅ **More reliable:** Only one SharePoint sync to maintain
✅ **Easier to debug:** Clear data flow path
✅ **Better performance:** Direct database-to-database transfer
