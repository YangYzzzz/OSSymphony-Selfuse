"""
Reward Script: Configure VSCode to find Python virtual environments in non-standard locations
Task ID: vscode_fix_051
Domain: vscode
Scoring:
  Component 1 (0.5): python.venvFolders contains '/opt/venvs'
  Component 2 (0.5): python.defaultInterpreterPath set to '/opt/venvs/myproject/bin/python'
"""

import os
import json
import re

HOME = '/home/user'
SETTINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'settings.json')


def load_settings():
    """Load VSCode settings.json, handling JSONC (comments)."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments before parsing
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

    # Component 1: python.venvFolders contains '/opt/venvs' (0.5 points)
    # Initial state: python.venvFolders is [] (empty)
    # Golden state: python.venvFolders includes '/opt/venvs'
    try:
        venv_folders = settings.get('python.venvFolders', [])
        if isinstance(venv_folders, list) and '/opt/venvs' in venv_folders:
            print(f"PASS: Component 1 - python.venvFolders contains '/opt/venvs' (value: {venv_folders}) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 - Expected '/opt/venvs' in python.venvFolders, found: {venv_folders}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: python.defaultInterpreterPath set to '/opt/venvs/myproject/bin/python' (0.5 points)
    # Initial state: python.defaultInterpreterPath is not set
    # Golden state: python.defaultInterpreterPath is '/opt/venvs/myproject/bin/python'
    try:
        interpreter_path = settings.get('python.defaultInterpreterPath', '')
        if interpreter_path == '/opt/venvs/myproject/bin/python':
            print(f"PASS: Component 2 - python.defaultInterpreterPath is correctly set (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 - Expected '/opt/venvs/myproject/bin/python', found: '{interpreter_path}'")
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
