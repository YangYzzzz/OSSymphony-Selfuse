"""
Reward Script: Configure VSCode Outline view settings
Task ID: vscode_rf_014
Domain: vscode
Scoring:
  - Component 1: outline.sortOrder == "position" (0.25 pts)
  - Component 2: outline.showVariables == false (0.2 pts)
  - Component 3: outline.showConstants == false (0.2 pts)
  - Component 4: outline.followCursor == true (0.2 pts)
  - Component 5: breadcrumbs.followCursor == true (0.15 pts)
"""

import os
import json
import re

HOME = '/home/user'
SETTINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'settings.json')


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify VSCode Outline view configuration with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Outline sort order is "position" (0.25 points)
    # Initial: "type" (alphabetical). Golden: "position" (source order).
    try:
        sort_order = settings.get("outline.sortOrder")
        if sort_order == "position":
            print(f"PASS: Component 1 — outline.sortOrder is 'position' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — expected outline.sortOrder='position', found: {sort_order!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Variables are hidden from Outline (0.2 points)
    # Initial: true (shown). Golden: false (hidden).
    try:
        show_vars = settings.get("outline.showVariables")
        if show_vars is False:
            print(f"PASS: Component 2 — outline.showVariables is false (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — expected outline.showVariables=false, found: {show_vars!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Constants are hidden from Outline (0.2 points)
    # Initial: true (shown). Golden: false (hidden).
    try:
        show_consts = settings.get("outline.showConstants")
        if show_consts is False:
            print(f"PASS: Component 3 — outline.showConstants is false (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — expected outline.showConstants=false, found: {show_consts!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Outline Follow Cursor is enabled (0.2 points)
    # Initial: false. Golden: true.
    try:
        follow_cursor = settings.get("outline.followCursor")
        if follow_cursor is True:
            print(f"PASS: Component 4 — outline.followCursor is true (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — expected outline.followCursor=true, found: {follow_cursor!r}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Breadcrumbs Follow Cursor is enabled (0.15 points)
    # Initial: false. Golden: true. Related to the Follow Cursor feature.
    try:
        bc_follow = settings.get("breadcrumbs.followCursor")
        if bc_follow is True:
            print(f"PASS: Component 5 — breadcrumbs.followCursor is true (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — expected breadcrumbs.followCursor=true, found: {bc_follow!r}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
