"""
Reward Script: Select lines 10-20 in data.json and use Find and Replace within selection to replace all 'null' values with '0'
Task ID: vscode_edit_068
Domain: vs_code
Scoring:
  Component 1 (0.6): All 5 null values in lines 10-20 are replaced with integer 0
                      (bonus, performance, certifications, end_date, notes on lines 11,14,15,18,19)
  Component 2 (0.4): The replacement is selective — the 5 changed values are 0 AND
                      the 7 null values outside lines 10-20 are still null
                      (manager, phone, emergency, linkedin, alt_email, termination, feedback)
                      This component captures both the change and its precision.

Note: Component 2 inherently FAILS on initial_env because the prerequisite (in-range nulls being 0)
      is not satisfied on initial_env. We verify it as a compound condition:
      "all 5 in-range are 0 AND all 7 outside-range are null" — fails on initial since in-range are null.
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_068'
FILE_PATH = os.path.join(WORKDIR, 'Desktop', 'data.json')

# Ground truth from task context:
# - 5 nulls within lines 10-20 must become 0: bonus(L11), performance(L14), certifications(L15), end_date(L18), notes(L19)
# - 7 nulls outside lines 10-20 must remain null: manager(L9), phone(L23), emergency(L27), linkedin(L33), alt_email(L38), termination(L43), feedback(L48)

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Checks that only the 5 null values within lines 10-20 were replaced with 0,
    while the 7 null values outside that range remain null.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: File must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: Must be valid JSON
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"CRITICAL: File is not valid JSON: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Read lines for line-number-based verification
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"CRITICAL: Cannot read file lines: {e}")
        print("REWARD: 0.0")
        return 0.0

    employees = data.get('employees', [])
    emp0 = employees[0] if len(employees) > 0 else {}
    emp1 = employees[1] if len(employees) > 1 else {}
    emp2 = employees[2] if len(employees) > 2 else {}

    # Component 1: All 5 null values in lines 10-20 are replaced with integer 0 (0.6 points)
    # The task requires replacing null->0 ONLY within lines 10-20 (1-indexed).
    # In the initial file, lines 11, 14, 15, 18, 19 within range had null values.
    # After the task, these should all be 0.
    try:
        # Keys that were null in lines 10-20 and should now be 0
        in_range_keys = ['bonus', 'performance', 'certifications', 'end_date', 'notes']
        keys_converted = 0

        for key in in_range_keys:
            val = emp0.get(key, 'MISSING')
            if val == 0:
                keys_converted += 1
                print(f"PASS: '{key}' (lines 10-20) is now 0 (was null)")
            elif val is None:
                print(f"FAIL: '{key}' (lines 10-20) is still null (expected 0)")
            else:
                print(f"FAIL: '{key}' (lines 10-20) has unexpected value: {val!r}")

        # Also verify via line-number check: no 'null' strings should appear in lines 10-20
        in_range_null_remaining = []
        for i in range(9, 20):  # lines 10-20 (0-indexed 9-19)
            if i < len(lines) and 'null' in lines[i]:
                in_range_null_remaining.append((i + 1, lines[i].strip()))

        if in_range_null_remaining:
            print(f"FAIL: Component 1 — {len(in_range_null_remaining)} null(s) remain in lines 10-20:")
            for lineno, content in in_range_null_remaining:
                print(f"  Line {lineno}: {content}")
        else:
            print("INFO: No 'null' strings remain in lines 10-20")

        if keys_converted == 5 and not in_range_null_remaining:
            print(f"PASS: Component 1 — All 5 in-range nulls replaced with 0 (0.6 pts)")
            total_score += 0.6
        elif keys_converted > 0:
            partial = round(keys_converted / 5 * 0.6, 2)
            print(f"PARTIAL: Component 1 — {keys_converted}/5 in-range nulls replaced ({partial} pts)")
            if partial > 0:
                total_score += partial
        else:
            print(f"FAIL: Component 1 — No in-range nulls replaced with 0 (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Selective replacement confirmed — in-range are 0 AND out-of-range remain null (0.4 points)
    # This compound check verifies both the task action AND its precision (no over-replacement).
    # It FAILS on initial_env because the in-range keys are still null (first sub-condition fails).
    # It PASSES on golden_env because in-range are 0 AND out-of-range remain null.
    try:
        # Sub-condition A: All 5 in-range are 0 (same check as component 1 — must pass first)
        in_range_all_zero = all(emp0.get(key) == 0 for key in ['bonus', 'performance', 'certifications', 'end_date', 'notes'])

        # Sub-condition B: All 7 out-of-range nulls remain null
        out_of_range_checks = [
            (emp0, 'manager', 'L9'),
            (emp1, 'phone', 'L23'),
            (emp1, 'emergency', 'L27'),
            (emp1, 'linkedin', 'L33'),
            (emp2, 'alt_email', 'L38'),
            (emp2, 'termination', 'L43'),
            (emp2, 'feedback', 'L48'),
        ]

        out_range_preserved = 0
        out_range_corrupted = []

        for emp_dict, key, lineno in out_of_range_checks:
            val = emp_dict.get(key, 'MISSING')
            if val is None:
                out_range_preserved += 1
                print(f"PASS: '{key}' ({lineno}) outside range remains null")
            elif val == 0:
                out_range_corrupted.append(key)
                print(f"FAIL: '{key}' ({lineno}) outside range was incorrectly changed to 0")
            else:
                print(f"FAIL: '{key}' ({lineno}) outside range has unexpected value: {val!r}")

        out_range_all_null = (out_range_preserved == 7 and not out_range_corrupted)

        if in_range_all_zero and out_range_all_null:
            print(f"PASS: Component 2 — Selective replacement confirmed: 5 in-range are 0, 7 out-of-range remain null (0.4 pts)")
            total_score += 0.4
        elif in_range_all_zero and out_range_preserved > 0:
            # Partial: in-range correct, some but not all out-of-range preserved
            partial = round(out_range_preserved / 7 * 0.4, 2)
            print(f"PARTIAL: Component 2 — In-range correct but {out_range_preserved}/7 out-of-range preserved ({partial} pts)")
            if partial > 0:
                total_score += partial
        else:
            # in_range_all_zero is False (initial env) OR no out-range preserved
            print(f"FAIL: Component 2 — Selective replacement not confirmed. in_range_all_zero={in_range_all_zero}, out_range_preserved={out_range_preserved}/7 (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
