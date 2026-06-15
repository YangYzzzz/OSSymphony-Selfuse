"""
Reward Script: Fix IndexError crash in expense tracker deletion logic
Task ID: osworld_multi_apps_vscode_debug_crash_003
Domain: multi_apps / vscode / python_debugging
Scoring:
  Component 1 (0.5 pts): The crash-causing line `self.expenses[0]` is removed from delete_expense
  Component 2 (0.3 pts): An empty-list guard (if not self.expenses) is added to delete_expense
  Component 3 (0.2 pts): Behavioral test — delete_expense on empty list returns False without IndexError
"""

import os
import re
import sys

WORKDIR = '/home/user/Desktop/expense_tracker'
TASK_ID = 'osworld_multi_apps_vscode_debug_crash_003'
TRACKER_PATH = os.path.join(WORKDIR, 'tracker.py')


def verify_task(tracker_path):
    """
    Verify that tracker.py has been fixed to handle empty-list deletion.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: tracker.py must exist
    if not os.path.isfile(tracker_path):
        print(f"CRITICAL: tracker.py not found at {tracker_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(tracker_path, 'r') as f:
            source = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read {tracker_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract just the delete_expense method body for targeted analysis.
    # We find the method by locating 'def delete_expense' and grabbing lines
    # until the next top-level method definition.
    try:
        lines = source.split('\n')
        delete_start = None
        delete_end = None
        for i, line in enumerate(lines):
            if re.match(r'\s+def delete_expense\s*\(', line):
                delete_start = i
            elif delete_start is not None and i > delete_start:
                # Next method definition at same indentation level ends the block
                if re.match(r'\s+def \w+\s*\(', line):
                    delete_end = i
                    break
        if delete_start is None:
            print("CRITICAL: delete_expense method not found in tracker.py")
            print("REWARD: 0.0")
            return 0.0
        if delete_end is None:
            delete_end = len(lines)
        delete_method_lines = lines[delete_start:delete_end]
        delete_method_source = '\n'.join(delete_method_lines)
        print(f"INFO: Found delete_expense method at line {delete_start + 1}, "
              f"spanning {delete_end - delete_start} lines")
    except Exception as e:
        print(f"ERROR: Could not extract delete_expense method: {e}")
        delete_method_source = source  # Fall back to full source

    # -------------------------------------------------------------------------
    # Component 1: The crash-causing line `self.expenses[0]` is removed (0.5 pts)
    # In the buggy initial version, the method contains:
    #   _ = self.expenses[0]  # <-- IndexError when list is empty
    # In the fixed version this line must NOT be present inside delete_expense.
    # -------------------------------------------------------------------------
    try:
        # Check for the pattern: accessing self.expenses[0] without a guard
        # The buggy pattern is an unconditional index access that ignores emptiness
        crash_pattern = re.search(
            r'self\.expenses\s*\[\s*0\s*\]',
            delete_method_source
        )
        if crash_pattern:
            print(f"FAIL: Component 1 — crash-causing `self.expenses[0]` "
                  f"still present in delete_expense (not fixed)")
        if not crash_pattern:
            print("PASS: Component 1 — crash-causing `self.expenses[0]` removed "
                  "from delete_expense (0.5 pts)")
            total_score += 0.5
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: An empty-list guard is added to delete_expense (0.3 pts)
    # The fix must include a check like:
    #   if not self.expenses:
    #       ...
    #       return False
    # or equivalent guard before the list is used.
    # -------------------------------------------------------------------------
    try:
        # Look for an empty-list guard in the method body.
        # Accept: `if not self.expenses`, `if len(self.expenses) == 0`,
        #         `if self.expenses == []`, or similar.
        guard_patterns = [
            r'if\s+not\s+self\.expenses',
            r'if\s+len\s*\(\s*self\.expenses\s*\)\s*==\s*0',
            r'if\s+len\s*\(\s*self\.expenses\s*\)\s*<\s*1',
            r'if\s+self\.expenses\s*==\s*\[\s*\]',
        ]
        guard_found = any(
            re.search(pat, delete_method_source)
            for pat in guard_patterns
        )
        if guard_found:
            print("PASS: Component 2 — empty-list guard found in delete_expense (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 2 — no empty-list guard detected in delete_expense; "
                  "expected `if not self.expenses:` or equivalent")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Behavioral test — delete on empty list returns False without crash (0.2 pts)
    # Import the fixed module and call delete_expense on an empty tracker.
    # This catches cases where the code looks structurally correct but still fails.
    # -------------------------------------------------------------------------
    try:
        # Insert WORKDIR into sys.path so we can import tracker.py
        if WORKDIR not in sys.path:
            sys.path.insert(0, WORKDIR)

        # Force reload to pick up the actual on-disk file (not a cached version)
        if 'tracker' in sys.modules:
            del sys.modules['tracker']
        if 'storage' in sys.modules:
            del sys.modules['storage']

        import tracker as tracker_module
        t = tracker_module.ExpenseTracker()
        # Force the expense list empty to test the boundary condition
        t.expenses = []
        try:
            result = t.delete_expense(999)
            # If we reach here with no exception, the fix is working
            if result is False:
                print(f"PASS: Component 3 — delete_expense(999) on empty list returned False "
                      f"without IndexError (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — delete_expense(999) on empty list returned "
                      f"{result!r} instead of False; unexpected return value")
        except IndexError as ie:
            print(f"FAIL: Component 3 — IndexError still raised on empty list: {ie}")
        except Exception as inner_e:
            print(f"FAIL: Component 3 — unexpected exception: "
                  f"{type(inner_e).__name__}: {inner_e}")
    except Exception as e:
        print(f"ERROR: Component 3 — could not import/run tracker module: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.1f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


verify_task(TRACKER_PATH)
