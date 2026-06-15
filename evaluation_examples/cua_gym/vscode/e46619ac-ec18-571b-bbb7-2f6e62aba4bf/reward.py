"""
Reward Script: Set up workspace setting to enforce LF for all file types
Task ID: vscode_code_069
Domain: vs_code
Scoring:
  Component 1 (0.5): Workspace settings.json exists at /home/user/project/.vscode/settings.json and is valid JSON
  Component 2 (0.5): settings.json contains "files.eol" set to "\n" (LF)
Total: 1.0
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_069'
SETTINGS_PATH = '/home/user/project/.vscode/settings.json'


def load_settings_json(path):
    """Load a settings.json (JSONC) file, stripping // comments. Returns dict or None."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Handle JSONC (JSON with comments) by stripping line comments
        clean_content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(clean_content)
    except Exception:
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Create /home/user/project/.vscode/settings.json with files.eol = "\n" (LF).
    This workspace setting enforces LF line endings for new files in the project.
    """
    total_score = 0.0

    # Component 1: Workspace settings.json exists and is valid JSON (0.5 points)
    # This FAILS on initial_env (no .vscode dir) and PASSES on golden_env
    settings_data = None
    try:
        settings_data = load_settings_json(SETTINGS_PATH)
        if settings_data is not None:
            print(f"PASS: Component 1 — settings.json exists and is valid JSON at {SETTINGS_PATH}")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — settings.json not found or invalid JSON at {SETTINGS_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: files.eol setting is "\n" (LF) in workspace settings (0.5 points)
    # This FAILS on initial_env (no settings.json) and PASSES on golden_env
    try:
        if settings_data is None:
            print("FAIL: Component 2 — cannot check files.eol (settings.json not loaded)")
        elif settings_data.get('files.eol') == '\n':
            print(f"PASS: Component 2 — files.eol is set to LF ('\\n') in workspace settings")
            total_score += 0.5
        else:
            eol_value = settings_data.get('files.eol')
            print(f"FAIL: Component 2 — expected files.eol='\\n' (LF), found: {repr(eol_value)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
