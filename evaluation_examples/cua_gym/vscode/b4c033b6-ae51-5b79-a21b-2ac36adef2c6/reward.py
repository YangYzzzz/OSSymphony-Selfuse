"""
Reward Script: Fix SSH config for Remote-SSH extension
Task ID: vscode_fix_048
Domain: vscode
Scoring:
  - Component 1 (0.4): devbox Host block contains an IdentityFile directive
  - Component 2 (0.4): IdentityFile points to ~/.ssh/id_ed25519_work
  - Component 3 (0.2): IdentityFile present AND other devbox config entries preserved (anchored to task change)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_048'
SSH_CONFIG_PATH = os.path.join(WORKDIR, '.ssh', 'config')


def parse_ssh_config(path):
    """
    Parse SSH config file into a dict of host -> dict of directives.
    Each host maps to a dict where keys are lowercase directive names
    and values are the directive values (as strings).
    """
    hosts = {}
    current_host = None

    with open(path, 'r') as f:
        for line in f:
            stripped = line.strip()
            # Skip empty lines and comments
            if not stripped or stripped.startswith('#'):
                continue
            # Match directive lines: "Key Value"
            match = re.match(r'^(\S+)\s+(.+)$', stripped)
            if not match:
                continue
            key = match.group(1)
            value = match.group(2).strip()

            if key.lower() == 'host':
                current_host = value
                hosts[current_host] = {}
            elif current_host is not None:
                hosts[current_host][key.lower()] = value

    return hosts


def verify_task():
    """
    Verify that the SSH config for 'devbox' has been fixed with the correct IdentityFile.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: SSH config file exists
    if not os.path.exists(SSH_CONFIG_PATH):
        print(f"CRITICAL: SSH config file not found at {SSH_CONFIG_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        hosts = parse_ssh_config(SSH_CONFIG_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse SSH config: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: devbox host entry exists
    if 'devbox' not in hosts:
        print("CRITICAL: No 'devbox' Host entry found in SSH config")
        print("REWARD: 0.0")
        return 0.0

    devbox = hosts['devbox']
    print(f"DEBUG: devbox directives = {devbox}")

    # Component 1: devbox has an IdentityFile directive (0.4 points)
    # This is the core task change - initial has no IdentityFile, golden does
    try:
        if 'identityfile' in devbox:
            identity_value = devbox['identityfile']
            print(f"PASS: Component 1 - devbox has IdentityFile directive: '{identity_value}' (0.4 pts)")
            total_score += 0.4
        else:
            print("FAIL: Component 1 - devbox does not have an IdentityFile directive")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: IdentityFile points to the correct key (0.4 points)
    # The task requires ~/.ssh/id_ed25519_work specifically
    try:
        if 'identityfile' in devbox:
            identity_value = devbox['identityfile']
            # Normalize: expand ~ and compare
            normalized = identity_value.replace('~', WORKDIR)
            expected_path = os.path.join(WORKDIR, '.ssh', 'id_ed25519_work')
            if normalized == expected_path or identity_value == '~/.ssh/id_ed25519_work':
                print(f"PASS: Component 2 - IdentityFile correctly points to ~/.ssh/id_ed25519_work (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 - IdentityFile is '{identity_value}', expected '~/.ssh/id_ed25519_work'")
        else:
            print("FAIL: Component 2 - No IdentityFile to check (depends on Component 1)")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: IdentityFile is set AND other devbox config entries are preserved (0.2 points)
    # Anchored to the task change: only awards points if IdentityFile exists (task was done)
    # AND the original directives (HostName, User, Port) are still intact
    try:
        has_identity = 'identityfile' in devbox
        if not has_identity:
            print("FAIL: Component 3 - No IdentityFile present, cannot award preservation points")
        else:
            preserved_count = 0
            expected_preserved = {
                'hostname': '10.128.0.47',
                'user': 'deploy',
                'port': '22',
            }
            for key, expected_val in expected_preserved.items():
                if key in devbox and devbox[key] == expected_val:
                    preserved_count += 1
                else:
                    actual_val = devbox.get(key, '<missing>')
                    print(f"WARN: Component 3 - devbox '{key}' expected '{expected_val}', found '{actual_val}'")

            if preserved_count == len(expected_preserved):
                print(f"PASS: Component 3 - IdentityFile present AND all original directives preserved (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 - Only {preserved_count}/{len(expected_preserved)} original directives preserved")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
