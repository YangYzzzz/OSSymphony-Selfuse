"""
Reward Script: Configure rust-analyzer to limit scope and reduce memory usage
Task ID: vscode_fix_062
Domain: vscode
Scoring:
  - Component 1: rust-analyzer.cargo.buildScripts.enable == false (0.35 pts)
  - Component 2: rust-analyzer.procMacro.enable == false (0.35 pts)
  - Component 3: rust-analyzer.checkOnSave.allTargets == false (0.30 pts)
"""

import os
import json
import re

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")
TASK_ID = "vscode_fix_062"


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip single-line comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        # Strip multi-line comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except FileNotFoundError:
        print(f"CRITICAL: Settings file not found at {SETTINGS_PATH}")
        return None
    except json.JSONDecodeError as e:
        print(f"CRITICAL: Cannot parse settings.json: {e}")
        return None


def verify_task():
    """
    Verify that rust-analyzer settings have been configured to reduce memory usage.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    # Component 1: rust-analyzer.cargo.buildScripts.enable == false (0.35 points)
    # In initial_env this is true; in golden_env it must be false.
    try:
        key = "rust-analyzer.cargo.buildScripts.enable"
        value = settings.get(key)
        if value is False:
            print(f"PASS: Component 1 - {key} is false (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 - Expected {key} == false, found: {value}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: rust-analyzer.procMacro.enable == false (0.35 points)
    # In initial_env this is true; in golden_env it must be false.
    try:
        key = "rust-analyzer.procMacro.enable"
        value = settings.get(key)
        if value is False:
            print(f"PASS: Component 2 - {key} is false (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 - Expected {key} == false, found: {value}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: rust-analyzer.checkOnSave.allTargets == false (0.30 points)
    # In initial_env this key is absent (defaults to true); in golden_env it must be explicitly false.
    try:
        key = "rust-analyzer.checkOnSave.allTargets"
        value = settings.get(key)
        if value is False:
            print(f"PASS: Component 3 - {key} is false (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 - Expected {key} == false, found: {value}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(SETTINGS_PATH):
    print(f"Settings file not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
