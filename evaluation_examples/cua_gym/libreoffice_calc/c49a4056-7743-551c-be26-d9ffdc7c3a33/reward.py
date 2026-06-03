"""
Reward Script: VSCode Port Forwarding Configuration
Task ID: vscode_rrt_014
Domain: vscode (remote SSH port forwarding)
Scoring:
  Component 1 (0.30): PostgreSQL port 5432 forwarding entry with correct label
  Component 2 (0.30): Redis port 6379 forwarding entry with correct label
  Component 3 (0.20): Both ports have correct protocol/forwarding attributes
  Component 4 (0.20): Auto-forward ports enabled
"""

import os
import json
import re

HOME = '/home/user'
SETTINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'settings.json')
TASK_ID = 'vscode_rrt_014'


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify VSCode port forwarding configuration.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    ports_attrs = settings.get('remote.portsAttributes', {})

    # Component 1: PostgreSQL port 5432 entry with label (0.30 points)
    try:
        pg_entry = ports_attrs.get('5432', {})
        if isinstance(pg_entry, dict) and pg_entry.get('label', '').lower() == 'postgresql':
            print(f"PASS: Component 1 - Port 5432 has label 'PostgreSQL' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 - Expected port 5432 with label 'PostgreSQL', found: {pg_entry}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Redis port 6379 entry with label (0.30 points)
    try:
        redis_entry = ports_attrs.get('6379', {})
        if isinstance(redis_entry, dict) and redis_entry.get('label', '').lower() == 'redis':
            print(f"PASS: Component 2 - Port 6379 has label 'Redis' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 - Expected port 6379 with label 'Redis', found: {redis_entry}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Both ports have correct protocol and forwarding attributes (0.20 points)
    try:
        pg_ok = (isinstance(ports_attrs.get('5432', {}), dict) and
                 ports_attrs.get('5432', {}).get('onAutoForward') in ('silent', 'notify', 'openBrowser', 'openPreview', 'openBrowserOnce') and
                 ports_attrs.get('5432', {}).get('protocol', 'tcp') == 'tcp')
        redis_ok = (isinstance(ports_attrs.get('6379', {}), dict) and
                    ports_attrs.get('6379', {}).get('onAutoForward') in ('silent', 'notify', 'openBrowser', 'openPreview', 'openBrowserOnce') and
                    ports_attrs.get('6379', {}).get('protocol', 'tcp') == 'tcp')
        if pg_ok and redis_ok:
            print(f"PASS: Component 3 - Both ports have valid protocol/forwarding config (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 - Port configs incomplete. PG ok={pg_ok}, Redis ok={redis_ok}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Auto-forward ports is enabled (0.20 points)
    try:
        auto_forward = settings.get('remote.autoForwardPorts', None)
        if auto_forward is True:
            print(f"PASS: Component 4 - remote.autoForwardPorts is true (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 - remote.autoForwardPorts expected true, found: {auto_forward}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
