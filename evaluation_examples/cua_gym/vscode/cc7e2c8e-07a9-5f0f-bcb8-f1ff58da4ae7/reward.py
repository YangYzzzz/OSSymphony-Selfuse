"""
Reward Script: Add 'export' before each of 5 function declarations in utilities.ts
Task ID: vscode_web_017
Domain: vscode
Scoring:
  - 5 components (0.2 each): verify each function line starts with 'export function'
  - Lines 10, 25, 40, 55, 70 in ~/projects/frontend/src/utils/utilities.ts
  - Only scores task-introduced changes (export keyword added)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_017'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'frontend', 'src', 'utils', 'utilities.ts')

# The 5 function names and their expected line numbers (1-indexed)
EXPECTED_EXPORTS = {
    10: 'formatCurrency',
    25: 'validateEmail',
    40: 'formatDate',
    55: 'debounce',
    70: 'deepClone',
}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be readable
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Verify each of the 5 export additions (0.2 points each)
    for line_num, func_name in EXPECTED_EXPORTS.items():
        component_label = f"Component (line {line_num}, {func_name})"
        try:
            if line_num > len(lines):
                print(f"FAIL: {component_label} -- file has only {len(lines)} lines")
                continue

            line_content = lines[line_num - 1]  # convert 1-indexed to 0-indexed
            stripped = line_content.lstrip()

            # Check that the line starts with 'export function <func_name>'
            expected_prefix = f"export function {func_name}"
            if stripped.startswith(expected_prefix):
                print(f"PASS: {component_label} -- line starts with 'export function {func_name}' (0.2 pts)")
                total_score += 0.2
            elif stripped.startswith(f"function {func_name}"):
                print(f"FAIL: {component_label} -- line still starts with 'function' (no export added)")
            else:
                print(f"FAIL: {component_label} -- unexpected content: {stripped[:60]}")
        except Exception as e:
            print(f"ERROR: {component_label} -- {e}")

    # Round to avoid floating point issues
    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
