"""
Reward Script: Enable word wrap in VSCode
Task ID: vscode_stu_006
Domain: vscode
Scoring:
  - Component 1 (0.6): editor.wordWrap is set to "on"
  - Component 2 (0.4): editor.wordWrap is not "off" (catches alternate valid values like "bounded", "wordWrapColumn")
    BUT only full credit if exactly "on"
"""

import os
import json
import re

HOME = '/home/user'
SETTINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'settings.json')
TASK_ID = 'vscode_stu_006'


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip single-line comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify that editor.wordWrap has been changed from 'off' to 'on'.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("CRITICAL: settings.json not found or unreadable")
        print("REWARD: 0.0")
        return 0.0

    word_wrap_value = settings.get('editor.wordWrap', None)
    print(f"INFO: editor.wordWrap = {word_wrap_value!r}")

    # Component 1: editor.wordWrap exists and is exactly "on" (0.6 points)
    # Initial state has "off", golden should have "on"
    try:
        if word_wrap_value == 'on':
            print(f"PASS: Component 1 — editor.wordWrap is 'on' (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 — expected 'on', found {word_wrap_value!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: editor.wordWrap is no longer "off" (0.4 points)
    # This catches the case where the user changed it but to a different valid value
    # Only awards points if the value actually changed from the initial "off"
    try:
        if word_wrap_value is not None and word_wrap_value != 'off':
            print(f"PASS: Component 2 — editor.wordWrap is not 'off' (value: {word_wrap_value!r}) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — editor.wordWrap is still 'off' or missing")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
