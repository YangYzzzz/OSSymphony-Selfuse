"""
Reward Script: Configure VSCode auto-save to onFocusChange
Task ID: vscode_we_026
Domain: vscode
Scoring:
  Component 1 (0.6 pts): files.autoSave == "onFocusChange"
  Component 2 (0.4 pts): files.autoSave is not "afterDelay" (changed from initial)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_026'

SETTINGS_PATH = os.path.expanduser("~/.config/Code/User/settings.json")


def load_settings(path):
    """Load VSCode settings.json, handling JSONC comments."""
    with open(path, "r") as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(cleaned)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must exist and be parseable
    if not os.path.exists(SETTINGS_PATH):
        print(f"CRITICAL: Settings file not found at {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        settings = load_settings(SETTINGS_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse settings.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    auto_save_value = settings.get("files.autoSave")
    print(f"INFO: files.autoSave = {auto_save_value!r}")

    # Component 1: files.autoSave is set to "onFocusChange" (0.6 points)
    # This FAILS on initial (afterDelay) -> PASSES on golden (onFocusChange)
    try:
        if auto_save_value == "onFocusChange":
            print(f"PASS: Component 1 — files.autoSave is 'onFocusChange' (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 — expected 'onFocusChange', found: {auto_save_value!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: files.autoSave is NOT "afterDelay" (0.4 points)
    # This FAILS on initial (afterDelay) -> PASSES on golden (onFocusChange)
    # This checks that the user actually changed the setting away from the initial value
    try:
        if auto_save_value is not None and auto_save_value != "afterDelay":
            print(f"PASS: Component 2 — files.autoSave changed from 'afterDelay' to {auto_save_value!r} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — files.autoSave is still 'afterDelay' or missing")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
