"""
Reward Script: Set up terminal auto-activation for a Python virtual environment
Task ID: vscode_rrt_076
Domain: vscode
Scoring:
  Component 1 (0.5) - python.defaultInterpreterPath set to "${workspaceFolder}/.venv/bin/python"
  Component 2 (0.3) - python.terminal.activateEnvironment set to true
  Component 3 (0.2) - Original settings preserved (formatOnSave, tabSize, trimTrailingWhitespace)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_076'
WORKSPACE_SETTINGS = os.path.join(WORKDIR, 'projects', 'myapp', '.vscode', 'settings.json')


def load_jsonc(path):
    """Load a JSON file, stripping // comments (JSONC support)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must exist and be valid JSON
    try:
        settings = load_jsonc(WORKSPACE_SETTINGS)
    except FileNotFoundError:
        print(f"CRITICAL: Settings file not found: {WORKSPACE_SETTINGS}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse settings file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: python.defaultInterpreterPath is set correctly (0.5 points)
    # Task requires: "${workspaceFolder}/.venv/bin/python"
    try:
        interpreter_path = settings.get("python.defaultInterpreterPath")
        expected_path = "${workspaceFolder}/.venv/bin/python"
        if interpreter_path == expected_path:
            print(f"PASS: Component 1 - python.defaultInterpreterPath = '{interpreter_path}' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 - Expected python.defaultInterpreterPath = '{expected_path}', found: '{interpreter_path}'")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: python.terminal.activateEnvironment is set to true (0.3 points)
    try:
        activate_env = settings.get("python.terminal.activateEnvironment")
        if activate_env is True:
            print(f"PASS: Component 2 - python.terminal.activateEnvironment = True (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 - Expected python.terminal.activateEnvironment = True, found: {activate_env}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Original workspace settings preserved (0.2 points)
    # The initial settings had formatOnSave, tabSize, trimTrailingWhitespace.
    # We verify these still exist AND the two new python settings are present,
    # ensuring the task was done additively (not by replacing the file).
    try:
        missing = []
        if settings.get("editor.formatOnSave") is not True:
            missing.append("editor.formatOnSave")
        if settings.get("editor.tabSize") != 4:
            missing.append("editor.tabSize")
        if settings.get("files.trimTrailingWhitespace") is not True:
            missing.append("files.trimTrailingWhitespace")

        # This component only scores if BOTH python settings are also present
        # (otherwise it's not measuring a task-introduced quality)
        has_python_settings = (
            settings.get("python.defaultInterpreterPath") is not None
            and settings.get("python.terminal.activateEnvironment") is not None
        )

        if len(missing) == 0 and has_python_settings:
            print(f"PASS: Component 3 - Original settings preserved alongside new python settings (0.2 pts)")
            total_score += 0.2
        elif len(missing) > 0:
            print(f"FAIL: Component 3 - Missing original settings: {missing}")
        else:
            print(f"FAIL: Component 3 - Python settings not yet added, so preservation check not applicable")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
