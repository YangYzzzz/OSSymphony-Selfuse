"""
Reward Script: Duplicate lines 20-25 of template.py and paste below with renamed variables
Task ID: vscode_edit_065
Domain: vs_code
Scoring:
  Component 1: File has 56 lines total (0.2 pts)
  Component 2: Lines 26-27 start the copied block with 'input_data_2' (0.2 pts)
  Component 3: Line 28 uses 'processed_2' referencing 'input_data_2' (0.2 pts)
  Component 4: Lines 29-31 define 'result_2' referencing 'processed_2' (0.2 pts)
  Component 5: Lines 20-25 unchanged AND copied block lines 26-31 fully correct (0.2 pts)
Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_065'
FILE_PATH = f'{WORKDIR}/Desktop/template.py'

# Expected original lines 20-25 (1-indexed) in the file
EXPECTED_LINES_20_25 = [
    '    input_data = [f for f in os.listdir(source_dir)\n',
    "                  if f.endswith('.csv')]\n",
    '    processed = [item.strip() for item in input_data]\n',
    "    result = {'count': len(processed),\n",
    "              'files': processed,\n",
    "              'source': source_dir}\n",
]

# Expected copied block at lines 26-31 (with renamed variables)
EXPECTED_LINES_26_31 = [
    '    input_data_2 = [f for f in os.listdir(source_dir)\n',
    "                  if f.endswith('.csv')]\n",
    '    processed_2 = [item.strip() for item in input_data_2]\n',
    "    result_2 = {'count': len(processed_2),\n",
    "              'files': processed_2,\n",
    "              'source': source_dir}\n",
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Checks:
    - File exists and has 56 lines total (initial has 50)
    - Lines 26-27 are the start of the copied block with 'input_data_2'
    - Line 28 uses 'processed_2' referencing 'input_data_2'
    - Lines 29-31 define 'result_2' with 'processed_2' values
    - Compound: lines 20-25 are unchanged AND lines 26-31 complete copied block
    """
    total_score = 0.0

    # Gate: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load file lines
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Total line count must be 56 (0.2 points)
    # Initial file has 50 lines; after duplicating 6 lines it must have exactly 56.
    try:
        actual_line_count = len(lines)
        if actual_line_count == 56:
            print(f"PASS: Component 1 — File has 56 lines (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected 56 lines, found {actual_line_count} lines")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Lines 26-27 start the copied block with 'input_data_2' (0.2 points)
    # Line 26 (1-indexed) = index 25 (0-indexed): 'input_data_2 = ...'
    # Line 27 (1-indexed) = index 26 (0-indexed): continuation of list comprehension
    try:
        if len(lines) >= 27:
            line_26 = lines[25]  # 0-indexed 25 = 1-indexed 26
            line_27 = lines[26]  # 0-indexed 26 = 1-indexed 27
            expected_line_26 = EXPECTED_LINES_26_31[0]
            expected_line_27 = EXPECTED_LINES_26_31[1]
            if line_26 == expected_line_26 and line_27 == expected_line_27:
                print(f"PASS: Component 2 — Lines 26-27 start copied block with 'input_data_2' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — Lines 26-27 do not start the 'input_data_2' copied block")
                print(f"  Expected line 26: {repr(expected_line_26)}, got: {repr(line_26)}")
                print(f"  Expected line 27: {repr(expected_line_27)}, got: {repr(line_27)}")
        else:
            print(f"FAIL: Component 2 — File too short to have lines 26-27 (only {len(lines)} lines)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Line 28 uses 'processed_2' referencing 'input_data_2' (0.2 points)
    # Line 28 (1-indexed) = index 27 (0-indexed)
    # Must be: '    processed_2 = [item.strip() for item in input_data_2]\n'
    try:
        if len(lines) >= 28:
            line_28 = lines[27]  # 0-indexed 27 = 1-indexed 28
            expected_line_28 = EXPECTED_LINES_26_31[2]
            if line_28 == expected_line_28:
                print(f"PASS: Component 3 — Line 28 assigns 'processed_2' from 'input_data_2' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Line 28 does not match expected 'processed_2' assignment")
                print(f"  Expected: {repr(expected_line_28)}")
                print(f"  Actual:   {repr(line_28)}")
        else:
            print(f"FAIL: Component 3 — File too short to have line 28 (only {len(lines)} lines)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Lines 29-31 define 'result_2' with 'processed_2' values (0.2 points)
    # Lines 29-31 (1-indexed) = indices 28-30 (0-indexed)
    # Should be the result_2 dict construction referencing processed_2
    try:
        if len(lines) >= 31:
            line_29 = lines[28]  # 0-indexed 28 = 1-indexed 29
            line_30 = lines[29]
            line_31 = lines[30]
            expected_29 = EXPECTED_LINES_26_31[3]
            expected_30 = EXPECTED_LINES_26_31[4]
            expected_31 = EXPECTED_LINES_26_31[5]
            if line_29 == expected_29 and line_30 == expected_30 and line_31 == expected_31:
                print(f"PASS: Component 4 — Lines 29-31 define 'result_2' with 'processed_2' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 — Lines 29-31 do not match expected 'result_2' block")
                print(f"  Expected line 29: {repr(expected_29)}, got: {repr(line_29)}")
                print(f"  Expected line 30: {repr(expected_30)}, got: {repr(line_30)}")
                print(f"  Expected line 31: {repr(expected_31)}, got: {repr(line_31)}")
        else:
            print(f"FAIL: Component 4 — File too short to have lines 29-31 (only {len(lines)} lines)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Compound — lines 20-25 unchanged AND full copied block (26-31) correct (0.2 points)
    # This verifies the complete task requirement: original block preserved + copy inserted below
    # Compound check: FAILS on initial because lines 26-31 don't match the renamed variables
    try:
        if len(lines) >= 31:
            actual_20_25 = lines[19:25]   # 0-indexed 19-24 = 1-indexed 20-25
            actual_26_31 = lines[25:31]   # 0-indexed 25-30 = 1-indexed 26-31
            original_preserved = (actual_20_25 == EXPECTED_LINES_20_25)
            copy_correct = (actual_26_31 == EXPECTED_LINES_26_31)
            if original_preserved and copy_correct:
                print(f"PASS: Component 5 — Lines 20-25 preserved AND copied block 26-31 fully correct (0.2 pts)")
                total_score += 0.2
            else:
                if not original_preserved:
                    print(f"FAIL: Component 5 — Lines 20-25 were modified (original block must be preserved)")
                if not copy_correct:
                    print(f"FAIL: Component 5 — Copied block at lines 26-31 is not fully correct")
        else:
            print(f"FAIL: Component 5 — File too short to verify lines 20-31 (only {len(lines)} lines)")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
