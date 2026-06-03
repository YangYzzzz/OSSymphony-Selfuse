"""
Reward Script: Configure type checking for custom type aliases with py.typed marker
Task ID: vscode_py_057
Domain: vscode
Scoring:
  Component 1 (0.4): py.typed marker file exists in src/mylib/
  Component 2 (0.3): Pylance typeCheckingMode configured to "basic" (workspace or global)
  Component 3 (0.3): Pylance autoSearchPaths and extraPaths configured in workspace settings
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_057'

# Paths
SRC_DIR = os.path.join(WORKDIR, 'src')
MYLIB_DIR = os.path.join(SRC_DIR, 'mylib')
PY_TYPED_PATH = os.path.join(MYLIB_DIR, 'py.typed')
WORKSPACE_SETTINGS_PATH = os.path.join(SRC_DIR, '.vscode', 'settings.json')
GLOBAL_SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_json_with_comments(path):
    """Load a JSON file, stripping // comments that VSCode allows (JSONC)."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"  Could not load {path}: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: mylib package directory must exist
    if not os.path.isdir(MYLIB_DIR):
        print(f"CRITICAL: mylib directory not found at {MYLIB_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: py.typed marker file exists in src/mylib/ (0.4 points)
    # This is the core deliverable - the PEP 561 marker file
    try:
        if os.path.isfile(PY_TYPED_PATH):
            # Verify it is an empty or near-empty marker file (PEP 561 spec)
            size = os.path.getsize(PY_TYPED_PATH)
            if size <= 100:  # py.typed should be empty or have minimal content
                print(f"PASS: Component 1 -- py.typed marker file exists at {PY_TYPED_PATH} (size: {size} bytes) (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 -- py.typed exists but is unexpectedly large ({size} bytes)")
        else:
            print(f"FAIL: Component 1 -- py.typed marker file not found at {PY_TYPED_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Pylance typeCheckingMode set to "basic" (0.3 points)
    # Check both workspace and global settings - either location is valid
    try:
        ws_settings = load_json_with_comments(WORKSPACE_SETTINGS_PATH)
        global_settings = load_json_with_comments(GLOBAL_SETTINGS_PATH)

        ws_mode = ws_settings.get('python.analysis.typeCheckingMode') if ws_settings else None
        global_mode = global_settings.get('python.analysis.typeCheckingMode') if global_settings else None

        if ws_mode == 'basic':
            print(f"  Found typeCheckingMode=basic in workspace settings")
            print(f"PASS: Component 2 -- python.analysis.typeCheckingMode is 'basic' (0.3 pts)")
            total_score += 0.3
        elif global_mode == 'basic':
            print(f"  Found typeCheckingMode=basic in global settings")
            print(f"PASS: Component 2 -- python.analysis.typeCheckingMode is 'basic' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- python.analysis.typeCheckingMode not set to 'basic' (ws={ws_mode}, global={global_mode})")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Pylance autoSearchPaths and extraPaths configured (0.3 points)
    # These settings help Pylance resolve the mylib package and its custom types
    try:
        ws_settings = load_json_with_comments(WORKSPACE_SETTINGS_PATH)
        if ws_settings is None:
            print(f"FAIL: Component 3 -- workspace settings not found or unreadable")
        else:
            auto_search = ws_settings.get('python.analysis.autoSearchPaths', False)
            extra_paths = ws_settings.get('python.analysis.extraPaths', [])

            sub_score = 0.0
            # autoSearchPaths should be true
            if auto_search is True:
                sub_score += 0.15
                print(f"  autoSearchPaths is True")
            else:
                print(f"  autoSearchPaths is {auto_search} (expected True)")

            # extraPaths should include a path referencing mylib
            if any('mylib' in p for p in extra_paths):
                sub_score += 0.15
                print(f"  extraPaths contains mylib reference: {extra_paths}")
            else:
                print(f"  extraPaths does not contain mylib reference: {extra_paths}")

            if sub_score > 0:
                print(f"PASS: Component 3 -- Pylance path config ({sub_score} of 0.3 pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 3 -- Neither autoSearchPaths nor extraPaths configured for mylib")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
