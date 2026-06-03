"""
Reward Script: Use the Outline view to navigate through this TypeScript class and find the 'updateUser' method.
Task ID: vscode_code_076
Domain: vs_code
Scoring:
  Component 1 (0.5): Cursor state file exists at /home/user/vscode_code_076_cursor_state.json
  Component 2 (0.3): The 'method' field in cursor state equals 'updateUser'
  Component 3 (0.2): The 'line' field points to the actual updateUser method in the TypeScript file
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_076'

CURSOR_STATE_PATH = f'{WORKDIR}/{TASK_ID}_cursor_state.json'
TS_FILE_PATH = f'{WORKDIR}/project/user-service.ts'


def find_updateUser_line(ts_path):
    """Return the 1-based line number of the 'updateUser' method definition in the TypeScript file."""
    try:
        with open(ts_path, 'r') as f:
            lines = f.readlines()
        for i, line in enumerate(lines, 1):
            # Match async method definition line
            if 'updateUser' in line and ('async' in line or 'updateUser(' in line):
                return i
        return None
    except Exception as e:
        print(f"ERROR: Could not read TypeScript file: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    The task requires navigation to the 'updateUser' method, evidenced by a cursor
    state JSON file written after using VSCode's Outline view.
    """
    total_score = 0.0

    # Component 1: Cursor state file exists (0.5 points)
    # This is the primary evidence that the agent navigated via the Outline view
    try:
        if os.path.exists(CURSOR_STATE_PATH):
            print(f"PASS: Component 1 — cursor state file exists at {CURSOR_STATE_PATH} (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — cursor state file NOT found at {CURSOR_STATE_PATH}")
            # No cursor state file at all; return early with 0.0
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load cursor state JSON for subsequent checks
    try:
        with open(CURSOR_STATE_PATH, 'r') as f:
            cursor_state = json.load(f)
    except Exception as e:
        print(f"ERROR: Cannot parse cursor state JSON at {CURSOR_STATE_PATH}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: The 'method' field equals 'updateUser' (0.3 points)
    try:
        method_value = cursor_state.get('method', None)
        if method_value == 'updateUser':
            print(f"PASS: Component 2 — cursor state method == 'updateUser' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — expected method='updateUser', found: {method_value!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The 'line' field points to the actual updateUser line in the TS file (0.2 points)
    try:
        recorded_line = cursor_state.get('line', None)
        actual_line = find_updateUser_line(TS_FILE_PATH)

        if actual_line is None:
            print(f"FAIL: Component 3 — could not locate 'updateUser' in {TS_FILE_PATH}")
        elif recorded_line is None:
            print(f"FAIL: Component 3 — 'line' field missing from cursor state")
        elif int(recorded_line) == actual_line:
            print(f"PASS: Component 3 — cursor state line={recorded_line} matches actual updateUser line={actual_line} (0.2 pts)")
            total_score += 0.2
        else:
            # Allow a tolerance of ±2 lines (method may start on a slightly different line)
            if abs(int(recorded_line) - actual_line) <= 2:
                print(f"PASS: Component 3 — cursor state line={recorded_line} is within ±2 of actual updateUser line={actual_line} (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — cursor state line={recorded_line} does not match actual updateUser line={actual_line}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
