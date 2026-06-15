"""
Reward Script: Configure VSCode to use 4 spaces for indentation
Task ID: vscode_stu_023
Domain: vscode
Scoring:
  Component 1: editor.insertSpaces is true  (0.5 points)
  Component 2: editor.tabSize is 4          (0.5 points)
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
        # Strip single-line comments (JSONC)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify that VSCode is configured to use 4 spaces for indentation.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    # Component 1: editor.insertSpaces is true (0.5 points)
    # Initial state has insertSpaces=false; golden has insertSpaces=true
    try:
        insert_spaces = settings.get("editor.insertSpaces")
        if insert_spaces is True:
            print(f"PASS: Component 1 - editor.insertSpaces is true (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 - editor.insertSpaces expected true, found: {insert_spaces}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: editor.tabSize is 4 (0.5 points)
    # Initial state has tabSize=8; golden has tabSize=4
    try:
        tab_size = settings.get("editor.tabSize")
        if tab_size == 4:
            print(f"PASS: Component 2 - editor.tabSize is 4 (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 - editor.tabSize expected 4, found: {tab_size}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
