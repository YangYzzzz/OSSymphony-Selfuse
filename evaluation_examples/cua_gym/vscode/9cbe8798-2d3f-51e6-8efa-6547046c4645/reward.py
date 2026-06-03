"""
Reward Script: Enable automatic trimming of trailing whitespace when saving files.
Task ID: vscode_code_059
Domain: vs_code
Scoring:
  Component 1: 'files.trimTrailingWhitespace' key exists in settings.json (0.5 pts)
  Component 2: 'files.trimTrailingWhitespace' value is exactly True (0.5 pts)
  Total: 1.0
"""

import os
import json
import re

SETTINGS_PATH = '/home/user/.config/Code/User/settings.json'
TASK_ID = 'vscode_code_059'


def load_settings(path):
    """Load settings.json, stripping JSONC-style // comments before parsing."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments (VSCode JSONC format)
        content_stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_stripped)
    except FileNotFoundError:
        print(f"CRITICAL: settings.json not found at {path}")
        return None
    except json.JSONDecodeError as e:
        print(f"CRITICAL: Failed to parse settings.json: {e}")
        return None


def verify_task():
    """
    Verify that VSCode is configured to trim trailing whitespace on save.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must exist and be parseable
    settings = load_settings(SETTINGS_PATH)
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    # Component 1: 'files.trimTrailingWhitespace' key exists in settings.json (0.5 points)
    # This FAILS on initial_env (key not present) → PASSES on golden_env (key present)
    try:
        if 'files.trimTrailingWhitespace' in settings:
            print("PASS: Component 1 — 'files.trimTrailingWhitespace' key is present in settings.json (0.5 pts)")
            total_score += 0.5
        else:
            print("FAIL: Component 1 — 'files.trimTrailingWhitespace' key is NOT present in settings.json")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'files.trimTrailingWhitespace' is set to True (0.5 points)
    # This FAILS on initial_env (key missing) → PASSES on golden_env (value is True)
    try:
        value = settings.get('files.trimTrailingWhitespace')
        if value is True:
            print(f"PASS: Component 2 — 'files.trimTrailingWhitespace' is set to true (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — Expected true, found: {value!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
