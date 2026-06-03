"""
Reward Script: Configure VSCode terminal font family and size
Task ID: vscode_we_017
Domain: vscode
Scoring:
  Component 1 (0.5): terminal.integrated.fontFamily == "Fira Code"
  Component 2 (0.5): terminal.integrated.fontSize == 14
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
        # Strip single-line comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARNING: Could not load settings.json: {e}")
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

    # Component 1: terminal.integrated.fontFamily == "Fira Code" (0.5 points)
    try:
        font_family = settings.get("terminal.integrated.fontFamily")
        if font_family is not None and str(font_family).strip() == "Fira Code":
            print(f"PASS: Component 1 — fontFamily is 'Fira Code' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — expected fontFamily='Fira Code', found: {font_family!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: terminal.integrated.fontSize == 14 (0.5 points)
    try:
        font_size = settings.get("terminal.integrated.fontSize")
        if font_size is not None and int(font_size) == 14:
            print(f"PASS: Component 2 — fontSize is 14 (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — expected fontSize=14, found: {font_size!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
