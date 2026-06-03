"""
Reward Script: Change VSCode color theme to Monokai and icon theme to Seti
Task ID: vscode_wf_002
Domain: vs_code
Scoring:
  - Component 1: workbench.colorTheme == "Monokai" (0.5 pts)
  - Component 2: workbench.iconTheme == "vs-seti" (0.5 pts)
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
        # Strip JSONC-style comments before parsing
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
        print("CRITICAL: settings.json not found or unreadable")
        print("REWARD: 0.0")
        return 0.0

    print(f"Loaded settings: {json.dumps(settings, indent=2)}")

    # Component 1: workbench.colorTheme == "Monokai" (0.5 points)
    try:
        color_theme = settings.get("workbench.colorTheme")
        if color_theme == "Monokai":
            print(f"PASS: Component 1 -- colorTheme is 'Monokai' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 -- expected colorTheme 'Monokai', found: '{color_theme}'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: workbench.iconTheme == "vs-seti" (0.5 points)
    try:
        icon_theme = settings.get("workbench.iconTheme")
        if icon_theme == "vs-seti":
            print(f"PASS: Component 2 -- iconTheme is 'vs-seti' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 -- expected iconTheme 'vs-seti', found: '{icon_theme}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved VSCode state before verification
def persist_app_state():
    """Best-effort save of VSCode settings via Ctrl+S."""
    try:
        os.environ["DISPLAY"] = ":0"
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        import time
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for VSCode")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


persist_app_state()
verify_task()
