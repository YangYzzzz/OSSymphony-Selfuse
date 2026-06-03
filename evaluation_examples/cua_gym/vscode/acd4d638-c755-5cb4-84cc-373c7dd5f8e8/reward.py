"""
Reward Script: Replace 'TODO: fix' with 'FIXME:' across project files
Task ID: vscode_gf5_008
Domain: vscode
Scoring:
  Component 1 (0.5): All 'TODO: fix' occurrences eliminated
  Component 2 (0.3): All 'FIXME:' replacements present with correct text
  Component 3 (0.2): Other TODO variants (non 'TODO: fix') are preserved unchanged
"""

import os
import glob

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_008'
DOCS_DIR = os.path.join(WORKDIR, 'projects', 'docs')

# Known files and line counts for 'TODO: fix' in initial state
# 12 total occurrences across 8 files
EXPECTED_REPLACEMENTS = {
    'testing-strategy.txt': 1,
    'architecture-decisions.md': 1,
    'troubleshooting.txt': 2,
    'security-audit.md': 2,
    'api-reference.md': 2,
    'deployment-guide.md': 2,
    'database-schema.md': 1,
    'changelog.md': 1,
}
TOTAL_TODO_FIX_COUNT = 12

# Known other TODO variants that must be preserved (19 total across 19 lines)
EXPECTED_OTHER_TODO_COUNT = 19


def verify_task(docs_dir):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    if not os.path.isdir(docs_dir):
        print(f"CRITICAL: Directory not found: {docs_dir}")
        print("REWARD: 0.0")
        return 0.0

    # Scan all files
    all_files = glob.glob(os.path.join(docs_dir, '*'))
    todo_fix_count = 0
    fixme_count = 0
    other_todo_count = 0

    for fpath in sorted(all_files):
        if not os.path.isfile(fpath):
            continue
        try:
            with open(fpath, 'r') as f:
                content = f.read()
        except Exception as e:
            print(f"WARN: Cannot read {fpath}: {e}")
            continue

        fname = os.path.basename(fpath)

        # Count 'TODO: fix' occurrences (should be 0 in golden)
        count = content.count('TODO: fix')
        if count > 0:
            print(f"  Found {count} 'TODO: fix' in {fname}")
        todo_fix_count += count

        # Count 'FIXME:' occurrences (should be 12 in golden)
        fc = content.count('FIXME:')
        if fc > 0:
            print(f"  Found {fc} 'FIXME:' in {fname}")
        fixme_count += fc

        # Count other TODO (not 'TODO: fix') occurrences
        # We need to count 'TODO' that are NOT followed by ': fix'
        lines = content.split('\n')
        for line in lines:
            if 'TODO' in line and 'TODO: fix' not in line:
                other_todo_count += 1

    print(f"\nSummary: TODO_fix={todo_fix_count}, FIXME={fixme_count}, other_TODO={other_todo_count}")

    # Component 1: All 'TODO: fix' occurrences eliminated (0.5 points)
    # This MUST fail on initial (12 occurrences) and pass on golden (0 occurrences)
    try:
        if todo_fix_count == 0:
            print(f"PASS: Component 1 - All 'TODO: fix' eliminated (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 - Found {todo_fix_count} remaining 'TODO: fix' (expected 0)")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: FIXME: replacements are present (0.3 points)
    # Expected: 12 FIXME: in golden (one for each replaced TODO: fix)
    # Initial should have 0 FIXME:
    try:
        if fixme_count >= TOTAL_TODO_FIX_COUNT:
            print(f"PASS: Component 2 - Found {fixme_count} 'FIXME:' replacements (expected >= {TOTAL_TODO_FIX_COUNT}) (0.3 pts)")
            total_score += 0.3
        elif fixme_count > 0:
            # Partial credit: proportional to replacements made
            partial = 0.3 * (fixme_count / TOTAL_TODO_FIX_COUNT)
            print(f"PARTIAL: Component 2 - Found {fixme_count}/{TOTAL_TODO_FIX_COUNT} 'FIXME:' replacements ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - Found 0 'FIXME:' replacements (expected {TOTAL_TODO_FIX_COUNT})")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Other TODO variants preserved unchanged (0.2 points)
    # Expected: 19 other TODO lines remain in both initial and golden
    # This component checks that only 'TODO: fix' was replaced, not all TODOs
    # On initial: other_todo_count = 19, todo_fix_count = 12 -> this checks preservation
    # On golden: other_todo_count = 19, todo_fix_count = 0 -> this checks preservation
    # Key: this component only awards points when todo_fix_count == 0 (task is done)
    #       AND other TODOs are preserved. This ensures it fails on initial.
    try:
        if todo_fix_count == 0 and other_todo_count >= EXPECTED_OTHER_TODO_COUNT:
            print(f"PASS: Component 3 - {other_todo_count} other TODO variants preserved (expected >= {EXPECTED_OTHER_TODO_COUNT}) (0.2 pts)")
            total_score += 0.2
        elif todo_fix_count == 0 and other_todo_count > 0:
            partial = 0.2 * (other_todo_count / EXPECTED_OTHER_TODO_COUNT)
            print(f"PARTIAL: Component 3 - {other_todo_count}/{EXPECTED_OTHER_TODO_COUNT} other TODO variants preserved ({partial:.2f} pts)")
            total_score += partial
        else:
            if todo_fix_count > 0:
                print(f"FAIL: Component 3 - Task not complete yet (TODO: fix still present)")
            else:
                print(f"FAIL: Component 3 - Other TODO variants may have been incorrectly replaced (found {other_todo_count}, expected {EXPECTED_OTHER_TODO_COUNT})")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task(DOCS_DIR)
