"""
Reward Script: Configure /etc/hosts for devdb.local and devredis.local
Task ID: os_adm_016
Domain: os (system administration)
Scoring:
  - Component 1 (0.3): /etc/hosts contains 192.168.1.50 -> devdb.local
  - Component 2 (0.3): /etc/hosts contains 192.168.1.51 -> devredis.local
  - Component 3 (0.2): getent resolves devdb.local to 192.168.1.50
  - Component 4 (0.2): getent resolves devredis.local to 192.168.1.51
"""

import os
import re
import subprocess


HOSTS_FILE = '/etc/hosts'


def verify_task():
    """
    Verify that /etc/hosts has been configured with the required host entries
    and that name resolution works correctly.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: /etc/hosts must exist
    if not os.path.isfile(HOSTS_FILE):
        print(f"CRITICAL: {HOSTS_FILE} does not exist")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(HOSTS_FILE, 'r') as f:
            hosts_content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read {HOSTS_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse hosts file into (ip, hostname) pairs, ignoring comments and blanks
    hosts_lines = []
    for line in hosts_content.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        parts = stripped.split()
        if len(parts) >= 2:
            ip = parts[0]
            hostnames = parts[1:]
            for h in hostnames:
                hosts_lines.append((ip, h.lower()))

    # Component 1: /etc/hosts contains 192.168.1.50 -> devdb.local (0.3 points)
    try:
        devdb_found = any(
            ip == '192.168.1.50' and hostname == 'devdb.local'
            for ip, hostname in hosts_lines
        )
        if devdb_found:
            print("PASS: Component 1 — /etc/hosts maps 192.168.1.50 to devdb.local (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 1 — No entry mapping 192.168.1.50 to devdb.local in /etc/hosts")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: /etc/hosts contains 192.168.1.51 -> devredis.local (0.3 points)
    try:
        devredis_found = any(
            ip == '192.168.1.51' and hostname == 'devredis.local'
            for ip, hostname in hosts_lines
        )
        if devredis_found:
            print("PASS: Component 2 — /etc/hosts maps 192.168.1.51 to devredis.local (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 2 — No entry mapping 192.168.1.51 to devredis.local in /etc/hosts")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: getent resolves devdb.local to 192.168.1.50 (0.2 points)
    try:
        result = subprocess.run(
            ['getent', 'hosts', 'devdb.local'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and '192.168.1.50' in result.stdout:
            print("PASS: Component 3 — getent resolves devdb.local to 192.168.1.50 (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — getent devdb.local returned rc={result.returncode}, stdout='{result.stdout.strip()}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: getent resolves devredis.local to 192.168.1.51 (0.2 points)
    try:
        result = subprocess.run(
            ['getent', 'hosts', 'devredis.local'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and '192.168.1.51' in result.stdout:
            print("PASS: Component 4 — getent resolves devredis.local to 192.168.1.51 (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — getent devredis.local returned rc={result.returncode}, stdout='{result.stdout.strip()}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
