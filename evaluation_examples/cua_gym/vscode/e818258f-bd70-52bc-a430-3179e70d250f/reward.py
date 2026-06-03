"""
Reward Script: Configure Remote-SSH showLoginTerminal and ForwardAgent for git-server
Task ID: vscode_rrt_013
Domain: vscode
Scoring:
  Component 1 (0.50): remote.SSH.showLoginTerminal is true in VSCode settings
  Component 2 (0.35): ForwardAgent yes in SSH config for Host git-server
  Component 3 (0.15): Other git-server config values unchanged
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")
SSH_CONFIG_PATH = os.path.join(HOME, ".ssh", "config")


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings.json: {e}")
        return None


def parse_ssh_config(path):
    """Parse SSH config into a dict of {host: {key: value, ...}}."""
    hosts = {}
    current_host = None
    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                # Match Host directive
                m = re.match(r'^Host\s+(.+)$', line, re.IGNORECASE)
                if m:
                    current_host = m.group(1).strip()
                    hosts[current_host] = {}
                    continue
                # Match key-value pairs under a host
                if current_host is not None:
                    m = re.match(r'^(\S+)\s+(.+)$', line)
                    if m:
                        key = m.group(1)
                        value = m.group(2).strip()
                        hosts[current_host][key] = value
    except FileNotFoundError as e:
        print(f"ERROR: Cannot read SSH config: {e}")
        return None
    return hosts


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: remote.SSH.showLoginTerminal is true (0.50 points)
    try:
        settings = load_settings()
        if settings is None:
            print("FAIL: Component 1 — Could not load settings.json")
        else:
            val = settings.get("remote.SSH.showLoginTerminal")
            if val is True:
                print(f"PASS: Component 1 — remote.SSH.showLoginTerminal is true (0.50 pts)")
                total_score += 0.50
            else:
                print(f"FAIL: Component 1 — remote.SSH.showLoginTerminal expected true, found: {val}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: ForwardAgent yes in SSH config for Host git-server (0.35 points)
    try:
        hosts = parse_ssh_config(SSH_CONFIG_PATH)
        if hosts is None:
            print("FAIL: Component 2 — Could not parse SSH config")
        elif "git-server" not in hosts:
            print("FAIL: Component 2 — Host 'git-server' not found in SSH config")
        else:
            git_server = hosts["git-server"]
            forward_agent = git_server.get("ForwardAgent", "").lower()
            if forward_agent == "yes":
                print(f"PASS: Component 2 — ForwardAgent yes found for git-server (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 — ForwardAgent expected 'yes', found: '{git_server.get('ForwardAgent', '<missing>')}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Other git-server values remain unchanged (0.15 points)
    # Expected: HostName git.internal.co, User gitadmin, IdentityFile ~/.ssh/id_rsa, Port 22
    try:
        hosts = parse_ssh_config(SSH_CONFIG_PATH)
        if hosts is None or "git-server" not in hosts:
            print("FAIL: Component 3 — Cannot verify git-server config integrity")
        else:
            gs = hosts["git-server"]
            expected_unchanged = {
                "HostName": "git.internal.co",
                "User": "gitadmin",
                "IdentityFile": "~/.ssh/id_rsa",
                "Port": "22",
            }
            # Only award points if ForwardAgent is also present (task change happened)
            forward_agent = gs.get("ForwardAgent", "").lower()
            if forward_agent != "yes":
                print("FAIL: Component 3 — ForwardAgent not set; skipping integrity check (no task change)")
            else:
                mismatches = []
                for key, exp_val in expected_unchanged.items():
                    actual_val = gs.get(key, "<missing>")
                    if actual_val != exp_val:
                        mismatches.append(f"{key}: expected '{exp_val}', found '{actual_val}'")
                if len(mismatches) == 0:
                    print(f"PASS: Component 3 — All other git-server values intact (0.15 pts)")
                    total_score += 0.15
                else:
                    for m in mismatches:
                        print(f"FAIL: Component 3 — git-server {m}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
