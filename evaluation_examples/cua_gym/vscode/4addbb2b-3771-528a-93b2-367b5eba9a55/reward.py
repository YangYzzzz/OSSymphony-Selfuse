"""
Reward Script: Set up a complete editor configuration for accessibility
Task ID: vscode_we_041
Domain: vscode
Scoring:
  Component 1: editor.cursorWidth == 3          (0.2 pts)
  Component 2: editor.accessibilitySupport == "on" (0.2 pts)
  Component 3: editor.lineHeight == 1.8         (0.2 pts)
  Component 4: editor.letterSpacing == 0.5      (0.2 pts)
  Component 5: workbench.colorTheme == "Default High Contrast" (0.2 pts)
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")


def load_settings():
    """Load VSCode settings.json, handling JSONC (comments)."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip // comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARN: Could not load settings.json: {e}")
        return None


def verify_task():
    """
    Verify accessibility configuration in VSCode settings.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("CRITICAL: settings.json not found or invalid")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: editor.cursorWidth == 3 (0.2 points)
    try:
        val = settings.get("editor.cursorWidth")
        if val is not None and val == 3:
            print(f"PASS: Component 1 — editor.cursorWidth is {val} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — expected editor.cursorWidth == 3, found: {val}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: editor.accessibilitySupport == "on" (0.2 points)
    try:
        val = settings.get("editor.accessibilitySupport")
        if val is not None and str(val).lower() == "on":
            print(f"PASS: Component 2 — editor.accessibilitySupport is '{val}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — expected editor.accessibilitySupport == 'on', found: {val}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: editor.lineHeight == 1.8 (0.2 points)
    try:
        val = settings.get("editor.lineHeight")
        if val is not None and abs(float(val) - 1.8) < 0.01:
            print(f"PASS: Component 3 — editor.lineHeight is {val} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — expected editor.lineHeight == 1.8, found: {val}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: editor.letterSpacing == 0.5 (0.2 points)
    try:
        val = settings.get("editor.letterSpacing")
        if val is not None and abs(float(val) - 0.5) < 0.01:
            print(f"PASS: Component 4 — editor.letterSpacing is {val} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — expected editor.letterSpacing == 0.5, found: {val}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: workbench.colorTheme == "Default High Contrast" (0.2 points)
    try:
        val = settings.get("workbench.colorTheme")
        if val is not None and val == "Default High Contrast":
            print(f"PASS: Component 5 — workbench.colorTheme is '{val}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 5 — expected workbench.colorTheme == 'Default High Contrast', found: {val}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
