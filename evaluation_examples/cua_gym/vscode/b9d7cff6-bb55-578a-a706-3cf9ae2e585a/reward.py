"""
Reward Script: Rename helpers.js to stringUtils.js and update all import paths
Task ID: vscode_rrt_047
Domain: vscode
Scoring:
  Component 1 (0.30): File renamed — helpers.js removed, stringUtils.js exists
  Component 2 (0.25): app.js import updated to stringUtils
  Component 3 (0.25): formatter.js import updated to stringUtils
  Component 4 (0.20): helpers.test.js import updated to stringUtils
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_047'
PROJECT_DIR = os.path.join(WORKDIR, 'projects')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: File renamed (0.3 points)
    # helpers.js must NOT exist AND stringUtils.js must exist under lib/
    try:
        old_path = os.path.join(PROJECT_DIR, 'lib', 'helpers.js')
        new_path = os.path.join(PROJECT_DIR, 'lib', 'stringUtils.js')
        old_gone = not os.path.exists(old_path)
        new_exists = os.path.exists(new_path)
        if old_gone and new_exists:
            print(f"PASS: Component 1 - helpers.js removed and stringUtils.js exists (0.3 pts)")
            total_score += 0.3
        elif new_exists and not old_gone:
            # File was copied but not removed — partial credit
            print(f"FAIL: Component 1 - stringUtils.js exists but helpers.js still present")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 - old_gone={old_gone}, new_exists={new_exists}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: app.js import updated to stringUtils (0.25 points)
    try:
        app_path = os.path.join(PROJECT_DIR, 'src', 'app.js')
        with open(app_path, 'r') as f:
            content = f.read()
        # Check that it imports from stringUtils (not helpers)
        has_new_import = bool(re.search(r"require\(\s*['\"]\.\.\/lib\/stringUtils['\"]", content))
        has_old_import = bool(re.search(r"require\(\s*['\"]\.\.\/lib\/helpers['\"]", content))
        if has_new_import and not has_old_import:
            print(f"PASS: Component 2 - app.js imports from ../lib/stringUtils (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 - has_new_import={has_new_import}, has_old_import={has_old_import}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: formatter.js import updated to stringUtils (0.25 points)
    try:
        fmt_path = os.path.join(PROJECT_DIR, 'src', 'formatter.js')
        with open(fmt_path, 'r') as f:
            content = f.read()
        has_new_import = bool(re.search(r"require\(\s*['\"]\.\.\/lib\/stringUtils['\"]", content))
        has_old_import = bool(re.search(r"require\(\s*['\"]\.\.\/lib\/helpers['\"]", content))
        if has_new_import and not has_old_import:
            print(f"PASS: Component 3 - formatter.js imports from ../lib/stringUtils (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 - has_new_import={has_new_import}, has_old_import={has_old_import}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: helpers.test.js import updated to stringUtils (0.2 points)
    try:
        test_path = os.path.join(PROJECT_DIR, 'tests', 'helpers.test.js')
        with open(test_path, 'r') as f:
            content = f.read()
        has_new_import = bool(re.search(r"require\(\s*['\"]\.\.\/lib\/stringUtils['\"]", content))
        has_old_import = bool(re.search(r"require\(\s*['\"]\.\.\/lib\/helpers['\"]", content))
        if has_new_import and not has_old_import:
            print(f"PASS: Component 4 - helpers.test.js imports from ../lib/stringUtils (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 - has_new_import={has_new_import}, has_old_import={has_old_import}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
