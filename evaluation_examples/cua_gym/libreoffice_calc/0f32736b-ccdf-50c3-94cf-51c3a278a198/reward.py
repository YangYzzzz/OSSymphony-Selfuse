"""
Reward Script: Configure VSCode editor settings for pair programming
Task ID: vscode_we_034
Domain: vscode (libreoffice_calc label, but actually VSCode settings)
Scoring: 5 settings x 0.2 points each = 1.0
"""

import os
import json
import re

HOME = '/home/user'
SETTINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'settings.json')
TASK_ID = 'vscode_we_034'


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments before parsing
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except FileNotFoundError:
        print(f"CRITICAL: Settings file not found: {SETTINGS_PATH}")
        return None
    except json.JSONDecodeError as e:
        print(f"CRITICAL: Cannot parse settings.json: {e}")
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

    # Component 1: editor.fontSize == 16 (0.2 points)
    try:
        font_size = settings.get('editor.fontSize')
        if font_size == 16:
            print(f"PASS: Component 1 -- editor.fontSize is 16 (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- expected editor.fontSize=16, found: {font_size}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: editor.stickyScroll.enabled == true (0.2 points)
    try:
        sticky_scroll = settings.get('editor.stickyScroll.enabled')
        if sticky_scroll is True:
            print(f"PASS: Component 2 -- editor.stickyScroll.enabled is true (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 -- expected editor.stickyScroll.enabled=true, found: {sticky_scroll}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: editor.lineNumbers == "relative" (0.2 points)
    try:
        line_numbers = settings.get('editor.lineNumbers')
        if line_numbers == 'relative':
            print(f"PASS: Component 3 -- editor.lineNumbers is 'relative' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 -- expected editor.lineNumbers='relative', found: {line_numbers}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: editor.bracketPairColorization.enabled == true (0.2 points)
    try:
        bracket_color = settings.get('editor.bracketPairColorization.enabled')
        if bracket_color is True:
            print(f"PASS: Component 4 -- editor.bracketPairColorization.enabled is true (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 -- expected editor.bracketPairColorization.enabled=true, found: {bracket_color}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: editor.cursorStyle == "block" (0.2 points)
    try:
        cursor_style = settings.get('editor.cursorStyle')
        if cursor_style == 'block':
            print(f"PASS: Component 5 -- editor.cursorStyle is 'block' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 5 -- expected editor.cursorStyle='block', found: {cursor_style}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
