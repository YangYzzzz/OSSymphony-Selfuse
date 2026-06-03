"""
Reward Script: Use Python IntelliSense to explore DataFrame methods by typing 'df.'
Task ID: vscode_lp_041
Domain: vscode
Scoring:
  Component 1 (0.5): 'df.' expression exists in analysis.py after the DataFrame creation line
  Component 2 (0.3): 'df.' appears as a standalone expression (not a complete method call)
  Component 3 (0.2): 'df.' is positioned on line 11 (immediately after df = pd.read_csv(...))
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_041'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be readable
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            lines = content.split('\n')
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: file must still contain the DataFrame creation (not corrupted)
    if 'df = pd.read_csv' not in content:
        print("FAIL: Precondition — df = pd.read_csv(...) not found, file may be corrupted")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: 'df.' expression exists after DataFrame creation line (0.5 points)
    # The task asks the user to type 'df.' to trigger IntelliSense.
    # We check that 'df.' appears in the file AFTER the line containing df = pd.read_csv(...)
    try:
        df_creation_line_idx = None
        for i, line in enumerate(lines):
            if 'df = pd.read_csv' in line:
                df_creation_line_idx = i
                break

        if df_creation_line_idx is not None:
            # Look for 'df.' in lines after the DataFrame creation
            df_dot_after_creation = any(
                lines[i].strip().startswith('df.')
                for i in range(df_creation_line_idx + 1, len(lines))
            )

            if df_dot_after_creation:
                print(f"PASS: Component 1 — 'df.' found after DataFrame creation line (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 1 — 'df.' not found after DataFrame creation line")
        else:
            print(f"FAIL: Component 1 — DataFrame creation line not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'df.' appears as a standalone expression, not a complete method call (0.3 points)
    # This verifies the user typed 'df.' to trigger autocomplete suggestions, not a full method call.
    # A standalone 'df.' means the line is just 'df.' (possibly with whitespace), without
    # parentheses or a method name following it (like df.head() or df.describe()).
    try:
        standalone_df_dot = any(
            line.strip() == 'df.'
            for line in lines
        )

        if standalone_df_dot:
            print(f"PASS: Component 2 — 'df.' is standalone expression (autocomplete trigger) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — 'df.' not found as standalone expression")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'df.' appears on line 11 (immediately after df = pd.read_csv on line 10) (0.2 points)
    # This verifies correct cursor positioning as described in the task context.
    try:
        # Line 11 is index 10 (0-based)
        if len(lines) > 10:
            line_11 = lines[10].strip()
            if line_11 == 'df.':
                print(f"PASS: Component 3 — 'df.' on line 11 (correct position) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Line 11 is '{line_11}', expected 'df.'")
        else:
            print(f"FAIL: Component 3 — File has fewer than 11 lines")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/analysis.py'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
