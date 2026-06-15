"""
Reward Script: Turn on line numbers in VSCode editor
Task ID: vscode_stu_021
Domain: vscode
Scoring:
  - Component 1 (0.6): editor.lineNumbers is set to "on"
  - Component 2 (0.4): editor.lineNumbers is not "off" (catches partial states like "relative")
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
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify that editor.lineNumbers has been set to 'on'.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    line_numbers_value = settings.get("editor.lineNumbers")
    print(f"INFO: editor.lineNumbers = {line_numbers_value!r}")

    # Component 1: editor.lineNumbers is exactly "on" (0.6 points)
    # FAILS on initial (value is "off") -> PASSES on golden (value is "on")
    try:
        if isinstance(line_numbers_value, str) and line_numbers_value.lower() == "on":
            print(f"PASS: Component 1 - editor.lineNumbers is 'on' (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 - expected 'on', found: {line_numbers_value!r}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: editor.lineNumbers is not "off" (0.4 points)
    # FAILS on initial (value is "off") -> PASSES on golden (value is "on")
    try:
        if isinstance(line_numbers_value, str) and line_numbers_value.lower() != "off":
            print(f"PASS: Component 2 - editor.lineNumbers is not 'off' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 - editor.lineNumbers is still 'off' or missing")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
