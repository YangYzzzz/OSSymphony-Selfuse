"""
Reward Script: Select entire function body of 'processOrder' in ~/Desktop/orders.py
Task ID: vscode_edit_080
Domain: vs_code
Scoring:
  Component 1 (0.6 pts): inSelectionMode is True AND selectionStart is at line 25, column 1
  Component 2 (0.4 pts): selection end position is at line 45 (covers entire function body)
"""

import os
import glob
import json
import sqlite3

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_080'

# Target file opened in VSCode
TARGET_FILE = 'file:///home/user/Desktop/orders.py'

# Expected selection boundaries for 'processOrder' function (lines 25-45)
EXPECTED_SELECTION_START_LINE = 25
EXPECTED_SELECTION_START_COL = 1
EXPECTED_POSITION_LINE = 45


def get_vscode_cursor_state():
    """
    Read the VSCode workspace state.vscdb SQLite database and return
    the cursor/selection state for the target file.
    Returns None if the state cannot be read.
    """
    ws_dirs = glob.glob('/home/user/.config/Code/User/workspaceStorage/*/state.vscdb')
    if not ws_dirs:
        print("ERROR: No VSCode workspace state.vscdb found")
        return None

    # Use the most recently modified workspace DB
    db_path = sorted(ws_dirs, key=os.path.getmtime)[-1]
    print(f"INFO: Using workspace DB: {db_path}")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM ItemTable WHERE key = ?',
                       ('memento/workbench.editors.files.textFileEditor',))
        row = cursor.fetchone()
        conn.close()
    except Exception as e:
        print(f"ERROR: Cannot read state.vscdb: {e}")
        return None

    if row is None:
        print("ERROR: Key 'memento/workbench.editors.files.textFileEditor' not found in DB")
        return None

    try:
        state = json.loads(row[0])
    except Exception as e:
        print(f"ERROR: Cannot parse textFileEditor state JSON: {e}")
        return None

    # Navigate: textEditorViewState -> [[uri, viewstate], ...]
    view_state_list = state.get('textEditorViewState', [])
    for entry in view_state_list:
        if len(entry) >= 2 and entry[0] == TARGET_FILE:
            editor_state = entry[1].get('0', {})
            cursor_states = editor_state.get('cursorState', [])
            if cursor_states:
                return cursor_states[0]  # primary cursor

    print(f"ERROR: No editor state found for URI: {TARGET_FILE}")
    return None


def verify_task():
    """
    Verify task completion: processOrder function (lines 25-45) is fully selected.
    Returns a float between 0.0 and 1.0.

    Precondition: orders.py must exist at expected path.
    Task verification is entirely via VSCode state DB — we check that an active
    text selection covers lines 25 through 45 (the complete processOrder function).
    """
    total_score = 0.0

    # Precondition gate: orders.py must exist
    orders_path = os.path.join(WORKDIR, 'Desktop', 'orders.py')
    if not os.path.exists(orders_path):
        print(f"CRITICAL: orders.py not found at {orders_path}")
        print("REWARD: 0.0")
        return 0.0

    # Get cursor state from VSCode DB
    cursor_state = get_vscode_cursor_state()
    if cursor_state is None:
        print("FAIL: Cannot retrieve VSCode cursor state")
        print("\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Raw cursor state: {json.dumps(cursor_state, indent=2)}")

    # Component 1: Active selection starting at line 25, column 1 (0.6 points)
    # Verifies: inSelectionMode=True AND selectionStart.lineNumber==25 AND selectionStart.column==1
    # This FAILS on initial_env (inSelectionMode=False, cursor at line 35) and
    # PASSES on golden_env (inSelectionMode=True, selectionStart at line 25)
    try:
        in_selection_mode = cursor_state.get('inSelectionMode', False)
        selection_start = cursor_state.get('selectionStart', {})
        start_line = selection_start.get('lineNumber', -1)
        start_col = selection_start.get('column', -1)
        component1_pass = (
            in_selection_mode is True
            and start_line == EXPECTED_SELECTION_START_LINE
            and start_col == EXPECTED_SELECTION_START_COL
        )
        if component1_pass:
            print(f"PASS: Component 1 — active selection starts at line {start_line}, "
                  f"col {start_col} (0.6 pts)")
            total_score += 0.6
        else:
            if not in_selection_mode:
                print(f"FAIL: Component 1 — inSelectionMode is False (no active selection)")
            elif start_line != EXPECTED_SELECTION_START_LINE:
                print(f"FAIL: Component 1 — selectionStart.lineNumber={start_line}, "
                      f"expected {EXPECTED_SELECTION_START_LINE}")
            elif start_col != EXPECTED_SELECTION_START_COL:
                print(f"FAIL: Component 1 — selectionStart.column={start_col}, "
                      f"expected {EXPECTED_SELECTION_START_COL}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Selection end position at line 45 (covers complete function body) (0.4 points)
    # Verifies: position.lineNumber==45 (the last line of processOrder function)
    # This FAILS on initial_env (position.lineNumber=35, inSelectionMode=False) and
    # PASSES on golden_env (position.lineNumber=45)
    try:
        position = cursor_state.get('position', {})
        pos_line = position.get('lineNumber', -1)

        if pos_line == EXPECTED_POSITION_LINE:
            print(f"PASS: Component 2 — selection end position at line {pos_line} "
                  f"(complete processOrder function selected) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — position.lineNumber={pos_line}, "
                  f"expected {EXPECTED_POSITION_LINE} (last line of processOrder)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
