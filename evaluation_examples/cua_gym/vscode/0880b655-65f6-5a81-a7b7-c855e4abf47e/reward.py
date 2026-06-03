"""
Reward Script: Configure multi-root workspace with per-folder formatter settings
Task ID: vscode_we_033
Domain: vscode
Scoring:
  Component 1 (0.35): Frontend .vscode/settings.json with Prettier, 2-space tabs, formatOnSave
  Component 2 (0.35): Backend .vscode/settings.json with Black for Python, 4-space tabs, formatOnSave
  Component 3 (0.15): Shared folder does NOT override formatter (compound: only scored when frontend OR backend configured)
  Component 4 (0.15): Workspace file intact with all three folders
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_033'

PROJECTS_DIR = os.path.join(WORKDIR, 'projects')
FRONTEND_SETTINGS = os.path.join(PROJECTS_DIR, 'frontend', '.vscode', 'settings.json')
BACKEND_SETTINGS = os.path.join(PROJECTS_DIR, 'backend', '.vscode', 'settings.json')
SHARED_SETTINGS = os.path.join(PROJECTS_DIR, 'shared', '.vscode', 'settings.json')
WORKSPACE_FILE = os.path.join(PROJECTS_DIR, 'platform.code-workspace')


def load_jsonc(path):
    """Load a JSON or JSONC file (strips // comments)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def _is_subset(expected, actual):
    """Check that expected is a subset of actual (deep)."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and _is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        return expected == actual
    return expected == actual


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    frontend_ok = False
    backend_ok = False

    # Component 1: Frontend settings (0.35 points)
    # Expected: tabSize=2, defaultFormatter=prettier, formatOnSave=true
    try:
        if not os.path.exists(FRONTEND_SETTINGS):
            print(f"FAIL: Component 1 -- frontend/.vscode/settings.json not found")
        else:
            frontend_data = load_jsonc(FRONTEND_SETTINGS)
            expected_frontend = {
                "editor.tabSize": 2,
                "editor.defaultFormatter": "esbenp.prettier-vscode",
                "editor.formatOnSave": True
            }
            sub_score = 0.0
            # Check tabSize
            if frontend_data.get("editor.tabSize") == 2:
                sub_score += 0.1
                print(f"PASS: Component 1a -- frontend tabSize is 2")
            else:
                print(f"FAIL: Component 1a -- expected tabSize 2, found {frontend_data.get('editor.tabSize')}")

            # Check defaultFormatter
            if frontend_data.get("editor.defaultFormatter") == "esbenp.prettier-vscode":
                sub_score += 0.15
                print(f"PASS: Component 1b -- frontend defaultFormatter is esbenp.prettier-vscode")
            else:
                print(f"FAIL: Component 1b -- expected defaultFormatter esbenp.prettier-vscode, found {frontend_data.get('editor.defaultFormatter')}")

            # Check formatOnSave
            if frontend_data.get("editor.formatOnSave") is True:
                sub_score += 0.1
                print(f"PASS: Component 1c -- frontend formatOnSave is true")
            else:
                print(f"FAIL: Component 1c -- expected formatOnSave true, found {frontend_data.get('editor.formatOnSave')}")

            if sub_score > 0:
                total_score += sub_score
            frontend_ok = (sub_score >= 0.35)  # derived from sub-checks above
            if frontend_ok:
                print(f"PASS: Component 1 -- frontend settings fully correct (0.35 pts)")
            else:
                print(f"PARTIAL: Component 1 -- frontend settings partially correct ({sub_score} pts)")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Backend settings (0.35 points)
    # Expected: tabSize=4, [python].defaultFormatter=black, formatOnSave=true
    try:
        if not os.path.exists(BACKEND_SETTINGS):
            print(f"FAIL: Component 2 -- backend/.vscode/settings.json not found")
        else:
            backend_data = load_jsonc(BACKEND_SETTINGS)
            sub_score = 0.0

            # Check tabSize
            if backend_data.get("editor.tabSize") == 4:
                sub_score += 0.1
                print(f"PASS: Component 2a -- backend tabSize is 4")
            else:
                print(f"FAIL: Component 2a -- expected tabSize 4, found {backend_data.get('editor.tabSize')}")

            # Check [python] defaultFormatter
            python_section = backend_data.get("[python]", {})
            if isinstance(python_section, dict) and python_section.get("editor.defaultFormatter") == "ms-python.black-formatter":
                sub_score += 0.15
                print(f"PASS: Component 2b -- backend [python] defaultFormatter is ms-python.black-formatter")
            else:
                print(f"FAIL: Component 2b -- expected [python].defaultFormatter ms-python.black-formatter, found {python_section}")

            # Check formatOnSave
            if backend_data.get("editor.formatOnSave") is True:
                sub_score += 0.1
                print(f"PASS: Component 2c -- backend formatOnSave is true")
            else:
                print(f"FAIL: Component 2c -- expected formatOnSave true, found {backend_data.get('editor.formatOnSave')}")

            if sub_score > 0:
                total_score += sub_score
            backend_ok = (sub_score >= 0.35)  # derived from sub-checks above
            if backend_ok:
                print(f"PASS: Component 2 -- backend settings fully correct (0.35 pts)")
            else:
                print(f"PARTIAL: Component 2 -- backend settings partially correct ({sub_score} pts)")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Shared folder does NOT override formatter (0.15 points)
    # This is a compound check: only scored when at least one of frontend/backend is configured
    # (prevents scoring on initial_env where none have settings)
    try:
        if not (frontend_ok or backend_ok):
            print(f"FAIL: Component 3 -- skipped because neither frontend nor backend is configured (no task changes detected)")
        else:
            shared_has_formatter_override = False
            if os.path.exists(SHARED_SETTINGS):
                shared_data = load_jsonc(SHARED_SETTINGS)
                if "editor.defaultFormatter" in shared_data:
                    shared_has_formatter_override = (len(shared_data.get("editor.defaultFormatter", "")) > 0)  # derived from data check

            if not shared_has_formatter_override:
                print(f"PASS: Component 3 -- shared folder does not override formatter (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 -- shared folder has formatter override, should not have one")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Workspace file intact with all three folders (0.15 points)
    # Compound check: workspace exists AND has all 3 folders AND at least one folder has settings configured
    try:
        if not (frontend_ok or backend_ok):
            print(f"FAIL: Component 4 -- skipped because no task changes detected")
        elif not os.path.exists(WORKSPACE_FILE):
            print(f"FAIL: Component 4 -- workspace file not found at {WORKSPACE_FILE}")
        else:
            ws_data = load_jsonc(WORKSPACE_FILE)
            folders = ws_data.get("folders", [])
            folder_paths = [f.get("path", "") for f in folders]
            expected_folders = {"frontend", "backend", "shared"}
            actual_folders = set(folder_paths)
            if expected_folders.issubset(actual_folders):
                print(f"PASS: Component 4 -- workspace has all three folders: {folder_paths} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 -- expected folders {expected_folders}, found {actual_folders}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
