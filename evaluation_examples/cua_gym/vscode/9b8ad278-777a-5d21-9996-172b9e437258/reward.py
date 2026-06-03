"""
Reward Script: Navigate breadcrumbs in dateFormatter.js to jump to 'src' directory level
Task ID: vscode_edit_067
Domain: vs_code
Scoring:
  Component 1 (0.6): Explorer focus and selection are on src/ directory
  Component 2 (0.4): src/ is expanded AND the deeper paths (utils/, utils/formatters/) are NOT expanded
"""

import os
import json
import sqlite3

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_067'

PROJECT_URI = 'file:///home/user/Desktop/project'
SRC_URI = f'{PROJECT_URI}/src'
DATE_FORMATTER_URI = f'{PROJECT_URI}/src/utils/formatters/dateFormatter.js'
WORKSPACE_HASH = '327339a174881ee581c572ba091d1f13'
WORKSPACE_STORAGE = f'{WORKDIR}/.config/Code/User/workspaceStorage'
DB_PATH = os.path.join(WORKSPACE_STORAGE, WORKSPACE_HASH, 'state.vscdb')
TREE_STATE_KEY = 'workbench.explorer.treeViewState'


def load_tree_state():
    """Load workbench.explorer.treeViewState from the project workspace DB."""
    if not os.path.exists(DB_PATH):
        print(f"CRITICAL: Workspace DB not found at {DB_PATH}")
        return None
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM ItemTable WHERE key = ?", (TREE_STATE_KEY,))
        row = cursor.fetchone()
        if row is None:
            print(f"CRITICAL: Key '{TREE_STATE_KEY}' not found in DB")
            return None
        return json.loads(row[0])
    except Exception as e:
        print(f"CRITICAL: Failed to read tree state: {e}")
        return None
    finally:
        conn.close()


def verify_task():
    """
    Verify that the explorer focus has been moved to 'src/' via breadcrumb navigation.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: workspace DB must exist for the project
    tree_state = load_tree_state()
    if tree_state is None:
        print("REWARD: 0.0")
        return 0.0

    print(f"DEBUG: treeViewState = {json.dumps(tree_state, indent=2)}")

    focus_list = tree_state.get('focus', [])
    selection_list = tree_state.get('selection', [])
    expanded_list = tree_state.get('expanded', [])

    # Component 1: Explorer focus AND selection are on src/ directory (0.6 points)
    # Task: "clicking 'src' in the breadcrumbs must ... explorer focus should be at the src directory level"
    # FAILS on initial_env (focus is on dateFormatter.js), PASSES on golden_env (focus is on src/)
    try:
        src_focus_key = f'{PROJECT_URI}::{SRC_URI}'
        focus_on_src = src_focus_key in focus_list
        selection_on_src = src_focus_key in selection_list

        if focus_on_src and selection_on_src:
            print(f"PASS: Component 1 — Explorer focus and selection are on src/ ({src_focus_key}) (0.6 pts)")
            total_score += 0.6
        else:
            if not focus_on_src:
                print(f"FAIL: Component 1 — Focus not on src/. Actual focus: {focus_list}")
            if not selection_on_src:
                print(f"FAIL: Component 1 — Selection not on src/. Actual selection: {selection_list}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: src/ is expanded AND deeper paths (utils/, utils/formatters/) are NOT in expanded (0.4 points)
    # When the agent navigates to src/ via breadcrumb, the sub-tree under utils/ and utils/formatters/ collapses.
    # On initial_env: expanded includes src/, src/utils, src/utils/formatters — the deeper paths are present.
    # On golden_env: expanded includes only src/ — deeper paths removed by the navigation.
    # FAILS on initial_env (deeper paths still expanded), PASSES on golden_env (only src/ expanded)
    try:
        src_expand_key = f'{PROJECT_URI}::{SRC_URI}'
        utils_expand_key = f'{PROJECT_URI}::{PROJECT_URI}/src/utils'
        formatters_expand_key = f'{PROJECT_URI}::{PROJECT_URI}/src/utils/formatters'

        src_is_expanded = src_expand_key in expanded_list
        utils_not_expanded = utils_expand_key not in expanded_list
        formatters_not_expanded = formatters_expand_key not in expanded_list

        if src_is_expanded and utils_not_expanded and formatters_not_expanded:
            print(f"PASS: Component 2 — src/ is expanded and deeper paths are collapsed (0.4 pts)")
            total_score += 0.4
        else:
            if not src_is_expanded:
                print(f"FAIL: Component 2 — src/ not in expanded list. Expanded: {expanded_list}")
            if not utils_not_expanded:
                print(f"FAIL: Component 2 — utils/ still in expanded list (deeper paths not collapsed). Expanded: {expanded_list}")
            if not formatters_not_expanded:
                print(f"FAIL: Component 2 — utils/formatters/ still in expanded list (deeper paths not collapsed). Expanded: {expanded_list}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
