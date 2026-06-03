"""
Reward Script: Save the currently open file in VSCode
Task ID: vscode_stu_005
Domain: vscode
Scoring:
  Component 1 (0.5): File contains the unsaved TODO comment line
  Component 2 (0.3): File contains the full original content plus the new line
  Component 3 (0.2): File size matches expected saved state (2057 bytes +/- tolerance)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_005'
FILE_PATH = os.path.join(WORKDIR, 'main.py')

# The key unsaved change: a TODO comment appended at the end
EXPECTED_NEW_LINE = '# TODO: Add export to CSV functionality'

# Key content that must be preserved from the original file
ORIGINAL_MARKERS = [
    'Student Grade Calculator',
    'def load_grades():',
    'def calculate_average(grades):',
    'def calculate_letter_grade(average):',
    'def generate_report(gradebook):',
    'if __name__ == "__main__":',
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File contains the previously-unsaved TODO comment (0.5 points)
    # This is the key change: the unsaved buffer had this line, and saving should persist it.
    # In initial_env, main.py does NOT contain this line. In golden_env, it DOES.
    try:
        if EXPECTED_NEW_LINE in content:
            print(f"PASS: Component 1 — TODO comment found in saved file (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Expected '{EXPECTED_NEW_LINE}' not found in file")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Original content is fully preserved (0.3 points)
    # All original function definitions and structural markers must still be present.
    # This ensures save didn't corrupt/truncate the file.
    # Only awards points if Component 1 also passed (compound check anchored to task change).
    try:
        if EXPECTED_NEW_LINE in content:
            all_markers_present = all(marker in content for marker in ORIGINAL_MARKERS)
            if all_markers_present:
                print(f"PASS: Component 2 — All {len(ORIGINAL_MARKERS)} original markers preserved (0.3 pts)")
                total_score += 0.3
            else:
                missing = [m for m in ORIGINAL_MARKERS if m not in content]
                print(f"FAIL: Component 2 — Missing markers: {missing}")
        else:
            print(f"FAIL: Component 2 — Skipped (Component 1 not met)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: File size is consistent with full saved content (0.2 points)
    # Golden file is ~2057 bytes. Initial file is ~2017 bytes.
    # Saved file should be larger than the initial (unsaved) version.
    # Only awards points if Component 1 also passed (compound check anchored to task change).
    try:
        if EXPECTED_NEW_LINE in content:
            file_size = os.path.getsize(file_path)
            if file_size > 2030:
                print(f"PASS: Component 3 — File size {file_size} bytes indicates full save (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — File size {file_size} bytes too small (expected > 2030)")
        else:
            print(f"FAIL: Component 3 — Skipped (Component 1 not met)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# NOTE: Persistence hook intentionally DISABLED for this task.
# The task IS "save the file" — running Ctrl+S here would perform the task itself,
# making initial_env pass. We must only verify the on-disk state.

# Run verification
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
