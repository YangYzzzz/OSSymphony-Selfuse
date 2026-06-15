"""
Reward Script: SSH config with identity file and strict host key checking disabled
Task ID: vscode_rrt_022
Domain: vscode
Scoring:
  Component 1 (0.20): Host test-env block exists
  Component 2 (0.20): HostName is 192.168.50.10
  Component 3 (0.15): User is tester
  Component 4 (0.15): IdentityFile is ~/.ssh/test_key
  Component 5 (0.15): StrictHostKeyChecking is no
  Component 6 (0.15): UserKnownHostsFile is /dev/null
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_022'
SSH_CONFIG_PATH = os.path.join(WORKDIR, '.ssh', 'config')


def parse_ssh_config(config_text):
    """Parse SSH config into a dict of {hostname: {key: value, ...}}."""
    hosts = {}
    current_host = None
    for line in config_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        # Match Host directive
        host_match = re.match(r'^Host\s+(.+)$', stripped, re.IGNORECASE)
        if host_match:
            current_host = host_match.group(1).strip()
            hosts[current_host] = {}
            continue
        # Match key-value pairs under a host
        if current_host:
            kv_match = re.match(r'^(\S+)\s+(.+)$', stripped)
            if kv_match:
                key = kv_match.group(1).strip()
                value = kv_match.group(2).strip()
                hosts[current_host][key] = value
    return hosts


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: SSH config file must exist
    if not os.path.exists(SSH_CONFIG_PATH):
        print(f"CRITICAL: SSH config not found at {SSH_CONFIG_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(SSH_CONFIG_PATH, 'r') as f:
            config_text = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read SSH config: {e}")
        print("REWARD: 0.0")
        return 0.0

    hosts = parse_ssh_config(config_text)

    # Component 1: Host test-env block exists (0.20 points)
    try:
        if 'test-env' in hosts:
            print(f"PASS: Component 1 — Host 'test-env' block exists (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Host 'test-env' block not found. Available hosts: {list(hosts.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # If test-env doesn't exist, no point checking its properties
    test_env = hosts.get('test-env', {})

    # Component 2: HostName is 192.168.50.10 (0.20 points)
    try:
        hostname = test_env.get('HostName', '')
        if hostname == '192.168.50.10':
            print(f"PASS: Component 2 — HostName is '192.168.50.10' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Expected HostName '192.168.50.10', found '{hostname}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: User is tester (0.15 points)
    try:
        user = test_env.get('User', '')
        if user == 'tester':
            print(f"PASS: Component 3 — User is 'tester' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — Expected User 'tester', found '{user}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: IdentityFile is ~/.ssh/test_key (0.15 points)
    try:
        identity = test_env.get('IdentityFile', '')
        if identity == '~/.ssh/test_key':
            print(f"PASS: Component 4 — IdentityFile is '~/.ssh/test_key' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Expected IdentityFile '~/.ssh/test_key', found '{identity}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: StrictHostKeyChecking is no (0.15 points)
    try:
        strict = test_env.get('StrictHostKeyChecking', '')
        if strict.lower() == 'no':
            print(f"PASS: Component 5 — StrictHostKeyChecking is 'no' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — Expected StrictHostKeyChecking 'no', found '{strict}'")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: UserKnownHostsFile is /dev/null (0.15 points)
    try:
        known_hosts = test_env.get('UserKnownHostsFile', '')
        if known_hosts == '/dev/null':
            print(f"PASS: Component 6 — UserKnownHostsFile is '/dev/null' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 — Expected UserKnownHostsFile '/dev/null', found '{known_hosts}'")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
