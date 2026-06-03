"""
Reward Script: Fix indentation error in loop.py
Task ID: vscode_rdb_004
Domain: vs_code
Scoring:
  Component 1: print(i) is properly indented inside the for loop (0.5 pts)
  Component 2: Script is syntactically valid Python (parses without error) (0.2 pts)
  Component 3: Script produces correct output "1\\n2\\n3\\n4\\n5\\n" (0.3 pts)
"""

import os
import ast
import io
import sys

WORKDIR = '/home/user'
TASK_ID = 'vscode_rdb_004'

FILE_PATH = f'{WORKDIR}/projects/bugfix/loop.py'


def verify_task(file_path):
    """
    Verify that loop.py has been fixed:
      - print(i) must be indented inside the for loop
      - script must be syntactically valid
      - script must produce correct output: 1 through 5
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
            lines = content.splitlines()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: print(i) is properly indented inside the for loop (0.5 points)
    # In the initial (buggy) file, line 3 is "    print(i)" with 4 spaces (or 0 spaces relative to for).
    # In the fixed file, line 3 must be indented deeper than the for loop line.
    # The for loop is at 4-space indent; print(i) must be at 8-space indent.
    try:
        # Find the line containing 'print(i)'
        print_line = None
        for_line = None
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('for ') and 'range' in stripped:
                for_line = (idx, line)
            if stripped == 'print(i)':
                print_line = (idx, line)

        if print_line is None:
            print("FAIL: Component 1 — 'print(i)' line not found in file")
        elif for_line is None:
            print("FAIL: Component 1 — 'for' loop line not found in file")
        else:
            for_indent = len(for_line[1]) - len(for_line[1].lstrip())
            print_indent = len(print_line[1]) - len(print_line[1].lstrip())
            # The fix: print(i) must be indented MORE than the for line
            # (for is at 4 spaces inside def; print must be at 8 spaces)
            if print_indent > for_indent:
                print(f"PASS: Component 1 — print(i) indented at col {print_indent} "
                      f"(inside for loop at col {for_indent})")
                total_score += 0.5
            else:
                print(f"FAIL: Component 1 — print(i) at indent {print_indent}, "
                      f"for loop at indent {for_indent}; print must be indented deeper")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Script is syntactically valid Python (0.2 points)
    # The initial file has an IndentationError; the fixed file should parse cleanly.
    syntax_error_msg = None
    try:
        ast.parse(content)
    except SyntaxError as e:
        syntax_error_msg = str(e)
    except Exception as e:
        syntax_error_msg = str(e)

    if syntax_error_msg is None:
        print("PASS: Component 2 — script parses without syntax errors")
        total_score += 0.2
    else:
        print(f"FAIL: Component 2 — SyntaxError: {syntax_error_msg}")

    # Component 3: Script produces correct output "1\n2\n3\n4\n5\n" (0.3 points)
    # Use exec() in a sandboxed namespace and capture stdout.
    # Only attempt if the script is already syntactically valid (Component 2 passed).
    try:
        # Redirect stdout to capture output
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        exec_namespace = {}
        try:
            exec(compile(content, file_path, 'exec'), exec_namespace)
        finally:
            sys.stdout = old_stdout

        actual_output = captured.getvalue()
        expected_output = "1\n2\n3\n4\n5\n"

        if actual_output == expected_output:
            print(f"PASS: Component 3 — output is exactly '1\\n2\\n3\\n4\\n5\\n'")
            total_score += 0.3
        else:
            # Normalize: strip trailing newline and split for better diagnostics
            actual_stripped = actual_output.strip()
            expected_stripped = expected_output.strip()
            print(f"FAIL: Component 3 — expected output '1 2 3 4 5' (one per line), "
                  f"got: {repr(actual_output)}")
    except SyntaxError as e:
        print(f"FAIL: Component 3 — script has syntax error, cannot execute: {e}")
    except Exception as e:
        print(f"FAIL: Component 3 — execution error: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path in the VM env
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
