"""
Reward Script: Disable ESLint extension for workspace only
Task ID: vscode_we_053
Domain: vscode
Scoring:
  Component 1 (0.5 pts): ESLint is disabled for the legacy-app workspace
  Component 2 (0.3 pts): ESLint is NOT globally disabled (remains enabled for other workspaces)
  Component 3 (0.2 pts): ESLint extension is still installed (not uninstalled)
"""

import os
import json
import sqlite3
import hashlib
import re

HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
GLOBAL_STATE_DB = os.path.join(VSCODE_USER, 'globalStorage', 'state.vscdb')
EXTENSIONS_DIR = os.path.join(HOME, '.vscode', 'extensions')
WORKSPACE_STORAGE_DIR = os.path.join(VSCODE_USER, 'workspaceStorage')

EXTENSION_ID = 'dbaeumer.vscode-eslint'
WORKSPACE_FOLDER_URI = 'file:///home/user/projects/legacy-app'


def find_workspace_hash():
    """Find the workspace storage hash for the legacy-app folder."""
    # Method 1: Scan workspace.json files to find the matching hash
    if os.path.isdir(WORKSPACE_STORAGE_DIR):
        for dirname in os.listdir(WORKSPACE_STORAGE_DIR):
            ws_json_path = os.path.join(WORKSPACE_STORAGE_DIR, dirname, 'workspace.json')
            if os.path.exists(ws_json_path):
                try:
                    with open(ws_json_path, 'r') as f:
                        data = json.load(f)
                    if data.get('folder') == WORKSPACE_FOLDER_URI:
                        return dirname
                except (json.JSONDecodeError, IOError):
                    continue
    return None


def get_disabled_extensions_for_workspace(conn, workspace_hash):
    """Query the global state DB for workspace-disabled extensions."""
    key = f'extensionManagement.disabled.{workspace_hash}'
    cur = conn.cursor()
    cur.execute('SELECT value FROM ItemTable WHERE key = ?', (key,))
    row = cur.fetchone()
    if row is None:
        return []
    try:
        return json.loads(row[0])
    except (json.JSONDecodeError, TypeError):
        return []


def get_globally_disabled_extensions(conn):
    """Query the global state DB for globally disabled extensions."""
    cur = conn.cursor()
    # VSCode stores globally disabled extensions under a key without a workspace hash
    cur.execute("SELECT key, value FROM ItemTable WHERE key LIKE 'extensionManagement.disabled%'")
    rows = cur.fetchall()
    globally_disabled = []
    for key, value in rows:
        # Keys with a hash suffix are workspace-specific; without are global
        # Global key format: 'extensionManagement.disabled' (no suffix)
        parts = key.split('.')
        # extensionManagement.disabled.<hash> = workspace-specific
        # extensionManagement.disabled = global
        if key == 'extensionManagement.disabled':
            try:
                globally_disabled = json.loads(value)
            except (json.JSONDecodeError, TypeError):
                pass
    return globally_disabled


def verify_task():
    """
    Verify that ESLint extension is disabled for the current workspace
    while remaining enabled globally.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: global state DB must exist
    if not os.path.exists(GLOBAL_STATE_DB):
        print(f"CRITICAL: Global state DB not found at {GLOBAL_STATE_DB}")
        print("REWARD: 0.0")
        return 0.0

    try:
        conn = sqlite3.connect(GLOBAL_STATE_DB)
    except Exception as e:
        print(f"CRITICAL: Cannot open global state DB: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the workspace hash for legacy-app
    workspace_hash = find_workspace_hash()
    if workspace_hash is None:
        print("FAIL: Could not find workspace storage hash for legacy-app folder")
        print("  This means the workspace was never opened in VSCode")
        conn.close()
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Workspace hash for legacy-app: {workspace_hash}")

    # Component 1: ESLint is disabled for the legacy-app workspace (0.5 points)
    try:
        disabled_for_workspace = get_disabled_extensions_for_workspace(conn, workspace_hash)
        eslint_disabled_for_workspace = any(
            entry.get('id', '').lower() == EXTENSION_ID.lower()
            for entry in disabled_for_workspace
            if isinstance(entry, dict)
        )
        if eslint_disabled_for_workspace:
            print(f"PASS: Component 1 -- ESLint is disabled for workspace legacy-app (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 -- ESLint is NOT disabled for workspace legacy-app")
            print(f"  Disabled extensions for workspace: {disabled_for_workspace}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: ESLint is NOT globally disabled (0.3 points)
    # This ensures the extension remains available for other workspaces
    try:
        globally_disabled = get_globally_disabled_extensions(conn)
        eslint_globally_disabled = any(
            entry.get('id', '').lower() == EXTENSION_ID.lower()
            for entry in globally_disabled
            if isinstance(entry, dict)
        )
        if not eslint_globally_disabled:
            # Also check: the extension should not be disabled for ALL workspaces
            # by checking if there's a universal disable
            # VSCode only workspace-disables, not global-disables, so this should pass
            # when extension is only workspace-disabled
            if eslint_disabled_for_workspace:
                # Only award points if Component 1 passed (extension IS workspace-disabled)
                # This makes this component conditional on the task change
                print(f"PASS: Component 2 -- ESLint is NOT globally disabled (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 -- ESLint is not workspace-disabled, so this check is moot")
        else:
            print(f"FAIL: Component 2 -- ESLint is globally disabled (should only be workspace-disabled)")
            print(f"  Globally disabled: {globally_disabled}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: ESLint extension is still installed (0.2 points)
    # The task says "disable" not "uninstall" -- extension files should still exist
    try:
        ext_entries = [
            entry for entry in os.listdir(EXTENSIONS_DIR)
            if entry.lower().startswith(EXTENSION_ID.lower())
        ] if os.path.isdir(EXTENSIONS_DIR) else []
        ext_installed = len(ext_entries) > 0
        if ext_installed and eslint_disabled_for_workspace:
            # Only award points if Component 1 passed (task change happened)
            print(f"PASS: Component 3 -- ESLint extension is still installed (0.2 pts)")
            total_score += 0.2
        elif not ext_installed:
            print(f"FAIL: Component 3 -- ESLint extension was uninstalled instead of disabled")
        else:
            print(f"FAIL: Component 3 -- Extension installed but not workspace-disabled")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    conn.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
