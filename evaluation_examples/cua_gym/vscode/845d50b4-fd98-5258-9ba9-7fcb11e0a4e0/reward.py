"""
Reward Script: Configure language-specific Python settings in VSCode
Task ID: vscode_we_015
Domain: vscode
Scoring:
  - Component 1 (0.35): [python] editor.tabSize == 4
  - Component 2 (0.35): [python] editor.formatOnSave == true
  - Component 3 (0.30): [python] editor.defaultFormatter == "ms-python.black-formatter"
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_015'
SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_settings(path):
    """Load VSCode settings.json, handling JSONC (comments)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify that language-specific Python settings are configured.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must exist and be parseable
    try:
        settings = load_settings(SETTINGS_PATH)
    except FileNotFoundError:
        print(f"CRITICAL: settings.json not found at {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse settings.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get the [python] language-specific block
    python_block = settings.get("[python]", None)
    if not isinstance(python_block, dict):
        print(f"FAIL: No [python] language-specific block found in settings.json")
        print(f"  Available keys: {list(settings.keys())}")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found [python] block with keys: {list(python_block.keys())}")

    # Component 1: [python] editor.tabSize == 4 (0.35 points)
    try:
        tab_size = python_block.get("editor.tabSize", None)
        if tab_size == 4:
            print(f"PASS: Component 1 -- [python] editor.tabSize is 4 (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 -- [python] editor.tabSize expected 4, found: {tab_size}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: [python] editor.formatOnSave == true (0.35 points)
    try:
        format_on_save = python_block.get("editor.formatOnSave", None)
        if format_on_save is True:
            print(f"PASS: Component 2 -- [python] editor.formatOnSave is true (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 -- [python] editor.formatOnSave expected true, found: {format_on_save}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: [python] editor.defaultFormatter == "ms-python.black-formatter" (0.30 points)
    try:
        formatter = python_block.get("editor.defaultFormatter", None)
        if formatter == "ms-python.black-formatter":
            print(f"PASS: Component 3 -- [python] editor.defaultFormatter is 'ms-python.black-formatter' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 -- [python] editor.defaultFormatter expected 'ms-python.black-formatter', found: {formatter}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
