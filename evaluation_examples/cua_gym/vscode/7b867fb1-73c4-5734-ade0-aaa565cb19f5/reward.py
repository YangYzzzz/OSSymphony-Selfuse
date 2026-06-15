"""
Reward Script: Configure VSCode format-on-save with autopep8
Task ID: vscode_stu_043
Domain: vscode
Scoring:
  Component 1 (0.5): editor.formatOnSave is true
  Component 2 (0.5): python.formatting.provider is "autopep8"
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
        # Strip // comments (JSONC)
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

    # Component 1: editor.formatOnSave is true (0.5 points)
    # Initial state has this as false; golden state has it as true.
    try:
        format_on_save = settings.get("editor.formatOnSave")
        if format_on_save is True:
            print(f"PASS: Component 1 - editor.formatOnSave is true (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 - editor.formatOnSave expected true, found: {format_on_save}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: python.formatting.provider is "autopep8" (0.5 points)
    # Initial state does not have this key; golden state sets it to "autopep8".
    try:
        formatter = settings.get("python.formatting.provider")
        if isinstance(formatter, str) and formatter.lower() == "autopep8":
            print(f"PASS: Component 2 - python.formatting.provider is autopep8 (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 - python.formatting.provider expected 'autopep8', found: {formatter}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
