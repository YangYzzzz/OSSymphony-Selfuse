"""
Reward Script: Custom color theme override in VSCode settings
Task ID: vscode_web_064
Domain: vscode
Scoring:
  Component 1: editor.background == '#1a1a2e'         — 0.30 pts
  Component 2: sideBar.background == '#16213e'         — 0.30 pts
  Component 3: activityBar.background == '#0f3460'     — 0.30 pts
  Component 4: Theme still Default Dark+ with overrides — 0.10 pts
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
        # Strip // comments (JSONC)
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

    # Get colorCustomizations block (precondition for all components)
    color_customizations = settings.get("workbench.colorCustomizations")
    if not isinstance(color_customizations, dict):
        print("FAIL: workbench.colorCustomizations not found or not a dict")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: editor.background == '#1a1a2e' (0.30 points)
    try:
        editor_bg = color_customizations.get("editor.background", "")
        if isinstance(editor_bg, str) and editor_bg.strip().lower() == "#1a1a2e":
            print(f"PASS: Component 1 — editor.background is '{editor_bg}' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — expected editor.background '#1a1a2e', found '{editor_bg}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: sideBar.background == '#16213e' (0.30 points)
    try:
        sidebar_bg = color_customizations.get("sideBar.background", "")
        if isinstance(sidebar_bg, str) and sidebar_bg.strip().lower() == "#16213e":
            print(f"PASS: Component 2 — sideBar.background is '{sidebar_bg}' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — expected sideBar.background '#16213e', found '{sidebar_bg}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: activityBar.background == '#0f3460' (0.30 points)
    try:
        activity_bg = color_customizations.get("activityBar.background", "")
        if isinstance(activity_bg, str) and activity_bg.strip().lower() == "#0f3460":
            print(f"PASS: Component 3 — activityBar.background is '{activity_bg}' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — expected activityBar.background '#0f3460', found '{activity_bg}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Theme still Default Dark+ AND all 3 color overrides present (0.10 points)
    # This verifies the user didn't install a new theme extension — they used colorCustomizations
    try:
        theme = settings.get("workbench.colorTheme", "")
        has_all_three = all(
            k in color_customizations
            for k in ("editor.background", "sideBar.background", "activityBar.background")
        )
        if theme == "Default Dark+" and has_all_three:
            print(f"PASS: Component 4 — Theme is '{theme}' with all 3 color overrides (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — Theme='{theme}', all_3_keys={has_all_three}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
