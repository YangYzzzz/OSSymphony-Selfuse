"""
Reward Script: Configure Python extension for virtual environment in VSCode
Task ID: vscode_we_062
Domain: vscode
Scoring:
  - Component 1 (0.30): python.defaultInterpreterPath set correctly
  - Component 2 (0.25): python.testing.pytestEnabled is true
  - Component 3 (0.20): python.testing.unittestEnabled is false
  - Component 4 (0.25): python.analysis.extraPaths contains workspaceFolder/src
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_062'
SETTINGS_PATH = os.path.join(WORKDIR, 'projects', 'myapp', '.vscode', 'settings.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments), stripping // comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (// ...) but not inside strings
    cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(cleaned)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must exist
    if not os.path.exists(SETTINGS_PATH):
        print(f"CRITICAL: settings.json not found at {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Load settings
    try:
        settings = load_jsonc(SETTINGS_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse settings.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: python.defaultInterpreterPath (0.30 points)
    # Expected: "${workspaceFolder}/.venv/bin/python"
    try:
        actual_path = settings.get("python.defaultInterpreterPath")
        expected_path = "${workspaceFolder}/.venv/bin/python"
        if actual_path == expected_path:
            print(f"PASS: Component 1 - python.defaultInterpreterPath = '{actual_path}' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 - Expected '{expected_path}', found '{actual_path}'")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: python.testing.pytestEnabled (0.25 points)
    # Expected: true
    try:
        pytest_enabled = settings.get("python.testing.pytestEnabled")
        if pytest_enabled is True:
            print(f"PASS: Component 2 - python.testing.pytestEnabled = true (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 - Expected true, found {pytest_enabled!r}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: python.testing.unittestEnabled (0.20 points)
    # Expected: false
    try:
        unittest_enabled = settings.get("python.testing.unittestEnabled")
        if unittest_enabled is False:
            print(f"PASS: Component 3 - python.testing.unittestEnabled = false (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 - Expected false, found {unittest_enabled!r}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: python.analysis.extraPaths (0.25 points)
    # Expected: ["${workspaceFolder}/src"]
    try:
        extra_paths = settings.get("python.analysis.extraPaths")
        expected_extra = ["${workspaceFolder}/src"]
        if isinstance(extra_paths, list) and "${workspaceFolder}/src" in extra_paths:
            print(f"PASS: Component 4 - python.analysis.extraPaths contains '${{workspaceFolder}}/src' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 - Expected {expected_extra}, found {extra_paths!r}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
