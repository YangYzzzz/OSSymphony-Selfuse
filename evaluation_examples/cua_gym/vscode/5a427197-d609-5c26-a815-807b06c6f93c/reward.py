"""
Reward Script: VSCode pre-save code transformation pipeline configuration
Task ID: vscode_gf5_036
Domain: vscode
Scoring:
  Component 1 (0.30): editor.formatOnSave is true
  Component 2 (0.35): editor.codeActionsOnSave includes source.organizeImports
  Component 3 (0.35): [python] section sets defaultFormatter to black
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_036'
SETTINGS_PATH = os.path.join(WORKDIR, 'projects', 'python-lib', '.vscode', 'settings.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments), stripping // comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (// ...) that are NOT inside strings
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip trailing commas before } or ]
    content = re.sub(r',\s*([}\]])', r'\1', content)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must exist and be loadable
    if not os.path.exists(SETTINGS_PATH):
        print(f"CRITICAL: Settings file not found: {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        settings = load_jsonc(SETTINGS_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse settings file: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Loaded settings with {len(settings)} keys")

    # Component 1: editor.formatOnSave is true (0.30 points)
    # This enables the format-on-save pipeline. Must be exactly boolean true.
    try:
        format_on_save = settings.get('editor.formatOnSave')
        if format_on_save is True:
            print(f"PASS: Component 1 - editor.formatOnSave is true (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 - editor.formatOnSave expected true, found: {format_on_save!r}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: editor.codeActionsOnSave includes source.organizeImports (0.35 points)
    # This configures isort to run as a code action on save (organizes imports).
    # The value should be "explicit" or "always" or true — any truthy activation.
    try:
        code_actions = settings.get('editor.codeActionsOnSave')
        if isinstance(code_actions, dict):
            organize_imports = code_actions.get('source.organizeImports')
            # Accept "explicit", "always", or boolean True as valid activation values
            valid_values = ["explicit", "always", True]
            if organize_imports in valid_values:
                print(f"PASS: Component 2 - source.organizeImports = {organize_imports!r} (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 - source.organizeImports = {organize_imports!r}, expected one of {valid_values}")
        else:
            print(f"FAIL: Component 2 - editor.codeActionsOnSave not found or not a dict, found: {code_actions!r}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: [python] section sets defaultFormatter to ms-python.black-formatter (0.35 points)
    # This makes black the formatter for Python files specifically.
    try:
        python_section = settings.get('[python]')
        if isinstance(python_section, dict):
            formatter = python_section.get('editor.defaultFormatter')
            if formatter == 'ms-python.black-formatter':
                print(f"PASS: Component 3 - [python] defaultFormatter = 'ms-python.black-formatter' (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 3 - [python] defaultFormatter = {formatter!r}, expected 'ms-python.black-formatter'")
        else:
            print(f"FAIL: Component 3 - [python] section not found or not a dict, found: {python_section!r}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
