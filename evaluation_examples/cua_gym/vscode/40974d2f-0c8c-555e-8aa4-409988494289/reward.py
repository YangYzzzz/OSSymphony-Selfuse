"""
Reward Script: Copy relative path of Header.tsx and paste import in App.tsx
Task ID: vscode_lp_065
Domain: vscode
Scoring:
  - Component 1 (0.3): TODO comment placeholder removed
  - Component 2 (0.5): Valid import statement for Header from relative path
  - Component 3 (0.2): Import path correctly references './components/Header'
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_065'
APP_TSX_PATH = os.path.join(WORKDIR, 'workspace', 'src', 'App.tsx')


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
        lines = content.strip().split('\n')
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: TODO comment placeholder is removed (0.3 points)
    # Initial has: // TODO: import Header from its relative path
    # Golden should NOT have this line
    try:
        has_todo_comment = any(
            '// TODO:' in line and 'import' in line.lower() and 'header' in line.lower()
            for line in lines
        )
        if not has_todo_comment:
            print(f"PASS: Component 1 -- TODO comment placeholder removed (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 -- TODO comment placeholder still present")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Valid import statement for Header exists (0.5 points)
    # Must have a line like: import Header from './components/Header'
    # or: import Header from "./components/Header"
    # Accept with or without file extension
    try:
        import_pattern = re.compile(
            r"""^import\s+Header\s+from\s+['"](\./components/Header(?:\.tsx)?)['"]\s*;?\s*$"""
        )
        matching_lines = [line.strip() for line in lines if import_pattern.match(line.strip())]
        if matching_lines:
            print(f"PASS: Component 2 -- Header import statement found: '{matching_lines[0]}' (0.5 pts)")
            total_score += 0.5
        else:
            # Check for any Header import (maybe different path format)
            any_header_import = [
                line.strip() for line in lines
                if re.match(r"^import\s+Header\s+from\s+['\"]", line.strip())
            ]
            if any_header_import:
                print(f"FAIL: Component 2 -- Header import found but path may be wrong: '{any_header_import[0]}'")
            else:
                print(f"FAIL: Component 2 -- No Header import statement found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Import path is specifically './components/Header' (0.2 points)
    # This checks the exact relative path matches what 'Copy Relative Path' would produce
    try:
        exact_path_pattern = re.compile(
            r"""^import\s+Header\s+from\s+['"]\.\/components\/Header['"]\s*;?\s*$"""
        )
        exact_matches = [line.strip() for line in lines if exact_path_pattern.match(line.strip())]
        if exact_matches:
            print(f"PASS: Component 3 -- Exact relative path './components/Header' used (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 -- Path is not exactly './components/Header'")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(APP_TSX_PATH):
    print(f"File not found: {APP_TSX_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(APP_TSX_PATH)
