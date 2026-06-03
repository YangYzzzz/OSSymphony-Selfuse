"""
Reward Script: Close all open editor tabs except main.py
Task ID: vscode_stu_019
Domain: vscode
Scoring:
  Component 1 (0.6 pts): Exactly 1 editor tab is open
  Component 2 (0.4 pts): None of the other files (utils.py, config.py, test.py, readme.md, notes.txt) are open
"""

import os
import json
import sqlite3
import glob

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_019'

# Files that should have been closed
CLOSED_FILES = ['utils.py', 'config.py', 'test.py', 'readme.md', 'notes.txt']


def find_workspace_state_db():
    """Find the VSCode workspace state database dynamically."""
    ws_storage_root = os.path.join(WORKDIR, '.config', 'Code', 'User', 'workspaceStorage')
    if not os.path.isdir(ws_storage_root):
        return None

    # Find all state.vscdb files in workspace storage subdirectories
    candidates = glob.glob(os.path.join(ws_storage_root, '*', 'state.vscdb'))
    if not candidates:
        return None

    # If multiple, pick the most recently modified one
    candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return candidates[0]


def get_open_editors(db_path):
    """
    Extract the list of open editor file paths from the VSCode workspace state DB.
    Returns a list of file paths (strings).
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT value FROM ItemTable WHERE key = ?",
        ('memento/workbench.parts.editor',)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return []

    data = json.loads(row[0])
    editors_list = []

    # Navigate the serialized grid to find editor entries
    try:
        root = data['editorpart.state']['serializedGrid']['root']
        _extract_editors_from_node(root, editors_list)
    except (KeyError, TypeError) as e:
        print(f"WARN: Could not parse editor grid: {e}")

    return editors_list


def _extract_editors_from_node(node, editors_list):
    """Recursively extract editor file paths from the serialized grid tree."""
    if node.get('type') == 'leaf':
        leaf_data = node.get('data', {})
        for editor in leaf_data.get('editors', []):
            try:
                value_str = editor.get('value', '')
                value_json = json.loads(value_str)
                resource = value_json.get('resourceJSON', {})
                file_path = resource.get('path', '')
                if file_path:
                    editors_list.append(file_path)
            except (json.JSONDecodeError, AttributeError):
                continue
    elif node.get('type') == 'branch':
        for child in node.get('data', []):
            _extract_editors_from_node(child, editors_list)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Find the workspace state DB
    db_path = find_workspace_state_db()
    if not db_path:
        print("CRITICAL: Could not find VSCode workspace state database")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Using workspace state DB: {db_path}")

    # Get open editors
    try:
        open_editors = get_open_editors(db_path)
        editor_filenames = [os.path.basename(p) for p in open_editors]
        print(f"INFO: Open editors ({len(open_editors)}): {editor_filenames}")
    except Exception as e:
        print(f"CRITICAL: Could not read editor state: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Exactly 1 editor tab is open (0.6 points)
    # Initial state has 6 tabs; golden state should have exactly 1
    try:
        num_editors = len(open_editors)
        if num_editors == 1:
            print(f"PASS: Component 1 — exactly 1 editor tab open (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 — expected 1 editor tab, found {num_editors}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: None of the 'other' files are open (0.4 points)
    # Initial state has utils.py, config.py, test.py, readme.md, notes.txt open
    # Golden state should have none of these
    try:
        still_open = [f for f in CLOSED_FILES if f in editor_filenames]
        if len(still_open) == 0:
            print(f"PASS: Component 2 — none of the other files are open (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — these files should be closed but are still open: {still_open}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification (save any unsaved VSCode state)
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        # Send Ctrl+S to save any open editor state
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.5)
        print("PERSIST: ctrl+s sent for vscode")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
persist_app_state()
verify_task()
