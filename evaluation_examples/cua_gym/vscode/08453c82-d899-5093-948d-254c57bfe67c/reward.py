"""
Reward Script: Configure VSCode to auto-fix ESLint issues on save
Task ID: vscode_web_003
Domain: vscode
Scoring:
  Component 1 (0.4): .vscode/settings.json exists and is valid JSON
  Component 2 (0.3): Contains editor.codeActionsOnSave key
  Component 3 (0.3): source.fixAll.eslint set to "explicit" or true
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_003'
SETTINGS_PATH = os.path.join(WORKDIR, 'projects', 'webapp', '.vscode', 'settings.json')


def load_jsonc(file_path):
    """Load a JSON file, stripping JSONC comments if present."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments (// ...)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: .vscode/settings.json exists and is valid JSON (0.4 points)
    # This FAILS on initial (no .vscode dir) and PASSES on golden
    settings = None
    try:
        if os.path.isfile(SETTINGS_PATH):
            settings = load_jsonc(SETTINGS_PATH)
            if isinstance(settings, dict):
                print(f"PASS: Component 1 - settings.json exists and is valid JSON (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 - settings.json is not a JSON object, got {type(settings).__name__}")
        else:
            print(f"FAIL: Component 1 - settings.json not found at {SETTINGS_PATH}")
    except (json.JSONDecodeError, Exception) as e:
        print(f"ERROR: Component 1 - Could not parse settings.json: {e}")

    if settings is None or not isinstance(settings, dict):
        # Cannot proceed without valid settings
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Contains editor.codeActionsOnSave key (0.3 points)
    # This FAILS on initial (file doesn't exist) and PASSES on golden
    try:
        code_actions = settings.get('editor.codeActionsOnSave')
        if isinstance(code_actions, dict):
            print(f"PASS: Component 2 - editor.codeActionsOnSave found: {code_actions} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 - editor.codeActionsOnSave not found or not a dict, got: {code_actions}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: source.fixAll.eslint is "explicit" or true (0.3 points)
    # This FAILS on initial (file doesn't exist) and PASSES on golden
    try:
        code_actions = settings.get('editor.codeActionsOnSave', {})
        if isinstance(code_actions, dict):
            eslint_value = code_actions.get('source.fixAll.eslint')
            # Accept "explicit" (string) or True (boolean) as valid values
            if eslint_value == 'explicit' or eslint_value is True:
                print(f"PASS: Component 3 - source.fixAll.eslint = {eslint_value!r} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 - source.fixAll.eslint = {eslint_value!r}, expected 'explicit' or true")
        else:
            print(f"FAIL: Component 3 - editor.codeActionsOnSave is not a dict")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
