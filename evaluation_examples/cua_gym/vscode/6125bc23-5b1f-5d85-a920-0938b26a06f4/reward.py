"""
Reward Script: Configure editor rulers at 80/120 and enable render whitespace "all"
Task ID: vscode_we_025
Domain: vscode
Scoring:
  Component 1 — editor.rulers == [80, 120]       (0.5 pts)
  Component 2 — editor.renderWhitespace == "all"  (0.5 pts)
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
        # Strip single-line comments (JSONC)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARN: Could not load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("CRITICAL: Cannot load settings.json")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: editor.rulers == [80, 120] (0.5 points)
    try:
        rulers = settings.get("editor.rulers")
        if isinstance(rulers, list) and rulers == [80, 120]:
            print(f"PASS: Component 1 — editor.rulers is [80, 120] (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — expected editor.rulers == [80, 120], found: {rulers}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: editor.renderWhitespace == "all" (0.5 points)
    try:
        rw = settings.get("editor.renderWhitespace")
        if isinstance(rw, str) and rw == "all":
            print(f"PASS: Component 2 — editor.renderWhitespace is 'all' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — expected editor.renderWhitespace == 'all', found: {rw}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
