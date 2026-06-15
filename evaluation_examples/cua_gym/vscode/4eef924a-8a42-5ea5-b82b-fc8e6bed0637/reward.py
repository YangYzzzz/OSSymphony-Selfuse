"""
Reward Script: Stage modified files and commit with specific message
Task ID: vscode_stu_032
Domain: vscode
Scoring:
  Component 1 (0.3): A new commit exists beyond the initial commit
  Component 2 (0.4): Latest commit message is exactly 'Complete exercise 3'
  Component 3 (0.3): All three files (main.py, utils.py, config.py) are in the latest commit
"""

import subprocess
import os

REPO_DIR = '/home/user/vscode_stu_032'
TASK_ID = 'vscode_stu_032'


def run_git(args):
    """Run a git command in the repo directory and return stdout."""
    result = subprocess.run(
        ['git'] + args,
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
        timeout=10
    )
    return result.stdout.strip(), result.returncode


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: repo exists
    if not os.path.isdir(os.path.join(REPO_DIR, '.git')):
        print("CRITICAL: Git repository not found at expected path")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: A new commit exists beyond the initial one (0.3 points)
    # Initial state has exactly 1 commit. Golden should have >= 2.
    try:
        commit_count_str, rc = run_git(['rev-list', '--count', 'HEAD'])
        if rc != 0:
            print(f"ERROR: Component 1 — git rev-list failed")
        else:
            commit_count = int(commit_count_str)
            if commit_count >= 2:
                print(f"PASS: Component 1 — Found {commit_count} commits (>= 2) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — Only {commit_count} commit(s), expected >= 2")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Latest commit message is exactly 'Complete exercise 3' (0.4 points)
    try:
        commit_msg, rc = run_git(['log', '-1', '--format=%s'])
        if rc != 0:
            print(f"ERROR: Component 2 — git log failed")
        else:
            if commit_msg == 'Complete exercise 3':
                print(f"PASS: Component 2 — Commit message matches exactly (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — Expected 'Complete exercise 3', found '{commit_msg}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All three files are included in the latest commit (0.3 points)
    try:
        files_in_commit, rc = run_git(['diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD'])
        if rc != 0:
            print(f"ERROR: Component 3 — git diff-tree failed")
        else:
            committed_files = set(files_in_commit.strip().split('\n')) if files_in_commit.strip() else set()
            expected_files = {'main.py', 'utils.py', 'config.py'}
            if expected_files.issubset(committed_files):
                print(f"PASS: Component 3 — All 3 files in commit: {committed_files} (0.3 pts)")
                total_score += 0.3
            else:
                missing = expected_files - committed_files
                print(f"FAIL: Component 3 — Missing files in commit: {missing}. Found: {committed_files}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
