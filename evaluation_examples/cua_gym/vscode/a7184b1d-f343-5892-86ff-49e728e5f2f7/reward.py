"""
Reward Script: Open long_function.py, fold at level 1, then unfold the first nested block (for-loop)
Task ID: vscode_edit_087
Domain: vs_code
Scoring:
  - Component 1: for-loop block (lines 5-25) is in visible state (0.4 pts)
  - Component 2: Three blocks (if-block 27-50, try-except 52-75, while-loop 77-98) are folded (0.4 pts)
  - Component 3: Fold state data integrity - correct block names and line ranges (0.2 pts)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_087'

# Target fold state file placed by golden_patch as verification artifact
FOLD_STATE_PATH = os.path.join(WORKDIR, 'Desktop', 'golden_fold_state.json')

# Expected state based on task requirements:
# After fold level-1 + unfold first block:
#   - for-loop (lines 5-25): visible
#   - if-block (lines 27-50): folded
#   - try-except (lines 52-75): folded
#   - while-loop (lines 77-98): folded

EXPECTED_VISIBLE_BLOCK = {
    "name": "for-loop",
    "start_line": 5,
    "end_line": 25,
    "state": "visible"
}

EXPECTED_FOLDED_BLOCKS = [
    {"name": "if-block", "start_line": 27, "end_line": 50, "state": "folded"},
    {"name": "try-except", "start_line": 52, "end_line": 75, "state": "folded"},
    {"name": "while-loop", "start_line": 77, "end_line": 98, "state": "folded"},
]

# VSCode workspace storage path for querying fold state from DB
VSCODE_WS_DIR = os.path.join(WORKDIR, '.config', 'Code', 'User', 'workspaceStorage')


def get_vscode_fold_state():
    """
    Query VSCode workspace storage SQLite DB for fold state of long_function.py.
    Returns dict with folding data or None if not found / no active folds.
    """
    if not os.path.isdir(VSCODE_WS_DIR):
        return None
    try:
        import sqlite3
        for ws_id in os.listdir(VSCODE_WS_DIR):
            db_path = os.path.join(VSCODE_WS_DIR, ws_id, 'state.vscdb')
            if not os.path.exists(db_path):
                continue
            try:
                conn = sqlite3.connect(db_path)
                cur = conn.cursor()
                cur.execute(
                    "SELECT value FROM ItemTable "
                    "WHERE key='memento/workbench.editors.files.textFileEditor'"
                )
                row = cur.fetchone()
                conn.close()
                if not row:
                    continue
                data = json.loads(row[0])
                view_states = data.get('textEditorViewState', [])
                for entry in view_states:
                    if len(entry) >= 2 and 'long_function' in str(entry[0]):
                        group_state = entry[1].get('0', {})
                        folding_state = group_state.get('contributionsState', {}).get(
                            'editor.contrib.folding', {}
                        )
                        # Only return if there are active folds (collapsedRegions or regions)
                        has_folds = bool(
                            folding_state.get('collapsedRegions') or
                            folding_state.get('regions')
                        )
                        if has_folds:
                            return folding_state
            except Exception:
                continue
    except Exception:
        pass
    return None


def verify_fold_state_from_json(fold_state_data):
    """
    Verify fold state from golden_fold_state.json artifact.
    Returns (score, log_messages) tuple.
    """
    total_score = 0.0
    logs = []

    # Component 1: for-loop is in visible_blocks with correct line range (0.4 pts)
    try:
        visible_blocks = fold_state_data.get('visible_blocks', [])
        for_loop_entry = None
        for block in visible_blocks:
            if block.get('name') == 'for-loop' and block.get('state') == 'visible':
                for_loop_entry = block
                break

        if for_loop_entry is not None:
            start_ok = for_loop_entry.get('start_line') == EXPECTED_VISIBLE_BLOCK['start_line']
            end_ok = for_loop_entry.get('end_line') == EXPECTED_VISIBLE_BLOCK['end_line']
            if start_ok and end_ok:
                total_score += 0.4  # Component 1 passed
                logs.append(
                    f"PASS: Component 1 — for-loop is visible with correct line range "
                    f"(lines {for_loop_entry['start_line']}-{for_loop_entry['end_line']}) (0.4 pts)"
                )
            else:
                logs.append(
                    f"FAIL: Component 1 — for-loop visible but wrong line range: "
                    f"start={for_loop_entry.get('start_line')} (expected 5), "
                    f"end={for_loop_entry.get('end_line')} (expected 25)"
                )
        else:
            logs.append(
                f"FAIL: Component 1 — for-loop not found in visible_blocks "
                f"(visible: {[b.get('name') for b in visible_blocks]})"
            )
    except Exception as e:
        logs.append(f"ERROR: Component 1 — {e}")

    # Component 2: All three blocks (if-block, try-except, while-loop) are folded (0.4 pts)
    try:
        folded_blocks = fold_state_data.get('folded_blocks', [])
        folded_by_name = {b.get('name'): b for b in folded_blocks}

        missing_folds = []
        wrong_lines = []
        for expected in EXPECTED_FOLDED_BLOCKS:
            name = expected['name']
            if name not in folded_by_name:
                missing_folds.append(name)
            else:
                actual = folded_by_name[name]
                if actual.get('state') != 'folded':
                    missing_folds.append(f"{name} (state={actual.get('state')})")
                elif (actual.get('start_line') != expected['start_line'] or
                      actual.get('end_line') != expected['end_line']):
                    wrong_lines.append(
                        f"{name}: got {actual.get('start_line')}-{actual.get('end_line')}, "
                        f"expected {expected['start_line']}-{expected['end_line']}"
                    )

        comp2_pass = (len(missing_folds) == 0 and len(wrong_lines) == 0)
        if comp2_pass:
            total_score += 0.4  # Component 2 passed
            logs.append("PASS: Component 2 — all 3 blocks folded correctly (if-block@27, try-except@52, while-loop@77) (0.4 pts)")
        else:
            if missing_folds:
                logs.append(f"FAIL: Component 2 — missing folds: {missing_folds}")
            if wrong_lines:
                logs.append(f"FAIL: Component 2 — wrong line ranges: {wrong_lines}")
    except Exception as e:
        logs.append(f"ERROR: Component 2 — {e}")

    # Component 3: Data integrity — correct file target and task type in JSON (0.2 pts)
    try:
        file_path = fold_state_data.get('file', '')
        task_type = fold_state_data.get('task', '')
        file_ok = 'long_function.py' in file_path
        task_ok = 'fold' in task_type.lower()
        comp3_pass = file_ok and task_ok
        if comp3_pass:
            total_score += 0.2  # Component 3 passed
            logs.append(f"PASS: Component 3 — fold state references correct file ('{file_path}') and task type ('{task_type}') (0.2 pts)")
        else:
            logs.append(f"FAIL: Component 3 — incorrect file='{file_path}' or task='{task_type}'")
    except Exception as e:
        logs.append(f"ERROR: Component 3 — {e}")

    return total_score, logs


def verify_fold_state_from_vscode_db(folding_state):
    """
    Verify fold state from VSCode workspace storage DB.
    After fold-level-1 + unfold for-loop:
      VSCode stores collapsed region start lines 0-indexed: 26 (if-block), 51 (try-except), 76 (while-loop)
      The for-loop start at 0-indexed line 4 should NOT be in the folded set.
    Returns (score, log_messages) tuple.
    """
    total_score = 0.0
    logs = []

    collapsed_regions = folding_state.get('collapsedRegions', [])
    regions = folding_state.get('regions', {})

    # Determine folded start lines (0-indexed in VSCode DB)
    folded_lines_0indexed = set()
    if collapsed_regions:
        for region in collapsed_regions:
            if isinstance(region, (list, tuple)) and len(region) >= 1:
                folded_lines_0indexed.add(region[0])
            elif isinstance(region, dict):
                start = region.get('startLineNumber', region.get('start', -1))
                if start >= 0:
                    folded_lines_0indexed.add(start)
    elif regions:
        start_lines = regions.get('startLineNumbers', regions.get('starts', []))
        for sl in start_lines:
            folded_lines_0indexed.add(sl)

    logs.append(f"INFO: Detected folded start lines (0-indexed): {sorted(folded_lines_0indexed)}")

    # 1-indexed line -> 0-indexed:
    # for-loop line 5 -> 4 (should be VISIBLE, not folded)
    # if-block line 27 -> 26 (should be FOLDED)
    # try-except line 52 -> 51 (should be FOLDED)
    # while-loop line 77 -> 76 (should be FOLDED)
    EXPECTED_FOLDED_0IDX = {26, 51, 76}
    FOR_LOOP_0IDX = 4

    # Component 1: for-loop (line 4, 0-indexed) is NOT folded -> visible (0.4 pts)
    try:
        comp1_pass = FOR_LOOP_0IDX not in folded_lines_0indexed
        if comp1_pass:
            total_score += 0.4  # Component 1 passed: for-loop is visible
            logs.append("PASS: Component 1 (DB) — for-loop (line 5) is not folded (visible) (0.4 pts)")
        else:
            logs.append("FAIL: Component 1 (DB) — for-loop (line 5) found in folded list")
    except Exception as e:
        logs.append(f"ERROR: Component 1 (DB) — {e}")

    # Component 2: Three blocks folded at correct 0-indexed lines (0.4 pts)
    try:
        comp2_pass = EXPECTED_FOLDED_0IDX.issubset(folded_lines_0indexed)
        if comp2_pass:
            total_score += 0.4  # Component 2 passed: all 3 blocks are folded
            logs.append("PASS: Component 2 (DB) — all 3 blocks folded at expected lines (if-block@26, try-except@51, while-loop@76) (0.4 pts)")
        else:
            missing = EXPECTED_FOLDED_0IDX - folded_lines_0indexed
            logs.append(f"FAIL: Component 2 (DB) — missing folds at 0-indexed lines: {sorted(missing)}")
    except Exception as e:
        logs.append(f"ERROR: Component 2 (DB) — {e}")

    # Component 3: for-loop not folded and fold state is correct (0.2 pts)
    try:
        for_loop_not_folded = FOR_LOOP_0IDX not in folded_lines_0indexed
        unexpected_folds = folded_lines_0indexed - EXPECTED_FOLDED_0IDX
        comp3_pass = for_loop_not_folded
        if comp3_pass:
            total_score += 0.2  # Component 3 passed: for-loop visible
            if len(unexpected_folds) == 0:
                logs.append("PASS: Component 3 (DB) — exactly 3 blocks folded, for-loop visible (0.2 pts)")
            else:
                logs.append(f"PASS: Component 3 (DB) — for-loop visible (extra folds at: {sorted(unexpected_folds)}) (0.2 pts)")
        else:
            logs.append("FAIL: Component 3 (DB) — for-loop unexpectedly folded")
    except Exception as e:
        logs.append(f"ERROR: Component 3 (DB) — {e}")

    return total_score, logs


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Verification strategy:
    1. Check VSCode workspace DB for active fold state (primary path for agent-completed tasks)
    2. Check golden_fold_state.json artifact (primary path for golden_env, fallback otherwise)
    """
    total_score = 0.0

    # Precondition gate: long_function.py must exist
    long_func_path = os.path.join(WORKDIR, 'Desktop', 'long_function.py')
    if not os.path.exists(long_func_path):
        print(f"CRITICAL: long_function.py not found at {long_func_path}")
        print("REWARD: 0.0")
        return 0.0

    # Strategy 1: Check VSCode workspace storage DB for active fold state
    # This is the primary path when the agent performs the task interactively
    vscode_fold_state = get_vscode_fold_state()
    if vscode_fold_state is not None:
        print("INFO: Using VSCode workspace DB for fold state verification")
        score, logs = verify_fold_state_from_vscode_db(vscode_fold_state)
        for log in logs:
            print(log)
        total_score = score
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Strategy 2: Check golden_fold_state.json artifact (placed by golden_patch on golden_env)
    # Also serves as fallback when VSCode DB does not have fold data
    if not os.path.exists(FOLD_STATE_PATH):
        print(
            f"FAIL: No fold state found — VSCode DB has no active folds, "
            f"and {FOLD_STATE_PATH} does not exist"
        )
        print("INFO: Initial state — no folding has been performed")
        print("REWARD: 0.0")
        return 0.0

    # Load and parse the fold state JSON
    try:
        with open(FOLD_STATE_PATH, 'r') as f:
            fold_state_data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"CRITICAL: Cannot parse {FOLD_STATE_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    print("INFO: Using golden_fold_state.json artifact for verification")
    score, logs = verify_fold_state_from_json(fold_state_data)
    for log in logs:
        print(log)
    total_score = score

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
