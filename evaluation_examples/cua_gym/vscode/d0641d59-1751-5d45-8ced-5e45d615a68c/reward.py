"""
Reward Script: Use Go to Definition to navigate to 'calculateTax' function definition
Task ID: vscode_code_038
Domain: vs_code
Scoring:
  Component 1 (0.5): tax.js is open in VSCode editor as a result of Go to Definition
  Component 2 (0.5): Cursor position in tax.js is at line 1 (calculateTax function declaration)
  Total: 1.0

Verification strategy:
  After "Go to Definition" on 'calculateTax' in main.js (line 4), VSCode navigates to tax.js
  and opens it with the cursor at line 1 (where 'function calculateTax' is declared).
  This leaves a trace in the project workspace's state.vscdb SQLite file:
    - history.entries will contain file:///home/user/project/tax.js
    - memento/workbench.editors.files.textFileEditor will contain tax.js cursor state at line 1

  Pre-task (initial_env): no workspace storage for the project folder exists
  Post-task (golden_env): tax.js is open in the editor, cursor at line 1
"""

import os
import json
import sqlite3

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_038'
PROJECT_DIR = '/home/user/project'
MAIN_JS = '/home/user/project/main.js'
TAX_JS = '/home/user/project/tax.js'
VSCODE_WORKSPACE_STORAGE = '/home/user/.config/Code/User/workspaceStorage'
PROJECT_FOLDER_URI = 'file:///home/user/project'
TAX_JS_URI = 'file:///home/user/project/tax.js'


def find_project_workspace_db():
    """
    Find the state.vscdb for the /home/user/project workspace.
    VSCode creates a hashed subdirectory under workspaceStorage/.
    The workspace.json file in each subdirectory identifies the folder.
    Returns path to state.vscdb, or None if not found.
    """
    if not os.path.isdir(VSCODE_WORKSPACE_STORAGE):
        return None
    for entry in os.listdir(VSCODE_WORKSPACE_STORAGE):
        ws_dir = os.path.join(VSCODE_WORKSPACE_STORAGE, entry)
        ws_json = os.path.join(ws_dir, 'workspace.json')
        db_path = os.path.join(ws_dir, 'state.vscdb')
        if os.path.exists(ws_json) and os.path.exists(db_path):
            try:
                with open(ws_json) as f:
                    data = json.load(f)
                if data.get('folder') == PROJECT_FOLDER_URI:
                    print(f"INFO: Found project workspace DB at {db_path}")
                    return db_path
            except Exception:
                continue
    return None


