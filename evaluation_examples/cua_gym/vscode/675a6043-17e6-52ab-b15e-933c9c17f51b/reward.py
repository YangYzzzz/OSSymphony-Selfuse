"""
Reward Script: Configure Better Comments extension FIXME tag in VSCode settings
Task ID: vscode_gf3_024
Domain: vscode
Scoring:
  Component 1: better-comments.tags exists and is a list (0.2)
  Component 2: A tag entry with tag="FIXME:" exists (0.3)
  Component 3: The FIXME tag has color="#FF2D00" (0.25)
  Component 4: The FIXME tag has bold=true (0.25)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_024'

SETTINGS_PATH = os.path.expanduser("~/.config/Code/User/settings.json")


def load_settings(path):
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(path, "r") as f:
            content = f.read()
        # Strip single-line comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings: {e}")
        return None


def verify_task():
    """
    Verify that Better Comments FIXME tag is configured in VSCode settings.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings(SETTINGS_PATH)
    if settings is None:
        print("CRITICAL: Cannot load settings.json")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: better-comments.tags exists and is a list (0.2 points)
    try:
        tags = settings.get("better-comments.tags")
        if isinstance(tags, list):
            print(f"PASS: Component 1 -- better-comments.tags is a list with {len(tags)} entries (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- better-comments.tags not found or not a list, got: {type(tags)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Find the FIXME: tag entry for subsequent checks
    fixme_tag = None
    if isinstance(tags, list):
        for entry in tags:
            if isinstance(entry, dict) and entry.get("tag") == "FIXME:":
                fixme_tag = entry
                break

    # Component 2: A tag entry with tag="FIXME:" exists (0.3 points)
    try:
        if fixme_tag is not None:
            print(f"PASS: Component 2 -- Found tag entry with tag='FIXME:' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- No tag entry with tag='FIXME:' found in better-comments.tags")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: The FIXME tag has color="#FF2D00" (0.25 points)
    try:
        if fixme_tag is not None:
            color = fixme_tag.get("color")
            # Case-insensitive comparison for hex colors
            if isinstance(color, str) and color.upper() == "#FF2D00":
                print(f"PASS: Component 3 -- FIXME tag color is '{color}' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 -- Expected color '#FF2D00', found: {color}")
        else:
            print(f"FAIL: Component 3 -- No FIXME tag to check color on")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: The FIXME tag has bold=true (0.25 points)
    try:
        if fixme_tag is not None:
            bold = fixme_tag.get("bold")
            if bold is True:
                print(f"PASS: Component 4 -- FIXME tag bold is True (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 -- Expected bold=true, found: {bold}")
        else:
            print(f"FAIL: Component 4 -- No FIXME tag to check bold on")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
