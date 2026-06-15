"""
Reward Script: Open README.md in VSCode and preview it side-by-side using Markdown Preview
Task ID: vscode_wf_004
Domain: vscode
Scoring:
  Component 1 (0.35): README.md is open as a file editor tab
  Component 2 (0.35): Markdown Preview webview is open showing README.md
  Component 3 (0.30): Editor layout has 2 side-by-side groups (horizontal split)
"""

import os
import json
import sqlite3
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_004'

# VSCode workspace storage path (project folder hash)
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
WORKSPACE_STORAGE = os.path.join(VSCODE_USER, 'workspaceStorage')


def find_workspace_db():
    """Find the workspace state.vscdb file."""
    if not os.path.isdir(WORKSPACE_STORAGE):
        return None
    for entry in os.listdir(WORKSPACE_STORAGE):
        db_path = os.path.join(WORKSPACE_STORAGE, entry, 'state.vscdb')
        if os.path.exists(db_path):
            return db_path
    return None


def get_editor_state(db_path):
    """Read the editor state from the workspace state database."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.execute(
            "SELECT value FROM ItemTable WHERE key = 'memento/workbench.parts.editor'"
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return json.loads(row[0])
    except Exception as e:
        print(f"ERROR: Could not read editor state: {e}")
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Find workspace database
    db_path = find_workspace_db()
    if not db_path:
        print("CRITICAL: No workspace state database found")
        print("REWARD: 0.0")
        return 0.0

    # Load editor state
    editor_state = get_editor_state(db_path)
    if not editor_state:
        print("CRITICAL: Could not load editor state from workspace DB")
        print("REWARD: 0.0")
        return 0.0

    state = editor_state.get('editorpart.state', {})
    grid = state.get('serializedGrid', {})
    root = grid.get('root', {})
    children = root.get('data', [])

    # Collect all leaf editor groups
    def collect_leaves(node):
        """Recursively collect all leaf nodes from the editor grid."""
        if node.get('type') == 'leaf':
            return [node.get('data', {})]
        elif node.get('type') == 'branch':
            leaves = []
            for child in node.get('data', []):
                leaves.extend(collect_leaves(child))
            return leaves
        return []

    leaves = collect_leaves(root)
    print(f"INFO: Found {len(leaves)} editor group(s) in the grid")

    # Analyze all editors across all groups using counters
    readme_file_count = 0
    markdown_preview_count = 0

    for group in leaves:
        editors = group.get('editors', [])
        for editor in editors:
            editor_id = editor.get('id', '')
            editor_value_str = editor.get('value', '{}')

            try:
                editor_value = json.loads(editor_value_str)
            except (json.JSONDecodeError, TypeError):
                editor_value = {}

            # Check for README.md file editor
            if editor_id == 'workbench.editors.files.fileEditorInput':
                resource = editor_value.get('resourceJSON', {})
                file_path = resource.get('path', '') or resource.get('fsPath', '')
                if file_path and 'README.md' in file_path:
                    readme_file_count += 1
                    print(f"INFO: Found README.md file editor tab at: {file_path}")

            # Check for Markdown Preview webview
            if editor_id == 'workbench.editors.webviewInput':
                view_type = editor_value.get('viewType', '')
                provided_id = editor_value.get('providedId', '')
                title = editor_value.get('title', '')
                editor_state_str = editor_value.get('state', '{}')

                is_md_preview = (
                    'markdown.preview' in view_type or
                    'markdown.preview' in provided_id
                )

                # Check that the preview is for README.md
                if is_md_preview:
                    try:
                        inner_state = json.loads(editor_state_str)
                        resource = inner_state.get('resource', '')
                        if 'README.md' in resource:
                            markdown_preview_count += 1
                            print(f"INFO: Found Markdown Preview for README.md (title: {title})")
                        else:
                            print(f"INFO: Found Markdown Preview but for different file: {resource}")
                    except (json.JSONDecodeError, TypeError):
                        # Fallback: check title
                        if 'README' in title:
                            markdown_preview_count += 1
                            print(f"INFO: Found Markdown Preview by title: {title}")

    # Component 1: README.md is open as a file editor tab (0.35 points)
    try:
        if readme_file_count > 0:
            print(f"PASS: Component 1 -- README.md is open in a file editor tab (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 -- README.md is NOT open as a file editor tab")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Markdown Preview is open showing README.md (0.35 points)
    try:
        if markdown_preview_count > 0:
            print(f"PASS: Component 2 -- Markdown Preview is open for README.md (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 -- Markdown Preview for README.md is NOT open")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Editor has 2+ groups (side-by-side layout) (0.30 points)
    # The task asks for side-by-side preview, meaning the editor grid should have
    # at least 2 leaf groups (one for the file, one for the preview).
    try:
        num_groups = len(leaves)
        if num_groups >= 2:
            print(f"PASS: Component 3 -- Editor has {num_groups} groups (side-by-side layout) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 -- Editor has only {num_groups} group(s), expected >= 2 for side-by-side")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
