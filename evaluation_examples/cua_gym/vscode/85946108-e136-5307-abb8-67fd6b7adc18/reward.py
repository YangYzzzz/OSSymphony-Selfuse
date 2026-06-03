"""
Reward Script: Configure VSCode to auto-activate Python virtual environment
Task ID: vscode_py_024
Domain: vscode
Scoring:
  - Component 1 (0.6): python.terminal.activateEnvironment is true in global settings
  - Component 2 (0.4): python.terminal.activateEnvironment is true in any valid location
"""

import os
import json
import re

HOME = '/home/user'
GLOBAL_SETTINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'settings.json')
WORKSPACE_SETTINGS_PATH = os.path.join(HOME, 'workspace', '.vscode', 'settings.json')

TARGET_KEY = 'python.terminal.activateEnvironment'


def load_jsonc(path):
    """Load a JSON/JSONC file, stripping // comments."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip // comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"  Could not load {path}: {e}")
        return None


def check_setting_in_file(path, key):
    """Check if a setting key exists and has value True in a JSON settings file."""
    data = load_jsonc(path)
    if data is None:
        return False, None
    if key in data:
        return True, data[key]
    return False, None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: python.terminal.activateEnvironment is true in global settings (0.6 points)
    # This is the primary expected location for this setting.
    try:
        found, value = check_setting_in_file(GLOBAL_SETTINGS_PATH, TARGET_KEY)
        if found and value is True:
            print(f"PASS: Component 1 — {TARGET_KEY} is true in global settings (0.6 pts)")
            total_score += 0.6
        elif found:
            print(f"FAIL: Component 1 — {TARGET_KEY} exists but value is {value!r} (expected true)")
        else:
            print(f"FAIL: Component 1 — {TARGET_KEY} not found in global settings at {GLOBAL_SETTINGS_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: python.terminal.activateEnvironment is true in ANY valid location (0.4 points)
    # The setting can be in global settings OR workspace settings — either is valid.
    try:
        global_found, global_val = check_setting_in_file(GLOBAL_SETTINGS_PATH, TARGET_KEY)
        ws_found, ws_val = check_setting_in_file(WORKSPACE_SETTINGS_PATH, TARGET_KEY)

        global_ok = global_found and global_val is True
        ws_ok = ws_found and ws_val is True

        if global_ok or ws_ok:
            location = "global" if global_ok else "workspace"
            print(f"PASS: Component 2 — {TARGET_KEY} is true in {location} settings (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — {TARGET_KEY} not set to true in any settings file")
            if global_found:
                print(f"  Global has key but value={global_val!r}")
            if ws_found:
                print(f"  Workspace has key but value={ws_val!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
