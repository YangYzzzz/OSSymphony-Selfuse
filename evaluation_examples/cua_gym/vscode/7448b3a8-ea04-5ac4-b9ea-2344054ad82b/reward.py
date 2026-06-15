"""
Reward Script: Create workspace settings file that excludes system files from explorer view.
Task ID: vscode_file_051
Domain: vs_code
Scoring:
  - Component 1: settings.json has files.exclude entry for **/.git (0.25 pts)
  - Component 2: settings.json has files.exclude entry for **/.DS_Store (0.25 pts)
  - Component 3: settings.json has files.exclude entry for **/Thumbs.db (0.25 pts)
  - Component 4: settings.json has files.exclude entry for **/*.swp (0.25 pts)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_051'
SETTINGS_PATH = '/home/user/project/.vscode/settings.json'


def _is_subset(expected, actual) -> bool:
    """Recursively check that expected is a subset of actual (containment check)."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and _is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        return expected == actual
    return expected == actual


def load_settings(path: str) -> dict:
    """Load JSON settings file, stripping JSONC comments if present."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line // comments (JSONC support)
        import re
        content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_clean)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"ERROR: Could not parse {path} as JSON: {e}")
        return None


def verify_task():
    """
    Verify that the workspace settings file excludes the required system files.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: settings.json must exist and be valid JSON
    settings = load_settings(SETTINGS_PATH)
    if settings is None:
        if not os.path.exists(SETTINGS_PATH):
            print(f"FAIL: settings.json not found at {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Extract files.exclude block
    files_exclude = settings.get('files.exclude', None)
    if files_exclude is None:
        print("FAIL: 'files.exclude' key not found in settings.json")
        print(f"\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    if not isinstance(files_exclude, dict):
        print(f"FAIL: 'files.exclude' must be a dict, got {type(files_exclude)}")
        print(f"\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: **/.git is excluded (0.25 points)
    try:
        key = '**/.git'
        val = files_exclude.get(key)
        if val is True:
            print(f"PASS: Component 1 — '{key}' is excluded (value: {val}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — expected '{key}': true in files.exclude, found: {val}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: **/.DS_Store is excluded (0.25 points)
    try:
        key = '**/.DS_Store'
        val = files_exclude.get(key)
        if val is True:
            print(f"PASS: Component 2 — '{key}' is excluded (value: {val}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — expected '{key}': true in files.exclude, found: {val}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: **/Thumbs.db is excluded (0.25 points)
    try:
        key = '**/Thumbs.db'
        val = files_exclude.get(key)
        if val is True:
            print(f"PASS: Component 3 — '{key}' is excluded (value: {val}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — expected '{key}': true in files.exclude, found: {val}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: **/*.swp is excluded (0.25 points)
    try:
        key = '**/*.swp'
        val = files_exclude.get(key)
        if val is True:
            print(f"PASS: Component 4 — '{key}' is excluded (value: {val}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — expected '{key}': true in files.exclude, found: {val}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
