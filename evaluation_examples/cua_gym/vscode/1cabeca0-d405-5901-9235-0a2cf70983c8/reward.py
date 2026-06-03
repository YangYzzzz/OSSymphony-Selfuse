"""
Reward Script: Create workspace-specific .vscode/settings.json
Task ID: vscode_stu_067
Domain: vscode
Scoring:
  Component 1: .vscode/settings.json exists and is valid JSON (0.10 pts)
  Component 2: editor.tabSize is 2 (0.25 pts)
  Component 3: editor.formatOnSave is true (0.25 pts)
  Component 4: editor.minimap.enabled is false (0.25 pts)
  Component 5: Global user settings unchanged — tabSize=4, formatOnSave=false, minimap=true (0.15 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_067'
PROJECT_DIR = os.path.join(WORKDIR, 'webdev', 'react-app')
WORKSPACE_SETTINGS = os.path.join(PROJECT_DIR, '.vscode', 'settings.json')
GLOBAL_SETTINGS = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_jsonc(path):
    """Load a JSON or JSONC file (strips // comments)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: .vscode/settings.json exists and is valid JSON (0.10 pts)
    # This file does NOT exist in initial_env, so this check differentiates.
    workspace_settings = None
    try:
        if os.path.isfile(WORKSPACE_SETTINGS):
            workspace_settings = load_jsonc(WORKSPACE_SETTINGS)
            if isinstance(workspace_settings, dict):
                print(f"PASS: Component 1 — .vscode/settings.json exists and is valid JSON (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 1 — .vscode/settings.json is not a JSON object, got {type(workspace_settings).__name__}")
        else:
            print(f"FAIL: Component 1 — .vscode/settings.json does not exist at {WORKSPACE_SETTINGS}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if workspace_settings is None or not isinstance(workspace_settings, dict):
        # Cannot proceed without valid workspace settings
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: editor.tabSize is 2 (0.25 pts)
    try:
        tab_size = workspace_settings.get("editor.tabSize")
        if tab_size == 2:
            print(f"PASS: Component 2 — editor.tabSize is 2 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — expected editor.tabSize=2, found: {tab_size!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: editor.formatOnSave is true (0.25 pts)
    try:
        format_on_save = workspace_settings.get("editor.formatOnSave")
        if format_on_save is True:
            print(f"PASS: Component 3 — editor.formatOnSave is true (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — expected editor.formatOnSave=true, found: {format_on_save!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: editor.minimap.enabled is false (0.25 pts)
    try:
        minimap_enabled = workspace_settings.get("editor.minimap.enabled")
        if minimap_enabled is False:
            print(f"PASS: Component 4 — editor.minimap.enabled is false (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — expected editor.minimap.enabled=false, found: {minimap_enabled!r}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Global user settings remain unchanged (0.15 pts)
    # The task says "without changing my global user settings".
    # Verify that global settings still have the original values for the three keys.
    # This component differentiates: if someone modified global instead of workspace,
    # they would fail here. On initial_env, global settings are correct BUT
    # this component is gated by Component 1 passing (we only reach here if
    # .vscode/settings.json exists), so initial_env returns 0.0 total.
    try:
        global_settings = load_jsonc(GLOBAL_SETTINGS)
        global_tab = global_settings.get("editor.tabSize")
        global_format = global_settings.get("editor.formatOnSave")
        global_minimap = global_settings.get("editor.minimap.enabled")

        global_ok = (global_tab == 4 and global_format is False and global_minimap is True)
        if global_ok:
            print(f"PASS: Component 5 — Global settings unchanged: tabSize=4, formatOnSave=false, minimap=true (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — Global settings were modified: tabSize={global_tab!r}, formatOnSave={global_format!r}, minimap={global_minimap!r}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