def query_workspace_db(db_path, key):
    """
    Query the workspace state.vscdb for a given key.
    Returns parsed JSON value, or None if not found.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM ItemTable WHERE key = ?', (key,))
        row = cursor.fetchone()
        conn.close()
        if row and row[0]:
            return json.loads(row[0])
    except Exception as e:
        print(f"ERROR: Could not query workspace DB key '{key}': {e}")
    return None


def tax_js_in_editor_history(db_path):
    """
    Check if tax.js appears in the navigation history entries.
    history.entries records files the user visited. After Go to Definition,
    tax.js should appear as a visited entry.
    Returns True if tax.js is found.
    """
    history = query_workspace_db(db_path, 'history.entries')
    if isinstance(history, list):
        for entry in history:
            if isinstance(entry, dict):
                resource = entry.get('editor', {}).get('resource', '')
                if 'tax.js' in resource:
                    return True
    return False


def tax_js_in_open_editors(db_path):
    """
    Check if tax.js is in the open editors state (memento/workbench.parts.editor).
    Returns True if tax.js is in the editor list.
    """
    editor_state = query_workspace_db(db_path, 'memento/workbench.parts.editor')
    if editor_state is not None:
        state_str = json.dumps(editor_state)
        if 'tax.js' in state_str:
            return True
    return False


def get_tax_js_cursor_line(db_path):
    """
    Get the cursor line number for tax.js from the textFileEditor view state.
    Returns the line number (1-indexed) if found, or None.
    """
    view_state = query_workspace_db(
        db_path, 'memento/workbench.editors.files.textFileEditor'
    )
    if not isinstance(view_state, dict):
        return None
    entries = view_state.get('textEditorViewState', [])
    for entry in entries:
        if not isinstance(entry, list) or len(entry) < 2:
            continue
        uri, state = entry[0], entry[1]
        if 'tax.js' not in str(uri):
            continue
        # state is keyed by editor group id (usually '0')
        group0 = state.get('0', {})
        cursor_states = group0.get('cursorState', [])
        if cursor_states:
            position = cursor_states[0].get('position', {})
            line = position.get('lineNumber', None)
            if line is not None:
                print(f"INFO: tax.js cursor state found at line {line}")
                return line
    return None


def verify_task():
    """
    Verify that the agent used Go to Definition to navigate from main.js to
    the calculateTax function definition in tax.js (line 1).

    Scoring:
      Component 1 (0.5): tax.js is open in VSCode editor (navigation history OR open editors)
      Component 2 (0.5): Cursor in tax.js is at line 1 (calculateTax function declaration)

    Both components FAIL on initial_env (no workspace storage exists for project).
    Both components PASS on golden_env (tax.js opened at line 1 via Go to Definition).
    """
    total_score = 0.0

    # Precondition gate: project files must exist with calculateTax at line 1
    if not os.path.exists(TAX_JS):
        print(f"CRITICAL: tax.js not found at {TAX_JS}")
        print("REWARD: 0.0")
        return 0.0

    if not os.path.exists(MAIN_JS):
        print(f"CRITICAL: main.js not found at {MAIN_JS}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(TAX_JS) as f:
            first_line = f.readline().strip()
        if 'calculateTax' not in first_line:
            print(f"CRITICAL: tax.js line 1 is '{first_line}', expected 'function calculateTax'")
            print("REWARD: 0.0")
            return 0.0
        print(f"INFO: tax.js line 1: '{first_line}' -- contains calculateTax OK")
    except Exception as e:
        print(f"CRITICAL: Cannot read tax.js: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the project workspace state database
    db_path = find_project_workspace_db()
    if db_path is None:
        print("FAIL: No VSCode workspace storage found for file:///home/user/project")
        print("INFO: This indicates VSCode was never opened with the project folder")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 1: tax.js is open in editor (history entries OR open editors) (0.5 points)
    # Initial state: no workspace storage exists -> 0 points
    # Post-task state: tax.js was navigated to via Go to Definition -> 0.5 points
    try:
        in_history = tax_js_in_editor_history(db_path)
        in_editors = tax_js_in_open_editors(db_path)
        tax_open = in_history or in_editors

        if tax_open:
            print(f"PASS: Component 1 -- tax.js is open in VSCode editor "
                  f"(in_history={in_history}, in_editors={in_editors}) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 -- tax.js NOT found in editor history or open editors")
            print(f"INFO: Only main.js is open -- task not yet completed")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Cursor in tax.js at line 1 (calculateTax definition) (0.5 points)
    # Go to Definition places cursor at line 1 of tax.js (function calculateTax declaration).
    # Initial state: no workspace storage -> 0 points.
    # Post-task state: cursor at line 1 in tax.js -> 0.5 points.
    try:
        cursor_line = get_tax_js_cursor_line(db_path)
        if cursor_line is not None:
            # calculateTax is defined at line 1 of tax.js; allow tolerance to line 2
            if cursor_line <= 2:
                print(f"PASS: Component 2 -- Cursor in tax.js at line {cursor_line} "
                      f"(calculateTax definition at line 1) (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 2 -- Cursor in tax.js at line {cursor_line}, "
                      f"expected line 1 (calculateTax function declaration)")
        else:
            print(f"FAIL: Component 2 -- No cursor state for tax.js in textEditorViewState")
            print(f"INFO: tax.js was never opened in this session")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
