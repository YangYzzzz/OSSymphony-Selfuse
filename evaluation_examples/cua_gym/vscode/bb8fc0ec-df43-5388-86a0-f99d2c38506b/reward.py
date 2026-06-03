"""
Reward Script: Configure Python import sorting using isort in VSCode settings
Task ID: vscode_lp_024
Domain: vs_code
Scoring:
  Component 1 (0.4): [python] language-specific block exists with codeActionsOnSave
  Component 2 (0.3): source.organizeImports is set to true/explicit
  Component 3 (0.3): Settings are valid (no corruption) and the organize imports
                      config is nested correctly under [python]
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_024'

# Both user-level and workspace-level settings are valid locations
USER_SETTINGS = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')
WORKSPACE_SETTINGS = os.path.join(WORKDIR, 'workspace', '.vscode', 'settings.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments) by stripping comments first."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip block comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return json.loads(content)


def check_settings(settings):
    """
    Check if settings dict contains the required isort/organizeImports config.
    Returns (score, details_list) where score is 0.0-1.0.
    """
    total_score = 0.0
    details = []

    # Component 1 (0.4 pts): [python] block with editor.codeActionsOnSave exists
    try:
        python_block = settings.get("[python]", None)
        if python_block is not None and isinstance(python_block, dict):
            code_actions = python_block.get("editor.codeActionsOnSave", None)
            if code_actions is not None and isinstance(code_actions, dict):
                details.append(("PASS", "Component 1", 0.4,
                    f"[python].editor.codeActionsOnSave block exists: {code_actions}"))
                total_score += 0.4
            else:
                details.append(("FAIL", "Component 1", 0.4,
                    f"[python] block exists but editor.codeActionsOnSave missing or not a dict. Found: {python_block}"))
        else:
            details.append(("FAIL", "Component 1", 0.4,
                f"[python] language-specific block not found in settings. Keys: {list(settings.keys())}"))
    except Exception as e:
        details.append(("ERROR", "Component 1", 0.4, f"Exception: {e}"))

    # Component 2 (0.3 pts): source.organizeImports is set to true or "explicit"
    try:
        python_block = settings.get("[python]", {})
        code_actions = python_block.get("editor.codeActionsOnSave", {}) if isinstance(python_block, dict) else {}
        organize_val = code_actions.get("source.organizeImports", None) if isinstance(code_actions, dict) else None

        # Accept True (bool), "true" (string), or "explicit" (VSCode also accepts this)
        if organize_val is True or organize_val == "explicit" or (isinstance(organize_val, str) and organize_val.lower() == "true"):
            details.append(("PASS", "Component 2", 0.3,
                f"source.organizeImports is set to {organize_val!r}"))
            total_score += 0.3
        else:
            details.append(("FAIL", "Component 2", 0.3,
                f"source.organizeImports expected true/explicit, found: {organize_val!r}"))
    except Exception as e:
        details.append(("ERROR", "Component 2", 0.3, f"Exception: {e}"))

    # Component 3 (0.3 pts): The full nested path is correctly structured
    # Verify the complete expected structure as a subset
    try:
        expected = {
            "[python]": {
                "editor.codeActionsOnSave": {
                    "source.organizeImports": True
                }
            }
        }

        def is_subset(expected_d, actual_d):
            if isinstance(expected_d, dict):
                if not isinstance(actual_d, dict):
                    return False
                return all(k in actual_d and is_subset(v, actual_d[k]) for k, v in expected_d.items())
            if isinstance(expected_d, bool) and isinstance(actual_d, bool):
                return expected_d == actual_d
            # Also accept "explicit" as equivalent to True for organizeImports
            if expected_d is True and (actual_d == "explicit" or (isinstance(actual_d, str) and actual_d.lower() == "true")):
                return True
            return expected_d == actual_d

        if is_subset(expected, settings):
            details.append(("PASS", "Component 3", 0.3,
                "Full nested structure verified: [python] > editor.codeActionsOnSave > source.organizeImports"))
            total_score += 0.3
        else:
            details.append(("FAIL", "Component 3", 0.3,
                f"Full nested structure check failed. Actual [python] block: {settings.get('[python]', 'MISSING')}"))
    except Exception as e:
        details.append(("ERROR", "Component 3", 0.3, f"Exception: {e}"))

    return total_score, details


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    all_details = []

    # Try both user-level and workspace-level settings
    settings_found = False
    for path_label, path in [("user-level", USER_SETTINGS), ("workspace-level", WORKSPACE_SETTINGS)]:
        if os.path.exists(path):
            try:
                settings = load_jsonc(path)
                print(f"INFO: Loaded {path_label} settings from {path}")
                score, details = check_settings(settings)
                if score > total_score:
                    total_score = score
                    all_details = details
                    settings_found = True
                    if score >= 1.0:
                        break
            except Exception as e:
                print(f"WARN: Could not parse {path_label} settings at {path}: {e}")

    if not settings_found:
        # Neither settings file contained the required config
        if not os.path.exists(USER_SETTINGS) and not os.path.exists(WORKSPACE_SETTINGS):
            print("CRITICAL: No settings.json found at user or workspace level")
            all_details = [("FAIL", "File check", 0.0, "No settings.json found")]
        elif not all_details:
            print("CRITICAL: Settings files found but none contained the required config")
            all_details = [("FAIL", "Config check", 0.0, "Settings parsed but no matching config")]

    # Print details
    for status, comp, pts, detail in all_details:
        print(f"{status}: {comp} ({pts} pts) -- {detail}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
