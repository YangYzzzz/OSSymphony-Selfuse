"""
Reward Script: Select Python interpreter from virtual environment
Task ID: vscode_stu_040
Domain: vscode
Scoring:
  Component 1 (0.5): python.defaultInterpreterPath is set to the venv path
  Component 2 (0.5): The path specifically references cs101/venv and is not the system default
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_040'

# The expected interpreter path (expanded)
EXPECTED_PATH = os.path.join(WORKDIR, 'cs101', 'venv', 'bin', 'python3')
# Also accept the tilde form
EXPECTED_PATH_TILDE = '~/cs101/venv/bin/python3'

SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_settings(path):
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments (JSONC)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings from {path}: {e}")
        return None


def verify_task():
    """
    Verify that the Python interpreter is set to ~/cs101/venv/bin/python3 in VSCode.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load settings
    settings = load_settings(SETTINGS_PATH)
    if settings is None:
        print("CRITICAL: Cannot load VSCode settings.json")
        print("REWARD: 0.0")
        return 0.0

    # Get the actual interpreter path
    actual_path = settings.get('python.defaultInterpreterPath', '')
    print(f"INFO: python.defaultInterpreterPath = '{actual_path}'")

    # Normalize: expand ~ to /home/user
    normalized_actual = actual_path.replace('~', WORKDIR) if actual_path else ''

    # Component 1: python.defaultInterpreterPath contains the venv path (0.5 points)
    # This checks that the setting references the cs101/venv interpreter
    try:
        if normalized_actual == EXPECTED_PATH:
            print(f"PASS: Component 1 - Interpreter path matches {EXPECTED_PATH} (0.5 pts)")
            total_score += 0.5
        elif actual_path == EXPECTED_PATH_TILDE:
            print(f"PASS: Component 1 - Interpreter path matches {EXPECTED_PATH_TILDE} (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 - Expected '{EXPECTED_PATH}' or '{EXPECTED_PATH_TILDE}', found '{actual_path}'")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: The path is NOT the default system Python (0.5 points)
    # The initial state has /usr/bin/python3 as the default. The task asks to change it.
    # This component verifies the change was actually made away from the default.
    try:
        system_defaults = ['/usr/bin/python3', '/usr/bin/python', 'python3', 'python', '']
        if actual_path not in system_defaults and 'cs101/venv' in normalized_actual:
            print(f"PASS: Component 2 - Path is not system default and references cs101/venv (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 - Path is system default or does not reference cs101/venv: '{actual_path}'")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
