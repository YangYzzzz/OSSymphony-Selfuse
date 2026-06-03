"""
Reward Script: ZFS Storage Server Setup Script
Task ID: os_gf2_091
Domain: os (bash script)
Scoring:
  Component 1 (0.15): Script exists and is executable
  Component 2 (0.20): Creates mirrored pool 'datapool' with mirror /dev/sdb /dev/sdc
  Component 3 (0.30): Three datasets with correct compression and quotas
  Component 4 (0.20): Auto-snapshot + cron entries for frequent/hourly/daily
  Component 5 (0.15): Proper shebang + rc.local persistence + zpool status verification
"""

import os
import re
import stat

WORKDIR = '/home/user'
TASK_ID = 'os_gf2_091'
SCRIPT_PATH = f'{WORKDIR}/zfs_setup.sh'


def check_dataset_line(content, dataset_name, compression, quota):
    """Check if a zfs create line exists with the given dataset, compression and quota."""
    for line in content.split('\n'):
        if dataset_name in line and 'zfs' in line and 'create' in line:
            if compression in line and quota in line:
                return True
    return False


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.isfile(SCRIPT_PATH):
        print(f"CRITICAL: Script not found at {SCRIPT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(SCRIPT_PATH, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read script: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Script is executable (0.15 points)
    try:
        mode = stat.S_IMODE(os.stat(SCRIPT_PATH).st_mode)
        if mode & stat.S_IXUSR:
            print(f"PASS: Component 1 — Script is executable (mode: {oct(mode)}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Script is not executable (mode: {oct(mode)})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Creates mirrored pool 'datapool' using mirror /dev/sdb /dev/sdc (0.20 points)
    try:
        if re.search(r'zpool\s+create\s+datapool\s+mirror\s+/dev/sdb\s+/dev/sdc', content):
            print(f"PASS: Component 2 — Mirrored pool creation command found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Missing 'zpool create datapool mirror /dev/sdb /dev/sdc'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3a: datapool/data with compression=lz4 quota=500G (0.10 points)
    try:
        if check_dataset_line(content, 'datapool/data', 'compression=lz4', 'quota=500G'):
            print(f"PASS: Component 3a — datapool/data with lz4, 500G (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3a — datapool/data with compression=lz4 quota=500G not found")
    except Exception as e:
        print(f"ERROR: Component 3a — {e}")

    # Component 3b: datapool/backups with compression=gzip-9 quota=200G (0.10 points)
    try:
        if check_dataset_line(content, 'datapool/backups', 'compression=gzip-9', 'quota=200G'):
            print(f"PASS: Component 3b — datapool/backups with gzip-9, 200G (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3b — datapool/backups with compression=gzip-9 quota=200G not found")
    except Exception as e:
        print(f"ERROR: Component 3b — {e}")

    # Component 3c: datapool/vms with compression=lz4 quota=300G (0.10 points)
    try:
        if check_dataset_line(content, 'datapool/vms', 'compression=lz4', 'quota=300G'):
            print(f"PASS: Component 3c — datapool/vms with lz4, 300G (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3c — datapool/vms with compression=lz4 quota=300G not found")
    except Exception as e:
        print(f"ERROR: Component 3c — {e}")

    # Component 4a: auto-snapshot enabled (0.05 points)
    try:
        if re.search(r'zfs\s+set\s+com\.sun:auto-snapshot=true\s+datapool', content):
            print(f"PASS: Component 4a — auto-snapshot enabled (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 4a — 'zfs set com.sun:auto-snapshot=true datapool' not found")
    except Exception as e:
        print(f"ERROR: Component 4a — {e}")

    # Component 4b: cron entry for frequent snapshots (*/15) (0.05 points)
    try:
        if re.search(r'\*/15\s+\*\s+\*\s+\*\s+\*.*zfs-auto-snapshot.*frequent.*datapool.*4', content):
            print(f"PASS: Component 4b — frequent snapshot cron (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 4b — frequent snapshot cron entry not found")
    except Exception as e:
        print(f"ERROR: Component 4b — {e}")

    # Component 4c: cron entry for hourly snapshots (0.05 points)
    try:
        if re.search(r'0\s+\*\s+\*\s+\*\s+\*.*zfs-auto-snapshot.*hourly.*datapool.*24', content):
            print(f"PASS: Component 4c — hourly snapshot cron (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 4c — hourly snapshot cron entry not found")
    except Exception as e:
        print(f"ERROR: Component 4c — {e}")

    # Component 4d: cron entry for daily snapshots (0.05 points)
    try:
        if re.search(r'0\s+0\s+\*\s+\*\s+\*.*zfs-auto-snapshot.*daily.*datapool.*30', content):
            print(f"PASS: Component 4d — daily snapshot cron (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 4d — daily snapshot cron entry not found")
    except Exception as e:
        print(f"ERROR: Component 4d — {e}")

    # Component 5a: Script has proper bash shebang and rc.local persistence (0.10 points)
    try:
        if content.strip().startswith('#!/bin/bash') and 'rc.local' in content and 'zpool' in content:
            print(f"PASS: Component 5a — proper shebang + rc.local persistence (0.10 pts)")
            total_score += 0.10
        else:
            missing = []
            if not content.strip().startswith('#!/bin/bash'):
                missing.append("shebang")
            if 'rc.local' not in content:
                missing.append("rc.local persistence")
            print(f"FAIL: Component 5a — missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 5a — {e}")

    # Component 5b: Script contains zpool status verification (0.05 points)
    try:
        if re.search(r'zpool\s+status\s+datapool', content):
            print(f"PASS: Component 5b — zpool status verification present (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 5b — 'zpool status datapool' not found in script")
    except Exception as e:
        print(f"ERROR: Component 5b — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
