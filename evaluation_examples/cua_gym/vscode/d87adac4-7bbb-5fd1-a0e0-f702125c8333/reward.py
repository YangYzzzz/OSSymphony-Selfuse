"""
Reward Script: Enable minimap in VSCode editor
Task ID: vscode_stu_015
Domain: vscode
Scoring:
  Component 1 (0.6): editor.minimap.enabled is true in settings.json
  Component 2 (0.4): editor.minimap.enabled is explicitly set to true (not absent/default)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_015'
SETTINGS_PATH = os.path.expanduser('~/.config/Code/User/settings.json')


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("CRITICAL: settings.json not found or invalid")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: editor.minimap.enabled key exists and is true (0.6 points)
    # This FAILS on initial (minimap.enabled = false) and PASSES on golden (= true)
    try:
        minimap_enabled = settings.get('editor.minimap.enabled')
        if minimap_enabled is True:
            print(f"PASS: Component 1 -- editor.minimap.enabled is true (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 -- editor.minimap.enabled is {minimap_enabled}, expected true")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Verify minimap is on the right side (default) - not explicitly set to left (0.4 points)
    # editor.minimap.side should be absent (defaults to "right") or explicitly "right"
    # This component also re-confirms minimap is enabled, ensuring both conditions for full score.
    # FAILS on initial (minimap.enabled = false) and PASSES on golden (= true)
    try:
        minimap_enabled = settings.get('editor.minimap.enabled')
        minimap_side = settings.get('editor.minimap.side', 'right')  # default is 'right'

        if minimap_enabled is True and minimap_side == 'right':
            print(f"PASS: Component 2 -- minimap enabled AND side is '{minimap_side}' (0.4 pts)")
            total_score += 0.4
        else:
            if minimap_enabled is not True:
                print(f"FAIL: Component 2 -- minimap not enabled (enabled={minimap_enabled})")
            else:
                print(f"FAIL: Component 2 -- minimap side is '{minimap_side}', expected 'right'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
