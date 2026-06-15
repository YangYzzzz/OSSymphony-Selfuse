"""
Reward Script: Configure multiple Python linters (flake8 + mypy)
Task ID: vscode_py_065
Domain: vscode
Scoring:
  Component 1 (0.35): pylintEnabled is disabled (false)
  Component 2 (0.35): flake8Enabled is enabled (true)
  Component 3 (0.30): mypyEnabled is enabled (true)
  Total: 1.0
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
        # Strip single-line comments (JSONC)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify that Python linters are configured correctly:
    - pylint disabled
    - flake8 enabled
    - mypy enabled
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    # Component 1: pylintEnabled is disabled (0.35 points)
    # Initial state has pylintEnabled=true, golden has it false.
    try:
        pylint_enabled = settings.get('python.linting.pylintEnabled')
        if pylint_enabled is False:
            print(f"PASS: Component 1 -- pylintEnabled is false (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 -- expected pylintEnabled=false, found: {pylint_enabled}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: flake8Enabled is enabled (0.35 points)
    # Initial state has flake8Enabled=false, golden has it true.
    try:
        flake8_enabled = settings.get('python.linting.flake8Enabled')
        if flake8_enabled is True:
            print(f"PASS: Component 2 -- flake8Enabled is true (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 -- expected flake8Enabled=true, found: {flake8_enabled}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: mypyEnabled is enabled (0.30 points)
    # Initial state has mypyEnabled=false, golden has it true.
    try:
        mypy_enabled = settings.get('python.linting.mypyEnabled')
        if mypy_enabled is True:
            print(f"PASS: Component 3 -- mypyEnabled is true (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 -- expected mypyEnabled=true, found: {mypy_enabled}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
