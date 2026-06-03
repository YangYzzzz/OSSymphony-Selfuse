"""
Reward Script: VSCode User Settings Configuration
Task ID: vscode_gf5_002
Domain: vscode
Scoring:
  Component 1 — editor.fontSize == 16          (0.25 pts)
  Component 2 — editor.tabSize == 2            (0.25 pts)
  Component 3 — editor.formatOnSave == true    (0.25 pts)
  Component 4 — [javascript] defaultFormatter  (0.25 pts)
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
        # Strip JSONC single-line comments before parsing
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify VSCode settings configuration with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    print(f"Loaded settings with {len(settings)} keys")

    # Component 1: editor.fontSize == 16 (0.25 points)
    try:
        font_size = settings.get("editor.fontSize")
        if font_size == 16:
            print(f"PASS: Component 1 — editor.fontSize is 16 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — expected editor.fontSize=16, found: {font_size}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: editor.tabSize == 2 (0.25 points)
    try:
        tab_size = settings.get("editor.tabSize")
        if tab_size == 2:
            print(f"PASS: Component 2 — editor.tabSize is 2 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — expected editor.tabSize=2, found: {tab_size}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: editor.formatOnSave == true (0.25 points)
    try:
        format_on_save = settings.get("editor.formatOnSave")
        if format_on_save is True:
            print(f"PASS: Component 3 — editor.formatOnSave is true (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — expected editor.formatOnSave=true, found: {format_on_save}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: [javascript].editor.defaultFormatter == "esbenp.prettier-vscode" (0.25 points)
    try:
        js_section = settings.get("[javascript]")
        if isinstance(js_section, dict):
            formatter = js_section.get("editor.defaultFormatter")
            if formatter == "esbenp.prettier-vscode":
                print(f"PASS: Component 4 — [javascript] defaultFormatter is esbenp.prettier-vscode (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 — expected formatter='esbenp.prettier-vscode', found: {formatter}")
        else:
            print(f"FAIL: Component 4 — [javascript] section not found or not a dict, found: {js_section}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
