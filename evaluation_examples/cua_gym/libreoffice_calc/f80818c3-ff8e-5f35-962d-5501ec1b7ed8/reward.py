"""
Reward Script: Implement quickSort in quicksort.py and save output to qs_output.txt
Task ID: osworld_multi_apps_misc_037
Domain: os / multi-apps
Scoring:
  Component 1: quicksort.py contains a real implementation (not stub/pass) — 0.35 pts
  Component 2: qs_output.txt exists on Desktop with output lines — 0.30 pts
  Component 3: qs_output.txt contains correctly sorted results for all 5 test cases — 0.35 pts
Total: 1.0
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_misc_037'

# Expected sorted arrays (from test cases in quicksort.py)
EXPECTED_OUTPUTS = [
    "Sorted array 1: [1, 5, 7, 8, 9, 10]",
    "Sorted array 2: [11, 12, 22, 25, 34, 64, 90]",
    "Sorted array 3: [1, 1, 2, 3, 6, 8, 10]",
    "Sorted array 4: [1]",
    "Sorted array 5: [1, 2, 3, 4, 5]",
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    quicksort_path = os.path.join(WORKDIR, 'quicksort.py')
    qs_output_path = os.path.join(WORKDIR, 'qs_output.txt')

    # Precondition gate: quicksort.py must exist
    if not os.path.isfile(quicksort_path):
        print(f"CRITICAL: quicksort.py not found at {quicksort_path}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: quicksort.py has a real implementation (not just pass/stub) (0.35 pts)
    # The initial file has both partition() and quickSort() returning 'pass'.
    # A real implementation will have actual logic (no bare 'pass' as the body).
    try:
        with open(quicksort_path, 'r') as f:
            quicksort_content = f.read()

        # Check partition function is implemented (not just 'pass')
        # A real Lomuto partition should assign a pivot and return an index
        has_pivot = 'pivot' in quicksort_content or 'arr[high]' in quicksort_content
        # quickSort must have actual logic beyond 'pass'
        # Split function bodies — partition body and quickSort body should have logic
        lines = [line.strip() for line in quicksort_content.splitlines()]
        # Count non-empty, non-comment, non-pass, non-docstring lines after function defs
        real_code_lines = [
            l for l in lines
            if l and not l.startswith('#') and not l.startswith('"""') and not l.startswith("'")
            and l not in ('pass', 'def partition(arr, low, high):', 'def quickSort(arr, low, high):')
            and not l.startswith('def ') and not l.startswith('if __name__')
            and not l.startswith('test') and not l.startswith('print') and not l.startswith('quick')
        ]
        partition_implemented = has_pivot and any('return' in l for l in lines)
        quicksort_implemented = any('if low < high' in l or 'if low<high' in l or 'pi' in l
                                    for l in lines)

        if partition_implemented and quicksort_implemented:
            print(f"PASS: Component 1 — quicksort.py contains real implementation "
                  f"(partition has pivot logic and return, quickSort has recursive structure) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — quicksort.py does not appear to have a complete implementation. "
                  f"partition_implemented={partition_implemented}, quicksort_implemented={quicksort_implemented}")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not read quicksort.py: {e}")

    # Component 2: qs_output.txt exists with output content (0.30 pts)
    # This file did NOT exist in the initial environment, so its existence is task-introduced.
    try:
        if not os.path.isfile(qs_output_path):
            print(f"FAIL: Component 2 — qs_output.txt not found at {qs_output_path}")
        else:
            with open(qs_output_path, 'r') as f:
                output_content = f.read().strip()
            output_lines = [l.strip() for l in output_content.splitlines() if l.strip()]
            if len(output_lines) >= 5:
                print(f"PASS: Component 2 — qs_output.txt exists with {len(output_lines)} output lines (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 — qs_output.txt exists but has only {len(output_lines)} lines "
                      f"(expected at least 5 output lines)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: qs_output.txt contains correctly sorted results for all 5 test cases (0.35 pts)
    # Expected outputs per the test cases in quicksort.py:
    #   Sorted array 1: [1, 5, 7, 8, 9, 10]
    #   Sorted array 2: [11, 12, 22, 25, 34, 64, 90]
    #   Sorted array 3: [1, 1, 2, 3, 6, 8, 10]
    #   Sorted array 4: [1]
    #   Sorted array 5: [1, 2, 3, 4, 5]
    try:
        if not os.path.isfile(qs_output_path):
            print(f"FAIL: Component 3 — qs_output.txt not found, cannot check correct sorted output")
        else:
            with open(qs_output_path, 'r') as f:
                output_content = f.read()

            matched = 0
            for expected_line in EXPECTED_OUTPUTS:
                if expected_line in output_content:
                    matched += 1
                else:
                    print(f"FAIL Component 3 — Missing expected line: {expected_line!r}")

            if matched == len(EXPECTED_OUTPUTS):
                print(f"PASS: Component 3 — qs_output.txt contains all {len(EXPECTED_OUTPUTS)} "
                      f"correctly sorted results (0.35 pts)")
                total_score += 0.35
            elif matched > 0:
                partial = round(0.35 * matched / len(EXPECTED_OUTPUTS), 4)
                print(f"PARTIAL: Component 3 — {matched}/{len(EXPECTED_OUTPUTS)} correct sorted results found ({partial} pts)")
                if matched > 0:
                    total_score += partial
            else:
                print(f"FAIL: Component 3 — No correctly sorted results found in qs_output.txt")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
