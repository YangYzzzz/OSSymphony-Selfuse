"""
Reward Script: Configure VSCode to automatically organize imports on save for TypeScript files
Task ID: vscode_web_094
Domain: vscode
Scoring:
  Component 1 (0.5): [typescript] scoped organizeImports on save
  Component 2 (0.5): [typescriptreact] scoped organizeImports on save
  Precondition gate: ESLint auto-fix on save still configured (not broken by changes)
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
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None


def _is_subset(expected, actual):
    """Check that expected is a subset of actual (recursive dict match)."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and _is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        return expected == actual
    return expected == actual


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

    # Precondition gate: ESLint auto-fix on save must still be configured
    # This was present before the task and must not be broken
    try:
        eslint_setting = settings.get("editor.codeActionsOnSave", {}).get("source.fixAll.eslint")
        if eslint_setting not in ("explicit", True, "always"):
            print(f"PRECONDITION FAIL: ESLint auto-fix on save is missing or broken (value: {eslint_setting})")
            print("REWARD: 0.0")
            return 0.0
        else:
            print(f"PRECONDITION OK: ESLint auto-fix on save is still configured (value: {eslint_setting})")
    except Exception as e:
        print(f"PRECONDITION ERROR: Could not check ESLint setting: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: [typescript] scoped organizeImports on save (0.5 points)
    # The task requires organize imports to be scoped to [typescript] files.
    # Valid values: "explicit", true, "always"
    try:
        ts_section = settings.get("[typescript]", {})
        ts_organize = None
        if isinstance(ts_section, dict):
            code_actions = ts_section.get("editor.codeActionsOnSave", {})
            if isinstance(code_actions, dict):
                ts_organize = code_actions.get("source.organizeImports")

        if ts_organize in ("explicit", True, "always"):
            print(f"PASS: Component 1 -- [typescript] organizeImports on save = {ts_organize} (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 -- [typescript] organizeImports on save not configured (found: {ts_organize})")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: [typescriptreact] scoped organizeImports on save (0.5 points)
    # The task requires organize imports to also be scoped to [typescriptreact] files.
    try:
        tsx_section = settings.get("[typescriptreact]", {})
        tsx_organize = None
        if isinstance(tsx_section, dict):
            code_actions = tsx_section.get("editor.codeActionsOnSave", {})
            if isinstance(code_actions, dict):
                tsx_organize = code_actions.get("source.organizeImports")

        if tsx_organize in ("explicit", True, "always"):
            print(f"PASS: Component 2 -- [typescriptreact] organizeImports on save = {tsx_organize} (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 -- [typescriptreact] organizeImports on save not configured (found: {tsx_organize})")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

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
