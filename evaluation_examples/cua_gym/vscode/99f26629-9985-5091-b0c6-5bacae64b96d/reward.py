"""
Reward Script: Enable trim trailing whitespace on save in VSCode
Task ID: vscode_we_008
Domain: vscode
Scoring:
  Component 1 (0.5): files.trimTrailingWhitespace key exists in settings.json
  Component 2 (0.5): The value is exactly the boolean True
"""

import os
import json
import re

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")
TASK_ID = "vscode_we_008"


def load_settings(path):
    """Load VSCode settings.json, handling JSONC (comments)."""
    try:
        with open(path, "r") as f:
            content = f.read()
        # Strip single-line comments (JSONC support)
        cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        # Strip trailing commas before } or ]
        cleaned = re.sub(r',\s*([}\]])', r'\1', cleaned)
        return json.loads(cleaned)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings from {path}: {e}")
        return None


def verify_task():
    """
    Verify that files.trimTrailingWhitespace is enabled in VSCode settings.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load settings
    settings = load_settings(SETTINGS_PATH)
    if settings is None:
        print("CRITICAL: Cannot load or parse settings.json")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Loaded settings.json with {len(settings)} keys: {list(settings.keys())}")

    # Component 1: files.trimTrailingWhitespace key exists in settings (0.5 points)
    try:
        key = "files.trimTrailingWhitespace"
        if key in settings:
            print(f"PASS: Component 1 — '{key}' key exists in settings.json (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — '{key}' key not found in settings.json. Keys present: {list(settings.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The value is exactly the boolean True (0.5 points)
    try:
        key = "files.trimTrailingWhitespace"
        if key in settings:
            value = settings[key]
            if value is True:
                print(f"PASS: Component 2 — '{key}' is boolean true (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 2 — '{key}' is {repr(value)} (type: {type(value).__name__}), expected boolean True")
        else:
            print(f"FAIL: Component 2 — '{key}' key not present, cannot check value")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
