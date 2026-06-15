"""
Reward Script: Customize editor appearance settings in VSCode
Task ID: vscode_we_042
Domain: vscode
Scoring:
  - Component 1: editor.guides.indentation == false (0.2)
  - Component 2: editor.linkedEditing == true (0.2)
  - Component 3: editor.cursorBlinking == "phase" (0.2)
  - Component 4: editor.smoothScrolling == true (0.2)
  - Component 5: terminal.integrated.smoothScrolling == true (0.2)
"""

import os
import json
import re

SETTINGS_PATH = os.path.expanduser("~/.config/Code/User/settings.json")


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARN: Could not load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("CRITICAL: Cannot load settings.json")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: editor.guides.indentation is false (0.2 points)
    # Task requires disabling indent guides
    try:
        val = settings.get("editor.guides.indentation")
        if val is False:
            print(f"PASS: Component 1 - editor.guides.indentation is false (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 - expected editor.guides.indentation=false, found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: editor.linkedEditing is true (0.2 points)
    # Task requires enabling linked editing for HTML tags
    try:
        val = settings.get("editor.linkedEditing")
        if val is True:
            print(f"PASS: Component 2 - editor.linkedEditing is true (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 - expected editor.linkedEditing=true, found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: editor.cursorBlinking is "phase" (0.2 points)
    # Task requires setting cursor blinking to 'phase'
    try:
        val = settings.get("editor.cursorBlinking")
        if isinstance(val, str) and val.lower() == "phase":
            print(f"PASS: Component 3 - editor.cursorBlinking is 'phase' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 - expected editor.cursorBlinking='phase', found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: editor.smoothScrolling is true (0.2 points)
    # Task requires enabling smooth scrolling for editor
    try:
        val = settings.get("editor.smoothScrolling")
        if val is True:
            print(f"PASS: Component 4 - editor.smoothScrolling is true (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 - expected editor.smoothScrolling=true, found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: terminal.integrated.smoothScrolling is true (0.2 points)
    # Task requires enabling smooth scrolling for terminal
    try:
        val = settings.get("terminal.integrated.smoothScrolling")
        if val is True:
            print(f"PASS: Component 5 - terminal.integrated.smoothScrolling is true (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 5 - expected terminal.integrated.smoothScrolling=true, found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
