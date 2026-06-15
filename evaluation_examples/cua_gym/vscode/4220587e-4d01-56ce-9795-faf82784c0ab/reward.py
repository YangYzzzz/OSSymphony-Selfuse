"""
Reward Script: Configure files.exclude to hide __pycache__ directories and .pyc files
Task ID: vscode_file_036
Domain: vs_code
Scoring:
  Component 1: files.exclude key exists in workspace settings.json (0.30 pts)
  Component 2: **/__pycache__ is set to true in files.exclude (0.35 pts)
  Component 3: **/*.pyc is set to true in files.exclude (0.35 pts)
  Total: 1.0
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_036'
SETTINGS_PATH = '/home/user/ml-project/.vscode/settings.json'


def load_settings(path):
    """Load settings.json, handling JSONC (JSON with Comments)."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip // comments (JSONC support)
        content_stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_stripped)
    except FileNotFoundError:
        print(f"CRITICAL: settings.json not found at {path}")
        return None
    except json.JSONDecodeError as e:
        print(f"CRITICAL: settings.json is not valid JSON: {e}")
        return None


def verify_task(settings_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Pre-condition gate: ensure settings.json exists and is valid JSON
    settings = load_settings(settings_path)
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    # Component 1: files.exclude key exists in settings.json (0.30 points)
    try:
        files_exclude = settings.get('files.exclude', None)
        if files_exclude is not None and isinstance(files_exclude, dict):
            print(f"PASS: Component 1 — 'files.exclude' key exists in settings.json (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — 'files.exclude' key not found or not a dict in settings.json; found: {files_exclude}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: **/__pycache__ is set to true in files.exclude (0.35 points)
    try:
        files_exclude = settings.get('files.exclude', {})
        pycache_value = files_exclude.get('**/__pycache__', None)
        if pycache_value is True:
            print(f"PASS: Component 2 — '**/__pycache__' is true in files.exclude (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — '**/__pycache__' expected true, found: {pycache_value}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: **/*.pyc is set to true in files.exclude (0.35 points)
    try:
        files_exclude = settings.get('files.exclude', {})
        pyc_value = files_exclude.get('**/*.pyc', None)
        if pyc_value is True:
            print(f"PASS: Component 3 — '**/*.pyc' is true in files.exclude (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 3 — '**/*.pyc' expected true, found: {pyc_value}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: verify workspace settings.json
if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(SETTINGS_PATH)
