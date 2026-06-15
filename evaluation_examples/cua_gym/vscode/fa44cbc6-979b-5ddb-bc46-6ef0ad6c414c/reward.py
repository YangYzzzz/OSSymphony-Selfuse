"""
Reward Script: Debug app.js and navigate Call Stack panel in VSCode
Task ID: vscode_dbg_026
Domain: vs_code
Scoring:
  Component 1 (0.7): workbench.debug.callStackView visible (isHidden: false) in any workspace storage
  Component 2 (0.3): debug.uxstate == "simple" in any workspace storage (indicates debug panel was opened/active)
"""

import os
import json
import sqlite3
import glob

WORKDIR = '/home/user'
TASK_ID = 'vscode_dbg_026'
VSCODE_WORKSPACE_STORAGE = os.path.join(WORKDIR, '.config', 'Code', 'User', 'workspaceStorage')


def get_workspace_db_paths():
    """Find all workspace state.vscdb files."""
    pattern = os.path.join(VSCODE_WORKSPACE_STORAGE, '*', 'state.vscdb')
    return glob.glob(pattern)


def read_workspace_key(db_path, key):
    """Read a specific key from a workspace state.vscdb file. Returns None if not found."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM ItemTable WHERE key = ?', (key,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return row[0]
        return None
    except Exception as e:
        print(f"  ERROR reading {db_path}: {e}")
        return None


def find_callstack_view_state(db_paths):
    """
    Search all workspace DBs for the callStackView hidden state.
    Returns (found, is_hidden, db_path) or (False, None, None) if not found.
    """
    for db_path in db_paths:
        debug_state_raw = read_workspace_key(db_path, 'workbench.view.debug.state')
        if debug_state_raw:
            try:
                debug_state = json.loads(debug_state_raw)
                callstack_state = debug_state.get('workbench.debug.callStackView', {})
                is_hidden = callstack_state.get('isHidden', True)
                return True, is_hidden, db_path
            except json.JSONDecodeError:
                pass
    return False, None, None


def find_debug_ux_state(db_paths):
    """
    Search all workspace DBs for debug.uxstate value.
    Returns (found, ux_state, db_path) or (False, None, None) if not found.
    """
    for db_path in db_paths:
        ux_state = read_workspace_key(db_path, 'debug.uxstate')
        if ux_state:
            return True, ux_state, db_path
    return False, None, None


def verify_task():
    """
    Verify that the agent has opened the VSCode debugger and viewed the Call Stack panel.

    The task requires:
    - Open ~/projects/callstack-demo in VSCode
    - Debug app.js using the "Debug app.js" configuration
    - Navigate to the Call Stack panel (which shows: checkBalance, validatePayment, processOrder, main)

    Verifiable state changes (initial -> golden):
    - workbench.debug.callStackView: isHidden changes from true -> false
    - debug.uxstate: "default" -> "simple" (debug panel was interacted with)
    """
    total_score = 0.0

    db_paths = get_workspace_db_paths()
    print(f"Found {len(db_paths)} workspace storage DB(s): {db_paths}")

    # Component 1: Call Stack view is visible (isHidden: false) in debug view state (0.7 points)
    # Initial state: all debug views have isHidden: true
    # Golden state: all debug views have isHidden: false
    try:
        found, is_hidden, db_path = find_callstack_view_state(db_paths)
        if found:
            print(f"  DB: {db_path}")
            print(f"  workbench.debug.callStackView.isHidden: {is_hidden}")
            if not is_hidden:
                print("PASS: Component 1 — Call Stack view is visible (isHidden: false) (0.7 pts)")
                total_score += 0.7
            else:
                print("FAIL: Component 1 — Call Stack view is hidden (isHidden: true)")
        else:
            print("FAIL: Component 1 — workbench.view.debug.state not found in any workspace DB")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: debug.uxstate == "simple" indicates the debug panel was actively used (0.3 points)
    # Initial state: debug.uxstate = "default"
    # Golden state: debug.uxstate = "simple" (set when the Debug View is opened/simplified mode used)
    try:
        found, ux_state, db_path = find_debug_ux_state(db_paths)
        if found:
            print(f"  DB: {db_path}")
            print(f"  debug.uxstate: '{ux_state}'")
            if ux_state == 'simple':
                print("PASS: Component 2 — debug.uxstate is 'simple' (debug panel was opened/active) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — debug.uxstate is '{ux_state}', expected 'simple'")
        else:
            print("FAIL: Component 2 — debug.uxstate key not found in any workspace DB")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
if not os.path.isdir(VSCODE_WORKSPACE_STORAGE):
    print(f"ERROR: VSCode workspace storage not found: {VSCODE_WORKSPACE_STORAGE}")
    print("REWARD: 0.0")
else:
    verify_task()
