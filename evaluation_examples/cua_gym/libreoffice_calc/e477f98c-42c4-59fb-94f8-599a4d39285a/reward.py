"""
Reward Script: Implement LinkedList methods and save output to ll_result.txt
Task ID: osworld_multi_apps_misc_035
Domain: multi_apps (os + python scripting)
Scoring:
  Component 1: ll_result.txt exists on Desktop (0.3 points)
  Component 2: ll_result.txt has correct content (0.4 points)
  Component 3: linked_list.py has non-stub implementations for append/delete/reverse (0.3 points)
"""

import os
import re

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_misc_035'

# Expected output lines from running linked_list.py with test cases
EXPECTED_OUTPUT_LINES = [
    "After appending 1, 2, 3, 4, 5:",
    "1 -> 2 -> 3 -> 4 -> 5 -> None",
    "After deleting 3:",
    "1 -> 2 -> 4 -> 5 -> None",
    "After reversing:",
    "5 -> 4 -> 2 -> 1 -> None",
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    ll_result_path = os.path.join(WORKDIR, 'll_result.txt')
    linked_list_path = os.path.join(WORKDIR, 'linked_list.py')

    # Component 1: ll_result.txt exists on Desktop (0.3 points)
    # This file does NOT exist in initial_env — it must be created by running the script
    try:
        if os.path.isfile(ll_result_path):
            print(f"PASS: Component 1 — ll_result.txt exists at {ll_result_path} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — ll_result.txt not found at {ll_result_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: ll_result.txt has correct content (0.4 points)
    # The content must match expected output from running the linked list test cases
    try:
        with open(ll_result_path, 'r') as f:
            content = f.read()

        # Check all expected lines are present in the output
        missing_lines = []
        for expected_line in EXPECTED_OUTPUT_LINES:
            if expected_line not in content:
                missing_lines.append(expected_line)

        if not missing_lines:
            print(f"PASS: Component 2 — ll_result.txt contains all expected output lines (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — ll_result.txt missing expected lines: {missing_lines}")
            print(f"  Actual content: {repr(content)}")
    except FileNotFoundError:
        print(f"FAIL: Component 2 — ll_result.txt not found, cannot check content")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: linked_list.py has non-stub implementations for append, delete, reverse (0.3 points)
    # In the initial_env, all three methods have only 'pass' as their body
    # In golden_env, actual implementations replace the stubs
    try:
        with open(linked_list_path, 'r') as f:
            py_content = f.read()

        # Check that none of the three stub method bodies are present
        # A stub looks like: method def followed by comments/hints and then just 'pass'
        # We detect this by checking if all three methods have real implementation
        # (i.e., each method body has more than just 'pass')

        # Parse each method section: find def append/delete/reverse and check body
        def method_is_implemented(source, method_name):
            """Returns True if the method has a non-pass body."""
            # Find the method definition
            pattern = rf'def {method_name}\s*\(self[^)]*\):\s*\n(.*?)(?=\n    def |\nclass |\Z)'
            match = re.search(pattern, source, re.DOTALL)
            if not match:
                return False
            body = match.group(1)
            # Remove comment lines and blank lines
            non_comment_lines = [
                line.strip() for line in body.split('\n')
                if line.strip() and not line.strip().startswith('#')
            ]
            # If the only non-comment line is 'pass', it's a stub
            if non_comment_lines == ['pass'] or non_comment_lines == []:
                return False
            return True

        append_impl = method_is_implemented(py_content, 'append')
        delete_impl = method_is_implemented(py_content, 'delete')
        reverse_impl = method_is_implemented(py_content, 'reverse')

        print(f"  append implemented: {append_impl}")
        print(f"  delete implemented: {delete_impl}")
        print(f"  reverse implemented: {reverse_impl}")

        if append_impl and delete_impl and reverse_impl:
            print(f"PASS: Component 3 — All three methods (append, delete, reverse) are implemented (0.3 pts)")
            total_score += 0.3
        else:
            not_impl = [m for m, v in [('append', append_impl), ('delete', delete_impl), ('reverse', reverse_impl)] if not v]
            print(f"FAIL: Component 3 — Methods still stub (pass-only): {not_impl}")
    except FileNotFoundError:
        print(f"FAIL: Component 3 — linked_list.py not found at {linked_list_path}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
