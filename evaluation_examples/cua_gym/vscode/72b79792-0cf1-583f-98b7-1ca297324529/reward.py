"""
Reward Script: Fold all <section> elements in report.html, then unfold only id='summary'
Task ID: vscode_edit_077
Domain: vs_code
Scoring:
  Component 1 (0.5 pts): All 4 non-summary sections are folded (header, details, charts, footer)
  Component 2 (0.5 pts): The summary section is NOT folded AND exactly 4 collapsed regions exist
"""

import os
import glob
import json
import sqlite3

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_077'

# Expected section fold state after task completion:
# - header     starts at line 10  (folded)
# - summary    starts at line 32  (NOT folded)
# - details    starts at line 62  (folded)
# - charts     starts at line 112 (folded)
# - footer     starts at line 157 (folded)

EXPECTED_FOLDED_STARTS = {10, 62, 112, 157}   # lines where folded sections start
SUMMARY_START = 32                              # summary section start line (must NOT be folded)
EXPECTED_FOLD_COUNT = 4                        # exactly 4 collapsed regions


def get_fold_state():
    """
    Read VSCode workspace SQLite db to get the folding state for report.html.
    VSCode stores fold state in workspaceStorage/<hash>/state.vscdb
    Returns the 'editor.contrib.folding' dict or None if not found.
    """
    # Find the workspace storage db dynamically
    db_paths = glob.glob(
        '/home/user/.config/Code/User/workspaceStorage/*/state.vscdb'
    )
    if not db_paths:
        print("ERROR: No VSCode workspace storage db found")
        return None

    report_file = '/home/user/Desktop/report.html'

    for db_path in db_paths:
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Try the key format used for textResourceEditorInput (direct file key)
            cursor.execute(
                'SELECT value FROM ItemTable WHERE key = ?',
                [f'workbench.editors.textResourceEditorInput:{report_file}']
            )
            row = cursor.fetchone()
            if row:
                data = json.loads(row[0])
                fold_state = data.get('contributionsState', {}).get('editor.contrib.folding')
                if fold_state:
                    conn.close()
                    return fold_state

            # Try the textFileEditor memento format
            cursor.execute(
                'SELECT value FROM ItemTable WHERE key = ?',
                ['memento/workbench.editors.files.textFileEditor']
            )
            row = cursor.fetchone()
            if row:
                data = json.loads(row[0])
                view_states = data.get('textEditorViewState', [])
                for entry in view_states:
                    # entry is [file_uri, {0: {...}}]
                    if isinstance(entry, list) and len(entry) == 2:
                        file_uri, state_obj = entry
                        if 'report.html' in file_uri:
                            inner = state_obj.get('0', {})
                            fold_state = inner.get('contributionsState', {}).get('editor.contrib.folding')
                            if fold_state:
                                conn.close()
                                return fold_state

            conn.close()

        except Exception as e:
            print(f"WARN: Could not read db {db_path}: {e}")
            continue

    return None


def verify_task():
    """
    Verify that the user has folded all sections except id='summary' in report.html.
    Returns float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Precondition: report.html must exist
    report_path = f'{WORKDIR}/Desktop/report.html'
    if not os.path.exists(report_path):
        print(f"CRITICAL: report.html not found at {report_path}")
        print("REWARD: 0.0")
        return 0.0

    # Get fold state from VSCode workspace database
    fold_state = get_fold_state()

    if fold_state is None:
        print("CRITICAL: Could not retrieve VSCode fold state for report.html")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Fold state retrieved: {json.dumps(fold_state, indent=2)}")

    collapsed_regions = fold_state.get('collapsedRegions', [])
    folded_start_lines = {r.get('startLineNumber') for r in collapsed_regions}

    print(f"INFO: Folded start lines: {sorted(folded_start_lines)}")
    print(f"INFO: Expected folded start lines: {sorted(EXPECTED_FOLDED_STARTS)}")
    print(f"INFO: Summary start line ({SUMMARY_START}) folded: {SUMMARY_START in folded_start_lines}")

    # Component 1: All 4 non-summary sections are folded (0.5 points)
    # header (line 10), details (line 62), charts (line 112), footer (line 157) must all be folded
    try:
        missing_folds = EXPECTED_FOLDED_STARTS - folded_start_lines
        if not missing_folds:
            print(f"PASS: Component 1 — All 4 non-summary sections are folded (0.5 pts)")
            total_score += 0.5
        else:
            missing_names = []
            name_map = {10: 'header', 62: 'details', 112: 'charts', 157: 'footer'}
            for ln in missing_folds:
                missing_names.append(name_map.get(ln, f'line_{ln}'))
            print(f"FAIL: Component 1 — Missing folded sections: {missing_names}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Summary section is NOT folded AND exactly 4 collapsed regions exist (0.5 points)
    # This verifies: (a) summary was unfolded after the all-fold operation, AND
    #                (b) no extra sections were accidentally left unfolded or incorrectly folded
    try:
        summary_not_folded = SUMMARY_START not in folded_start_lines
        correct_count = len(collapsed_regions) == EXPECTED_FOLD_COUNT
        comp2_pass = summary_not_folded and correct_count
        if comp2_pass:
            print(f"PASS: Component 2 — Summary (line {SUMMARY_START}) is NOT folded AND "
                  f"exactly {EXPECTED_FOLD_COUNT} collapsed regions (0.5 pts)")
            total_score += 0.5
        elif not summary_not_folded:
            print(f"FAIL: Component 2 — Summary section (line {SUMMARY_START}) is still "
                  f"folded; it should be unfolded")
        elif not correct_count:
            print(f"FAIL: Component 2 — Expected {EXPECTED_FOLD_COUNT} collapsed regions, "
                  f"found {len(collapsed_regions)}. Summary folded: {not summary_not_folded}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
