"""
Reward Script: View all disabled extensions by filtering the Extensions panel
Task ID: vscode_ext_017
Domain: vs_code

Task: The user should type '@disabled' in the Extensions panel search bar,
causing VSCode to filter and show only disabled extensions.

Scoring:
  Component 1 (0.6 pts): memento/workbench.view.extensions has query.value == "@disabled"
                          in the workspace state SQLite DB — verifies the search query was typed
  Component 2 (0.4 pts): workbench.view.extensions.state key exists in the workspace DB,
                          confirming the Extensions panel was opened/active

Both components are ABSENT from the initial_env artifact and PRESENT on golden_env.
"""

import os
import json
import glob
import sqlite3

WORKSPACE_STORAGE_BASE = '/home/user/.config/Code/User/workspaceStorage'
TASK_ID = 'vscode_ext_017'


def find_workspace_db():
    """Find the most recently modified workspace state.vscdb file."""
    pattern = os.path.join(WORKSPACE_STORAGE_BASE, '*', 'state.vscdb')
    candidates = glob.glob(pattern)
    if not candidates:
        return None
    return max(candidates, key=os.path.getmtime)


def get_db_value(db_path, key):
    """Fetch a single value from the ItemTable in a workspace state.vscdb.
    Returns the raw string value, or None if the key is absent or DB is unreadable.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM ItemTable WHERE key = ?', (key,))
        row = cursor.fetchone()
        conn.close()
        if row is None:
            return None
        return row[0]
    except Exception as e:
        print(f"ERROR: Cannot read key '{key}' from DB {db_path}: {e}")
        return None


def verify_task():
    """
    Verify that the user performed '@disabled' search in the Extensions panel.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Locate the workspace state DB
    db_path = find_workspace_db()
    if db_path is None:
        print("CRITICAL: No workspace state.vscdb found under workspaceStorage/")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Using workspace DB at {db_path}")

    # Component 1: '@disabled' query stored in Extensions panel memento (0.6 points)
    # The key 'memento/workbench.view.extensions' holds the last search query typed
    # in the Extensions panel as JSON {"query.value": "<search_text>"}.
    # On initial_env this key is absent; on golden_env it must have query.value == "@disabled".
    try:
        raw_value = get_db_value(db_path, 'memento/workbench.view.extensions')
        if raw_value is None:
            print("FAIL: Component 1 — key 'memento/workbench.view.extensions' not found in DB (no @disabled search performed)")
        else:
            parsed = json.loads(raw_value)
            query_value = parsed.get('query.value', '')
            if query_value == '@disabled':
                print(f"PASS: Component 1 — Extensions panel query is '@disabled' (0.6 pts)")
                total_score += 0.6
            else:
                print(f"FAIL: Component 1 — expected query.value='@disabled', found: '{query_value}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: workbench.view.extensions.state key present (0.4 points)
    # This key is written by VSCode when the Extensions panel view state is persisted
    # (i.e., the panel was opened and its state saved).
    # On initial_env this key is absent; on golden_env it is present.
    try:
        state_value = get_db_value(db_path, 'workbench.view.extensions.state')
        if state_value is not None:
            print(f"PASS: Component 2 — workbench.view.extensions.state present (Extensions panel was opened) (0.4 pts)")
            total_score += 0.4
        else:
            print("FAIL: Component 2 — workbench.view.extensions.state not found (Extensions panel was not opened)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
