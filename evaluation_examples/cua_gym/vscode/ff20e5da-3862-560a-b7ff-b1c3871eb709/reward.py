"""
Reward Script: Add 'use strict'; to all JS files missing it
Task ID: vscode_gs_079
Domain: vscode
Scoring:
  Component 1 (0.6): 6 previously-missing files now have 'use strict'; as first line
  Component 2 (0.2): 6 previously-missing files have exactly 1 'use strict'; (no duplication) AND content preserved
  Component 3 (0.2): All 10 files uniformly have 'use strict'; as first line with exactly 1 occurrence each
"""

import os
import glob

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'legacy-app')
TASK_ID = 'vscode_gs_079'

# Files that did NOT have 'use strict'; in the initial state — these are the task targets
INITIALLY_MISSING = {'cache.js', 'database.js', 'events.js', 'helpers.js', 'logger.js', 'routes.js'}

# Files that already HAD 'use strict'; in the initial state
INITIALLY_PRESENT = {'app.js', 'config.js', 'middleware.js', 'validators.js'}

ALL_JS_FILES = INITIALLY_MISSING | INITIALLY_PRESENT


def get_first_non_empty_line(filepath):
    """Return the first non-empty stripped line of a file."""
    try:
        with open(filepath, 'r') as f:
            for line in f:
                stripped = line.strip()
                if stripped:
                    return stripped
    except Exception:
        pass
    return None


def count_use_strict(filepath):
    """Count occurrences of 'use strict'; lines in a file."""
    try:
        with open(filepath, 'r') as f:
            count = 0
            for line in f:
                stripped = line.strip()
                if stripped in ("'use strict';", '"use strict";'):
                    count += 1
            return count
    except Exception:
        return -1


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: project directory and all 10 JS files exist
    if not os.path.isdir(PROJECT_DIR):
        print(f"CRITICAL: Project directory not found: {PROJECT_DIR}")
        print("REWARD: 0.0")
        return 0.0

    js_files = glob.glob(os.path.join(PROJECT_DIR, '*.js'))
    js_basenames = {os.path.basename(f) for f in js_files}
    missing_files = ALL_JS_FILES - js_basenames
    if missing_files:
        print(f"CRITICAL: Missing JS files: {missing_files}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: The 6 previously-missing files now have 'use strict'; as first non-empty line (0.6 points)
    # This FAILS on initial_env (none of them have it) and PASSES on golden_env (all 6 have it)
    try:
        comp1_pass_count = 0
        per_file_pts = 0.6 / len(INITIALLY_MISSING)
        for fname in sorted(INITIALLY_MISSING):
            fpath = os.path.join(PROJECT_DIR, fname)
            first_line = get_first_non_empty_line(fpath)
            if first_line in ("'use strict';", '"use strict";'):
                print(f"PASS: Component 1 — {fname} now has 'use strict'; as first line ({per_file_pts:.3f} pts)")
                comp1_pass_count += 1
                total_score += per_file_pts
            else:
                print(f"FAIL: Component 1 — {fname} first line is: {first_line!r}, expected 'use strict';")
        print(f"  Component 1 subtotal: {comp1_pass_count}/{len(INITIALLY_MISSING)} files, {comp1_pass_count * per_file_pts:.3f}/0.6")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The 6 previously-missing files have exactly 1 'use strict'; (no duplication) (0.2 points)
    # This also FAILS on initial_env (count==0) because the check requires count==1
    # On golden_env it PASSES (count==1 for each)
    try:
        comp2_pass_count = 0
        per_file_pts = 0.2 / len(INITIALLY_MISSING)
        for fname in sorted(INITIALLY_MISSING):
            fpath = os.path.join(PROJECT_DIR, fname)
            count = count_use_strict(fpath)
            if count == 1:
                print(f"PASS: Component 2 — {fname} has exactly 1 'use strict'; ({per_file_pts:.3f} pts)")
                comp2_pass_count += 1
                total_score += per_file_pts
            else:
                print(f"FAIL: Component 2 — {fname} has {count} 'use strict'; occurrences, expected 1")
        print(f"  Component 2 subtotal: {comp2_pass_count}/{len(INITIALLY_MISSING)} files, {comp2_pass_count * per_file_pts:.3f}/0.2")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 10 files uniformly have 'use strict'; as first line with exactly 1 occurrence (0.2 points)
    # This FAILS on initial_env (6 files lack it) and PASSES on golden_env (all 10 have it)
    # Also ensures the 4 previously-compliant files weren't corrupted
    try:
        all_pass = True
        for fname in sorted(ALL_JS_FILES):
            fpath = os.path.join(PROJECT_DIR, fname)
            first_line = get_first_non_empty_line(fpath)
            count = count_use_strict(fpath)
            if first_line not in ("'use strict';", '"use strict";') or count != 1:
                all_pass = False
                print(f"FAIL: Component 3 — {fname}: first_line={first_line!r}, count={count}")
                break
        if all_pass:
            print(f"PASS: Component 3 — All 10 files have exactly 1 'use strict'; at top (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Not all files meet the holistic check")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
