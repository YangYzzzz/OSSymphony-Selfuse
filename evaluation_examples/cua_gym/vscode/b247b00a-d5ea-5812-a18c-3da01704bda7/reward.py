"""
Reward Script: Set tab size to 4 and enable insert spaces in VSCode
Task ID: vscode_we_002
Domain: vscode
Scoring:
  Component 1 (0.5): editor.tabSize == 4
  Component 2 (0.5): editor.insertSpaces == true
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_002'
SETTINGS_PATH = os.path.expanduser('~/.config/Code/User/settings.json')


def load_settings(path):
    """Load VSCode settings.json, handling JSONC comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must exist and be parseable
    if not os.path.exists(SETTINGS_PATH):
        print(f"CRITICAL: Settings file not found: {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        settings = load_settings(SETTINGS_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse settings.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: editor.tabSize == 4 (0.5 points)
    # Initial state has tabSize=2, golden should have tabSize=4
    try:
        tab_size = settings.get('editor.tabSize')
        if tab_size == 4:
            print(f"PASS: Component 1 - editor.tabSize is 4 (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 - editor.tabSize expected 4, found: {tab_size}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: editor.insertSpaces == true (0.5 points)
    # Initial state has insertSpaces=false, golden should have insertSpaces=true
    try:
        insert_spaces = settings.get('editor.insertSpaces')
        if insert_spaces is True:
            print(f"PASS: Component 2 - editor.insertSpaces is true (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 - editor.insertSpaces expected true, found: {insert_spaces}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
