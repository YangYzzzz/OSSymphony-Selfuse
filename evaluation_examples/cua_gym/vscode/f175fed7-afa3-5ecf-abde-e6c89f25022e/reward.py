"""
Reward Script: Add JSDoc block comments to fibonacci and factorial functions
Task ID: vscode_code_033
Domain: vs_code
Scoring:
  - Component 1: JSDoc block comment present for fibonacci function AND implementation unchanged (0.5 pts)
  - Component 2: JSDoc block comment present for factorial function AND implementation unchanged (0.5 pts)
  Total: 1.0

Note: "implementations unchanged" is a compound sub-condition within each JSDoc component,
not a standalone scoring component. Both checks must pass together to earn points.
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_033'

FILE_PATH = '/home/user/project/math.js'

# Expected original function implementations (unchanged after task)
EXPECTED_FIBONACCI_IMPL = "function fibonacci(n) {\n  if (n <= 1) return n;\n  return fibonacci(n - 1) + fibonacci(n - 2);\n}"
EXPECTED_FACTORIAL_IMPL = "function factorial(n) {\n  if (n <= 1) return 1;\n  return n * factorial(n - 1);\n}"


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Each component checks BOTH that a JSDoc comment was added AND that the function
    implementation is intact (compound check). This ensures initial_env scores 0.0
    since JSDoc comments are absent initially.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must be readable
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: JSDoc block comment present for fibonacci AND fibonacci implementation intact (0.5 points)
    # This fails on initial_env (no JSDoc comment) and passes on golden_env (JSDoc present + impl unchanged)
    try:
        fibonacci_jsdoc_pattern = re.compile(
            r'/\*\*[\s\S]*?\*/\s*\nfunction fibonacci',
            re.MULTILINE
        )
        fibonacci_jsdoc_found = bool(fibonacci_jsdoc_pattern.search(content))
        fibonacci_impl_intact = EXPECTED_FIBONACCI_IMPL in content

        if fibonacci_jsdoc_found and fibonacci_impl_intact:
            print(f"PASS: Component 1 - JSDoc comment added above fibonacci AND implementation unchanged (0.5 pts)")
            total_score += 0.5
        elif not fibonacci_jsdoc_found:
            print(f"FAIL: Component 1 - No JSDoc block comment (/** ... */) found before 'function fibonacci'")
        else:
            print(f"FAIL: Component 1 - JSDoc present but fibonacci implementation was altered")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: JSDoc block comment present for factorial AND factorial implementation intact (0.5 points)
    # This fails on initial_env (no JSDoc comment) and passes on golden_env (JSDoc present + impl unchanged)
    try:
        factorial_jsdoc_pattern = re.compile(
            r'/\*\*[\s\S]*?\*/\s*\nfunction factorial',
            re.MULTILINE
        )
        factorial_jsdoc_found = bool(factorial_jsdoc_pattern.search(content))
        factorial_impl_intact = EXPECTED_FACTORIAL_IMPL in content
        exports_intact = "module.exports = { fibonacci, factorial };" in content

        if factorial_jsdoc_found and factorial_impl_intact and exports_intact:
            print(f"PASS: Component 2 - JSDoc comment added above factorial AND implementation unchanged (0.5 pts)")
            total_score += 0.5
        elif not factorial_jsdoc_found:
            print(f"FAIL: Component 2 - No JSDoc block comment (/** ... */) found before 'function factorial'")
        elif not factorial_impl_intact:
            print(f"FAIL: Component 2 - JSDoc present but factorial implementation was altered")
        else:
            print(f"FAIL: Component 2 - JSDoc present but module.exports line was altered or missing")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
