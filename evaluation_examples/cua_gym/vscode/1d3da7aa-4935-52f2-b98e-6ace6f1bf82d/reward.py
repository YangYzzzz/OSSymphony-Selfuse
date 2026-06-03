"""
Reward Script: Enable TypeScript inlay hints in VSCode
Task ID: vscode_web_066
Domain: vs_code
Scoring:
  Component 1 (0.4): parameterNames.enabled set to 'all' or 'literals'
  Component 2 (0.3): functionLikeReturnTypes.enabled set to true
  Component 3 (0.3): variableTypes.enabled set to true
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


def verify_task():
    """
    Verify that TypeScript inlay hints are properly configured.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    # Component 1: typescript.inlayHints.parameterNames.enabled is 'all' or 'literals' (0.4 points)
    # Initial state has this as "none"; task requires enabling it.
    try:
        param_names = settings.get("typescript.inlayHints.parameterNames.enabled")
        if param_names in ("all", "literals"):
            print(f"PASS: Component 1 -- parameterNames.enabled = '{param_names}' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 -- parameterNames.enabled = '{param_names}', expected 'all' or 'literals'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: typescript.inlayHints.functionLikeReturnTypes.enabled is true (0.3 points)
    # Initial state has this as false; task requires enabling it.
    try:
        return_types = settings.get("typescript.inlayHints.functionLikeReturnTypes.enabled")
        if return_types is True:
            print(f"PASS: Component 2 -- functionLikeReturnTypes.enabled = {return_types} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- functionLikeReturnTypes.enabled = {return_types}, expected true")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: typescript.inlayHints.variableTypes.enabled is true (0.3 points)
    # Initial state has this as false; task requires enabling it.
    try:
        var_types = settings.get("typescript.inlayHints.variableTypes.enabled")
        if var_types is True:
            print(f"PASS: Component 3 -- variableTypes.enabled = {var_types} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 -- variableTypes.enabled = {var_types}, expected true")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
