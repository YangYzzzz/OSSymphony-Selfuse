"""
Reward Script: Change VSCode icon theme to 'material-icon-theme' and product icon theme to 'fluent-icons'
Task ID: vscode_we_021
Domain: vscode
Scoring:
  Component 1: workbench.iconTheme == "material-icon-theme" (0.5 points)
  Component 2: workbench.productIconTheme == "fluent-icons" (0.5 points)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_021'
SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_settings(path):
    """Load VSCode settings.json, handling JSONC (comments)."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings from {path}: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings(SETTINGS_PATH)
    if settings is None:
        print("CRITICAL: Cannot load settings.json")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: workbench.iconTheme == "material-icon-theme" (0.5 points)
    try:
        icon_theme = settings.get("workbench.iconTheme")
        if icon_theme == "material-icon-theme":
            print(f"PASS: Component 1 — workbench.iconTheme is 'material-icon-theme' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — expected 'material-icon-theme', found: {icon_theme!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: workbench.productIconTheme == "fluent-icons" (0.5 points)
    try:
        product_icon_theme = settings.get("workbench.productIconTheme")
        if product_icon_theme == "fluent-icons":
            print(f"PASS: Component 2 — workbench.productIconTheme is 'fluent-icons' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — expected 'fluent-icons', found: {product_icon_theme!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
