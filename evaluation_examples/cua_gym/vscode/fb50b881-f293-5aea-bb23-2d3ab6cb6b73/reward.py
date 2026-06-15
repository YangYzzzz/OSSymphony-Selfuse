"""
Reward Script: Fold code to level 2 in VSCode
Task ID: vscode_code_025
Domain: vs_code
Scoring:
  - Component 1 (0.6 pts): collapsedRegions key present in editor.contrib.folding for app.js
                            AND at least 3 inner blocks have isCollapsed == True
  - Component 2 (0.4 pts): All 4 expected inner blocks folded at correct line numbers
                            (constructor 2-5, if-cache 8-10, if-user 12-14, try-catch 19-25)
"""

import os
import json
import sqlite3

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_025'
FOLDER_URI = 'file:///home/user/project'
FILE_URI = 'file:///home/user/project/app.js'
WS_STORAGE_ROOT = '/home/user/.config/Code/User/workspaceStorage'

# Expected inner blocks for level-2 fold (1-indexed line numbers from app.js with 28 lines)
# Level 2 fold collapses inner (nested) blocks while keeping top-level class/method visible:
#   - constructor body: lines 2-5
#   - if (this.cache.has) block in getUser: lines 8-10
#   - if (user) block in getUser: lines 12-14
#   - try block in deleteUser: lines 19-25
EXPECTED_COLLAPSED = [
    {"startLineNumber": 2, "endLineNumber": 5},
    {"startLineNumber": 8, "endLineNumber": 10},
    {"startLineNumber": 12, "endLineNumber": 14},
    {"startLineNumber": 19, "endLineNumber": 25},
]


def find_workspace_db():
    """Find the state.vscdb for /home/user/project workspace storage."""
    if not os.path.isdir(WS_STORAGE_ROOT):
        return None
    for entry in os.listdir(WS_STORAGE_ROOT):
        ws_json_path = os.path.join(WS_STORAGE_ROOT, entry, 'workspace.json')
        if os.path.exists(ws_json_path):
            try:
                with open(ws_json_path) as f:
                    data = json.load(f)
                if data.get('folder') == FOLDER_URI:
                    db_path = os.path.join(WS_STORAGE_ROOT, entry, 'state.vscdb')
                    if os.path.exists(db_path):
                        return db_path
            except Exception:
                continue
    return None


def get_fold_state(db_path):
    """
    Read the fold state for app.js from the workspace state.vscdb SQLite database.
    Returns the editor.contrib.folding dict, or None if not found.
    """
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT value FROM ItemTable WHERE key = ?',
            ('memento/workbench.editors.files.textFileEditor',)
        )
        row = cursor.fetchone()
        if row is None:
            return None
        view_state = json.loads(row[0])
        # Navigate: textEditorViewState -> [[fileUri, {0: {contributionsState: {...}}}], ...]
        text_editor_view = view_state.get('textEditorViewState', [])
        for entry in text_editor_view:
            if len(entry) == 2 and entry[0] == FILE_URI:
                groups = entry[1]
                for group_key in groups:
                    group = groups[group_key]
                    contributions = group.get('contributionsState', {})
                    folding_state = contributions.get('editor.contrib.folding', None)
                    if folding_state is not None:
                        return folding_state
        return None
    finally:
        conn.close()


def verify_task():
    """
    Verify that code folding to level 2 was applied in VSCode for app.js.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate 1: app.js must exist (folding is visual only — content must NOT change)
    try:
        app_js_path = '/home/user/project/app.js'
        if not os.path.exists(app_js_path):
            print(f"CRITICAL: app.js not found at {app_js_path}")
            print("REWARD: 0.0")
            return 0.0
        print(f"GATE PASS: app.js exists at {app_js_path}")
    except Exception as e:
        print(f"GATE ERROR checking app.js: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate 2: workspace storage DB must exist for /home/user/project
    try:
        db_path = find_workspace_db()
        if db_path is None:
            print(f"CRITICAL: No VSCode workspace storage found for {FOLDER_URI}")
            print("REWARD: 0.0")
            return 0.0
        print(f"GATE PASS: Found workspace DB at {db_path}")
    except Exception as e:
        print(f"GATE ERROR finding workspace DB: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Read fold state from SQLite DB
    try:
        fold_state = get_fold_state(db_path)
        if fold_state is None:
            print(f"FAIL: No fold state found for {FILE_URI} in workspace DB")
            print(f"\nScore: 0.0/1.0")
            print("REWARD: 0.0")
            return 0.0
        print(f"INFO: Fold state retrieved: {json.dumps(fold_state)[:400]}")
    except Exception as e:
        print(f"CRITICAL: Cannot read fold state from DB: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: collapsedRegions present AND at least 3 inner blocks collapsed (0.6 points)
    # This is the core indicator that level-2 folding was applied.
    # FAILS on initial_env (fold state has no collapsedRegions key — all code expanded)
    # PASSES on golden_env (4 collapsedRegions with isCollapsed=True)
    try:
        collapsed_regions = fold_state.get('collapsedRegions', None)
        if collapsed_regions is not None and isinstance(collapsed_regions, list):
            collapsed_count = sum(
                1 for r in collapsed_regions
                if isinstance(r, dict) and r.get('isCollapsed') is True
            )
            if collapsed_count >= 3:
                print(f"PASS: Component 1 — collapsedRegions present with {collapsed_count} collapsed block(s) (>= 3 for level-2 fold) (0.6 pts)")
                total_score += 0.6
            else:
                print(f"FAIL: Component 1 — collapsedRegions present but only {collapsed_count} block(s) have isCollapsed=True; need >= 3 for level-2 fold")
        else:
            print(f"FAIL: Component 1 — collapsedRegions key missing or invalid in fold state (no folding applied)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 4 expected inner blocks folded at correct line numbers (0.4 points)
    # Verifies precise fold points match the level-2 expected blocks in app.js (28 lines total).
    # FAILS on initial_env (no collapsedRegions) → PASSES on golden_env (exact match)
    try:
        if collapsed_regions is not None and isinstance(collapsed_regions, list):
            actual_collapsed_set = {
                (r['startLineNumber'], r['endLineNumber'])
                for r in collapsed_regions
                if isinstance(r, dict) and r.get('isCollapsed') is True
            }
            expected_set = {
                (b['startLineNumber'], b['endLineNumber'])
                for b in EXPECTED_COLLAPSED
            }
            missing = expected_set - actual_collapsed_set
            if not missing:
                print(f"PASS: Component 2 — All 4 expected inner blocks folded at correct line numbers (0.4 pts)")
                print(f"  Confirmed blocks: {sorted(actual_collapsed_set)}")
                total_score += 0.4
            else:
                missing_str = ", ".join(f"lines {s}-{e}" for s, e in sorted(missing))
                print(f"FAIL: Component 2 — Missing expected collapsed blocks: {missing_str}")
                print(f"  Actual collapsed: {sorted(actual_collapsed_set)}")
                print(f"  Expected collapsed: {sorted(expected_set)}")
        else:
            print("FAIL: Component 2 — skipped (no collapsedRegions available)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
