"""
Reward Script: Add folder-specific tab size settings to multi-root workspace
Task ID: vscode_we_019
Domain: vscode
Scoring:
  - Component 1 (0.25): frontend/.vscode/settings.json exists and is valid JSON
  - Component 2 (0.25): backend/.vscode/settings.json exists and is valid JSON
  - Component 3 (0.25): frontend settings contain editor.tabSize == 2
  - Component 4 (0.25): backend settings contain editor.tabSize == 4
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_019'

FRONTEND_SETTINGS = os.path.join(WORKDIR, 'projects', 'frontend', '.vscode', 'settings.json')
BACKEND_SETTINGS = os.path.join(WORKDIR, 'projects', 'backend', '.vscode', 'settings.json')


def load_jsonc(path):
    """Load a JSON or JSONC file (strips // comments)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: frontend/.vscode/settings.json exists and is valid JSON (0.25 pts)
    frontend_data = None
    try:
        if os.path.isfile(FRONTEND_SETTINGS):
            frontend_data = load_jsonc(FRONTEND_SETTINGS)
            if isinstance(frontend_data, dict):
                print(f"PASS: Component 1 — frontend settings.json exists and is valid JSON (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 — frontend settings.json is not a JSON object, got {type(frontend_data).__name__}")
        else:
            print(f"FAIL: Component 1 — {FRONTEND_SETTINGS} does not exist")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: backend/.vscode/settings.json exists and is valid JSON (0.25 pts)
    backend_data = None
    try:
        if os.path.isfile(BACKEND_SETTINGS):
            backend_data = load_jsonc(BACKEND_SETTINGS)
            if isinstance(backend_data, dict):
                print(f"PASS: Component 2 — backend settings.json exists and is valid JSON (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — backend settings.json is not a JSON object, got {type(backend_data).__name__}")
        else:
            print(f"FAIL: Component 2 — {BACKEND_SETTINGS} does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: frontend editor.tabSize == 2 (0.25 pts)
    try:
        if frontend_data is not None and isinstance(frontend_data, dict):
            tab_size = frontend_data.get('editor.tabSize')
            if tab_size == 2:
                print(f"PASS: Component 3 — frontend editor.tabSize is 2 (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — frontend editor.tabSize expected 2, found {tab_size}")
        else:
            print(f"FAIL: Component 3 — frontend settings not loaded, cannot check editor.tabSize")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: backend editor.tabSize == 4 (0.25 pts)
    try:
        if backend_data is not None and isinstance(backend_data, dict):
            tab_size = backend_data.get('editor.tabSize')
            if tab_size == 4:
                print(f"PASS: Component 4 — backend editor.tabSize is 4 (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 — backend editor.tabSize expected 4, found {tab_size}")
        else:
            print(f"FAIL: Component 4 — backend settings not loaded, cannot check editor.tabSize")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
