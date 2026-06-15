"""
Reward Script: Use F2 to rename 'getData' function to 'fetchUserData' across the entire file.
Task ID: vscode_code_035
Domain: vs_code
Scoring:
  Component 1: Function declaration renamed (getData -> fetchUserData)   — 0.4 pts
  Component 2: Function call inside processUser renamed                  — 0.3 pts
  Component 3: Export object updated to use fetchUserData                — 0.3 pts
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_035'

FILE_PATH = '/home/user/project/api.js'


def verify_task(file_path):
    """
    Verify that 'getData' has been fully renamed to 'fetchUserData' in api.js.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be readable
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Function declaration renamed to 'fetchUserData' (0.4 points)
    # The declaration line should be "async function fetchUserData(userId)" not "async function getData(userId)"
    try:
        # Check for renamed function declaration
        decl_new = bool(re.search(r'\bfunction\s+fetchUserData\s*\(', content))
        decl_old = bool(re.search(r'\bfunction\s+getData\s*\(', content))

        if decl_new and not decl_old:
            print(f"PASS: Component 1 — function declaration renamed to 'fetchUserData' (0.4 pts)")
            total_score += 0.4
        elif decl_old and not decl_new:
            print(f"FAIL: Component 1 — function declaration still uses 'getData'")
        elif decl_new and decl_old:
            print(f"FAIL: Component 1 — both 'fetchUserData' and 'getData' declarations found (partial rename)")
        else:
            print(f"FAIL: Component 1 — neither 'fetchUserData' nor 'getData' function declaration found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Function call inside processUser updated to 'fetchUserData' (0.3 points)
    # The call "const data = await getData(id);" should become "const data = await fetchUserData(id);"
    try:
        call_new = bool(re.search(r'\bawait\s+fetchUserData\s*\(', content))
        call_old = bool(re.search(r'\bawait\s+getData\s*\(', content))

        if call_new and not call_old:
            print(f"PASS: Component 2 — function call updated to 'fetchUserData(id)' (0.3 pts)")
            total_score += 0.3
        elif call_old and not call_new:
            print(f"FAIL: Component 2 — function call still uses 'getData(id)'")
        elif call_new and call_old:
            print(f"FAIL: Component 2 — both 'fetchUserData' and 'getData' calls found")
        else:
            print(f"FAIL: Component 2 — neither 'fetchUserData' nor 'getData' await call found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Export object updated from 'getData' to 'fetchUserData' (0.3 points)
    # "module.exports = { getData, processUser };" should become "module.exports = { fetchUserData, processUser };"
    try:
        # Match module.exports line with fetchUserData
        export_new = bool(re.search(r'module\.exports\s*=\s*\{[^}]*\bfetchUserData\b[^}]*\}', content))
        export_old = bool(re.search(r'module\.exports\s*=\s*\{[^}]*\bgetData\b[^}]*\}', content))

        if export_new and not export_old:
            print(f"PASS: Component 3 — export updated to 'fetchUserData' (0.3 pts)")
            total_score += 0.3
        elif export_old and not export_new:
            print(f"FAIL: Component 3 — export still uses 'getData'")
        elif export_new and export_old:
            print(f"FAIL: Component 3 — both 'fetchUserData' and 'getData' found in exports")
        else:
            print(f"FAIL: Component 3 — no recognizable module.exports found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
