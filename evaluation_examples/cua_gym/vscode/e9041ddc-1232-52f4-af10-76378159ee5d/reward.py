"""
Reward Script: Configure VSCode workbench layout settings
Task ID: vscode_we_044
Domain: vscode
Scoring:
  - Component 1: workbench.panel.defaultLocation == "right"  (0.25)
  - Component 2: workbench.activityBar.location == "top"     (0.25)
  - Component 3: explorer.compactFolders == false             (0.25)
  - Component 4: workbench.startupEditor == "none"            (0.25)
"""

import os
import json
import re

HOME = '/home/user'
SETTINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'settings.json')
TASK_ID = 'vscode_we_044'


def load_settings(path):
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARNING: Could not load settings from {path}: {e}")
        return None


def verify_task():
    """
    Verify VSCode workbench layout configuration with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must be loadable
    settings = load_settings(SETTINGS_PATH)
    if settings is None:
        print("CRITICAL: Cannot load settings.json")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Panel position set to "right" (0.25 points)
    try:
        actual = settings.get("workbench.panel.defaultLocation")
        if actual == "right":
            print(f"PASS: Component 1 — workbench.panel.defaultLocation is 'right' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — expected 'right', found: {actual!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Activity bar location set to "top" (0.25 points)
    try:
        actual = settings.get("workbench.activityBar.location")
        if actual == "top":
            print(f"PASS: Component 2 — workbench.activityBar.location is 'top' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — expected 'top', found: {actual!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Compact folders disabled (0.25 points)
    try:
        actual = settings.get("explorer.compactFolders")
        if actual is False:
            print(f"PASS: Component 3 — explorer.compactFolders is false (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — expected false, found: {actual!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Startup editor set to "none" (0.25 points)
    try:
        actual = settings.get("workbench.startupEditor")
        if actual == "none":
            print(f"PASS: Component 4 — workbench.startupEditor is 'none' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — expected 'none', found: {actual!r}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
