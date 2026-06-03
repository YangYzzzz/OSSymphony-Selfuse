"""
Reward Script: Configure VSCode Pylance stub path for pandas-stubs
Task ID: vscode_py_046
Domain: vscode
Scoring:
  Component 1 (0.4): python.analysis.stubPath key exists in workspace settings
  Component 2 (0.4): stubPath value contains correct pandas-stubs path
  Component 3 (0.2): The pandas-stubs directory exists and has .pyi files
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_046'

# Workspace settings path (where the task change should appear)
WORKSPACE_SETTINGS = os.path.join(WORKDIR, 'workspace', '.vscode', 'settings.json')
# User-level settings (also acceptable location)
USER_SETTINGS = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')
# Expected stub path fragments
PANDAS_STUBS_FRAGMENT = 'pandas-stubs'
EXPECTED_STUB_DIR = os.path.join(WORKDIR, 'workspace', '.venv', 'lib', 'python3.10', 'site-packages', 'pandas-stubs')


def load_jsonc(path):
    """Load a JSON/JSONC file, stripping comments."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"  Could not load {path}: {e}")
        return None


def find_stub_path_setting():
    """Search workspace and user settings for python.analysis.stubPath.
    Returns (value, location) or (None, None)."""
    # Check workspace settings first (preferred)
    ws_settings = load_jsonc(WORKSPACE_SETTINGS)
    if ws_settings and 'python.analysis.stubPath' in ws_settings:
        return ws_settings['python.analysis.stubPath'], 'workspace'

    # Check user-level settings
    user_settings = load_jsonc(USER_SETTINGS)
    if user_settings and 'python.analysis.stubPath' in user_settings:
        return user_settings['python.analysis.stubPath'], 'user'

    return None, None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: python.analysis.stubPath key exists in settings (0.4 points)
    try:
        stub_path_value, location = find_stub_path_setting()
        if stub_path_value is not None:
            print(f"PASS: Component 1 — python.analysis.stubPath found in {location} settings (value: {stub_path_value}) (0.4 pts)")
            total_score += 0.4
        else:
            print("FAIL: Component 1 — python.analysis.stubPath not found in workspace or user settings")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: stubPath value references the pandas-stubs directory (0.4 points)
    try:
        if stub_path_value is not None:
            # The value could be relative (e.g., ".venv/lib/...") or absolute
            if PANDAS_STUBS_FRAGMENT in str(stub_path_value):
                print(f"PASS: Component 2 — stubPath contains '{PANDAS_STUBS_FRAGMENT}' (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — stubPath '{stub_path_value}' does not contain '{PANDAS_STUBS_FRAGMENT}'")
        else:
            print("FAIL: Component 2 — No stubPath setting to check")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The pandas-stubs directory exists and contains .pyi stub files (0.2 points)
    try:
        # Resolve relative path if needed
        if stub_path_value is not None:
            resolved_path = stub_path_value
            if not os.path.isabs(resolved_path):
                resolved_path = os.path.join(WORKDIR, 'workspace', resolved_path)

            if os.path.isdir(resolved_path):
                pyi_files = [f for f in os.listdir(resolved_path) if f.endswith('.pyi')]
                if len(pyi_files) > 0:
                    print(f"PASS: Component 3 — Stub directory exists at {resolved_path} with {len(pyi_files)} .pyi files (0.2 pts)")
                    total_score += 0.2
                else:
                    # Check subdirectories for .pyi files
                    pyi_count = sum(1 for root, dirs, files in os.walk(resolved_path)
                                    for f in files if f.endswith('.pyi'))
                    if pyi_count > 0:
                        print(f"PASS: Component 3 — Stub directory exists at {resolved_path} with .pyi files in subdirs (0.2 pts)")
                        total_score += 0.2
                    else:
                        print(f"FAIL: Component 3 — Directory {resolved_path} exists but no .pyi files found")
            else:
                print(f"FAIL: Component 3 — Stub directory not found at {resolved_path}")
        else:
            print("FAIL: Component 3 — No stubPath setting to validate")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
