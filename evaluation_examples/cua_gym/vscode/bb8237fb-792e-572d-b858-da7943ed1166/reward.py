"""
Reward Script: Create sorting.py with proper Python template structure
Task ID: vscode_stu_042
Domain: vscode
Scoring:
  Component 1 (0.3) - File exists and contains import-related content
  Component 2 (0.35) - def main() function is defined
  Component 3 (0.35) - if __name__ == '__main__' guard block calls main()
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_042'
TARGET_FILE = os.path.join(WORKDIR, 'cs101', 'hw5', 'sorting.py')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: file must exist — if not, nothing to verify
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not content.strip():
        print("CRITICAL: File is empty")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Import section present (0.3 points)
    # The task requires an "import statements area". We check for actual import
    # statements OR an import section comment/marker.
    try:
        has_import_stmt = bool(re.search(r'^\s*import\s+\w+', content, re.MULTILINE))
        has_from_import = bool(re.search(r'^\s*from\s+\w+\s+import', content, re.MULTILINE))
        has_import_comment = bool(re.search(r'#.*[Ii]mport', content))
        if has_import_stmt or has_from_import or has_import_comment:
            print(f"PASS: Component 1 — Import section found (import_stmt={has_import_stmt}, from_import={has_from_import}, comment={has_import_comment}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No import statements or import section marker found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: def main() function defined (0.35 points)
    # The task requires a "main function"
    try:
        has_main_def = bool(re.search(r'^\s*def\s+main\s*\(', content, re.MULTILINE))
        if has_main_def:
            print(f"PASS: Component 2 — def main() function found (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — No def main() function found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: if __name__ == '__main__' guard that calls main() (0.35 points)
    # The task requires an "if __name__ == '__main__' block"
    try:
        # Check for the guard pattern (allowing single or double quotes)
        has_name_guard = bool(re.search(
            r'''^\s*if\s+__name__\s*==\s*['"]__main__['"]\s*:''',
            content, re.MULTILINE
        ))
        # Check that main() is called somewhere after the guard
        has_main_call = bool(re.search(
            r'''if\s+__name__\s*==\s*['"]__main__['"]\s*:.*?main\s*\(''',
            content, re.DOTALL
        ))
        if has_name_guard and has_main_call:
            print(f"PASS: Component 3 — if __name__ == '__main__': main() guard found (0.35 pts)")
            total_score += 0.35
        elif has_name_guard:
            print(f"PARTIAL: Component 3 — Guard found but main() not called in block (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — No if __name__ == '__main__' guard found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
if not os.path.exists(TARGET_FILE):
    print(f"File not found: {TARGET_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(TARGET_FILE)
