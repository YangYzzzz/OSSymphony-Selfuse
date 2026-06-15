"""
Reward Script: Configure SQLTools extension settings in VSCode
Task ID: vscode_gf3_004
Domain: vscode
Scoring:
  Component 1 — sqltools.autoOpenSessionFiles == false (0.35)
  Component 2 — sqltools.results.limit == 500        (0.35)
  Component 3 — sqltools.format.indentSize == 2       (0.30)
  Total: 1.0
"""

import os
import json
import re

SETTINGS_PATH = os.path.expanduser("~/.config/Code/User/settings.json")


def load_settings(path):
    """Load VSCode settings.json, handling JSONC comments."""
    with open(path, "r") as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify that the three SQLTools settings have been configured correctly.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must exist and be parseable
    if not os.path.exists(SETTINGS_PATH):
        print(f"CRITICAL: Settings file not found: {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        settings = load_settings(SETTINGS_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse settings.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: sqltools.autoOpenSessionFiles == false (0.35 points)
    try:
        key = "sqltools.autoOpenSessionFiles"
        if key in settings and settings[key] is False:
            print(f"PASS: Component 1 — {key} is false (0.35 pts)")
            total_score += 0.35
        else:
            actual = settings.get(key, "<missing>")
            print(f"FAIL: Component 1 — expected {key} == false, found: {actual}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: sqltools.results.limit == 500 (0.35 points)
    try:
        key = "sqltools.results.limit"
        if key in settings and settings[key] == 500:
            print(f"PASS: Component 2 — {key} is 500 (0.35 pts)")
            total_score += 0.35
        else:
            actual = settings.get(key, "<missing>")
            print(f"FAIL: Component 2 — expected {key} == 500, found: {actual}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: sqltools.format.indentSize == 2 (0.30 points)
    try:
        key = "sqltools.format.indentSize"
        if key in settings and settings[key] == 2:
            print(f"PASS: Component 3 — {key} is 2 (0.30 pts)")
            total_score += 0.30
        else:
            actual = settings.get(key, "<missing>")
            print(f"FAIL: Component 3 — expected {key} == 2, found: {actual}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
