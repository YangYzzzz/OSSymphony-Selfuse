"""
Reward Script: Open main.py, utils.py, and config.py as tabs in VSCode
Task ID: vscode_stu_085
Domain: vscode
Scoring:
  Component 1: main.py open as editor tab   (0.34 pts)
  Component 2: utils.py open as editor tab   (0.33 pts)
  Component 3: config.py open as editor tab  (0.33 pts)
"""

import os
import json
import sqlite3

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_085'

# Workspace state DB path (VSCode stores open editors here)
WORKSPACE_DB = os.path.join(
    WORKDIR,
    '.config', 'Code', 'User', 'workspaceStorage',
    'ed8bf10ce6648d60f7cd05ad41397703', 'state.vscdb'
)

EXPECTED_FILES = {
    'main.py': '/home/user/cs101/project/main.py',
    'utils.py': '/home/user/cs101/project/utils.py',
    'config.py': '/home/user/cs101/project/config.py',
}


def get_open_editor_paths(db_path):
    """
    Read the VSCode workspace state DB and extract file paths
    of all currently open editor tabs.
    Returns a set of absolute file paths.
    """
    open_paths = set()
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT value FROM ItemTable WHERE key='memento/workbench.parts.editor'"
        )
        row = cursor.fetchone()
        conn.close()

        if not row:
            print("WARN: No editor state found in workspace DB")
            return open_paths

        data = json.loads(row[0])
        # Navigate the serialized grid to find editor entries
        grid_root = data.get('editorpart.state', {}).get('serializedGrid', {}).get('root', {})
        groups = grid_root.get('data', [])

        for group in groups:
            group_data = group.get('data', {})
            editors = group_data.get('editors', [])
            for editor in editors:
                editor_id = editor.get('id', '')
                if editor_id == 'workbench.editors.files.fileEditorInput':
                    try:
                        value_obj = json.loads(editor.get('value', '{}'))
                        resource = value_obj.get('resourceJSON', {})
                        fspath = resource.get('fsPath', '')
                        if fspath:
                            open_paths.add(fspath)
                    except (json.JSONDecodeError, KeyError):
                        pass

    except Exception as e:
        print(f"ERROR: Failed to read workspace DB: {e}")

    return open_paths


def verify_task():
    """
    Verify that main.py, utils.py, and config.py are all open as
    editor tabs in VSCode. Progressive scoring: each file = ~0.33 pts.
    Returns float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Precondition: workspace DB exists
    if not os.path.exists(WORKSPACE_DB):
        print(f"CRITICAL: Workspace state DB not found: {WORKSPACE_DB}")
        print("REWARD: 0.0")
        return 0.0

    open_paths = get_open_editor_paths(WORKSPACE_DB)
    print(f"INFO: Found {len(open_paths)} open editor tab(s): {open_paths}")

    # Component 1: main.py is open as a tab (0.34 points)
    try:
        expected = EXPECTED_FILES['main.py']
        if expected in open_paths:
            print(f"PASS: Component 1 — main.py is open as editor tab (0.34 pts)")
            total_score += 0.34
        else:
            print(f"FAIL: Component 1 — main.py not found in open tabs. Expected: {expected}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: utils.py is open as a tab (0.33 points)
    try:
        expected = EXPECTED_FILES['utils.py']
        if expected in open_paths:
            print(f"PASS: Component 2 — utils.py is open as editor tab (0.33 pts)")
            total_score += 0.33
        else:
            print(f"FAIL: Component 2 — utils.py not found in open tabs. Expected: {expected}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: config.py is open as a tab (0.33 points)
    try:
        expected = EXPECTED_FILES['config.py']
        if expected in open_paths:
            print(f"PASS: Component 3 — config.py is open as editor tab (0.33 pts)")
            total_score += 0.33
        else:
            print(f"FAIL: Component 3 — config.py not found in open tabs. Expected: {expected}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
