"""
Reward Script: Configure VSCode language-specific indentation
Task ID: vscode_we_014
Domain: vscode
Scoring:
  Component 1 (0.5): [javascript] override with editor.tabSize = 2
  Component 2 (0.5): [typescript] override with editor.tabSize = 2
  Precondition: settings.json must be readable JSON
"""

import json
import os
import re

SETTINGS_PATH = os.path.expanduser("~/.config/Code/User/settings.json")


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
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must be loadable
    settings = load_settings()
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    # Component 1: [javascript] language override with editor.tabSize = 2 (0.5 points)
    # This checks a task-introduced change: initial_env has no [javascript] override
    try:
        js_override = settings.get("[javascript]", {})
        js_tab_size = js_override.get("editor.tabSize")
        if isinstance(js_override, dict) and js_tab_size == 2:
            print(f"PASS: Component 1 — [javascript] editor.tabSize = {js_tab_size} (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — expected [javascript].editor.tabSize = 2, found: {js_tab_size}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: [typescript] language override with editor.tabSize = 2 (0.5 points)
    # This checks a task-introduced change: initial_env has no [typescript] override
    try:
        ts_override = settings.get("[typescript]", {})
        ts_tab_size = ts_override.get("editor.tabSize")
        if isinstance(ts_override, dict) and ts_tab_size == 2:
            print(f"PASS: Component 2 — [typescript] editor.tabSize = {ts_tab_size} (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — expected [typescript].editor.tabSize = 2, found: {ts_tab_size}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
