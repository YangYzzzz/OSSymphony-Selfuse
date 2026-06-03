"""
Reward Script: Configure Python import sorting on save via codeActionsOnSave
Task ID: vscode_fix_088
Domain: vscode
Scoring:
  Component 1 (0.4): [python] language-specific section exists
  Component 2 (0.3): editor.codeActionsOnSave exists within [python]
  Component 3 (0.3): source.organizeImports is true in Python codeActionsOnSave
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")
TASK_ID = "vscode_fix_088"


def load_settings_jsonc(path):
    """Load VSCode settings.json, stripping JSONC comments."""
    with open(path, "r") as f:
        content = f.read()
    # Strip single-line comments (// ...)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip block comments (/* ... */)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return json.loads(content)


def verify_task():
    """
    Verify that VSCode settings.json has Python-specific codeActionsOnSave
    with source.organizeImports enabled.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must exist and be parseable
    try:
        settings = load_settings_jsonc(SETTINGS_PATH)
    except FileNotFoundError:
        print(f"CRITICAL: Settings file not found at {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse settings.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: [python] language-specific section exists (0.4 points)
    # The task requires language-specific configuration for Python
    try:
        python_section = settings.get("[python]")
        if isinstance(python_section, dict):
            print(f"PASS: Component 1 -- [python] section exists with {len(python_section)} key(s) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 -- [python] section not found or not a dict. Found: {type(python_section)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: editor.codeActionsOnSave exists within [python] (0.3 points)
    try:
        python_section = settings.get("[python]", {})
        code_actions = python_section.get("editor.codeActionsOnSave")
        if isinstance(code_actions, dict):
            print(f"PASS: Component 2 -- editor.codeActionsOnSave exists in [python] with {len(code_actions)} action(s) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- editor.codeActionsOnSave not found in [python] or not a dict. Found: {code_actions}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: source.organizeImports is true (0.3 points)
    try:
        python_section = settings.get("[python]", {})
        code_actions = python_section.get("editor.codeActionsOnSave", {})
        organize_imports = code_actions.get("source.organizeImports")
        # Accept True (bool) or "explicit" (string) -- both enable the feature
        if organize_imports is True or organize_imports == "explicit":
            print(f"PASS: Component 3 -- source.organizeImports = {organize_imports} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 -- source.organizeImports expected true, found: {organize_imports}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Also check if organizeImports was set at global level (alternative valid approach)
# Some users might set it globally instead of Python-specific
def verify_task_with_fallback():
    """
    Primary: check [python] language-specific setting.
    Fallback: check global editor.codeActionsOnSave (still valid for the task).
    """
    total_score = 0.0

    try:
        settings = load_settings_jsonc(SETTINGS_PATH)
    except FileNotFoundError:
        print(f"CRITICAL: Settings file not found at {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse settings.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Check Python-specific path first
    python_section = settings.get("[python]", {})
    python_code_actions = python_section.get("editor.codeActionsOnSave", {}) if isinstance(python_section, dict) else {}

    # Also check global path
    global_code_actions = settings.get("editor.codeActionsOnSave", {})
    if not isinstance(global_code_actions, dict):
        global_code_actions = {}

    python_organize = python_code_actions.get("source.organizeImports")
    global_organize = global_code_actions.get("source.organizeImports")

    has_python_section = isinstance(settings.get("[python]"), dict)
    has_python_code_actions = isinstance(python_code_actions, dict) and len(python_code_actions) > 0
    has_organize_in_python = python_organize is True or python_organize == "explicit"
    has_organize_in_global = global_organize is True or global_organize == "explicit"

    # Component 1: Python-specific or global codeActionsOnSave configured (0.4 points)
    try:
        if has_python_section:
            print(f"PASS: Component 1 -- [python] language-specific section exists (0.4 pts)")
            total_score += 0.4
        elif has_organize_in_global:
            # Global config also achieves the task goal, partial credit
            print(f"PASS: Component 1 -- organizeImports set globally (acceptable alternative) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 -- No [python] section and no global organizeImports config")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: codeActionsOnSave has entries (0.3 points)
    try:
        if has_python_code_actions:
            print(f"PASS: Component 2 -- editor.codeActionsOnSave in [python] has entries (0.3 pts)")
            total_score += 0.3
        elif has_organize_in_global:
            print(f"PASS: Component 2 -- editor.codeActionsOnSave globally has organizeImports (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- No codeActionsOnSave with organizeImports in either scope")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: source.organizeImports is enabled (0.3 points)
    try:
        if has_organize_in_python:
            print(f"PASS: Component 3 -- source.organizeImports = {python_organize} in [python] (0.3 pts)")
            total_score += 0.3
        elif has_organize_in_global:
            print(f"PASS: Component 3 -- source.organizeImports = {global_organize} globally (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 -- source.organizeImports not enabled anywhere")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(SETTINGS_PATH):
    print(f"Settings file not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task_with_fallback()
