"""
Reward Script: Configure VSCode file-saving and EOL settings
Task ID: vscode_we_031
Domain: vscode
Scoring:
  Component 1 — files.insertFinalNewline == true  (0.35 pts)
  Component 2 — files.trimFinalNewlines  == true   (0.35 pts)
  Component 3 — files.eol               == "\\n"   (0.30 pts)
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
        # Strip single-line JSONC comments before parsing
        stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(stripped)
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
        print("CRITICAL: settings.json not found or unreadable")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: files.insertFinalNewline is true (0.35 points)
    try:
        val = settings.get("files.insertFinalNewline")
        if val is True:
            print(f"PASS: Component 1 — files.insertFinalNewline is true (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — expected files.insertFinalNewline == true, found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: files.trimFinalNewlines is true (0.35 points)
    try:
        val = settings.get("files.trimFinalNewlines")
        if val is True:
            print(f"PASS: Component 2 — files.trimFinalNewlines is true (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — expected files.trimFinalNewlines == true, found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: files.eol is "\n" (0.30 points)
    try:
        val = settings.get("files.eol")
        if val == "\n":
            print(f"PASS: Component 3 — files.eol is '\\n' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — expected files.eol == '\\n', found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
