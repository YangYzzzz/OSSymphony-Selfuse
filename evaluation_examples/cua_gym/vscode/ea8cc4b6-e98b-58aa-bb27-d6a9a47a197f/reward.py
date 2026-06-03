"""
Reward Script: Configure Prettier + ESLint cooperation in VSCode
Task ID: vscode_we_084
Domain: vscode
Scoring:
  Component 1 (0.2): editor.defaultFormatter set to esbenp.prettier-vscode
  Component 2 (0.2): editor.formatOnSave set to true
  Component 3 (0.2): eslint.format.enable set to false
  Component 4 (0.2): editor.codeActionsOnSave with source.fixAll.eslint = explicit
  Component 5 (0.2): [javascript] and [typescript] language-specific defaultFormatter
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")


def load_settings():
    """Load VSCode user settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip JSONC comments (// style)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARN: Could not load settings.json: {e}")
        return None


def verify_task():
    """
    Verify Prettier + ESLint configuration in VSCode settings.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("CRITICAL: Cannot load settings.json")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: editor.defaultFormatter = esbenp.prettier-vscode (0.2 points)
    try:
        val = settings.get("editor.defaultFormatter")
        if val == "esbenp.prettier-vscode":
            print(f"PASS: Component 1 -- editor.defaultFormatter is 'esbenp.prettier-vscode' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- expected editor.defaultFormatter='esbenp.prettier-vscode', found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: editor.formatOnSave = true (0.2 points)
    try:
        val = settings.get("editor.formatOnSave")
        if val is True:
            print(f"PASS: Component 2 -- editor.formatOnSave is true (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 -- expected editor.formatOnSave=true, found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: eslint.format.enable = false (0.2 points)
    try:
        val = settings.get("eslint.format.enable")
        if val is False:
            print(f"PASS: Component 3 -- eslint.format.enable is false (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 -- expected eslint.format.enable=false, found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: editor.codeActionsOnSave with source.fixAll.eslint = "explicit" (0.2 points)
    try:
        code_actions = settings.get("editor.codeActionsOnSave")
        if isinstance(code_actions, dict):
            val = code_actions.get("source.fixAll.eslint")
            if val == "explicit":
                print(f"PASS: Component 4 -- source.fixAll.eslint is 'explicit' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 -- expected source.fixAll.eslint='explicit', found: {val!r}")
        else:
            print(f"FAIL: Component 4 -- editor.codeActionsOnSave is not a dict, found: {code_actions!r}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: [javascript] and [typescript] both have editor.defaultFormatter = esbenp.prettier-vscode (0.2 points)
    try:
        js_block = settings.get("[javascript]", {})
        ts_block = settings.get("[typescript]", {})

        js_formatter = js_block.get("editor.defaultFormatter") if isinstance(js_block, dict) else None
        ts_formatter = ts_block.get("editor.defaultFormatter") if isinstance(ts_block, dict) else None

        js_ok = js_formatter == "esbenp.prettier-vscode"
        ts_ok = ts_formatter == "esbenp.prettier-vscode"

        if js_ok and ts_ok:
            print(f"PASS: Component 5 -- [javascript] and [typescript] defaultFormatter set correctly (0.2 pts)")
            total_score += 0.2
        else:
            if not js_ok:
                print(f"FAIL: Component 5 -- [javascript].editor.defaultFormatter expected 'esbenp.prettier-vscode', found: {js_formatter!r}")
            if not ts_ok:
                print(f"FAIL: Component 5 -- [typescript].editor.defaultFormatter expected 'esbenp.prettier-vscode', found: {ts_formatter!r}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
