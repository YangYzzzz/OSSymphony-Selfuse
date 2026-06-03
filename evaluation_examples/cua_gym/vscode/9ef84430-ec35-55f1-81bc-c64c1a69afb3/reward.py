"""
Reward Script: Configure HTML auto-closing tags and auto-rename matching tags in VSCode settings.
Task ID: vscode_lp_045
Domain: vs_code
Scoring:
  Component 1: html.autoClosingTags is true (0.5 points)
  Component 2: editor.linkedEditing is true (0.5 points)
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
        # Strip JSONC single-line comments before parsing
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

    # Component 1: html.autoClosingTags is true (0.5 points)
    # Initial state has this set to false; golden state has true.
    try:
        value = settings.get("html.autoClosingTags")
        if value is True:
            print(f"PASS: Component 1 — html.autoClosingTags is true (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — expected html.autoClosingTags=true, found: {value}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: editor.linkedEditing is true (0.5 points)
    # Initial state has this set to false; golden state has true.
    try:
        value = settings.get("editor.linkedEditing")
        if value is True:
            print(f"PASS: Component 2 — editor.linkedEditing is true (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — expected editor.linkedEditing=true, found: {value}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
