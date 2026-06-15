"""
Reward Script: Configure VSCode workspace settings for Python data science project
Task ID: vscode_we_022
Domain: vscode
Scoring:
  - Component 1 (0.35): notebook.formatOnSave.enabled == true
  - Component 2 (0.35): python.analysis.typeCheckingMode == "basic"
  - Component 3 (0.30): jupyter.notebookFileRoot == "${workspaceFolder}"
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_022'
SETTINGS_PATH = os.path.join(WORKDIR, 'projects', 'data-analysis', '.vscode', 'settings.json')


def load_jsonc(path):
    """Load a JSON file, stripping // comments (VSCode JSONC support)."""
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

    # Precondition gate: settings.json must exist and be valid JSON
    if not os.path.exists(SETTINGS_PATH):
        print(f"CRITICAL: Settings file not found: {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        settings = load_jsonc(SETTINGS_PATH)
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse settings.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not isinstance(settings, dict):
        print(f"CRITICAL: settings.json is not a JSON object, got {type(settings).__name__}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: notebook.formatOnSave.enabled == true (0.35 points)
    try:
        val = settings.get("notebook.formatOnSave.enabled")
        if val is True:
            print(f"PASS: Component 1 — notebook.formatOnSave.enabled is true (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — expected notebook.formatOnSave.enabled=true, found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: python.analysis.typeCheckingMode == "basic" (0.35 points)
    try:
        val = settings.get("python.analysis.typeCheckingMode")
        if isinstance(val, str) and val.strip().lower() == "basic":
            print(f"PASS: Component 2 — python.analysis.typeCheckingMode is 'basic' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — expected python.analysis.typeCheckingMode='basic', found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: jupyter.notebookFileRoot == "${workspaceFolder}" (0.30 points)
    try:
        val = settings.get("jupyter.notebookFileRoot")
        if isinstance(val, str) and val.strip() == "${workspaceFolder}":
            print(f"PASS: Component 3 — jupyter.notebookFileRoot is '${{workspaceFolder}}' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — expected jupyter.notebookFileRoot='${{workspaceFolder}}', found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
