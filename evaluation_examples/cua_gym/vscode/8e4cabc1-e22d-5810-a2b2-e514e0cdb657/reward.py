"""
Reward Script: Collapse all expanded folders in VSCode explorer sidebar
Task ID: vscode_file_053
Domain: vs_code
Scoring:
  Component 1 (0.5 pts): workbench.explorer.treeViewState key exists for big-project
                          AND expanded list is NOT fully expanded (< 9 items)
  Component 2 (0.5 pts): expanded list is exactly empty [] (all folders collapsed)
  Total: 1.0

Verification approach:
  - Find the workspace storage directory for file:///home/user/big-project
  - Read state.vscdb (SQLite) and query the workbench.explorer.treeViewState key
  - Parse the JSON value and check the 'expanded' array
  - Initial state: expanded = [9 folder URIs] → score should be 0.0
  - Golden state:  expanded = [] → score should be 1.0
"""

import os
import json
import sqlite3

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_053'
PROJECT_URI = 'file:///home/user/big-project'
WS_STORAGE = '/home/user/.config/Code/User/workspaceStorage'

# The initial state has all 9 folders in the expanded list.
# Any value < 9 means some collapse action occurred.
INITIAL_EXPANDED_COUNT = 9


def find_workspace_storage_dir(project_uri):
    """
    Find the workspaceStorage directory for the given project URI.
    Returns the path to the workspace storage directory, or None if not found.
    """
    if not os.path.isdir(WS_STORAGE):
        return None
    for entry in os.listdir(WS_STORAGE):
        ws_dir = os.path.join(WS_STORAGE, entry)
        wjson_path = os.path.join(ws_dir, 'workspace.json')
        if os.path.isfile(wjson_path):
            try:
                with open(wjson_path, 'r') as f:
                    data = json.load(f)
                if data.get('folder') == project_uri:
                    return ws_dir
            except (json.JSONDecodeError, IOError):
                continue
    return None


def get_tree_view_state(ws_dir):
    """
    Read the workbench.explorer.treeViewState from state.vscdb.
    Returns the parsed JSON dict, or None if not found.
    """
    db_path = os.path.join(ws_dir, 'state.vscdb')
    if not os.path.isfile(db_path):
        return None
    try:
        conn = sqlite3.connect(db_path)
        rows = conn.execute(
            "SELECT value FROM ItemTable WHERE key = ?",
            ("workbench.explorer.treeViewState",)
        ).fetchall()
        conn.close()
        if rows:
            return json.loads(rows[0][0])
        return None
    except (sqlite3.Error, json.JSONDecodeError) as e:
        print(f"ERROR: Failed to read state.vscdb: {e}")
        return None


def verify_task():
    """
    Verify that all explorer folders are collapsed in the VSCode workspace.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: find workspace storage for big-project
    ws_dir = find_workspace_storage_dir(PROJECT_URI)
    if ws_dir is None:
        print(f"CRITICAL: No workspace storage found for {PROJECT_URI}")
        print(f"REWARD: 0.0")
        return 0.0

    print(f"INFO: Found workspace storage at {ws_dir}")

    # Read the treeViewState
    tree_state = get_tree_view_state(ws_dir)
    if tree_state is None:
        print("CRITICAL: workbench.explorer.treeViewState key not found in state.vscdb")
        print("REWARD: 0.0")
        return 0.0

    expanded = tree_state.get('expanded', None)
    if expanded is None:
        print("CRITICAL: 'expanded' field missing from treeViewState")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: treeViewState.expanded = {expanded}")
    print(f"INFO: Number of expanded folders: {len(expanded)}")

    # Component 1: Some collapse action was done — expanded count < INITIAL_EXPANDED_COUNT (0.5 pts)
    # This FAILS on initial_env (9 items == INITIAL_EXPANDED_COUNT)
    # This PASSES on golden_env (0 items < INITIAL_EXPANDED_COUNT)
    # Also passes if agent collapsed some but not all folders
    try:
        if len(expanded) < INITIAL_EXPANDED_COUNT:
            print(f"PASS: Component 1 — explorer folders partially or fully collapsed "
                  f"(expanded count: {len(expanded)} < {INITIAL_EXPANDED_COUNT}) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — all {INITIAL_EXPANDED_COUNT} folders still expanded "
                  f"(expanded count: {len(expanded)}) — no collapse action detected")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All folders completely collapsed — expanded is exactly [] (0.5 pts)
    # This FAILS on initial_env (9 items)
    # This PASSES on golden_env (empty list)
    try:
        if expanded == []:
            print(f"PASS: Component 2 — all folders collapsed, expanded list is empty (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — explorer not fully collapsed, "
                  f"{len(expanded)} folder(s) still expanded: {expanded}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
