"""
Reward Script: Configure custom Dracula color theme in VSCode
Task ID: vscode_gf5_010
Domain: vscode
Scoring:
  Component 1 (0.35): Dracula Official extension is installed
  Component 2 (0.35): workbench.colorTheme is set to 'Dracula'
  Component 3 (0.30): workbench.colorCustomizations overrides editor.background to '#1a1a2e'
"""

import os
import json
import re
import subprocess

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARNING: Could not load settings.json: {e}")
        return {}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Dracula Official extension is installed (0.35 points)
    try:
        result = subprocess.run(
            ["code", "--list-extensions"],
            capture_output=True, text=True, timeout=15
        )
        extensions = result.stdout.strip().lower().split('\n')
        # The canonical extension ID is dracula-theme.theme-dracula
        if any("dracula" in ext for ext in extensions):
            print(f"PASS: Component 1 — Dracula extension installed (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — Dracula extension not found. Installed: {extensions}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: workbench.colorTheme is 'Dracula' (0.35 points)
    try:
        settings = load_settings()
        theme = settings.get("workbench.colorTheme", "")
        if isinstance(theme, str) and theme.lower() == "dracula":
            print(f"PASS: Component 2 — colorTheme is '{theme}' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — Expected colorTheme 'Dracula', found: '{theme}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: colorCustomizations editor.background is '#1a1a2e' (0.30 points)
    try:
        settings = load_settings()
        customizations = settings.get("workbench.colorCustomizations", {})
        bg_color = customizations.get("editor.background", "")
        if isinstance(bg_color, str) and bg_color.lower() == "#1a1a2e":
            print(f"PASS: Component 3 — editor.background is '{bg_color}' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — Expected editor.background '#1a1a2e', found: '{bg_color}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
