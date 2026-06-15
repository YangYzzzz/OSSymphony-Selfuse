"""
Reward Script: Uninstall Bracket Pair Colorizer extension and enable native bracket pair colorization
Task ID: vscode_we_060
Domain: vscode
Scoring:
  - Component 1 (0.4): Extension CoenraadS.bracket-pair-colorizer-2 is uninstalled
  - Component 2 (0.3): editor.bracketPairColorization.enabled is true in settings.json
  - Component 3 (0.3): editor.guides.bracketPairs is "active" in settings.json
"""

import json
import os
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
        # Strip JSONC comments before parsing
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARNING: Could not load settings.json: {e}")
        return None


def check_extension_installed(extension_id):
    """Check if a VSCode extension is installed via CLI."""
    try:
        result = subprocess.run(
            ["code", "--list-extensions"],
            capture_output=True, text=True, timeout=15
        )
        installed = [ext.strip().lower() for ext in result.stdout.strip().split('\n') if ext.strip()]
        return extension_id.lower() in installed
    except Exception as e:
        print(f"WARNING: Could not list extensions: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Extension CoenraadS.bracket-pair-colorizer-2 is uninstalled (0.4 points)
    try:
        ext_installed = check_extension_installed("CoenraadS.bracket-pair-colorizer-2")
        if ext_installed is None:
            print("ERROR: Component 1 -- could not determine extension status")
        elif not ext_installed:
            print("PASS: Component 1 -- Extension CoenraadS.bracket-pair-colorizer-2 is NOT installed (0.4 pts)")
            total_score += 0.4
        else:
            print("FAIL: Component 1 -- Extension CoenraadS.bracket-pair-colorizer-2 is still installed")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: editor.bracketPairColorization.enabled is true (0.3 points)
    try:
        settings = load_settings()
        if settings is None:
            print("FAIL: Component 2 -- settings.json not readable")
        else:
            val = settings.get("editor.bracketPairColorization.enabled")
            if val is True:
                print(f"PASS: Component 2 -- editor.bracketPairColorization.enabled is true (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 -- editor.bracketPairColorization.enabled is {val!r}, expected true")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: editor.guides.bracketPairs is "active" (0.3 points)
    try:
        settings = load_settings()
        if settings is None:
            print("FAIL: Component 3 -- settings.json not readable")
        else:
            val = settings.get("editor.guides.bracketPairs")
            if val == "active":
                print(f"PASS: Component 3 -- editor.guides.bracketPairs is 'active' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 -- editor.guides.bracketPairs is {val!r}, expected 'active'")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
