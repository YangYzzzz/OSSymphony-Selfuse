"""
Reward Script: Use expand selection feature to select entire <div class="content"> element
Task ID: vscode_edit_035
Domain: vs_code
Scoring:
  - Component 1 (0.4): selection_result.txt exists and has non-empty content
  - Component 2 (0.3): selected region starts with opening <div class="content"> tag
  - Component 3 (0.3): selected region ends with closing </div> and spans exactly 16 lines (lines 20-35)
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'vscode_edit_035'

# Expected: selection_result.txt should contain exactly lines 20-35 of template.html,
# i.e., the entire <div class="content">...</div> block (16 lines).

EXPECTED_FIRST_LINE = '    <div class="content">\n'
EXPECTED_LAST_LINE  = '    </div>\n'
EXPECTED_LINE_COUNT = 16
# Line 6 in selection_result.txt corresponds to line 25 of template.html (cursor start: <span>)
EXPECTED_SPAN_LINE  = '            <span class="highlight">latest arrivals</span>\n'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    selection_path = os.path.join(WORKDIR, 'selection_result.txt')

    # Component 1: selection_result.txt exists and is non-empty (0.4 points)
    # This file does NOT exist in the initial_env, only in the golden_env after the agent
    # has performed the expand selection and recorded the result.
    try:
        if not os.path.exists(selection_path):
            print(f"FAIL: Component 1 — selection_result.txt not found at {selection_path}")
            # Without the selection artifact, further checks are impossible
            print("\nScore: 0.0/1.0")
            print("REWARD: 0.0")
            return 0.0

        with open(selection_path, 'r') as f:
            content = f.read()

        if content.strip():
            print(f"PASS: Component 1 — selection_result.txt exists and has content ({len(content)} bytes) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — selection_result.txt exists but is empty")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Read all lines for remaining checks
    try:
        with open(selection_path, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"ERROR: Cannot read lines from selection_result.txt: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: The selected region starts with <div class="content"> opening tag (0.3 points)
    # The expand selection should have expanded outward to capture the parent <div class="content">
    # which begins at line 20 of template.html. The first line of selection_result.txt must be
    # that opening tag.
    try:
        if lines and lines[0] == EXPECTED_FIRST_LINE:
            print(f'PASS: Component 2 — selection starts with \'    <div class="content">\' (0.3 pts)')
            total_score += 0.3
        else:
            actual_first = lines[0] if lines else '(empty)'
            print(f"FAIL: Component 2 — expected first line {repr(EXPECTED_FIRST_LINE)}, "
                  f"got {repr(actual_first)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The selected region ends with the closing </div> tag AND spans exactly 16 lines
    # (lines 20-35 inclusive = the complete <div class="content"> block). (0.3 points)
    try:
        actual_count = len(lines)
        actual_last  = lines[-1] if lines else '(empty)'

        last_ok  = (actual_last == EXPECTED_LAST_LINE)
        count_ok = (actual_count == EXPECTED_LINE_COUNT)

        if last_ok and count_ok:
            print(f"PASS: Component 3 — selection ends with '    </div>' and spans {actual_count} lines (0.3 pts)")
            total_score += 0.3
        else:
            if not last_ok:
                print(f"FAIL: Component 3 — expected last line {repr(EXPECTED_LAST_LINE)}, got {repr(actual_last)}")
            if not count_ok:
                print(f"FAIL: Component 3 — expected {EXPECTED_LINE_COUNT} lines, got {actual_count}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
