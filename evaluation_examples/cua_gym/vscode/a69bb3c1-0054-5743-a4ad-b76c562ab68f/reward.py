"""
Reward Script: Add a logpoint on line 20 of process.js that logs 'Current item: {item}'
Task ID: vscode_dbg_013
Domain: vs_code
Scoring:
  Component 1 (0.4): A breakpoint/logpoint entry exists for process.js at line 20 (lineNumber=19, 0-indexed)
  Component 2 (0.4): The logpoint message matches 'Current item: {item}' exactly
  Component 3 (0.2): Entry is a true logpoint — has logMessage set, condition empty, enabled=True
  Total: 1.0
"""

import os
import json
import sqlite3

WORKDIR = '/home/user'
TASK_ID = 'vscode_dbg_013'
TARGET_FILE_URI = 'file:///home/user/projects/data-processor/process.js'
TARGET_LINE = 19  # VSCode uses 0-indexed line numbers; line 20 in editor = 19 here
EXPECTED_LOG_MESSAGE = 'Current item: {item}'
WORKSPACE_FOLDER_URI = 'file:///home/user/projects/data-processor'


def find_workspace_storage_path():
    """
    Find the VSCode workspaceStorage directory for the data-processor folder.
    VSCode hashes the workspace URI to form the directory name, so we search
    by reading workspace.json in each subdirectory.
    """
    ws_storage_root = os.path.join(WORKDIR, '.config', 'Code', 'User', 'workspaceStorage')
    if not os.path.isdir(ws_storage_root):
        return None

    for hash_dir in os.listdir(ws_storage_root):
        hash_path = os.path.join(ws_storage_root, hash_dir)
        workspace_json = os.path.join(hash_path, 'workspace.json')
        if os.path.isfile(workspace_json):
            try:
                with open(workspace_json, 'r') as f:
                    data = json.load(f)
                if data.get('folder') == WORKSPACE_FOLDER_URI:
                    return hash_path
            except (json.JSONDecodeError, IOError):
                continue
    return None


def get_breakpoints_from_vscdb(state_db_path):
    """
    Read the 'debug.breakpoints' key from the VSCode workspace state.vscdb SQLite database.
    Returns the parsed list or None if not found.
    """
    if not os.path.isfile(state_db_path):
        return None
    try:
        conn = sqlite3.connect(state_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM ItemTable WHERE key = 'debug.breakpoints'")
        row = cursor.fetchone()
        conn.close()
        if row is None:
            return None
        return json.loads(row[0])
    except Exception as e:
        print(f"ERROR: Could not read state.vscdb: {e}")
        return None


def verify_task():
    """
    Verify that a logpoint exists on line 20 of process.js with message 'Current item: {item}'.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: find workspace storage
    ws_path = find_workspace_storage_path()
    if ws_path is None:
        print("CRITICAL: Could not find workspace storage for data-processor folder.")
        print("REWARD: 0.0")
        return 0.0

    state_db_path = os.path.join(ws_path, 'state.vscdb')
    print(f"INFO: Using workspace state DB: {state_db_path}")

    # Load breakpoints list
    breakpoints = get_breakpoints_from_vscdb(state_db_path)
    if breakpoints is None:
        print("FAIL: No 'debug.breakpoints' key found in workspace state — no logpoints set.")
        print(f"\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(breakpoints)} breakpoint(s)/logpoint(s) in workspace state.")

    # Component 1: A logpoint entry exists for process.js at line 20 (lineNumber=19, 0-indexed) (0.4 points)
    try:
        matching_entries = [
            bp for bp in breakpoints
            if bp.get('uri') == TARGET_FILE_URI and bp.get('lineNumber') == TARGET_LINE
        ]
        if matching_entries:
            print(f"PASS: Component 1 — Found breakpoint/logpoint entry for process.js at line {TARGET_LINE} (0-indexed = editor line 20). (0.4 pts)")
            total_score += 0.4
        else:
            # Check if there's any entry for process.js at any line to give diagnostic info
            any_for_file = [bp for bp in breakpoints if 'process.js' in bp.get('uri', '')]
            if any_for_file:
                lines = [bp.get('lineNumber') for bp in any_for_file]
                print(f"FAIL: Component 1 — Found entries for process.js but at wrong line(s): {lines}. Expected lineNumber={TARGET_LINE}.")
            else:
                print(f"FAIL: Component 1 — No breakpoint/logpoint found for {TARGET_FILE_URI} at lineNumber={TARGET_LINE}.")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Only proceed with Components 2 and 3 if we have matching entries
    entry = matching_entries[0] if (total_score >= 0.4 and matching_entries) else None

    # Component 2: The logpoint message matches 'Current item: {item}' exactly (0.4 points)
    try:
        if entry is not None:
            actual_msg = entry.get('logMessage', '')
            if actual_msg == EXPECTED_LOG_MESSAGE:
                print(f"PASS: Component 2 — logMessage is exactly '{EXPECTED_LOG_MESSAGE}'. (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — Expected logMessage='{EXPECTED_LOG_MESSAGE}', found='{actual_msg}'.")
        else:
            print("FAIL: Component 2 — No matching entry to check logMessage.")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Entry is a true logpoint — logMessage set, condition empty, enabled=True (0.2 points)
    try:
        if entry is not None:
            log_msg_set = bool(entry.get('logMessage', ''))
            condition_empty = entry.get('condition', '') == ''
            is_enabled = entry.get('enabled', False) is True

            if log_msg_set and condition_empty and is_enabled:
                print(f"PASS: Component 3 — Entry is a valid logpoint: logMessage set, condition empty, enabled=True. (0.2 pts)")
                total_score += 0.2
            else:
                reasons = []
                if not log_msg_set:
                    reasons.append("logMessage is empty (not a logpoint)")
                if not condition_empty:
                    reasons.append(f"condition is '{entry.get('condition')}' (should be empty for logpoint)")
                if not is_enabled:
                    reasons.append("enabled is not True")
                print(f"FAIL: Component 3 — Logpoint validity checks failed: {'; '.join(reasons)}.")
        else:
            print("FAIL: Component 3 — No matching entry to check logpoint properties.")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
