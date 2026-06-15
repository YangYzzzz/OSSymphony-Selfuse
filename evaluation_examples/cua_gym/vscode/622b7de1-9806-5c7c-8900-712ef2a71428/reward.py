"""
Reward Script: Configure JavaScript import suggestions to prefer relative path imports
                over absolute paths and enable auto-import updates on file move.
Task ID: vscode_lp_052
Domain: vscode
Scoring:
  Component 1 (0.5): javascript.preferences.importModuleSpecifier == "relative"
  Component 2 (0.5): javascript.updateImportsOnFileMove.enabled == "always"
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")
TASK_ID = "vscode_lp_052"


def load_settings():
    """Load VSCode settings.json, handling JSONC (comments)."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip // comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except FileNotFoundError:
        print(f"CRITICAL: settings.json not found at {SETTINGS_PATH}")
        return None
    except json.JSONDecodeError as e:
        print(f"CRITICAL: settings.json is not valid JSON: {e}")
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

    # Component 1: javascript.preferences.importModuleSpecifier == "relative" (0.5 points)
    # This setting controls whether VSCode suggests relative or absolute import paths.
    # Task requires it to be set to "relative".
    try:
        value = settings.get("javascript.preferences.importModuleSpecifier")
        if value == "relative":
            print(f"PASS: Component 1 — importModuleSpecifier is 'relative' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — expected 'relative', found: {value!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: javascript.updateImportsOnFileMove.enabled == "always" (0.5 points)
    # This setting controls whether moving a file updates its import references.
    # Task requires it to be set to "always".
    try:
        value = settings.get("javascript.updateImportsOnFileMove.enabled")
        if value == "always":
            print(f"PASS: Component 2 — updateImportsOnFileMove is 'always' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — expected 'always', found: {value!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
