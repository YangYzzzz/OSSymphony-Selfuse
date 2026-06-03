"""
Reward Script: Enable bracket pair colorization in VSCode
Task ID: vscode_code_047
Domain: vs_code
Scoring:
  Component 1 (0.5): settings.json exists and is valid JSON
  Component 2 (0.5): editor.bracketPairColorization.enabled is set to true
  Total: 1.0
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_047'
SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_settings(settings_path):
    """Load settings.json, handling JSONC (JSON with comments)."""
    try:
        with open(settings_path, 'r') as f:
            content = f.read()
        # Strip JSONC comments (VSCode settings may use them)
        content_stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_stripped)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON parse error: {e}")


def verify_task():
    """
    Verify that bracket pair colorization has been enabled in VSCode settings.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: settings.json exists and is parseable (0.5 points)
    # This check is only meaningful if the file is present and valid; the initial_env
    # has the file with the setting explicitly set to false, so just existence is a
    # precondition — the score is ONLY awarded if the setting is true (Component 2).
    # We use Component 1 as a gate: if file is missing/corrupt we return 0.0 early.
    try:
        settings = load_settings(SETTINGS_PATH)
        if settings is None:
            print(f"FAIL: settings.json not found at {SETTINGS_PATH}")
            print("REWARD: 0.0")
            return 0.0
        print(f"PASS: settings.json found and parsed successfully")
    except ValueError as e:
        print(f"FAIL: settings.json could not be parsed: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: editor.bracketPairColorization.enabled is present in settings (0.3 points)
    # Note: This alone is NOT sufficient — initial_env has it set to false.
    # We only award points if the VALUE is true (see Component 2).
    # We split into: key-present-with-any-value (0.0 guard) + value-is-true (1.0).
    # Since both initial and golden have the key, we must discriminate on value.
    # So we use a single component: value must be True.

    # Component 1: editor.bracketPairColorization.enabled is explicitly set to true (1.0 points)
    try:
        setting_key = 'editor.bracketPairColorization.enabled'
        if setting_key in settings:
            actual_value = settings[setting_key]
            if actual_value is True:
                print(f"PASS: Component 1 — '{setting_key}' is set to true (1.0 pts)")
                total_score += 1.0
            else:
                print(f"FAIL: Component 1 — '{setting_key}' is '{actual_value}', expected true")
        else:
            print(f"FAIL: Component 1 — '{setting_key}' key not found in settings.json")
            print(f"       Available keys: {list(settings.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check bracketPairColorization setting: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
