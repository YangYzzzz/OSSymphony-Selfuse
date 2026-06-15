"""
Reward Script: Enable trailing whitespace trimming globally but disable it for Markdown files.
Task ID: vscode_code_060
Domain: vs_code
Scoring:
  Component 1: files.trimTrailingWhitespace == true (global setting)         (0.5 pts)
  Component 2: [markdown].files.trimTrailingWhitespace == false (override)   (0.5 pts)
  Total: 1.0
"""

import os
import json
import re

WORKDIR = '/home/user'
SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_settings(path):
    """Load settings.json, stripping JSONC-style // comments before parsing."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line // comments (JSONC support)
        content_stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_stripped)
    except FileNotFoundError:
        print(f"ERROR: settings.json not found at {path}")
        return None
    except json.JSONDecodeError as e:
        print(f"ERROR: Could not parse settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: settings.json must exist and be parseable
    settings = load_settings(SETTINGS_PATH)
    if settings is None:
        print("CRITICAL: settings.json missing or unparseable — cannot verify task")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Loaded settings.json with {len(settings)} top-level keys: {list(settings.keys())}")

    # Component 1: Global files.trimTrailingWhitespace is set to true (0.5 points)
    # This must FAIL on initial_env (key not present) and PASS on golden_env
    try:
        global_trim = settings.get('files.trimTrailingWhitespace', None)
        if global_trim is True:
            print("PASS: Component 1 — files.trimTrailingWhitespace is true globally (0.5 pts)")
            total_score += 0.5
        elif global_trim is None:
            print("FAIL: Component 1 — files.trimTrailingWhitespace key is absent from settings.json")
        elif global_trim is False:
            print("FAIL: Component 1 — files.trimTrailingWhitespace is false (expected true)")
        else:
            print(f"FAIL: Component 1 — files.trimTrailingWhitespace has unexpected value: {global_trim!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: [markdown] language override disables trimTrailingWhitespace (0.5 points)
    # This must FAIL on initial_env (key not present) and PASS on golden_env
    try:
        markdown_overrides = settings.get('[markdown]', None)
        if markdown_overrides is None:
            print("FAIL: Component 2 — [markdown] language override block is absent from settings.json")
        elif not isinstance(markdown_overrides, dict):
            print(f"FAIL: Component 2 — [markdown] is not a dict, got: {type(markdown_overrides).__name__}")
        else:
            md_trim = markdown_overrides.get('files.trimTrailingWhitespace', None)
            if md_trim is False:
                print("PASS: Component 2 — [markdown].files.trimTrailingWhitespace is false (0.5 pts)")
                total_score += 0.5
            elif md_trim is None:
                print("FAIL: Component 2 — [markdown] block exists but files.trimTrailingWhitespace key is absent")
            elif md_trim is True:
                print("FAIL: Component 2 — [markdown].files.trimTrailingWhitespace is true (expected false)")
            else:
                print(f"FAIL: Component 2 — [markdown].files.trimTrailingWhitespace has unexpected value: {md_trim!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
