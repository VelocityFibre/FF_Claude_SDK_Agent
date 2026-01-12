#!/usr/bin/env python3
"""
Check what's using a specific port on the VF server
"""
import subprocess
import sys
import json
import os

def check_port(port=None):
    """Check what's using a specific port or all ports"""

    # Must run on VF server
    password = os.getenv('VF_SERVER_PASSWORD', 'VeloAdmin2025!')

    if port:
        # Check specific port
        cmd = f'ss -tlnp 2>/dev/null | grep :{port} && lsof -i:{port} 2>/dev/null | tail -n +2'
    else:
        # Show all listening ports
        cmd = 'ss -tlnp 2>/dev/null | grep LISTEN | sort -t: -k2 -n'

    # Execute on VF server
    execute_script = os.path.join(os.path.dirname(__file__), '../../vf-server/scripts/execute.py')
    result = subprocess.run(
        [execute_script, cmd],
        env={'VF_SERVER_PASSWORD': password},
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"❌ Error checking port: {result.stderr}")
        return False

    output = json.loads(result.stdout)

    if not output.get('output'):
        if port:
            print(f"✅ Port {port} is free!")
        else:
            print("❌ No listening ports found")
        return True

    if port:
        print(f"📍 Port {port} Status:")
        print("-" * 50)
    else:
        print("📍 All Listening Ports:")
        print("-" * 50)

    print(output['output'])

    # Parse and show process details for specific port
    if port and 'next-server' in output['output']:
        print("\n⚠️  FibreFlow instance(s) detected on port", port)

        # Get detailed process info
        ps_cmd = 'ps aux | grep "[n]ext-server" | grep -v grep'
        ps_result = subprocess.run(
            [execute_script, ps_cmd],
            env={'VF_SERVER_PASSWORD': password},
            capture_output=True,
            text=True
        )

        if ps_result.returncode == 0:
            ps_output = json.loads(ps_result.stdout)
            if ps_output.get('output'):
                print("\nProcess Details:")
                for line in ps_output['output'].strip().split('\n'):
                    parts = line.split()
                    if len(parts) > 10:
                        user = parts[0]
                        pid = parts[1]
                        cpu = parts[2]
                        mem = parts[3]
                        print(f"  • User: {user:8} PID: {pid:8} CPU: {cpu}% MEM: {mem}%")

    return True

if __name__ == '__main__':
    port = sys.argv[1] if len(sys.argv) > 1 else None
    check_port(port)