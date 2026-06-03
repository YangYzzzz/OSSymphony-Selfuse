"""
Reward Script: Add multiple SSH host entries to ~/.ssh/config
Task ID: vscode_rrt_010
Domain: vscode
Scoring:
  - Component 1 (0.35): prod-web host entry with correct HostName, User, IdentityFile
  - Component 2 (0.35): prod-api host entry with correct HostName, User, IdentityFile
  - Component 3 (0.30): prod-db host entry with correct HostName, User, IdentityFile
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_010'
SSH_CONFIG_PATH = os.path.join(WORKDIR, '.ssh', 'config')

# Expected host entries: (host_name, hostname_ip, user, identity_file)
EXPECTED_HOSTS = {
    'prod-web': {
        'HostName': '10.0.1.10',
        'User': 'ubuntu',
        'IdentityFile': '~/.ssh/prod_key',
    },
    'prod-api': {
        'HostName': '10.0.1.11',
        'User': 'ubuntu',
        'IdentityFile': '~/.ssh/prod_key',
    },
    'prod-db': {
        'HostName': '10.0.1.12',
        'User': 'ubuntu',
        'IdentityFile': '~/.ssh/prod_key',
    },
}

# Points per host
HOST_POINTS = {
    'prod-web': 0.35,
    'prod-api': 0.35,
    'prod-db': 0.30,
}


def parse_ssh_config(path):
    """Parse SSH config file into a dict of {host_name: {key: value, ...}}."""
    hosts = {}
    current_host = None

    try:
        with open(path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        return hosts

    for line in content.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue

        # Match "Host <name>" lines
        host_match = re.match(r'^Host\s+(\S+)', stripped, re.IGNORECASE)
        if host_match:
            current_host = host_match.group(1)
            hosts[current_host] = {}
            continue

        # Match "Key Value" lines within a host block
        if current_host is not None:
            kv_match = re.match(r'^(\S+)\s+(.+)', stripped)
            if kv_match:
                key = kv_match.group(1)
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
        print(f"CRITICAL: SSH config file not found at {SSH_CONFIG_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Parse the SSH config
    hosts = parse_ssh_config(SSH_CONFIG_PATH)
    print(f"INFO: Found {len(hosts)} host entries in SSH config: {list(hosts.keys())}")

    for host_name, expected_props in EXPECTED_HOSTS.items():
        points = HOST_POINTS[host_name]
        component_label = f"Host '{host_name}'"

        try:
            if host_name not in hosts:
                print(f"FAIL: {component_label} -- not found in SSH config ({points} pts)")
                continue

            actual_props = hosts[host_name]
            all_match = True
            details = []

            for key, expected_val in expected_props.items():
                actual_val = actual_props.get(key)
                if actual_val is None:
                    all_match = False
                    details.append(f"{key}: MISSING (expected '{expected_val}')")
                elif actual_val != expected_val:
                    all_match = False
                    details.append(f"{key}: '{actual_val}' != '{expected_val}'")
                else:
                    details.append(f"{key}: OK")

            if all_match:
                print(f"PASS: {component_label} -- all properties correct ({points} pts) [{', '.join(details)}]")
                total_score += points
            else:
                print(f"FAIL: {component_label} -- property mismatch ({points} pts) [{', '.join(details)}]")

        except Exception as e:
            print(f"ERROR: {component_label} -- {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
