"""
Reward Script: VSCode axe Accessibility Linter configuration
Task ID: vscode_gf3_016
Domain: vscode
Scoring:
  - Component 1 (0.35): axe Accessibility Linter extension installed
  - Component 2 (0.35): axe-linter.lintHTML set to true in User settings
  - Component 3 (0.30): axe-linter.rules disables color-contrast
"""

import os
import json
import re
import glob

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")
EXTENSIONS_DIR = os.path.join(HOME, ".vscode", "extensions")


def load_settings():
    """Load VSCode settings.json, handling JSONC (comments)."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip single-line comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        # Strip multi-line comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
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

    # Component 1: axe Accessibility Linter extension is installed (0.35 points)
    # Check by looking for extension directory in ~/.vscode/extensions/
    try:
        ext_dirs = os.listdir(EXTENSIONS_DIR) if os.path.isdir(EXTENSIONS_DIR) else []
        axe_installed = any(
            d.lower().startswith("deque-systems.vscode-axe-linter")
            for d in ext_dirs
        )
        if axe_installed:
            print(f"PASS: Component 1 — axe-linter extension installed (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — axe-linter extension not found in {EXTENSIONS_DIR}. Found: {ext_dirs}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: axe-linter.lintHTML set to true in settings.json (0.35 points)
    try:
        settings = load_settings()
        if settings is None:
            print("FAIL: Component 2 — settings.json could not be loaded")
        else:
            lint_html = settings.get("axe-linter.lintHTML")
            if lint_html is True:
                print(f"PASS: Component 2 — axe-linter.lintHTML is true (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 — axe-linter.lintHTML expected true, found: {lint_html!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: axe-linter.rules disables color-contrast (0.30 points)
    try:
        settings = load_settings()
        if settings is None:
            print("FAIL: Component 3 — settings.json could not be loaded")
        else:
            rules = settings.get("axe-linter.rules")
            if isinstance(rules, dict):
                cc_value = rules.get("color-contrast")
                # Accept "off", "disabled", or False as valid disable values
                if cc_value in ("off", "disabled", False):
                    print(f"PASS: Component 3 — color-contrast rule disabled (value: {cc_value!r}) (0.30 pts)")
                    total_score += 0.30
                else:
                    print(f"FAIL: Component 3 — color-contrast expected 'off', found: {cc_value!r}")
            else:
                print(f"FAIL: Component 3 — axe-linter.rules expected dict, found: {type(rules).__name__} = {rules!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
