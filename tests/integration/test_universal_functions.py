#!/usr/bin/env python3
"""
Test universal Convex functions with real FibreFlow data.
"""

import os
import requests
import json

def load_env():
    with open('.env') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

load_env()
convex_url = os.environ.get("CONVEX_URL")

print("="*70)
print("TESTING UNIVERSAL CONVEX FUNCTIONS")
print("="*70)
print(f"\nConvex URL: {convex_url}\n")

# Test tables
test_tables = [
    ("BOQs", "boqs"),
    ("RFQs", "rfqs"),
    ("Materials", "materials"),
    ("Equipment", "equipment"),
    ("Quotes", "quotes"),
    ("Meetings", "meetings"),
    ("Clients", "clients"),
    ("VPS Servers", "vps_servers"),
]

results = []

for display_name, table_name in test_tables:
    print(f"{'─'*70}")
    print(f"Testing: {display_name} ({table_name})")
    print("─"*70)

    # Test universal function
    payload = {
        "path": "universal:listFromTable",
        "args": {"tableName": table_name, "limit": 3}
    }

    try:
        response = requests.post(
            f"{convex_url}/api/query",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            value = result.get("value", result)

            if value.get("status") == "success":
                data = value.get("data", [])
                total = value.get("total", 0)
                print(f"✅ SUCCESS: Found {total} records")
                if data and len(data) > 0:
                    print(f"   Sample: {json.dumps(data[0], indent=2)[:200]}...")
                results.append((display_name, True, total))
            else:
                print(f"⚠️  Table exists but empty or error")
                print(f"   {value.get('message', 'Unknown error')}")
                results.append((display_name, False, 0))
        else:
            print(f"❌ HTTP {response.status_code}")
            results.append((display_name, False, 0))

    except Exception as e:
        print(f"❌ Error: {e}")
        results.append((display_name, False, 0))

print("\n" + "="*70)
print("TEST SUMMARY")
print("="*70)

success_count = sum(1 for _, success, _ in results if success)
total_records = sum(count for _, success, count in results if success)

print(f"\nTables tested: {len(results)}")
print(f"Accessible: {success_count}")
print(f"Total records found: {total_records}")

print(f"\n{'Table':<20} {'Status':<15} {'Records'}")
print("─"*70)
for name, success, count in results:
    status = "✅ Accessible" if success else "❌ Failed"
    print(f"{name:<20} {status:<15} {count if success else '-'}")

if success_count > 0:
    print(f"\n🎉 SUCCESS! {success_count} FibreFlow tables now accessible to agents!")
else:
    print("\n⚠️  No tables accessible yet. May need schema adjustments.")
