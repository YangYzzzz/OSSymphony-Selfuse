"""
Reward Script: Configure SSH multiplexing for faster reconnections
Task ID: vscode_rrt_016
Domain: vscode (OS/SSH config)
Scoring:
  - Precondition gate: Original host entries must be preserved (no points, but 0.0 if broken)
  - Component 1: Host * block exists in ~/.ssh/config (0.15 pts)
  - Component 2: ControlMaster auto directive present (0.25 pts)
  - Component 3: ControlPath ~/.ssh/sockets/%r@%h-%p directive present (0.25 pts)
  - Component 4: ControlPersist 600 directive present (0.2 pts)
  - Component 5: ~/.ssh/sockets/ directory exists (0.15 pts)
"""

import os
import re

HOME = os.path.expanduser("~")
SSH_CONFIG = os.path.join(HOME, ".ssh", "config")
SOCKETS_DIR = os.path.join(HOME, ".ssh", "sockets")

# The three original host entries that must be preserved
ORIGINAL_HOSTS = ["dev-server", "staging-bastion", "prod-db"]


def parse_ssh_config(config_text):
    """Parse SSH config into a dict of {host_pattern: {directive: value}}."""
    hosts = {}
    current_host = None
    for line in config_text.splitlines():
        stripped = line.strip()
        # Skip comments and empty lines
        if not stripped or stripped.startswith("#"):
            continue
        # Check for Host directive
        host_match = re.match(r'^Host\s+(.+)$', stripped, re.IGNORECASE)
        if host_match:
            current_host = host_match.group(1).strip()
            hosts[current_host] = {}
            continue
        # Parse key-value directives under a host block
        if current_host is not None:
            kv_match = re.match(r'^(\S+)\s+(.+)$', stripped)
            if kv_match:
                key = kv_match.group(1)
                value = kv_match.group(2).strip()
                hosts[current_host][key] = value
    return hosts


def verify_task():
    """
    Verify SSH multiplexing configuration.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: SSH config file must exist
    if not os.path.exists(SSH_CONFIG):
        print(f"CRITICAL: SSH config not found at {SSH_CONFIG}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(SSH_CONFIG, "r") as f:
            config_text = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read {SSH_CONFIG}: {e}")
        print("REWARD: 0.0")
        return 0.0

    hosts = parse_ssh_config(config_text)

    # Precondition gate: Original host entries must be preserved (no points)
    try:
        missing_hosts = [h for h in ORIGINAL_HOSTS if h not in hosts]
        if missing_hosts:
            print(f"PRECONDITION FAIL: Original hosts missing: {missing_hosts}. Returning 0.0.")
            print("REWARD: 0.0")
            return 0.0
        else:
            print(f"PRECONDITION OK: All {len(ORIGINAL_HOSTS)} original host entries preserved")
    except Exception as e:
        print(f"ERROR: Precondition check -- {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Host * block exists (0.15 points)
    try:
        if "*" in hosts:
            print(f"PASS: Component 1 -- Host * block exists (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- No Host * block found. Found hosts: {list(hosts.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: ControlMaster auto (0.25 points)
    try:
        wildcard = hosts.get("*", {})
        cm_value = wildcard.get("ControlMaster", "")
        if cm_value.lower() == "auto":
            print(f"PASS: Component 2 -- ControlMaster is 'auto' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- ControlMaster expected 'auto', found: '{cm_value}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: ControlPath ~/.ssh/sockets/%r@%h-%p (0.25 points)
    try:
        wildcard = hosts.get("*", {})
        cp_value = wildcard.get("ControlPath", "")
        expected_path = "~/.ssh/sockets/%r@%h-%p"
        if cp_value == expected_path:
            print(f"PASS: Component 3 -- ControlPath is '{expected_path}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 -- ControlPath expected '{expected_path}', found: '{cp_value}'")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: ControlPersist 600 (0.2 points)
    try:
        wildcard = hosts.get("*", {})
        persist_value = wildcard.get("ControlPersist", "")
        if persist_value == "600":
            print(f"PASS: Component 4 -- ControlPersist is '600' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 -- ControlPersist expected '600', found: '{persist_value}'")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: ~/.ssh/sockets/ directory exists (0.15 points)
    try:
        if os.path.isdir(SOCKETS_DIR):
            print(f"PASS: Component 5 -- {SOCKETS_DIR} directory exists (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 -- {SOCKETS_DIR} does not exist or is not a directory")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
