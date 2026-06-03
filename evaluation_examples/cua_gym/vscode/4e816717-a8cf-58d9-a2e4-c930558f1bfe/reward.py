"""
Reward Script: Configure multi-root workspace with separate Python interpreters
Task ID: vscode_py_022
Domain: vs_code
Scoring:
  Component 1 (0.4): Workspace file exists with both folders listed
  Component 2 (0.3): Backend folder has correct Python interpreter setting
  Component 3 (0.3): Shared-lib folder has correct Python interpreter setting
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_022'

# Expected paths
BACKEND_PATH = '/home/user/backend'
SHAREDLIB_PATH = '/home/user/shared-lib'
BACKEND_PYTHON = '/home/user/backend/.venv/bin/python'
SHAREDLIB_PYTHON = '/home/user/shared-lib/.venv/bin/python'


def load_jsonc(file_path):
    """Load a JSON or JSONC file (strips // comments)."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def find_workspace_file():
    """Find any .code-workspace file in /home/user/."""
    for fname in os.listdir(WORKDIR):
        if fname.endswith('.code-workspace'):
            return os.path.join(WORKDIR, fname)
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Workspace file exists and contains both folders (0.4 points)
    try:
        ws_path = find_workspace_file()
        if ws_path is None:
            print("FAIL: Component 1 — No .code-workspace file found in /home/user/")
        else:
            ws_data = load_jsonc(ws_path)
            folders = ws_data.get('folders', [])
            folder_paths = set()
            for folder in folders:
                p = folder.get('path', '')
                # Normalize: remove trailing slash
                folder_paths.add(p.rstrip('/'))

            has_backend = BACKEND_PATH in folder_paths
            has_sharedlib = SHAREDLIB_PATH in folder_paths

            if has_backend and has_sharedlib:
                print(f"PASS: Component 1 — Workspace file {os.path.basename(ws_path)} contains both folders (0.4 pts)")
                total_score += 0.4
            else:
                missing = []
                if not has_backend:
                    missing.append(BACKEND_PATH)
                if not has_sharedlib:
                    missing.append(SHAREDLIB_PATH)
                print(f"FAIL: Component 1 — Workspace missing folders: {missing}. Found: {folder_paths}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Backend folder has correct Python interpreter (0.3 points)
    try:
        backend_settings_path = os.path.join(BACKEND_PATH, '.vscode', 'settings.json')
        if not os.path.exists(backend_settings_path):
            # Also check workspace-level settings as alternative
            ws_path = find_workspace_file()
            found_in_workspace = False
            if ws_path:
                ws_data = load_jsonc(ws_path)
                # Check folder-specific settings in workspace file
                folders = ws_data.get('folders', [])
                for folder in folders:
                    p = folder.get('path', '').rstrip('/')
                    if p == BACKEND_PATH:
                        folder_settings = folder.get('settings', {})
                        interp = folder_settings.get('python.defaultInterpreterPath', '')
                        if interp == BACKEND_PYTHON:
                            found_in_workspace = True
                            break
            if not found_in_workspace:
                print(f"FAIL: Component 2 — No .vscode/settings.json in backend and no folder-level workspace setting")
            else:
                print(f"PASS: Component 2 — Backend interpreter set in workspace file (0.3 pts)")
                total_score += 0.3
        else:
            settings = load_jsonc(backend_settings_path)
            interp = settings.get('python.defaultInterpreterPath', '')
            if interp == BACKEND_PYTHON:
                print(f"PASS: Component 2 — Backend interpreter correctly set to {BACKEND_PYTHON} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Backend interpreter is '{interp}', expected '{BACKEND_PYTHON}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Shared-lib folder has correct Python interpreter (0.3 points)
    try:
        sharedlib_settings_path = os.path.join(SHAREDLIB_PATH, '.vscode', 'settings.json')
        if not os.path.exists(sharedlib_settings_path):
            # Also check workspace-level settings as alternative
            ws_path = find_workspace_file()
            found_in_workspace = False
            if ws_path:
                ws_data = load_jsonc(ws_path)
                folders = ws_data.get('folders', [])
                for folder in folders:
                    p = folder.get('path', '').rstrip('/')
                    if p == SHAREDLIB_PATH:
                        folder_settings = folder.get('settings', {})
                        interp = folder_settings.get('python.defaultInterpreterPath', '')
                        if interp == SHAREDLIB_PYTHON:
                            found_in_workspace = True
                            break
            if not found_in_workspace:
                print(f"FAIL: Component 3 — No .vscode/settings.json in shared-lib and no folder-level workspace setting")
            else:
                print(f"PASS: Component 3 — Shared-lib interpreter set in workspace file (0.3 pts)")
                total_score += 0.3
        else:
            settings = load_jsonc(sharedlib_settings_path)
            interp = settings.get('python.defaultInterpreterPath', '')
            if interp == SHAREDLIB_PYTHON:
                print(f"PASS: Component 3 — Shared-lib interpreter correctly set to {SHAREDLIB_PYTHON} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Shared-lib interpreter is '{interp}', expected '{SHAREDLIB_PYTHON}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
