"""
Reward Script: Toggle off the Explorer sidebar in VSCode
Task ID: vscode_stu_009
Domain: vs_code
Scoring:
  Component 1 (0.6): workbench.sideBar.visible is explicitly false in settings.json
  Component 2 (0.4): settings.json is valid JSON and the sidebar setting is boolean false (not string, not missing)
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")


def load_settings():
    """Load VSCode settings.json, handling JSONC (comments)."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip single-line comments for JSONC compatibility
        cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(cleaned)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify that the Explorer sidebar has been toggled off.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("CRITICAL: settings.json not found or invalid")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: workbench.sideBar.visible is false (0.6 points)
    # This is the primary task requirement - the sidebar must be hidden.
    # In initial_env this is true; in golden_env this must be false.
    try:
        sidebar_visible = settings.get("workbench.sideBar.visible")
        if sidebar_visible is False:
            print(f"PASS: Component 1 -- workbench.sideBar.visible is false (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 -- workbench.sideBar.visible is {sidebar_visible!r}, expected false")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: The setting is explicitly boolean false, not a string or absent (0.4 points)
    # Verifies data type correctness and that the key actually exists.
    # In initial_env, the key is true (so this fails). In golden_env, it must be exactly boolean false.
    try:
        if "workbench.sideBar.visible" in settings:
            val = settings["workbench.sideBar.visible"]
            if isinstance(val, bool) and val is False:
                print(f"PASS: Component 2 -- Setting is explicitly boolean false (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 -- Setting is {type(val).__name__}={val!r}, expected bool false")
        else:
            print(f"FAIL: Component 2 -- workbench.sideBar.visible key not found in settings")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
