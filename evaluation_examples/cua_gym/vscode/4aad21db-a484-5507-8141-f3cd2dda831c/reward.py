"""
Reward Script: Change multi-cursor modifier from Alt to Ctrl
Task ID: vscode_fix_080
Domain: vscode
Scoring:
  Component 1 (0.7): editor.multiCursorModifier is set to 'ctrlCmd'
  Component 2 (0.3): Setting changed AND other settings preserved intact
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")
TASK_ID = "vscode_fix_080"


def load_settings_jsonc(path):
    """Load settings.json, stripping JSONC comments if present."""
    with open(path, "r") as f:
        content = f.read()
    # Strip single-line // comments (JSONC support)
    cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(cleaned)


def verify_task():
    """
    Verify that editor.multiCursorModifier has been changed to 'ctrlCmd'.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must exist and be valid JSON
    if not os.path.exists(SETTINGS_PATH):
        print(f"CRITICAL: Settings file not found at {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        settings = load_settings_jsonc(SETTINGS_PATH)
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse settings.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: editor.multiCursorModifier is 'ctrlCmd' (0.7 points)
    # This is the core task requirement. In initial_env it is 'alt', so this
    # component correctly FAILS on initial and PASSES on golden.
    try:
        modifier_value = settings.get("editor.multiCursorModifier")
        if modifier_value == "ctrlCmd":
            print(f"PASS: Component 1 — editor.multiCursorModifier is 'ctrlCmd' (0.7 pts)")
            total_score += 0.7
        else:
            print(f"FAIL: Component 1 — expected 'ctrlCmd', found: {modifier_value!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Setting changed AND other pre-existing settings preserved (0.3 points)
    # This is a compound check anchored to the task change. It ensures the agent
    # didn't break the file while making the change. Only awards points if
    # Component 1 also passed (modifier is 'ctrlCmd'), so it returns 0 on initial_env.
    try:
        if settings.get("editor.multiCursorModifier") == "ctrlCmd":
            # Verify that key pre-existing settings are still intact
            expected_preserved = {
                "editor.fontSize": 14,
                "editor.tabSize": 4,
                "workbench.colorTheme": "Default Dark Modern",
                "files.autoSave": "afterDelay",
            }
            mismatches = []
            for key, expected_val in expected_preserved.items():
                actual_val = settings.get(key)
                if actual_val != expected_val:
                    print(f"  WARN: {key} expected {expected_val!r}, found {actual_val!r}")
                    mismatches.append(key)

            if len(mismatches) == 0:
                print(f"PASS: Component 2 — modifier changed AND other settings preserved (0.3 pts)")
                total_score += 0.3
            else:
                print(f"PARTIAL FAIL: Component 2 — modifier correct but some settings changed")
        else:
            print(f"FAIL: Component 2 — modifier not 'ctrlCmd', skipping preservation check")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
