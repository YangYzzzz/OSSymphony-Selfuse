"""
Reward Script: Set up file nesting rules for .spec.ts and .module.css files
Task ID: vscode_lp_064
Domain: vscode
Scoring:
  - Component 1: explorer.fileNesting.enabled is true (0.3 pts)
  - Component 2: *.ts nesting pattern for .spec.ts files (0.35 pts)
  - Component 3: *.tsx nesting pattern for .module.css files (0.35 pts)
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")
WORKSPACE_SETTINGS_PATH = "/home/user/workspace/.vscode/settings.json"
TASK_ID = "vscode_lp_064"


def load_jsonc(path):
    """Load a JSONC file (JSON with comments), stripping comments first."""
    try:
        with open(path, "r") as f:
            content = f.read()
        # Strip single-line comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        # Strip multi-line comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return None


def get_merged_settings():
    """Load user-level settings and workspace-level settings, merge them.
    Workspace settings override user settings in VSCode."""
    user_settings = load_jsonc(SETTINGS_PATH) or {}
    workspace_settings = load_jsonc(WORKSPACE_SETTINGS_PATH) or {}
    merged = dict(user_settings)
    merged.update(workspace_settings)
    return merged


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load settings from both possible locations
    settings = get_merged_settings()
    if settings is None or len(settings) == 0:
        print("CRITICAL: Cannot load any VSCode settings file")
        print("REWARD: 0.0")
        return 0.0

    print(f"Loaded settings with {len(settings)} keys")

    # Component 1: explorer.fileNesting.enabled is true (0.3 points)
    try:
        nesting_enabled = settings.get("explorer.fileNesting.enabled")
        if nesting_enabled is True:
            print(f"PASS: Component 1 - fileNesting.enabled is true (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 - expected explorer.fileNesting.enabled=true, found: {nesting_enabled}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: *.ts pattern nests .spec.ts files (0.35 points)
    # The pattern key "*.ts" should map to a value containing "${capture}.spec.ts"
    try:
        patterns = settings.get("explorer.fileNesting.patterns")
        if isinstance(patterns, dict):
            ts_pattern = patterns.get("*.ts", "")
            # The pattern value can contain multiple entries comma-separated
            # We need "${capture}.spec.ts" to appear somewhere in the value
            if "${capture}.spec.ts" in str(ts_pattern):
                print(f"PASS: Component 2 - *.ts pattern includes ${{capture}}.spec.ts (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 - *.ts pattern value is '{ts_pattern}', expected to contain '${{capture}}.spec.ts'")
        else:
            print(f"FAIL: Component 2 - explorer.fileNesting.patterns not found or not a dict (found: {type(patterns).__name__})")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: *.tsx pattern nests .module.css files (0.35 points)
    # The pattern key "*.tsx" should map to a value containing "${capture}.module.css"
    try:
        patterns = settings.get("explorer.fileNesting.patterns")
        if isinstance(patterns, dict):
            tsx_pattern = patterns.get("*.tsx", "")
            if "${capture}.module.css" in str(tsx_pattern):
                print(f"PASS: Component 3 - *.tsx pattern includes ${{capture}}.module.css (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 3 - *.tsx pattern value is '{tsx_pattern}', expected to contain '${{capture}}.module.css'")
        else:
            print(f"FAIL: Component 3 - explorer.fileNesting.patterns not found or not a dict (found: {type(patterns).__name__})")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
