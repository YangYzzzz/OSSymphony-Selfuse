"""
Reward Script: Delete line 14 from ~/Desktop/script.sh using VSCode
Task ID: vscode_edit_007
Domain: vs_code

Scoring Rubric:
  Component 1: File has exactly 19 lines (down from 20) — 0.4 points
  Component 2: The debug echo line is absent from the file — 0.4 points
  Component 3: Key surrounding lines are preserved (content integrity) — 0.2 points
  Total: 1.0
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'vscode_edit_007'
TARGET_FILE = os.path.join(WORKDIR, 'script.sh')

# The exact debug line that must be removed
DEBUG_LINE = 'echo "DEBUG: temporary output"'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        lines = content.splitlines()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File has exactly 19 lines (0.4 points)
    # Initial env has 20 lines; after deleting line 14, it must have 19 lines.
    try:
        actual_line_count = len(lines)
        if actual_line_count == 19:
            print(f"PASS: Component 1 — file has exactly 19 lines (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — expected 19 lines, found {actual_line_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The debug echo line is absent from the file (0.4 points)
    # This is the specific line that was requested to be deleted.
    try:
        debug_present = any(DEBUG_LINE in line for line in lines)
        if not debug_present:
            print(f"PASS: Component 2 — debug echo line is absent from file (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — debug echo line still present: '{DEBUG_LINE}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The line following the deleted line has shifted up to position 14 (0.2 points)
    # In the initial file, 'pip install -r requirements.txt' was at line 15.
    # After deleting line 14, it must now be at line 14 (index 13).
    # This check FAILS on initial (pip is at line 15/index 14) and PASSES on golden (pip is at line 14/index 13).
    try:
        EXPECTED_LINE_14_CONTENT = 'pip install -r requirements.txt'
        if len(lines) >= 14 and EXPECTED_LINE_14_CONTENT in lines[13]:
            print(f"PASS: Component 3 — '{EXPECTED_LINE_14_CONTENT}' is now at line 14 (shifted up after deletion) (0.2 pts)")
            total_score += 0.2
        else:
            actual_line_14 = lines[13] if len(lines) >= 14 else '<no line 14>'
            print(f"FAIL: Component 3 — expected '{EXPECTED_LINE_14_CONTENT}' at line 14, found: '{actual_line_14}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: verify the canonical artifact
if not os.path.exists(TARGET_FILE):
    print(f"File not found: {TARGET_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(TARGET_FILE)
