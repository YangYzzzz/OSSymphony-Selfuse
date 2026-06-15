"""
Reward Script: Create hello.py with a Python function that prints 'Hello, World!' and run it
Task ID: vscode_wf_003
Domain: vscode
Scoring:
  Component 1 (0.3) - hello.py contains a Python function definition
  Component 2 (0.4) - The function prints 'Hello, World!' (verified by running the file)
  Component 3 (0.3) - File has an if __name__ == '__main__' entry point that invokes the function
"""

import os
import re
import ast
import sys
import io

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_003'
FILE_PATH = os.path.join(WORKDIR, 'project', 'hello.py')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: file must exist and be readable
    if not os.path.isfile(FILE_PATH):
        print(f"CRITICAL: File not found: {FILE_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(FILE_PATH, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {FILE_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not content.strip():
        print("CRITICAL: File is empty")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: hello.py contains a Python function definition (0.3 points)
    # We check that the file has at least one 'def' statement using AST parsing
    try:
        tree = ast.parse(content)
        func_defs = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        if len(func_defs) > 0:
            func_names = [f.name for f in func_defs]
            print(f"PASS: Component 1 -- Found function definition(s): {func_names} (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 1 -- No function definitions found in hello.py")
    except SyntaxError as e:
        print(f"FAIL: Component 1 -- hello.py has syntax errors: {e}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Running the file produces 'Hello, World!' output (0.4 points)
    # We execute the file and capture stdout to verify the print output
    try:
        old_stdout = sys.stdout
        captured = io.StringIO()
        sys.stdout = captured

        # Execute the file content in an isolated namespace
        exec_globals = {'__name__': '__main__', '__file__': FILE_PATH}
        exec(compile(content, FILE_PATH, 'exec'), exec_globals)

        sys.stdout = old_stdout
        output = captured.getvalue().strip()

        if 'Hello, World!' in output:
            print(f"PASS: Component 2 -- File execution produced 'Hello, World!' (output: {repr(output)}) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 -- Expected 'Hello, World!' in output, got: {repr(output)}")
    except Exception as e:
        sys.stdout = old_stdout
        print(f"ERROR: Component 2 -- Execution failed: {e}")

    # Component 3: File has if __name__ == '__main__' entry point (0.3 points)
    # This verifies the file is structured to be runnable as a script
    try:
        # Search AST for if __name__ == '__main__' pattern
        main_blocks = [
            node for node in ast.walk(tree)
            if isinstance(node, ast.If)
            and isinstance(node.test, ast.Compare)
            and isinstance(node.test.left, ast.Name)
            and node.test.left.id == '__name__'
            and any(
                isinstance(c, ast.Constant) and c.value == '__main__'
                for c in node.test.comparators
            )
        ]

        if len(main_blocks) > 0:
            print(f"PASS: Component 3 -- Found if __name__ == '__main__' entry point (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 3 -- No if __name__ == '__main__' block found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
