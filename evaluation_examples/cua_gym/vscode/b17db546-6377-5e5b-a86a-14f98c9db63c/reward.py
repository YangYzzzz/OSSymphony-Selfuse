"""
Reward Script: Unfold all collapsed code in VSCode editor
Task ID: vscode_code_028
Domain: vs_code
Scoring:
  Component 1 (0.5): collapsedRegions key exists AND is empty list in golden env fold state
  Component 2 (0.5): The service.js fold state confirms all 4 previously-collapsed regions are gone
                      (compound: file has correct line count as sanity check)
"""

import os
import json
import sqlite3

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_028'

# The target file whose fold state we verify
TARGET_FILE_URI = 'file:///home/user/project/service.js'
TARGET_FILE_PATH = '/home/user/project/service.js'
WORKSPACE_STORAGE = '/home/user/.config/Code/User/workspaceStorage'

# The initial env had 4 collapsed regions for: DatabaseService, CacheService, ApiService, initialize
INITIAL_COLLAPSED_REGIONS_COUNT = 4


def find_workspace_db_for_project():
    """
    Find the state.vscdb file for the /home/user/project workspace folder.
    Returns the path to state.vscdb, or None if not found.
    """
    if not os.path.isdir(WORKSPACE_STORAGE):
        print(f"FAIL: Workspace storage dir not found: {WORKSPACE_STORAGE}")
        return None

    for dirname in os.listdir(WORKSPACE_STORAGE):
        dir_path = os.path.join(WORKSPACE_STORAGE, dirname)
        workspace_json = os.path.join(dir_path, 'workspace.json')
        if os.path.exists(workspace_json):
            try:
                with open(workspace_json) as f:
                    data = json.load(f)
                if data.get('folder') == 'file:///home/user/project':
                    db_path = os.path.join(dir_path, 'state.vscdb')
                    if os.path.exists(db_path):
                        print(f"INFO: Found project workspace DB: {db_path}")
                        return db_path
                    else:
                        print(f"WARN: workspace.json found but no state.vscdb in {dir_path}")
            except Exception as e:
                print(f"WARN: Could not read {workspace_json}: {e}")

    print("FAIL: No workspace storage DB found for file:///home/user/project")
    return None


def get_fold_state_from_db(db_path):
    """
    Read the editor fold state for service.js from the workspace state.vscdb.
    Returns the fold state dict, or None if not found.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT value FROM ItemTable WHERE key = ?",
            ('memento/workbench.editors.files.textFileEditor',)
        )
        row = cursor.fetchone()
        conn.close()

        if row is None:
            print("FAIL: No textFileEditor state found in ItemTable")
            return None

        state = json.loads(row[0])

        # Navigate to the fold state for the target file
        # Structure: {"textEditorViewState": [["file:///...", {"0": {...}}], ...]}
        view_states = state.get('textEditorViewState', [])
        for entry in view_states:
            if len(entry) >= 2 and entry[0] == TARGET_FILE_URI:
                editor_groups = entry[1]
                # Check group 0 (primary editor group)
                group_state = editor_groups.get('0', {})
                contributions = group_state.get('contributionsState', {})
                fold_state = contributions.get('editor.contrib.folding')
                if fold_state is not None:
                    print(f"INFO: Found fold state for {TARGET_FILE_URI}")
                    print(f"INFO: Fold state: {json.dumps(fold_state)}")
                    return fold_state
                else:
                    print(f"INFO: No folding contribution state for group 0")
                    return {}

        print(f"FAIL: No textEditorViewState entry for {TARGET_FILE_URI}")
        return None

    except Exception as e:
        print(f"ERROR: Could not read fold state from DB: {e}")
        return None


def verify_task():
    """
    Verify task completion: all collapsed code regions have been unfolded.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: verify target file exists
    if not os.path.exists(TARGET_FILE_PATH):
        print(f"CRITICAL: Target file not found: {TARGET_FILE_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Gate: find workspace DB for the project
    db_path = find_workspace_db_for_project()
    if db_path is None:
        print("CRITICAL: Cannot find workspace storage DB — cannot verify fold state")
        print("REWARD: 0.0")
        return 0.0

    # Get fold state from DB
    fold_state = get_fold_state_from_db(db_path)
    if fold_state is None:
        print("CRITICAL: Could not retrieve fold state for service.js from workspace DB")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: collapsedRegions key exists AND is empty list (0.5 points)
    # This check:
    # - FAILS on initial_env: collapsedRegions has 4 entries [[20,60],[62,115],[117,155],[157,171]]
    # - PASSES on golden_env: collapsedRegions is [] (all unfolded by agent action)
    try:
        collapsed_regions = fold_state.get('collapsedRegions', None)

        if collapsed_regions is None:
            print(f"FAIL: Component 1 — 'collapsedRegions' key is absent from fold state. "
                  f"Expected empty list [] after unfolding all. Fold state: {fold_state}")
        elif not isinstance(collapsed_regions, list):
            print(f"FAIL: Component 1 — 'collapsedRegions' is not a list: {collapsed_regions}")
        elif len(collapsed_regions) == 0:
            print(f"PASS: Component 1 — collapsedRegions is empty [] (all code unfolded) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — collapsedRegions still has {len(collapsed_regions)} "
                  f"collapsed region(s): {collapsed_regions}. Expected empty list after unfold all.")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 4 previously-collapsed regions are absent (compound check) (0.5 points)
    # Initial env had 4 collapsed regions for DatabaseService, CacheService, ApiService, initialize.
    # After "unfold all" (Ctrl+K Ctrl+J), all regions should be gone.
    # Additionally verify the file has the expected line count (confirming no content was changed).
    # This check:
    # - FAILS on initial_env: 4 collapsed regions exist (len > 0)
    # - PASSES on golden_env: no collapsed regions AND file has correct line count
    try:
        collapsed_regions = fold_state.get('collapsedRegions', None)

        # Check file line count as compound condition (implementation visible = file intact)
        file_line_count = 0
        with open(TARGET_FILE_PATH, 'r') as f:
            for _ in f:
                file_line_count += 1

        if collapsed_regions is None:
            print(f"FAIL: Component 2 — 'collapsedRegions' key absent, cannot verify "
                  f"that all 4 regions were unfolded")
        elif len(collapsed_regions) > 0:
            print(f"FAIL: Component 2 — {len(collapsed_regions)} region(s) still collapsed "
                  f"(expected 0 after 'unfold all'). Regions: {collapsed_regions}")
        elif file_line_count < 150:
            # Task context says file has 150 lines; actual is 172-173 lines
            print(f"FAIL: Component 2 — File has unexpected line count: {file_line_count} "
                  f"(expected >= 150). File may have been modified.")
        else:
            print(f"PASS: Component 2 — All {INITIAL_COLLAPSED_REGIONS_COUNT} collapsed regions "
                  f"are gone AND file has {file_line_count} lines (content intact) (0.5 pts)")
            total_score += 0.5
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
