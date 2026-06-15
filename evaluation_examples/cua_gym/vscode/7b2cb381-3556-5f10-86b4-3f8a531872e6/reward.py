"""
Reward Script: Configure ESLint extension for auto-fix on save and onType mode
Task ID: vscode_we_072
Domain: vscode
Scoring:
  Component 1 (0.35): editor.codeActionsOnSave has source.fixAll.eslint = "explicit"
  Component 2 (0.30): eslint.run = "onType"
  Component 3 (0.35): eslint.validate includes all 4 language identifiers
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")
TASK_ID = "vscode_we_072"


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip JSONC comments before parsing
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
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

    # Component 1: editor.codeActionsOnSave contains source.fixAll.eslint = "explicit" (0.35 points)
    try:
        code_actions = settings.get("editor.codeActionsOnSave", {})
        eslint_fix = code_actions.get("source.fixAll.eslint") if isinstance(code_actions, dict) else None
        if eslint_fix == "explicit":
            print(f"PASS: Component 1 — editor.codeActionsOnSave.source.fixAll.eslint = 'explicit' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — expected source.fixAll.eslint = 'explicit', found: {eslint_fix}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: eslint.run = "onType" (0.30 points)
    try:
        eslint_run = settings.get("eslint.run")
        if eslint_run == "onType":
            print(f"PASS: Component 2 — eslint.run = 'onType' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — expected eslint.run = 'onType', found: {eslint_run}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: eslint.validate includes all 4 language identifiers (0.35 points)
    try:
        eslint_validate = settings.get("eslint.validate", [])
        expected_langs = {"javascript", "javascriptreact", "typescript", "typescriptreact"}
        if isinstance(eslint_validate, list):
            actual_langs = set(eslint_validate)
            if expected_langs.issubset(actual_langs):
                print(f"PASS: Component 3 — eslint.validate contains all 4 languages (0.35 pts)")
                total_score += 0.35
            else:
                missing = expected_langs - actual_langs
                print(f"FAIL: Component 3 — eslint.validate missing: {missing}, found: {actual_langs}")
        else:
            print(f"FAIL: Component 3 — eslint.validate is not a list: {type(eslint_validate)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
