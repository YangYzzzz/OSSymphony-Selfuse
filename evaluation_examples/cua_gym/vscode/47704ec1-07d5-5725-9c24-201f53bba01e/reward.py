"""
Reward Script: Configure remote development workspace settings
Task ID: vscode_we_040
Domain: vscode
Scoring:
  Component 1 (0.4) — remote.SSH.defaultExtensions == ["ms-python.python", "ms-toolsai.jupyter"]
  Component 2 (0.3) — remote.SSH.connectTimeout == 30
  Component 3 (0.3) — remote.SSH.remotePlatform == {"*": "linux"}
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
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
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

    # Component 1: remote.SSH.defaultExtensions (0.4 points)
    # Task requires: ["ms-python.python", "ms-toolsai.jupyter"]
    try:
        default_ext = settings.get("remote.SSH.defaultExtensions")
        if isinstance(default_ext, list):
            # Check both required extensions are present (order-independent)
            expected_set = {"ms-python.python", "ms-toolsai.jupyter"}
            actual_set = set(default_ext)
            if expected_set == actual_set:
                print(f"PASS: Component 1 — defaultExtensions correct: {default_ext} (0.4 pts)")
                total_score += 0.4
            elif expected_set.issubset(actual_set):
                # Has extra extensions but includes required ones
                print(f"PARTIAL: Component 1 — defaultExtensions has extras: {default_ext} (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 1 — defaultExtensions mismatch. Expected {sorted(expected_set)}, found {default_ext}")
        else:
            print(f"FAIL: Component 1 — remote.SSH.defaultExtensions not found or not a list, found: {default_ext}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: remote.SSH.connectTimeout == 30 (0.3 points)
    try:
        timeout_val = settings.get("remote.SSH.connectTimeout")
        if timeout_val == 30:
            print(f"PASS: Component 2 — connectTimeout is 30 (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — connectTimeout expected 30, found: {timeout_val}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: remote.SSH.remotePlatform == {"*": "linux"} (0.3 points)
    try:
        platform_val = settings.get("remote.SSH.remotePlatform")
        if isinstance(platform_val, dict) and platform_val.get("*") == "linux":
            print(f"PASS: Component 3 — remotePlatform is {platform_val} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — remotePlatform expected {{'*': 'linux'}}, found: {platform_val}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
