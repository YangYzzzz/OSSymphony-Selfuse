"""
Reward Script: Git reflog recovery operation
Task ID: vscode_gf1_080
Domain: vscode (git operations)
Scoring:
  Component 1 (0.2): recovery/lost-work branch exists
  Component 2 (0.2): recovery/lost-work branch contains the 5 lost commits
  Component 3 (0.3): Lost commits cherry-picked back to main (main has 7+ commits)
  Component 4 (0.3): Key files from lost commits are present on main working tree
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf1_080'
REPO_DIR = os.path.join(WORKDIR, 'projects', 'accident-prone')

# Expected commit messages from the 5 lost commits (in chronological order)
LOST_COMMIT_MESSAGES = [
    'Add payment processing feature with order management',
    'Add JWT authentication middleware',
    'Add comprehensive test suite for products and payments',
    'Add Redis caching layer for product queries',
    'Add API rate limiting middleware',
]

# Key files that should be restored by the cherry-picks
RESTORED_FILES = [
    'src/services/payment.py',
    'src/middleware/auth.py',
    'src/middleware/rate_limit.py',
    'src/services/cache.py',
    'tests/test_payment.py',
    'tests/test_products.py',
    'src/routes/orders.py',
]


def run_git(cmd):
    """Run a git command in the repo directory and return stdout."""
    full_cmd = f"cd {REPO_DIR} && {cmd} 2>/dev/null"
    stream = os.popen(full_cmd)
    output = stream.read().strip()
    rc = stream.close()
    # os.popen.close() returns None on success, or exit status on failure
    return_code = 0 if rc is None else (rc >> 8)
    return output, return_code


def verify_task():
    """
    Verify git reflog recovery task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: repo directory exists
    if not os.path.isdir(REPO_DIR):
        print(f"CRITICAL: Repository directory not found: {REPO_DIR}")
        print("REWARD: 0.0")
        return 0.0

    if not os.path.isdir(os.path.join(REPO_DIR, '.git')):
        print(f"CRITICAL: Not a git repository: {REPO_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: recovery/lost-work branch exists (0.2 points)
    # This branch does NOT exist in initial_env, only in golden_env
    try:
        branches_out, rc = run_git("git branch --list 'recovery/lost-work'")
        if 'recovery/lost-work' in branches_out:
            print(f"PASS: Component 1 — recovery/lost-work branch exists (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — recovery/lost-work branch not found. Branches: {branches_out}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: recovery/lost-work branch contains the 5 lost commits (0.2 points)
    # In initial_env, the branch doesn't exist so this will fail
    try:
        log_out, rc = run_git("git log --oneline recovery/lost-work 2>/dev/null")
        if rc != 0 or not log_out:
            print(f"FAIL: Component 2 — Cannot read recovery/lost-work log (branch may not exist)")
        else:
            commit_lines = log_out.strip().split('\n')
            # The recovery branch should have 7 commits (2 original + 5 lost)
            # Check that commit messages from the lost work appear in the branch
            found_msgs = 0
            for msg in LOST_COMMIT_MESSAGES:
                for line in commit_lines:
                    if msg in line:
                        found_msgs += 1
                        break

            if found_msgs >= 4:
                # At least 4 of 5 lost commit messages found on the recovery branch
                print(f"PASS: Component 2 — recovery/lost-work has {found_msgs}/5 lost commit messages (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — recovery/lost-work only has {found_msgs}/5 lost commit messages")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Lost commits cherry-picked back to main (0.3 points)
    # Initial_env main has only 2 commits; golden_env main has 7 (cherry-picked)
    try:
        log_out, rc = run_git("git log --oneline main")
        if rc != 0:
            print(f"FAIL: Component 3 — Cannot read main log")
        else:
            commit_lines = [l for l in log_out.strip().split('\n') if l.strip()]
            main_count = len(commit_lines)

            # Check that lost commit messages appear in main's log
            found_on_main = 0
            for msg in LOST_COMMIT_MESSAGES:
                for line in commit_lines:
                    if msg in line:
                        found_on_main += 1
                        break

            if main_count >= 7 and found_on_main >= 4:
                print(f"PASS: Component 3 — main has {main_count} commits with {found_on_main}/5 recovered messages (0.3 pts)")
                total_score += 0.3
            elif main_count > 2 and found_on_main >= 2:
                # Partial credit: some commits cherry-picked but not all
                if found_on_main >= 2:
                    partial = 0.15
                    print(f"PARTIAL: Component 3 — main has {main_count} commits with {found_on_main}/5 recovered messages ({partial} pts)")
                    total_score += partial
            else:
                print(f"FAIL: Component 3 — main has only {main_count} commits, {found_on_main}/5 recovered messages")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Key files from lost commits present on main working tree (0.3 points)
    # Initial_env is missing these files; golden_env has them restored
    try:
        files_found = 0
        missing_files = []
        for rel_path in RESTORED_FILES:
            full_path = os.path.join(REPO_DIR, rel_path)
            if os.path.isfile(full_path):
                files_found += 1
            else:
                missing_files.append(rel_path)

        total_expected = len(RESTORED_FILES)
        ratio = files_found / total_expected

        if ratio >= 0.85:
            print(f"PASS: Component 4 — {files_found}/{total_expected} key files present on main (0.3 pts)")
            total_score += 0.3
        elif ratio >= 0.5:
            partial = round(0.3 * ratio, 2)
            print(f"PARTIAL: Component 4 — {files_found}/{total_expected} key files present ({partial} pts). Missing: {missing_files}")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Only {files_found}/{total_expected} key files present. Missing: {missing_files}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
