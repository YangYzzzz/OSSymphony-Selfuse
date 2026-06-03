"""
Reward Script: Rename helper.js to utils.js and update all imports
Task ID: vscode_lp_058
Domain: vscode
Scoring:
  Component 1 (0.3): helper.js no longer exists in src/
  Component 2 (0.3): utils.js exists in src/ with valid exported functions
  Component 3 (0.4): All 4 importing files updated from './helper' to './utils'
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_058'
SRC_DIR = os.path.join(WORKDIR, 'src')

# The 4 files that originally imported from './helper'
IMPORTING_FILES = ['app.js', 'index.js', 'middleware.js', 'routes.js']


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: src/ directory exists
    if not os.path.isdir(SRC_DIR):
        print(f"CRITICAL: src/ directory not found at {SRC_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: helper.js no longer exists (0.3 points)
    # This PASSES on golden (file renamed away) and FAILS on initial (file still there)
    try:
        helper_path = os.path.join(SRC_DIR, 'helper.js')
        if not os.path.exists(helper_path):
            print(f"PASS: Component 1 — helper.js does not exist (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — helper.js still exists at {helper_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: utils.js exists with the expected exported functions (0.3 points)
    # This PASSES on golden (utils.js created) and FAILS on initial (no utils.js)
    try:
        utils_path = os.path.join(SRC_DIR, 'utils.js')
        if os.path.exists(utils_path):
            with open(utils_path, 'r') as f:
                content = f.read()
            # Check that it exports the key functions that were in helper.js
            expected_exports = ['formatDate', 'capitalize', 'debounce', 'generateId']
            found_exports = [fn for fn in expected_exports if fn in content]
            if len(found_exports) == len(expected_exports):
                print(f"PASS: Component 2 — utils.js exists with all {len(expected_exports)} exported functions (0.3 pts)")
                total_score += 0.3
            else:
                missing = set(expected_exports) - set(found_exports)
                print(f"FAIL: Component 2 — utils.js exists but missing functions: {missing}")
        else:
            print(f"FAIL: Component 2 — utils.js does not exist at {utils_path}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 4 importing files reference './utils' instead of './helper' (0.4 points)
    # Each file contributes 0.1 points. This FAILS on initial (all reference './helper')
    # and PASSES on golden (all reference './utils')
    try:
        files_updated = 0
        for filename in IMPORTING_FILES:
            filepath = os.path.join(SRC_DIR, filename)
            if not os.path.exists(filepath):
                print(f"FAIL: Component 3 — {filename} not found")
                continue
            with open(filepath, 'r') as f:
                content = f.read()
            # Check that it imports from './utils' (not './helper')
            has_utils_import = bool(re.search(r"require\(\s*['\"]\.\/utils['\"]\s*\)", content))
            has_helper_import = bool(re.search(r"require\(\s*['\"]\.\/helper['\"]\s*\)", content))
            if has_utils_import and not has_helper_import:
                print(f"PASS: Component 3 — {filename} imports from './utils' (0.1 pts)")
                files_updated += 1
            elif has_helper_import:
                print(f"FAIL: Component 3 — {filename} still imports from './helper'")
            else:
                print(f"FAIL: Component 3 — {filename} has no recognizable import from './utils' or './helper'")
        component3_score = files_updated * 0.1
        if files_updated > 0:
            total_score += component3_score
        print(f"Component 3 subtotal: {files_updated}/4 files updated ({component3_score:.1f} pts)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score:.1f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
