"""
Reward Script: Customize diff editor settings in VSCode
Task ID: vscode_we_049
Domain: vscode
Scoring:
  Component 1: diffEditor.wordWrap == "on"           (0.35 points)
  Component 2: diffEditor.renderSideBySide == false   (0.35 points)
  Component 3: diffEditor.ignoreTrimWhitespace == true (0.30 points)
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")
TASK_ID = "vscode_we_049"


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip // comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("CRITICAL: settings.json not found or invalid")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: diffEditor.wordWrap == "on" (0.35 points)
    # Task says "enable word diff" -> VSCode setting is diffEditor.wordWrap: "on"
    try:
        val = settings.get("diffEditor.wordWrap")
        if val == "on":
            print(f"PASS: Component 1 - diffEditor.wordWrap is 'on' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 - diffEditor.wordWrap expected 'on', found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: diffEditor.renderSideBySide == false (0.35 points)
    # Task says "show inline diff view by default instead of side-by-side"
    try:
        val = settings.get("diffEditor.renderSideBySide")
        if val is False:
            print(f"PASS: Component 2 - diffEditor.renderSideBySide is false (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 - diffEditor.renderSideBySide expected false, found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: diffEditor.ignoreTrimWhitespace == true (0.30 points)
    # Task says "ignore leading and trailing whitespace in diffs"
    try:
        val = settings.get("diffEditor.ignoreTrimWhitespace")
        if val is True:
            print(f"PASS: Component 3 - diffEditor.ignoreTrimWhitespace is true (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 - diffEditor.ignoreTrimWhitespace expected true, found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
