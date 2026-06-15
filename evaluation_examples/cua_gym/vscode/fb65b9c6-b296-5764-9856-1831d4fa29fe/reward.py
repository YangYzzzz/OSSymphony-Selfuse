"""
Reward Script: Save draft.py in VSCode using keyboard shortcut
Task ID: vscode_edit_012
Domain: vs_code
Scoring:
  - Component 1: File content reflects saved edits (file size > initial, edits on lines 10-15)  0.4 pts
  - Component 2: calculate_regional_totals has exclude_unknown parameter                         0.3 pts
  - Component 3: Skip logic for unknown regions is present                                       0.3 pts
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_012'
FILE_PATH = '/home/user/Desktop/draft.py'

# The initial file (unsaved state) had these characteristics:
#   - 59 lines, 1747 bytes
#   - calculate_regional_totals(sales_data) — no exclude_unknown parameter
# The saved (golden) file has:
#   - 61 lines, 1855 bytes
#   - calculate_regional_totals(sales_data, exclude_unknown=True) — with parameter
#   - logic to skip unknown regions when exclude_unknown is True

INITIAL_FILE_SIZE = 1747  # bytes on initial_env (before save)


def verify_task(file_path):
    """
    Verify that draft.py has been saved with the edits applied to lines 10-15.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    lines = content.splitlines()

    # Component 1: File content reflects the saved edits — file is larger than the
    # initial (pre-edit) version. The edits added lines to the function, so the saved
    # file must be strictly larger than the original 1747-byte initial file.
    # This fails on initial_env (same as initial size) and passes on golden_env.
    try:
        file_size = os.path.getsize(file_path)
        if file_size > INITIAL_FILE_SIZE:
            print(f"PASS: Component 1 — File size {file_size} bytes > initial {INITIAL_FILE_SIZE} bytes (edits saved)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — File size {file_size} bytes not greater than initial {INITIAL_FILE_SIZE} bytes; edits may not be saved")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The edited function signature includes the 'exclude_unknown' parameter.
    # The task context says lines 10-15 were edited; in the golden file, the function
    # calculate_regional_totals now takes exclude_unknown=True as a second argument.
    # This fails on initial_env (no such parameter) and passes on golden_env.
    try:
        matching_lines = [
            line for line in lines
            if 'calculate_regional_totals' in line and 'exclude_unknown' in line
        ]
        if len(matching_lines) > 0:
            print(f"PASS: Component 2 — 'exclude_unknown' parameter found in calculate_regional_totals signature")
            total_score += 0.3
        else:
            print("FAIL: Component 2 — 'exclude_unknown' parameter NOT found in calculate_regional_totals; edit not saved")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The skip-logic for unknown regions is present in the file.
    # The edit adds: if exclude_unknown and region == "Unknown": continue
    # This fails on initial_env and passes on golden_env.
    try:
        # Find all lines containing 'exclude_unknown' along with 'Unknown' or 'continue'
        candidate_lines = [line.strip() for line in lines if 'exclude_unknown' in line]
        # Check if any line or immediate context contains 'continue'
        skip_logic_count = sum(
            1 for line in candidate_lines
            if 'Unknown' in line or 'continue' in line
        )
        # Also scan the full content for a multi-line if block pattern
        if skip_logic_count == 0:
            # Check for 'continue' in the vicinity of exclude_unknown lines
            for i, line in enumerate(lines):
                if 'exclude_unknown' in line:
                    window = lines[i:min(i+4, len(lines))]
                    if any('continue' in wl for wl in window):
                        skip_logic_count += 1
                        break
        if skip_logic_count > 0:
            print("PASS: Component 3 — Skip logic for unknown regions found (exclude_unknown + continue)")
            total_score += 0.3
        else:
            print("FAIL: Component 3 — Skip logic for unknown regions NOT found; edit not saved")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
