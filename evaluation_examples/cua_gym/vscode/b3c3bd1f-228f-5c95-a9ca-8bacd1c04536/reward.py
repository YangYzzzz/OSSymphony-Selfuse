"""
Reward Script: Add SSH host 'secure-server' to ~/.ssh/config
Task ID: vscode_rrt_012
Domain: vscode
Scoring:
  - Component 1: Host 'secure-server' entry exists (0.2)
  - Component 2: HostName is secure.example.com (0.2)
  - Component 3: Port is 2222 (0.2)
  - Component 4: User is secops (0.2)
  - Component 5: Compression is yes (0.1)
  - Component 6: Existing host entries preserved (0.1)
"""

import os
import re

SSH_CONFIG_PATH = os.path.expanduser("~/.ssh/config")


def parse_ssh_config(path):
    """
    Parse SSH config into a dict of {host_name: {key: value, ...}}.
    Keys are lowercased for consistent comparison.
    """
    hosts = {}
    current_host = None
    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                # Match Host directive
                match = re.match(r"^Host\s+(.+)$", line, re.IGNORECASE)
                if match:
                    current_host = match.group(1).strip()
                    hosts[current_host] = {}
                    continue
                # Match key-value pairs under a host
                if current_host is not None:
                    kv_match = re.match(r"^(\S+)\s+(.+)$", line)
                    if kv_match:
                        key = kv_match.group(1).strip().lower()
                        value = kv_match.group(2).strip()
                        hosts[current_host][key] = value
    except FileNotFoundError:
        print(f"CRITICAL: SSH config not found at {path}")
    except Exception as e:
        print(f"CRITICAL: Error reading SSH config: {e}")
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

    hosts = parse_ssh_config(SSH_CONFIG_PATH)
    print(f"INFO: Found {len(hosts)} host entries: {list(hosts.keys())}")

    # Component 1: Host entry 'secure-server' exists (0.2 points)
    # This is the task-introduced change -- initial has no 'secure-server'
    try:
        if "secure-server" in hosts:
            print(f"PASS: Component 1 -- Host 'secure-server' entry exists (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- No 'secure-server' host entry found")
            # If host doesn't exist, no point checking its properties
            final_score = min(total_score, 1.0)
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {final_score}")
            return final_score
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    secure = hosts.get("secure-server", {})

    # Component 2: HostName is secure.example.com (0.2 points)
    try:
        hostname_val = secure.get("hostname", "")
        if hostname_val.lower() == "secure.example.com":
            print(f"PASS: Component 2 -- HostName is 'secure.example.com' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 -- Expected HostName 'secure.example.com', found '{hostname_val}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Port is 2222 (0.2 points)
    try:
        port_val = secure.get("port", "")
        if str(port_val).strip() == "2222":
            print(f"PASS: Component 3 -- Port is 2222 (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 -- Expected Port '2222', found '{port_val}'")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: User is secops (0.2 points)
    try:
        user_val = secure.get("user", "")
        if user_val == "secops":
            print(f"PASS: Component 4 -- User is 'secops' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 -- Expected User 'secops', found '{user_val}'")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Compression is yes (0.1 points)
    try:
        compression_val = secure.get("compression", "")
        if compression_val.lower() == "yes":
            print(f"PASS: Component 5 -- Compression is 'yes' (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 5 -- Expected Compression 'yes', found '{compression_val}'")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: Existing host entries preserved (0.1 points)
    # Both 'dev-gateway' and 'staging-db' must still be present
    try:
        preserved = ("dev-gateway" in hosts) and ("staging-db" in hosts)
        if preserved:
            print(f"PASS: Component 6 -- Existing entries 'dev-gateway' and 'staging-db' preserved (0.1 pts)")
            total_score += 0.1
        else:
            missing = []
            if "dev-gateway" not in hosts:
                missing.append("dev-gateway")
            if "staging-db" not in hosts:
                missing.append("staging-db")
            print(f"FAIL: Component 6 -- Missing existing entries: {missing}")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
