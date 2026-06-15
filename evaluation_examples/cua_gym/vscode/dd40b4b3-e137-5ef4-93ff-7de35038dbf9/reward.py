"""
Reward Script: Open Markdown preview side by side in VSCode
Task ID: vscode_stu_016
Domain: vscode
Scoring:
  - Component 1 (0.4): Editor grid is split into 2+ groups (branch layout)
  - Component 2 (0.3): One of the editor groups contains a Markdown preview webview
  - Component 3 (0.3): The Markdown preview is for README.md specifically
"""

import json
import sqlite3
import os
import glob

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_016'


def find_workspace_state_db():
    """Find the most recently modified workspace state.vscdb file."""
    pattern = os.path.join(WORKDIR, '.config', 'Code', 'User', 'workspaceStorage', '*', 'state.vscdb')
    dbs = glob.glob(pattern)
    if not dbs:
        return None
    # Return the most recently modified one
    dbs.sort(key=os.path.getmtime, reverse=True)
    return dbs[0]


def get_editor_state(db_path):
    """Read the editor layout state from the workspace state DB."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT value FROM ItemTable WHERE key='memento/workbench.parts.editor'")
    row = cur.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None


def collect_leaves(node):
    """Recursively collect all leaf nodes from the editor grid."""
    if node.get('type') == 'leaf':
        return [node]
    elif node.get('type') == 'branch':
        leaves = []
        for child in node.get('data', []):
            leaves.extend(collect_leaves(child))
        return leaves
    return []


def find_markdown_preview_editors(leaves):
    """Search all editor groups for markdown preview webviews.
    Returns a list of (view_type, title, state_str) tuples for found previews."""
    results = []
    for leaf in leaves:
        leaf_data = leaf.get('data', {})
        editors = leaf_data.get('editors', [])
        for editor in editors:
            editor_id = editor.get('id', '')
            editor_value_str = editor.get('value', '')
            if 'webview' in editor_id.lower():
                try:
                    editor_value = json.loads(editor_value_str)
                    view_type = editor_value.get('viewType', '')
                    provided_id = editor_value.get('providedId', '')
                    title = editor_value.get('title', '')
                    state_str = editor_value.get('state', '')
                    if 'markdown.preview' in view_type or 'markdown.preview' in provided_id:
                        results.append((view_type, title, state_str))
                except (json.JSONDecodeError, TypeError):
                    pass
    return results


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Find the workspace state DB
    db_path = find_workspace_state_db()
    if not db_path:
        print("CRITICAL: No workspace state.vscdb found")
        print("REWARD: 0.0")
        return 0.0

    # Load editor state
    editor_state = get_editor_state(db_path)
    if not editor_state:
        print("CRITICAL: No editor state found in workspace DB")
        print("REWARD: 0.0")
        return 0.0

    editor_part = editor_state.get('editorpart.state', {})
    grid = editor_part.get('serializedGrid', {})
    root = grid.get('root', {})

    print(f"DEBUG: Grid root type = {root.get('type')}")

    # Component 1: Editor grid is split into 2+ groups (0.4 points)
    # In the initial state, root has only 1 leaf (no split).
    # In the golden state, root is a branch with 2 leaves (split pane).
    try:
        leaves = collect_leaves(root)
        num_groups = len(leaves)
        print(f"DEBUG: Number of editor groups = {num_groups}")

        if root.get('type') == 'branch' and num_groups >= 2:
            print(f"PASS: Component 1 -- Editor is split into {num_groups} groups (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 -- Expected split layout (branch with 2+ groups), found root type={root.get('type')}, groups={num_groups}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: One of the editor groups contains a Markdown preview webview (0.3 points)
    try:
        preview_editors = find_markdown_preview_editors(leaves)

        if len(preview_editors) > 0:
            vt, title, _ = preview_editors[0]
            print(f"DEBUG: Found markdown preview: viewType={vt}, title={title}")
            if 'markdown.preview' in vt:
                print(f"PASS: Component 2 -- Markdown preview found in split pane (0.3 pts)")
                total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- No Markdown preview webview found in any editor group")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: The Markdown preview is for README.md specifically (0.3 points)
    try:
        readme_preview_found = any(
            'README.md' in title or 'README' in title or _check_state_for_readme(state_str)
            for _, title, state_str in preview_editors
        ) if len(preview_editors) > 0 else False

        if readme_preview_found:
            print(f"PASS: Component 3 -- Markdown preview is for README.md (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 -- Markdown preview does not reference README.md")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


def _check_state_for_readme(state_str):
    """Check if the preview state JSON references README.md."""
    try:
        state = json.loads(state_str)
        resource = state.get('resource', '')
        return 'README.md' in resource
    except (json.JSONDecodeError, TypeError):
        return False


# Persistence hook: save VSCode state before verification
def persist_app_state():
    """Send Ctrl+S to save any unsaved state."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent to VSCode")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


persist_app_state()
verify_task()
