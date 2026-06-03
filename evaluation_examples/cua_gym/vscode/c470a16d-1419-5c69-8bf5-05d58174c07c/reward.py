"""
Reward Script: Configure ESLint + Prettier in VSCode workspace settings
Task ID: vscode_gf3_054
Domain: vs_code
Scoring:
  - Component 1: editor.formatOnSave is true (0.2)
  - Component 2: editor.codeActionsOnSave includes source.fixAll.eslint (0.2)
  - Component 3: [javascript] defaultFormatter is esbenp.prettier-vscode (0.2)
  - Component 4: [typescript] defaultFormatter is esbenp.prettier-vscode (0.2)
  - Component 5: eslint.validate includes all 4 language IDs (0.2)
"""

import json
import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_054'
SETTINGS_PATH = '/home/user/projects/react-app/.vscode/settings.json'


def load_jsonc(path):
    """Load a JSONC file (JSON with Comments) by stripping comments first."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip multi-line comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return json.loads(content)


def verify_task(settings_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        settings = load_jsonc(settings_path)
    except FileNotFoundError:
        print(f"CRITICAL: Settings file not found: {settings_path}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse settings file {settings_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: editor.formatOnSave is true (0.2 points)
    try:
        format_on_save = settings.get("editor.formatOnSave")
        if format_on_save is True:
            print(f"PASS: Component 1 — editor.formatOnSave is true (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — editor.formatOnSave expected true, found: {format_on_save}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: editor.codeActionsOnSave includes source.fixAll.eslint (0.2 points)
    try:
        code_actions = settings.get("editor.codeActionsOnSave", {})
        if isinstance(code_actions, dict):
            eslint_fix = code_actions.get("source.fixAll.eslint")
            # Accept both True (boolean) and "explicit" (string, newer VSCode format)
            if eslint_fix is True or eslint_fix == "explicit":
                print(f"PASS: Component 2 — source.fixAll.eslint is enabled (value: {eslint_fix}) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — source.fixAll.eslint expected true/explicit, found: {eslint_fix}")
        else:
            print(f"FAIL: Component 2 — editor.codeActionsOnSave is not a dict: {type(code_actions)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: [javascript] defaultFormatter is esbenp.prettier-vscode (0.2 points)
    try:
        js_settings = settings.get("[javascript]", {})
        js_formatter = js_settings.get("editor.defaultFormatter", "") if isinstance(js_settings, dict) else ""
        if js_formatter == "esbenp.prettier-vscode":
            print(f"PASS: Component 3 — [javascript] defaultFormatter is esbenp.prettier-vscode (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — [javascript] defaultFormatter expected 'esbenp.prettier-vscode', found: '{js_formatter}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: [typescript] defaultFormatter is esbenp.prettier-vscode (0.2 points)
    try:
        ts_settings = settings.get("[typescript]", {})
        ts_formatter = ts_settings.get("editor.defaultFormatter", "") if isinstance(ts_settings, dict) else ""
        if ts_formatter == "esbenp.prettier-vscode":
            print(f"PASS: Component 4 — [typescript] defaultFormatter is esbenp.prettier-vscode (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — [typescript] defaultFormatter expected 'esbenp.prettier-vscode', found: '{ts_formatter}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: eslint.validate includes all 4 language IDs (0.2 points)
    try:
        eslint_validate = settings.get("eslint.validate", [])
        required_langs = {"javascript", "javascriptreact", "typescript", "typescriptreact"}
        if isinstance(eslint_validate, list):
            actual_langs = set(eslint_validate)
            missing = required_langs - actual_langs
            if not missing:
                print(f"PASS: Component 5 — eslint.validate contains all 4 languages (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 5 — eslint.validate missing: {missing}, found: {actual_langs}")
        else:
            print(f"FAIL: Component 5 — eslint.validate is not a list: {type(eslint_validate)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(SETTINGS_PATH)
