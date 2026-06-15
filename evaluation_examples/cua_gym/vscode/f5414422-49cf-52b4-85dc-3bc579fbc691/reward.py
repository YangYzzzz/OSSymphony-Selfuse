"""
Reward Script: Disable Code Lens globally but enable it for Python only
Task ID: vscode_prod_020
Domain: vscode
Scoring:
  Component 1 (0.4): editor.codeLens is false globally
  Component 2 (0.4): [python] language override has editor.codeLens true
  Component 3 (0.2): Both settings coexist (compound verification)
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
        print(f"CRITICAL: Cannot load settings.json: {e}")
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

    print(f"INFO: Loaded settings with keys: {list(settings.keys())}")

    # Component 1: editor.codeLens is set to false globally (0.4 points)
    # Initial state has editor.codeLens = true, golden has it = false
    try:
        codelens_global = settings.get("editor.codeLens")
        if codelens_global is False:
            print(f"PASS: Component 1 — editor.codeLens is false globally (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — expected editor.codeLens=false, found: {codelens_global}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: [python] language-specific override with editor.codeLens = true (0.4 points)
    # Initial state has no [python] section, golden has it with codeLens true
    try:
        python_section = settings.get("[python]")
        if isinstance(python_section, dict):
            python_codelens = python_section.get("editor.codeLens")
            if python_codelens is True:
                print(f"PASS: Component 2 — [python].editor.codeLens is true (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — [python] section exists but editor.codeLens={python_codelens}")
        else:
            print(f"FAIL: Component 2 — no [python] language-specific section found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Both global disable AND python enable coexist (0.2 points)
    # This is a compound check: only passes when BOTH conditions are true together
    # Ensures the task was completed fully (not just one half)
    try:
        global_disabled = settings.get("editor.codeLens") is False
        python_section = settings.get("[python]")
        python_enabled = (
            isinstance(python_section, dict)
            and python_section.get("editor.codeLens") is True
        )
        if global_disabled and python_enabled:
            print(f"PASS: Component 3 — Both global disable and Python enable coexist (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Compound check: global_disabled={global_disabled}, python_enabled={python_enabled}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
