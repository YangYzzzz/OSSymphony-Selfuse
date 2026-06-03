"""
Reward Script: Verify SSH host configuration for dev-server
Task ID: vscode_we_065
Domain: vscode
Scoring:
  - Component 1 (0.20): Host entry 'dev-server' exists
  - Component 2 (0.20): HostName is dev.example.com
  - Component 3 (0.20): User is developer
  - Component 4 (0.20): Port is 2222
  - Component 5 (0.20): IdentityFile is ~/.ssh/dev_key
"""

import os
import re

WORKDIR = '/home/user'
SSH_CONFIG = os.path.join(WORKDIR, '.ssh', 'config')
TASK_ID = 'vscode_we_065'


def parse_ssh_config(path):
    """Parse SSH config file into a dict of {host_alias: {key: value, ...}}."""
    hosts = {}
    current_host = None
    try:
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # Match "Host <alias>" lines
                m = re.match(r'^Host\s+(.+)$', line, re.IGNORECASE)
                if m:
                    current_host = m.group(1).strip()
                    hosts[current_host] = {}
                    continue
                # Match "Key Value" lines
                if current_host is not None:
                    parts = line.split(None, 1)
                    if len(parts) == 2:
                        hosts[current_host][parts[0].lower()] = parts[1].strip()
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"ERROR: Failed to parse SSH config: {e}")
    return hosts


def verify_task():
    """
    Verify SSH host configuration with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: config file must exist
    if not os.path.exists(SSH_CONFIG):
        print(f"CRITICAL: SSH config not found at {SSH_CONFIG}")
        print("REWARD: 0.0")
        return 0.0

    hosts = parse_ssh_config(SSH_CONFIG)
    print(f"INFO: Found {len(hosts)} host entries: {list(hosts.keys())}")

    # Find the dev-server entry (case-insensitive match on alias)
    dev_entry = None
    matched_alias = None
    for alias, config in hosts.items():
        if alias.lower() == 'dev-server':
            dev_entry = config
            matched_alias = alias
            break

    # Component 1: Host entry 'dev-server' exists (0.20 points)
    try:
        if dev_entry is not None:
            print(f"PASS: Component 1 — Host entry '{matched_alias}' found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — No 'dev-server' Host entry found. Entries: {list(hosts.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if dev_entry is None:
        # No point checking further
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: HostName is dev.example.com (0.20 points)
    try:
        hostname = dev_entry.get('hostname', '')
        if hostname.lower() == 'dev.example.com':
            print(f"PASS: Component 2 — HostName is '{hostname}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — HostName expected 'dev.example.com', found '{hostname}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: User is developer (0.20 points)
    try:
        user = dev_entry.get('user', '')
        if user == 'developer':
            print(f"PASS: Component 3 — User is '{user}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — User expected 'developer', found '{user}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Port is 2222 (0.20 points)
    try:
        port = dev_entry.get('port', '')
        if str(port) == '2222':
            print(f"PASS: Component 4 — Port is '{port}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — Port expected '2222', found '{port}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: IdentityFile is ~/.ssh/dev_key (0.20 points)
    try:
        identity = dev_entry.get('identityfile', '')
        if identity == '~/.ssh/dev_key':
            print(f"PASS: Component 5 — IdentityFile is '{identity}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 5 — IdentityFile expected '~/.ssh/dev_key', found '{identity}'")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
