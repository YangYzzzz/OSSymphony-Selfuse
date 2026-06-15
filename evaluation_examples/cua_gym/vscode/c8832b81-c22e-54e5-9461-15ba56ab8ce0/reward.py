"""
Reward Script: Add watch expression 'total' in VSCode Debug Watch panel
Task ID: vscode_dbg_008
Domain: vs_code
Scoring:
  - Component 1: debug.watchExpressions key exists in workspace storage.json (0.5 pts)
  - Component 2: 'total' expression is in the watch expressions list (0.5 pts)

VSCode stores watch expressions per-workspace in:
  ~/.config/Code/User/workspaceStorage/<workspace_hash>/storage.json
  Key: "debug.watchExpressions" -> JSON-encoded list of expressions, e.g. '["total"]'

We check this file plus the backup/workbench.json as a fallback.
"""

import os
import json
import sqlite3

WORKDIR = '/home/user'
TASK_ID = 'vscode_dbg_008'

# The workspace hash for /home/user/projects/utils-lib
WORKSPACE_HASH = 'c4bd55975025cabafc24b05043a0b8ab'
WORKSPACE_STORAGE_DIR = os.path.join(
    WORKDIR, '.config', 'Code', 'User', 'workspaceStorage', WORKSPACE_HASH
)
STORAGE_JSON_PATH = os.path.join(WORKSPACE_STORAGE_DIR, 'storage.json')
BACKUP_JSON_PATH = os.path.join(WORKSPACE_STORAGE_DIR, 'backup', 'workbench.json')
STATE_VSCDB_PATH = os.path.join(WORKSPACE_STORAGE_DIR, 'state.vscdb')


def get_watch_expressions():
    """
    Try to read debug.watchExpressions from multiple VSCode storage locations.
    Returns the list of watch expressions, or None if not found anywhere.

    Priority:
    1. storage.json (the JSON override file setup-gen writes)
    2. backup/workbench.json (backup copy)
    3. state.vscdb (SQLite database, for completeness)
    """
    # Attempt 1: storage.json
    if os.path.exists(STORAGE_JSON_PATH):
        try:
            with open(STORAGE_JSON_PATH, 'r') as f:
                data = json.load(f)
            if 'debug.watchExpressions' in data:
                raw = data['debug.watchExpressions']
                # The value is a JSON-encoded string like '["total"]'
                exprs = json.loads(raw) if isinstance(raw, str) else raw
                print(f"INFO: Found debug.watchExpressions in storage.json: {exprs}")
                return exprs
        except Exception as e:
            print(f"WARN: Could not read storage.json: {e}")

    # Attempt 2: backup/workbench.json
    if os.path.exists(BACKUP_JSON_PATH):
        try:
            with open(BACKUP_JSON_PATH, 'r') as f:
                data = json.load(f)
            if 'debug.watchExpressions' in data:
                raw = data['debug.watchExpressions']
                exprs = json.loads(raw) if isinstance(raw, str) else raw
                print(f"INFO: Found debug.watchExpressions in backup/workbench.json: {exprs}")
                return exprs
        except Exception as e:
            print(f"WARN: Could not read backup/workbench.json: {e}")

    # Attempt 3: state.vscdb SQLite
    if os.path.exists(STATE_VSCDB_PATH):
        try:
            conn = sqlite3.connect(STATE_VSCDB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM ItemTable WHERE key = 'debug.watchExpressions'")
            row = cursor.fetchone()
            conn.close()
            if row:
                raw = row[0]
                exprs = json.loads(raw) if isinstance(raw, str) else raw
                print(f"INFO: Found debug.watchExpressions in state.vscdb: {exprs}")
                return exprs
        except Exception as e:
            print(f"WARN: Could not read state.vscdb: {e}")

    print("INFO: debug.watchExpressions not found in any storage location")
    return None


def verify_task():
    """
    Verify that the Watch panel in VSCode's Run and Debug sidebar contains 'total'.
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Component 1: debug.watchExpressions key exists with a non-empty list (0.5 pts)
    # This FAILS on initial_env (no storage.json, no watch expressions set)
    # This PASSES on golden_env (storage.json has debug.watchExpressions)
    watch_expressions = None
    try:
        watch_expressions = get_watch_expressions()
        if watch_expressions is not None and isinstance(watch_expressions, list) and len(watch_expressions) > 0:
            print(f"PASS: Component 1 — debug.watchExpressions key found with {len(watch_expressions)} expression(s) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — debug.watchExpressions not found or is empty (expected non-empty list, got: {watch_expressions})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'total' is in the watch expressions list (0.5 pts)
    # This FAILS on initial_env (no watch expressions at all)
    # This PASSES on golden_env (watch_expressions = ["total"])
    try:
        if watch_expressions is not None and isinstance(watch_expressions, list):
            if 'total' in watch_expressions:
                print(f"PASS: Component 2 — 'total' found in watch expressions list: {watch_expressions} (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 2 — 'total' not found in watch expressions list: {watch_expressions}")
        else:
            print(f"FAIL: Component 2 — no watch expressions list available to search")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
