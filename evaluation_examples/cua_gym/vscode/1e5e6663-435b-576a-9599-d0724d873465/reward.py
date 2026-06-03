"""
Reward Script: Configure Todo Tree extension with custom tag highlights
Task ID: vscode_we_068
Domain: vscode
Scoring:
  Component 1 (0.3) — todo-tree.general.tags contains all 4 tags
  Component 2 (0.3) — customHighlight has entries for all 4 tags with correct backgrounds
  Component 3 (0.2) — All 4 tags have foreground "#fff"
  Component 4 (0.2) — All 4 tags have correct icon assignments
"""

import os
import json
import re

SETTINGS_PATH = os.path.expanduser("~/.config/Code/User/settings.json")

EXPECTED_TAGS = ["TODO", "FIXME", "HACK", "BUG"]

EXPECTED_HIGHLIGHTS = {
    "TODO": {"foreground": "#fff", "background": "#ffbd2a", "icon": "check"},
    "FIXME": {"foreground": "#fff", "background": "#ff2a2a", "icon": "bug"},
    "HACK": {"foreground": "#fff", "background": "#8b008b", "icon": "alert"},
    "BUG": {"foreground": "#fff", "background": "#d32f2f", "icon": "bug"},
}


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip JSONC comments
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

    # Component 1: todo-tree.general.tags contains all 4 required tags (0.3 points)
    try:
        tags = settings.get("todo-tree.general.tags", [])
        if isinstance(tags, list) and set(EXPECTED_TAGS).issubset(set(tags)):
            print(f"PASS: Component 1 — tags list contains all 4 tags: {tags} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — expected tags {EXPECTED_TAGS}, found: {tags}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: customHighlight entries exist for all 4 tags with correct background colors (0.3 points)
    try:
        highlights = settings.get("todo-tree.highlights.customHighlight", {})
        if not isinstance(highlights, dict):
            print(f"FAIL: Component 2 — customHighlight is not a dict: {type(highlights)}")
        else:
            bg_matches = 0
            for tag in EXPECTED_TAGS:
                if tag in highlights and isinstance(highlights[tag], dict):
                    actual_bg = highlights[tag].get("background", "")
                    expected_bg = EXPECTED_HIGHLIGHTS[tag]["background"]
                    if actual_bg.lower() == expected_bg.lower():
                        bg_matches += 1
                    else:
                        print(f"  DETAIL: {tag} background mismatch: expected {expected_bg}, got {actual_bg}")
                else:
                    print(f"  DETAIL: {tag} missing from customHighlight")

            if bg_matches == 4:
                print(f"PASS: Component 2 — all 4 tags have correct background colors (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — {bg_matches}/4 tags have correct background colors")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 4 tags have foreground "#fff" (0.2 points)
    try:
        highlights = settings.get("todo-tree.highlights.customHighlight", {})
        fg_matches = 0
        for tag in EXPECTED_TAGS:
            if tag in highlights and isinstance(highlights[tag], dict):
                actual_fg = highlights[tag].get("foreground", "")
                # Accept common white variants: #fff, #ffffff, #FFF, #FFFFFF
                if actual_fg.lower() in ("#fff", "#ffffff"):
                    fg_matches += 1
                else:
                    print(f"  DETAIL: {tag} foreground mismatch: expected #fff, got {actual_fg}")
            else:
                print(f"  DETAIL: {tag} missing from customHighlight")

        if fg_matches == 4:
            print(f"PASS: Component 3 — all 4 tags have white foreground (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — {fg_matches}/4 tags have correct foreground")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: All 4 tags have correct icon assignments (0.2 points)
    try:
        highlights = settings.get("todo-tree.highlights.customHighlight", {})
        icon_matches = 0
        for tag in EXPECTED_TAGS:
            if tag in highlights and isinstance(highlights[tag], dict):
                actual_icon = highlights[tag].get("icon", "")
                expected_icon = EXPECTED_HIGHLIGHTS[tag]["icon"]
                if actual_icon == expected_icon:
                    icon_matches += 1
                else:
                    print(f"  DETAIL: {tag} icon mismatch: expected {expected_icon}, got {actual_icon}")
            else:
                print(f"  DETAIL: {tag} missing from customHighlight")

        if icon_matches == 4:
            print(f"PASS: Component 4 — all 4 tags have correct icons (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — {icon_matches}/4 tags have correct icons")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
