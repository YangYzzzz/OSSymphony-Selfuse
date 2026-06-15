"""
Reward Script: Configure VSCode to organize imports on save
Task ID: vscode_stu_093
Domain: vscode
Scoring:
  Component 1 (0.4): editor.codeActionsOnSave key exists and is a dict
  Component 2 (0.6): source.organizeImports is set to boolean true
"""

import os
import json
import re

HOME = '/home/user'
SETTINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'settings.json')
TASK_ID = 'vscode_stu_093'


def load_settings(path):
    """Load VSCode settings.json, handling JSONC comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip JSONC comments (// style)
    stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(stripped)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must exist and be parseable
    try:
        settings = load_settings(SETTINGS_PATH)
    except FileNotFoundError:
        print(f"CRITICAL: Settings file not found: {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse settings file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: editor.codeActionsOnSave key exists and is a dict (0.4 points)
    # This key does NOT exist in initial_env, so it discriminates correctly.
    try:
        code_actions = settings.get('editor.codeActionsOnSave')
        if isinstance(code_actions, dict):
            print(f"PASS: Component 1 — editor.codeActionsOnSave exists and is a dict (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — editor.codeActionsOnSave missing or not a dict, found: {code_actions}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: source.organizeImports is set to boolean true (0.6 points)
    # This is the core task requirement. Must be exactly True (boolean), not "true" (string).
    try:
        code_actions = settings.get('editor.codeActionsOnSave', {})
        if isinstance(code_actions, dict):
            organize_val = code_actions.get('source.organizeImports')
            if organize_val is True:
                print(f"PASS: Component 2 — source.organizeImports is true (0.6 pts)")
                total_score += 0.6
            elif organize_val == "explicit" or organize_val == "always":
                # VSCode also accepts string values like "explicit" or "always" as valid
                print(f"PASS: Component 2 — source.organizeImports is '{organize_val}' (accepted) (0.6 pts)")
                total_score += 0.6
            else:
                print(f"FAIL: Component 2 — source.organizeImports expected true, found: {organize_val} (type: {type(organize_val).__name__})")
        else:
            print(f"FAIL: Component 2 — editor.codeActionsOnSave is not a dict, cannot check source.organizeImports")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(SETTINGS_PATH):
    print(f"Settings file not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
