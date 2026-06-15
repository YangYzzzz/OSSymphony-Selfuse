"""
Reward Script: Configure VSCode workbench for web-development-optimized layout
Task ID: vscode_web_061
Domain: vscode
Scoring:
  - Component 1: Activity Bar location set to 'top' (0.25 pts)
  - Component 2: Sidebar location set to 'right' (0.25 pts)
  - Component 3: Minimap enabled with scale 2 (0.25 pts)
  - Component 4: Breadcrumbs enabled with filePath 'on' (0.25 pts)
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
        # Strip JSONC comments before parsing
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify VSCode workbench layout configuration with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    print(f"Loaded settings with {len(settings)} keys")

    # Component 1: Activity Bar location set to 'top' (0.25 points)
    try:
        activity_bar_loc = settings.get("workbench.activityBar.location")
        if activity_bar_loc == "top":
            print(f"PASS: Component 1 — activityBar.location is 'top' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — expected activityBar.location='top', found: {activity_bar_loc!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Sidebar location set to 'right' (0.25 points)
    try:
        sidebar_loc = settings.get("workbench.sideBar.location")
        if sidebar_loc == "right":
            print(f"PASS: Component 2 — sideBar.location is 'right' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — expected sideBar.location='right', found: {sidebar_loc!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Minimap enabled with render scale 2 (0.25 points)
    # Both sub-checks must pass for full credit
    try:
        minimap_enabled = settings.get("editor.minimap.enabled")
        minimap_scale = settings.get("editor.minimap.scale")
        if minimap_enabled is True and minimap_scale == 2:
            print(f"PASS: Component 3 — minimap enabled with scale=2 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — expected minimap.enabled=True and minimap.scale=2, "
                  f"found enabled={minimap_enabled!r}, scale={minimap_scale!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Breadcrumbs enabled with filePath 'on' (0.25 points)
    # Both sub-checks must pass for full credit
    try:
        breadcrumbs_enabled = settings.get("breadcrumbs.enabled")
        breadcrumbs_filepath = settings.get("breadcrumbs.filePath")
        if breadcrumbs_enabled is True and breadcrumbs_filepath == "on":
            print(f"PASS: Component 4 — breadcrumbs enabled with filePath='on' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — expected breadcrumbs.enabled=True and breadcrumbs.filePath='on', "
                  f"found enabled={breadcrumbs_enabled!r}, filePath={breadcrumbs_filepath!r}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
