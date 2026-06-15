"""
Reward Script: Configure Ruff as linter and formatter for Python workspace
Task ID: vscode_py_015
Domain: vscode
Scoring:
  Component 1 (0.4): python.linting.pylintEnabled set to false
  Component 2 (0.6): [python].editor.defaultFormatter set to charliermarsh.ruff
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
        # Strip JSONC comments (// style)
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

    # Component 1: python.linting.pylintEnabled is false (0.4 points)
    # Initial state has this as true; golden state has false.
    try:
        pylint_enabled = settings.get("python.linting.pylintEnabled")
        if pylint_enabled is False:
            print(f"PASS: Component 1 -- pylintEnabled is false (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 -- expected pylintEnabled=false, found: {pylint_enabled}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: [python].editor.defaultFormatter is charliermarsh.ruff (0.6 points)
    # Initial state has ms-python.black-formatter; golden state has charliermarsh.ruff.
    try:
        python_section = settings.get("[python]", {})
        default_formatter = python_section.get("editor.defaultFormatter")
        if default_formatter == "charliermarsh.ruff":
            print(f"PASS: Component 2 -- defaultFormatter is charliermarsh.ruff (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 2 -- expected defaultFormatter='charliermarsh.ruff', found: {default_formatter}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

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
