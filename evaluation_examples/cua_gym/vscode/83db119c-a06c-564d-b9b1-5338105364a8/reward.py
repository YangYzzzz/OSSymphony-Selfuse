"""
Reward Script: Add #region and #endregion markers in TypeScript file to organize code into logical sections
Task ID: vscode_code_027
Domain: vs_code
Scoring:
  - Component 1: // #region Imports and // #endregion present (0.3 pts)
  - Component 2: // #region Interfaces and // #endregion present (0.2 pts)
  - Component 3: // #region User Functions and // #endregion present (0.2 pts)
  - Component 4: // #region Product Functions and // #endregion present (0.2 pts)
  - Component 5: // #region Exports and // #endregion present (0.1 pts)
  Total: 1.0

Note: The "fold all regions" part of the task is a VSCode editor state that is not
persisted to disk files. Verification is based on the file content changes (region markers).
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_027'
FILE_PATH = '/home/user/project/api.ts'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Checks that all required #region/#endregion markers were added to api.ts.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load file -- if missing, fail immediately
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    lines = content.split('\n')

    # Component 1: // #region Imports section (0.3 points)
    # Verify that the file has "// #region Imports" AND "// #endregion" markers
    try:
        has_imports_region_open = any(
            re.match(r'^\s*//\s*#region\s+Imports\s*$', line) for line in lines
        )
        # There should be at least one #endregion marker in the file
        has_endregion = any(
            re.match(r'^\s*//\s*#endregion\s*$', line) for line in lines
        )

        if has_imports_region_open and has_endregion:
            print("PASS: Component 1 -- '// #region Imports' marker found with corresponding '// #endregion' (0.3 pts)")
            total_score += 0.3
        else:
            if not has_imports_region_open:
                print("FAIL: Component 1 -- '// #region Imports' marker not found in file")
            else:
                print("FAIL: Component 1 -- '// #endregion' marker not found in file")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: // #region Interfaces section (0.2 points)
    # Verify that "// #region Interfaces" is present to wrap the interface definitions.
    try:
        has_interfaces_region = any(
            re.match(r'^\s*//\s*#region\s+Interfaces\s*$', line) for line in lines
        )

        if has_interfaces_region:
            print("PASS: Component 2 -- '// #region Interfaces' marker found (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 2 -- '// #region Interfaces' marker not found in file")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: // #region User Functions section (0.2 points)
    # Verify that "// #region User Functions" is present to wrap getUsers and getUserById.
    try:
        has_user_functions_region = any(
            re.match(r'^\s*//\s*#region\s+User Functions\s*$', line) for line in lines
        )

        if has_user_functions_region:
            print("PASS: Component 3 -- '// #region User Functions' marker found (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 3 -- '// #region User Functions' marker not found in file")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: // #region Product Functions section (0.2 points)
    # Verify that "// #region Product Functions" is present to wrap getProducts and getProductById.
    try:
        has_product_functions_region = any(
            re.match(r'^\s*//\s*#region\s+Product Functions\s*$', line) for line in lines
        )

        if has_product_functions_region:
            print("PASS: Component 4 -- '// #region Product Functions' marker found (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 4 -- '// #region Product Functions' marker not found in file")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: // #region Exports section (0.1 points)
    # Verify that "// #region Exports" is present to wrap the export statement.
    try:
        has_exports_region = any(
            re.match(r'^\s*//\s*#region\s+Exports\s*$', line) for line in lines
        )

        if has_exports_region:
            print("PASS: Component 5 -- '// #region Exports' marker found (0.1 pts)")
            total_score += 0.1
        else:
            print("FAIL: Component 5 -- '// #region Exports' marker not found in file")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {round(total_score, 2)}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification against canonical path on VM
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
