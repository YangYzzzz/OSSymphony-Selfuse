"""
Reward Script: Extend eslint.validate to cover Vue files
Task ID: vscode_fix_060
Domain: vscode
Scoring:
  Component 1 (0.6): 'vue' is present in eslint.validate array
  Component 2 (0.4): 'vue' in eslint.validate AND original languages preserved AND codeActionsOnSave still active
"""

import os
import json
import re

SETTINGS_PATH = os.path.expanduser("~/.config/Code/User/settings.json")
TASK_ID = "vscode_fix_060"


def load_settings(path):
    """Load VSCode settings.json, handling JSONC (comments)."""
    with open(path, "r") as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
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

    # Precondition: settings.json must exist and be parseable
    try:
        settings = load_settings(SETTINGS_PATH)
    except FileNotFoundError:
        print(f"CRITICAL: Settings file not found at {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse settings.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: 'vue' is present in eslint.validate array (0.6 points)
    # This is the core task requirement - adding Vue to eslint validation
    try:
        eslint_validate = settings.get("eslint.validate", [])
        if not isinstance(eslint_validate, list):
            print(f"FAIL: Component 1 — eslint.validate is not a list, found: {type(eslint_validate)}")
        else:
            # Check for 'vue' in the array (case-insensitive)
            validate_lower = [str(v).lower() for v in eslint_validate]
            if "vue" in validate_lower:
                print(f"PASS: Component 1 — 'vue' found in eslint.validate: {eslint_validate} (0.6 pts)")
                total_score += 0.6
            else:
                print(f"FAIL: Component 1 — 'vue' not found in eslint.validate: {eslint_validate}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'vue' in eslint.validate AND original languages preserved AND codeActionsOnSave active (0.4 points)
    # Compound check: verifies the change was additive (didn't break existing config)
    try:
        eslint_validate = settings.get("eslint.validate", [])
        if not isinstance(eslint_validate, list):
            print(f"FAIL: Component 2 — eslint.validate is not a list")
        else:
            validate_lower = [str(v).lower() for v in eslint_validate]
            vue_present = "vue" in validate_lower
            js_present = "javascript" in validate_lower
            ts_present = "typescript" in validate_lower

            # Check codeActionsOnSave has eslint fix
            code_actions = settings.get("editor.codeActionsOnSave", {})
            eslint_fix = code_actions.get("source.fixAll.eslint") if isinstance(code_actions, dict) else None
            # Value can be true or "explicit" - both enable the feature
            eslint_active = eslint_fix is not None and eslint_fix is not False and eslint_fix != "never"

            if vue_present and js_present and ts_present and eslint_active:
                print(f"PASS: Component 2 — vue added, original languages preserved, codeActionsOnSave active (0.4 pts)")
                total_score += 0.4
            else:
                reasons = []
                if not vue_present:
                    reasons.append("'vue' missing")
                if not js_present:
                    reasons.append("'javascript' missing")
                if not ts_present:
                    reasons.append("'typescript' missing")
                if not eslint_active:
                    reasons.append(f"codeActionsOnSave.source.fixAll.eslint not active (value: {eslint_fix})")
                print(f"FAIL: Component 2 — {', '.join(reasons)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
