"""
Reward Script: Complete budget_tracker.py and run it to produce budget_summary.txt
Task ID: osworld_multi_apps_vscode_run_capture_012
Domain: multi_apps (VSCode + OS file system)
Scoring:
  Component 1 (0.3 pts): budget_summary.txt exists on Desktop
  Component 2 (0.4 pts): budget_summary.txt contains correct numeric values
                          (Total Income $3870.00, Total Expenses $1860.50, Net Balance $2009.50)
  Component 3 (0.3 pts): budget_tracker.py has a complete implementation
                          (no TODO stubs, has actual computation logic)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_run_capture_012'

DESKTOP = os.path.join(WORKDIR, 'Desktop')
SUMMARY_FILE = os.path.join(DESKTOP, 'budget_summary.txt')
TRACKER_FILE = os.path.join(DESKTOP, 'budget_tracker.py')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: budget_summary.txt exists on Desktop (0.3 points)
    # This is a task-introduced change: the file does NOT exist in initial_env
    try:
        if os.path.isfile(SUMMARY_FILE):
            print(f"PASS: Component 1 — budget_summary.txt exists at {SUMMARY_FILE} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — budget_summary.txt not found at {SUMMARY_FILE}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: budget_summary.txt contains correct numeric values (0.4 points)
    # Expected values from running the completed script against transactions.csv:
    #   Total Income:    $3870.00
    #   Total Expenses:  $1860.50
    #   Net Balance:     $2009.50
    try:
        if os.path.isfile(SUMMARY_FILE):
            with open(SUMMARY_FILE, 'r') as f:
                content = f.read()

            expected_lines = [
                'Total Income:    $3870.00',
                'Total Expenses:  $1860.50',
                'Net Balance:     $2009.50',
            ]

            all_present = all(line in content for line in expected_lines)
            if all_present:
                print(f"PASS: Component 2 — budget_summary.txt contains correct values "
                      f"(Income=$3870.00, Expenses=$1860.50, Balance=$2009.50) (0.4 pts)")
                total_score += 0.4
            else:
                missing = [line for line in expected_lines if line not in content]
                print(f"FAIL: Component 2 — budget_summary.txt missing expected lines: {missing}")
                print(f"  Actual content: {repr(content)}")
        else:
            print(f"FAIL: Component 2 — cannot check values, budget_summary.txt not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: budget_tracker.py has complete implementation (0.3 points)
    # In initial_env, compute_summary has TODO stubs with no loop and hardcoded net_balance=0.0
    # In golden_env, compute_summary has actual iteration logic and print_summary is implemented
    # We check that the TODO stubs have been replaced with actual code:
    # - no "# TODO:" comments remain in the logic sections
    # - the compute_summary function actually iterates (contains a for loop over transactions)
    # - print_summary builds the output lines
    try:
        if os.path.isfile(TRACKER_FILE):
            with open(TRACKER_FILE, 'r') as f:
                tracker_content = f.read()

            # Check 1: No TODO stubs remaining (indicates completion)
            has_todo_stubs = '# TODO:' in tracker_content

            # Check 2: compute_summary contains iteration over transactions with type check
            has_income_check = (
                'transaction["type"] == "income"' in tracker_content or
                "transaction['type'] == 'income'" in tracker_content or
                '"income"' in tracker_content
            )
            has_expense_check = (
                'transaction["type"] == "expense"' in tracker_content or
                "transaction['type'] == 'expense'" in tracker_content or
                '"expense"' in tracker_content
            )
            has_loop = 'for transaction in transactions' in tracker_content

            # Check 3: print_summary writes to OUTPUT_FILE (the function is actually implemented)
            has_file_write = 'open(OUTPUT_FILE' in tracker_content or "open(OUTPUT_FILE" in tracker_content

            implementation_complete = (
                not has_todo_stubs and
                has_income_check and
                has_expense_check and
                has_loop and
                has_file_write
            )

            if implementation_complete:
                print(f"PASS: Component 3 — budget_tracker.py has complete implementation "
                      f"(no TODOs, has loop and type checks, writes to file) (0.3 pts)")
                total_score += 0.3
            else:
                reasons = []
                if has_todo_stubs:
                    reasons.append("TODO stubs still present")
                if not has_income_check:
                    reasons.append("missing income type check")
                if not has_expense_check:
                    reasons.append("missing expense type check")
                if not has_loop:
                    reasons.append("missing for-loop over transactions")
                if not has_file_write:
                    reasons.append("print_summary does not write to OUTPUT_FILE")
                print(f"FAIL: Component 3 — budget_tracker.py incomplete: {', '.join(reasons)}")
        else:
            print(f"FAIL: Component 3 — budget_tracker.py not found at {TRACKER_FILE}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.1f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
