"""
Reward Script: Enable pylint as the Python linter in VSCode and disable pylance type checking
Task ID: vscode_lp_002
Domain: vscode
Scoring:
  - Component 1 (0.35): python.linting.pylintEnabled == true
  - Component 2 (0.30): python.linting.enabled == true
  - Component 3 (0.35): python.analysis.typeCheckingMode == "off"
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
        # Strip single-line comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
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

    print(f"Loaded settings: {json.dumps(settings, indent=2)}")

    # Component 1: python.linting.pylintEnabled is true (0.35 points)
    # This setting does NOT exist in initial_env, so it only passes on golden_env
    try:
        pylint_enabled = settings.get("python.linting.pylintEnabled")
        if pylint_enabled is True:
            print(f"PASS: Component 1 — python.linting.pylintEnabled is true (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — expected python.linting.pylintEnabled=true, found: {pylint_enabled}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: python.linting.enabled is true (0.30 points)
    # This setting does NOT exist in initial_env, so it only passes on golden_env
    try:
        linting_enabled = settings.get("python.linting.enabled")
        if linting_enabled is True:
            print(f"PASS: Component 2 — python.linting.enabled is true (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — expected python.linting.enabled=true, found: {linting_enabled}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: python.analysis.typeCheckingMode is "off" (0.35 points)
    # In initial_env this is "basic", so this only passes on golden_env where it is "off"
    try:
        type_checking = settings.get("python.analysis.typeCheckingMode")
        if type_checking == "off":
            print(f"PASS: Component 3 — python.analysis.typeCheckingMode is 'off' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 3 — expected python.analysis.typeCheckingMode='off', found: {type_checking}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task()
