"""
Reward Script: Set word wrap column to 80 characters in VSCode settings
Task ID: vscode_edit_047
Domain: vs_code
Scoring:
  Component 1: editor.wordWrap == "wordWrapColumn"   (0.5 points)
  Component 2: editor.wordWrapColumn == 80            (0.5 points)
  Total: 1.0
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_047'
SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_settings(path):
    """Load settings.json, stripping JSONC-style comments if present."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line // comments (JSONC support)
        content_stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_stripped)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse {path}: {e}")
        return None


def verify_task(settings_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    The task requires:
      1. editor.wordWrap changed from "on" to "wordWrapColumn"
      2. editor.wordWrapColumn set to 80
    """
    total_score = 0.0

    # Precondition: settings file must exist and be parseable
    settings = load_settings(settings_path)
    if settings is None:
        print(f"CRITICAL: Cannot load settings from {settings_path}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: editor.wordWrap set to "wordWrapColumn" (0.5 points)
    # Initial state has "editor.wordWrap": "on" — this check FAILS there.
    # Golden state has "editor.wordWrap": "wordWrapColumn" — this check PASSES there.
    try:
        actual_wrap = settings.get('editor.wordWrap')
        expected_wrap = 'wordWrapColumn'
        if actual_wrap == expected_wrap:
            print(f"PASS: Component 1 — editor.wordWrap == 'wordWrapColumn' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — expected editor.wordWrap='wordWrapColumn', found: {actual_wrap!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: editor.wordWrapColumn set to 80 (0.5 points)
    # Initial state has no editor.wordWrapColumn key — this check FAILS there.
    # Golden state has "editor.wordWrapColumn": 80 — this check PASSES there.
    try:
        actual_col = settings.get('editor.wordWrapColumn')
        expected_col = 80
        if actual_col == expected_col:
            print(f"PASS: Component 2 — editor.wordWrapColumn == 80 (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — expected editor.wordWrapColumn=80, found: {actual_col!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: verify against canonical settings path on VM
if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(SETTINGS_PATH)
