"""
Reward Script: Switch VSCode color theme to Solarized Dark and set icon theme to vs-seti
Task ID: vscode_gf2_008
Domain: vscode
Scoring:
  Component 1 (0.6): workbench.colorTheme == "Solarized Dark"
  Component 2 (0.4): workbench.iconTheme == "vs-seti"
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
        # Strip single-line comments (JSONC)
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

    # Component 1: workbench.colorTheme is "Solarized Dark" (0.6 points)
    try:
        color_theme = settings.get("workbench.colorTheme")
        if color_theme == "Solarized Dark":
            print(f"PASS: Component 1 — colorTheme is 'Solarized Dark' (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 — expected colorTheme 'Solarized Dark', found: '{color_theme}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: workbench.iconTheme is "vs-seti" (0.4 points)
    try:
        icon_theme = settings.get("workbench.iconTheme")
        if icon_theme == "vs-seti":
            print(f"PASS: Component 2 — iconTheme is 'vs-seti' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — expected iconTheme 'vs-seti', found: '{icon_theme}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
