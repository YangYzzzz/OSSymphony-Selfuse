"""
Reward Script: Open '~/Desktop/notes.md' in VSCode and select the entire line 8.
Task ID: vscode_edit_005
Domain: vs_code
Scoring:
  Component 1 (0.3): notes.md is open in VSCode with an active selection (inSelectionMode == True)
  Component 2 (0.4): Selection anchor (selectionStart) is at lineNumber=8, column=1
  Component 3 (0.3): Cursor position is at lineNumber=9, column=1 (full line 8 incl. newline selected)
"""

import os
import json
import glob
import sqlite3

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_005'
NOTES_PATH = '/home/user/Desktop/notes.md'


def verify_task():
    """
    Verify that the agent opened notes.md in VSCode and selected the entire line 8.
    Reads VSCode workspaceStorage SQLite DB to check cursor/selection state.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: notes.md must exist
    if not os.path.exists(NOTES_PATH):
        print(f"CRITICAL: notes.md not found at {NOTES_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Locate workspaceStorage SQLite DB
    pattern = '/home/user/.config/Code/User/workspaceStorage/*/state.vscdb'
    db_paths = glob.glob(pattern)
    if not db_paths:
        print("CRITICAL: No VSCode workspaceStorage database found")
        print("REWARD: 0.0")
        return 0.0

    db_path = db_paths[0]
    print(f"Using VSCode DB: {db_path}")

    # Load the textFileEditor state from the SQLite DB
    cursor_state = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT value FROM ItemTable WHERE key=?",
            ("memento/workbench.editors.files.textFileEditor",)
        )
        row = cursor.fetchone()
        conn.close()

        if row is None:
            print("FAIL: key 'memento/workbench.editors.files.textFileEditor' not found in DB")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        data = json.loads(row[0])
        view_states = data.get("textEditorViewState", [])

        # Find the entry for notes.md
        notes_uri = "file:///home/user/Desktop/notes.md"
        for entry in view_states:
            if isinstance(entry, list) and len(entry) >= 2 and entry[0] == notes_uri:
                editor_state = entry[1]
                # editor_state is keyed by viewport index ("0" for primary)
                viewport = editor_state.get("0", {})
                cursor_states = viewport.get("cursorState", [])
                if cursor_states:
                    cursor_state = cursor_states[0]
                break

        if cursor_state is None:
            print(f"FAIL: No cursor state found for {notes_uri} in textEditorViewState")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

    except Exception as e:
        print(f"CRITICAL: Could not read workspaceStorage DB: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found cursor state: {json.dumps(cursor_state, indent=2)}")

    in_selection_mode = cursor_state.get("inSelectionMode", False)
    sel_start = cursor_state.get("selectionStart", {})
    sel_start_line = sel_start.get("lineNumber", -1)
    sel_start_col = sel_start.get("column", -1)
    pos = cursor_state.get("position", {})
    pos_line = pos.get("lineNumber", -1)
    pos_col = pos.get("column", -1)

    # Component 1: notes.md is open in VSCode with an active selection (0.3 points)
    # inSelectionMode must be True — this FAILS in initial_env (False) and PASSES in golden_env (True)
    try:
        notes_open_in_editor = False
        try:
            conn2 = sqlite3.connect(db_path)
            c2 = conn2.cursor()
            c2.execute(
                "SELECT value FROM ItemTable WHERE key=?",
                ("memento/workbench.parts.editor",)
            )
            row2 = c2.fetchone()
            conn2.close()
            if row2:
                parts_str = json.dumps(json.loads(row2[0]))
                notes_open_in_editor = "/home/user/Desktop/notes.md" in parts_str
        except Exception as e2:
            print(f"WARN: Could not check parts.editor: {e2}")

        if notes_open_in_editor and in_selection_mode:
            print(f"PASS: Component 1 — notes.md is open and inSelectionMode=True (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — notes_open={notes_open_in_editor}, inSelectionMode={in_selection_mode} (expected True)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Selection anchor (selectionStart) is at lineNumber=8, column=1 (0.4 points)
    # This FAILS in initial_env (line=1, col=1) and PASSES in golden_env (line=8, col=1)
    try:
        if sel_start_line == 8 and sel_start_col == 1:
            print(f"PASS: Component 2 — selectionStart at lineNumber=8, column=1 (0.4 pts)")
            total_score += 0.4
        else:
            print(
                f"FAIL: Component 2 — expected selectionStart={{lineNumber:8, column:1}}, "
                f"found {{lineNumber:{sel_start_line}, column:{sel_start_col}}}"
            )
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Cursor position is at lineNumber=9, column=1 (entire line 8 incl. newline selected) (0.3 points)
    # VSCode Ctrl+L (select line) moves cursor to start of next line.
    # This FAILS in initial_env (pos.line=1) and PASSES in golden_env (pos.line=9, col=1)
    try:
        if pos_line == 9 and pos_col == 1:
            print(f"PASS: Component 3 — cursor position at lineNumber=9, column=1 (full line 8 selected) (0.3 pts)")
            total_score += 0.3
        else:
            print(
                f"FAIL: Component 3 — expected position={{lineNumber:9, column:1}}, "
                f"found {{lineNumber:{pos_line}, column:{pos_col}}}"
            )
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
