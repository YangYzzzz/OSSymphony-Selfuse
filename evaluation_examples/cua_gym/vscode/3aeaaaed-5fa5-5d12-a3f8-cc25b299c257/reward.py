"""
Reward Script: VSCode terminal profile configuration
Task ID: vscode_we_035
Domain: vscode
Scoring:
  Component 1: bash profile with path /bin/bash (0.25)
  Component 2: node profile with path /usr/bin/node (0.25)
  Component 3: node profile has --interactive arg (0.25)
  Component 4: default profile set to bash (0.25)
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip // comments (VSCode uses JSONC)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    profiles = settings.get("terminal.integrated.profiles.linux", {})
    if not isinstance(profiles, dict):
        profiles = {}

    # Component 1: bash profile with path /bin/bash (0.25 points)
    try:
        bash_profile = profiles.get("bash", {})
        if isinstance(bash_profile, dict) and bash_profile.get("path") == "/bin/bash":
            print(f"PASS: Component 1 — bash profile has path /bin/bash (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — expected bash profile with path /bin/bash, found: {bash_profile}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: node profile with path /usr/bin/node (0.25 points)
    try:
        node_profile = profiles.get("node", {})
        if isinstance(node_profile, dict) and node_profile.get("path") == "/usr/bin/node":
            print(f"PASS: Component 2 — node profile has path /usr/bin/node (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — expected node profile with path /usr/bin/node, found: {node_profile}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: node profile has --interactive arg (0.25 points)
    try:
        node_profile = profiles.get("node", {})
        if isinstance(node_profile, dict):
            args = node_profile.get("args", [])
            if isinstance(args, list) and "--interactive" in args:
                print(f"PASS: Component 3 — node profile has --interactive arg (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — expected args containing --interactive, found: {args}")
        else:
            print(f"FAIL: Component 3 — node profile not a dict: {node_profile}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: default terminal profile set to bash (0.25 points)
    try:
        default_profile = settings.get("terminal.integrated.defaultProfile.linux")
        if default_profile == "bash":
            print(f"PASS: Component 4 — default profile is bash (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — expected defaultProfile.linux = 'bash', found: {default_profile}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
