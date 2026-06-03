"""
Reward Script: Enable Git auto-fetch in VSCode
Task ID: vscode_we_010
Domain: vscode
Scoring:
  Component 1 (0.5): settings.json contains "git.autofetch" key
  Component 2 (0.5): "git.autofetch" value is exactly true (boolean)
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")
TASK_ID = "vscode_we_010"


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    with open(SETTINGS_PATH, "r") as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip trailing commas before } or ]
    content = re.sub(r',\s*([}\]])', r'\1', content)
    return json.loads(content)


def verify_task():
    """
    Verify that git.autofetch is enabled in VSCode settings.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must exist and be parseable
    try:
        settings = load_settings()
    except FileNotFoundError:
        print(f"CRITICAL: settings.json not found at {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse settings.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: settings.json contains "git.autofetch" key (0.5 points)
    # This key does NOT exist in the initial empty settings, so it is task-introduced.
    try:
        if "git.autofetch" in settings:
            print(f"PASS: Component 1 — 'git.autofetch' key found in settings.json (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — 'git.autofetch' key not found in settings.json. Keys present: {list(settings.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: "git.autofetch" value is exactly true (boolean) (0.5 points)
    # The task says "enable Git auto-fetch", meaning the value must be boolean true.
    try:
        value = settings.get("git.autofetch")
        if value is True:
            print(f"PASS: Component 2 — 'git.autofetch' is True (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — 'git.autofetch' expected True (bool), found: {value!r} (type: {type(value).__name__})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
