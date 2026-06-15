"""
Reward Script: Set a conditional breakpoint in VSCode
Task ID: vscode_dbg_012
Domain: vs_code
Scoring:
  - Component 1: Conditional breakpoint exists at line 15 of test.js (0.4 pts)
  - Component 2: Breakpoint condition is exactly 'i === 5' (0.3 pts)
  - Component 3: Breakpoint is enabled and targets the correct file path (0.3 pts)
  Total: 1.0
"""

import os
import json
import sqlite3

WORKDIR = '/home/user'
TASK_ID = 'vscode_dbg_012'
TARGET_FILE = 'test.js'
TARGET_PROJECT = 'test-runner'
TARGET_LINE = 15
TARGET_CONDITION = 'i === 5'
TARGET_FILE_PATH = f'{WORKDIR}/projects/{TARGET_PROJECT}/{TARGET_FILE}'


def find_workspace_storage_db(project_folder_uri: str) -> str:
    """
    Find the VSCode workspace storage SQLite DB for the given project folder.
    VSCode stores per-workspace state under:
      ~/.config/Code/User/workspaceStorage/<hash>/state.vscdb
    The matching directory is identified by workspace.json containing the folder URI.
    Returns path to state.vscdb, or None if not found.
    """
    ws_storage_root = os.path.join(WORKDIR, '.config', 'Code', 'User', 'workspaceStorage')
    if not os.path.isdir(ws_storage_root):
        return None
    for entry in os.listdir(ws_storage_root):
        entry_path = os.path.join(ws_storage_root, entry)
        ws_json_path = os.path.join(entry_path, 'workspace.json')
        if not os.path.exists(ws_json_path):
            continue
        try:
            with open(ws_json_path, 'r') as f:
                ws_data = json.load(f)
            if ws_data.get('folder') == project_folder_uri:
                db_path = os.path.join(entry_path, 'state.vscdb')
                if os.path.exists(db_path):
                    return db_path
        except (json.JSONDecodeError, IOError):
            continue
    return None


def get_breakpoints(db_path: str):
    """
    Read the 'debug.breakpoint' entry from the VSCode workspace SQLite DB.
    Returns a list of breakpoint dicts, or None if the key does not exist.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM ItemTable WHERE key = 'debug.breakpoint'")
        row = cursor.fetchone()
        conn.close()
        if row is None:
            return None
        return json.loads(row[0])
    except (sqlite3.Error, json.JSONDecodeError) as e:
        print(f"ERROR: Failed to read breakpoints from DB: {e}")
        return None


def verify_task():
    """
    Verify that a conditional breakpoint is set at line 15 of test.js
    with condition 'i === 5'.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Locate the workspace storage DB for the test-runner project
    project_uri = f'file://{WORKDIR}/projects/{TARGET_PROJECT}'
    db_path = find_workspace_storage_db(project_uri)

    if db_path is None:
        print(f"FAIL: Could not find VSCode workspace storage DB for project '{project_uri}'")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found workspace DB at: {db_path}")

    # Read breakpoints from the DB
    breakpoints = get_breakpoints(db_path)

    if breakpoints is None:
        print("FAIL: No 'debug.breakpoint' key found in workspace storage — no breakpoints have been set")
        print("\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(breakpoints)} breakpoint(s) in workspace storage")

    # ------------------------------------------------------------------
    # Component 1: A breakpoint exists at line 15 of test.js (0.4 points)
    # This FAILS on initial_env (no debug.breakpoint key at all) and
    # PASSES on golden_env (breakpoint at line 15 present).
    # ------------------------------------------------------------------
    bp_at_line15 = None
    try:
        for bp in breakpoints:
            # lineNumber in VSCode DB is 0-indexed? Check against expected value
            bp_line = bp.get('lineNumber')
            bp_uri = bp.get('uri', {})
            bp_file = bp_uri.get('fsPath', '') or bp_uri.get('path', '')
            # Normalize path for comparison
            if (bp_file == TARGET_FILE_PATH or
                    bp_file.endswith(f'/{TARGET_FILE}')) and bp_line == TARGET_LINE:
                bp_at_line15 = bp
                break

        if bp_at_line15 is not None:
            print(f"PASS: Component 1 — breakpoint found at line {TARGET_LINE} of {TARGET_FILE} (0.4 pts)")
            total_score += 0.4
        else:
            # Dump what we found to help debug
            for bp in breakpoints:
                bp_file = (bp.get('uri') or {}).get('fsPath', 'unknown')
                print(f"FAIL: Component 1 — found breakpoint at line {bp.get('lineNumber')} in {bp_file}, "
                      f"expected line {TARGET_LINE} in {TARGET_FILE_PATH}")
            if not breakpoints:
                print(f"FAIL: Component 1 — no breakpoints present")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ------------------------------------------------------------------
    # Component 2: The breakpoint condition is exactly 'i === 5' (0.3 points)
    # Only meaningful if we found a breakpoint at line 15 above.
    # ------------------------------------------------------------------
    try:
        if bp_at_line15 is not None:
            actual_condition = bp_at_line15.get('condition', '')
            if actual_condition == TARGET_CONDITION:
                print(f"PASS: Component 2 — breakpoint condition is '{actual_condition}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — expected condition '{TARGET_CONDITION}', "
                      f"found '{actual_condition}'")
        else:
            print(f"FAIL: Component 2 — skipped (no breakpoint at line {TARGET_LINE})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ------------------------------------------------------------------
    # Component 3: Breakpoint is enabled and targets the correct file (0.3 points)
    # Confirms the breakpoint is active (enabled=True) and maps to the right file.
    # ------------------------------------------------------------------
    try:
        if bp_at_line15 is not None:
            is_enabled = bp_at_line15.get('enabled', False)
            bp_uri = bp_at_line15.get('uri', {})
            bp_file = bp_uri.get('fsPath', '') or bp_uri.get('path', '')
            correct_file = (bp_file == TARGET_FILE_PATH or
                            bp_file.endswith(f'/{TARGET_PROJECT}/{TARGET_FILE}'))

            if is_enabled and correct_file:
                print(f"PASS: Component 3 — breakpoint is enabled and targets "
                      f"'{TARGET_FILE_PATH}' (0.3 pts)")
                total_score += 0.3
            elif not is_enabled:
                print(f"FAIL: Component 3 — breakpoint exists but is disabled (enabled=False)")
            else:
                print(f"FAIL: Component 3 — breakpoint file path mismatch: "
                      f"expected '{TARGET_FILE_PATH}', found '{bp_file}'")
        else:
            print(f"FAIL: Component 3 — skipped (no breakpoint at line {TARGET_LINE})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
