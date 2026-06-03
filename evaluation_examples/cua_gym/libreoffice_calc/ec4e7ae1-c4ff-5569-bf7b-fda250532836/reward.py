"""
Reward Script: Implement mergeSort function and save output to result.txt
Task ID: osworld_multi_apps_misc_033
Domain: os / python coding
Scoring:
  - Component 1 (0.3): result.txt exists on the Desktop
  - Component 2 (0.3): result.txt contains all 7 PASS lines (no FAIL entries)
  - Component 3 (0.2): result.txt contains "All test cases passed!" summary line
  - Component 4 (0.2): mergeSort.py has a real implementation (not just pass/stub)
"""

import os
import re

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_misc_033'

RESULT_PATH = f'{WORKDIR}/result.txt'
MERGE_SORT_PATH = f'{WORKDIR}/mergeSort.py'

# Expected test case descriptions from the test suite
EXPECTED_TEST_DESCRIPTIONS = [
    "Example from tutorial",
    "Already sorted list",
    "Reverse sorted list",
    "Single element",
    "Empty list",
    "List with duplicates",
    "Two elements",
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: result.txt exists on the Desktop (0.3 points)
    # This FAILS on initial (no result.txt) and PASSES on golden
    try:
        if os.path.isfile(RESULT_PATH):
            print(f"PASS: Component 1 — result.txt exists at {RESULT_PATH} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — result.txt not found at {RESULT_PATH}")
            # Without result.txt, remaining components cannot pass; return early
            final_score = min(total_score, 1.0)
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {final_score}")
            return final_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Read result.txt content for components 2 & 3
    try:
        with open(RESULT_PATH, 'r') as f:
            result_content = f.read()
        print(f"INFO: result.txt content preview: {result_content[:200]!r}")
    except Exception as e:
        print(f"ERROR: Cannot read result.txt: {e}")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: result.txt contains all 7 PASS lines, no FAIL lines (0.3 points)
    # The test runner outputs "[PASS] ..." or "[FAIL] ..." for each test case
    try:
        pass_lines = [line for line in result_content.split('\n') if line.strip().startswith('[PASS]')]
        fail_lines = [line for line in result_content.split('\n') if line.strip().startswith('[FAIL]')]

        num_pass = len(pass_lines)
        num_fail = len(fail_lines)

        if num_pass >= 7 and num_fail == 0:
            print(f"PASS: Component 2 — All 7 test cases show PASS, 0 FAILs in result.txt (0.3 pts)")
            total_score += 0.3
        elif num_pass > 0 and num_fail == 0:
            print(f"FAIL: Component 2 — Only {num_pass}/7 PASS entries found, no FAILs")
        elif num_fail > 0:
            print(f"FAIL: Component 2 — {num_fail} FAIL entries found in result.txt: {fail_lines}")
        else:
            print(f"FAIL: Component 2 — No [PASS] entries found in result.txt")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: result.txt contains "All test cases passed!" summary (0.2 points)
    try:
        if "All test cases passed!" in result_content:
            print(f"PASS: Component 3 — 'All test cases passed!' summary found in result.txt (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — 'All test cases passed!' summary NOT found in result.txt")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: mergeSort.py has a real implementation, not just a stub (0.2 points)
    # The initial file only has "pass" in the mergeSort function body.
    # A real implementation must contain algorithmic keywords: return, mid, left, right,
    # or equivalent logic indicating a working merge sort.
    try:
        if not os.path.isfile(MERGE_SORT_PATH):
            print(f"FAIL: Component 4 — mergeSort.py not found at {MERGE_SORT_PATH}")
        else:
            with open(MERGE_SORT_PATH, 'r') as f:
                py_content = f.read()

            # Extract just the mergeSort function body
            # Look for the function definition and check it has substantive code beyond "pass"
            func_match = re.search(
                r'def mergeSort\(arr\):.*?(?=\ndef |\Z)',
                py_content,
                re.DOTALL
            )

            if func_match:
                func_body = func_match.group(0)
                # The stub only has "pass"; a real implementation has return statements
                # and references to arr slicing / merging logic
                has_return = 'return' in func_body
                # Check it's not just the stub (stub has only "pass" as logic)
                lines_in_body = [
                    l.strip() for l in func_body.split('\n')
                    if l.strip() and not l.strip().startswith('#') and not l.strip().startswith('"""') and l.strip() != '"""'
                ]
                # Filter out docstring lines
                code_lines = [l for l in lines_in_body if not l.startswith('Sort') and
                              not l.startswith('Args') and not l.startswith('arr') and
                              not l.startswith('Returns') and not l.startswith('list') and
                              not l.startswith('TODO') and not l.startswith('Hint') and
                              l not in ('pass',)]

                is_stub = func_body.strip().endswith('pass') and not has_return

                if has_return and len(code_lines) >= 3:
                    print(f"PASS: Component 4 — mergeSort function has real implementation "
                          f"({len(code_lines)} non-trivial code lines, has return) (0.2 pts)")
                    total_score += 0.2
                elif is_stub:
                    print(f"FAIL: Component 4 — mergeSort function only contains 'pass' (stub not implemented)")
                else:
                    print(f"FAIL: Component 4 — mergeSort function appears incomplete "
                          f"(has_return={has_return}, code_lines={len(code_lines)})")
            else:
                print(f"FAIL: Component 4 — Could not find mergeSort function definition in mergeSort.py")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task()
