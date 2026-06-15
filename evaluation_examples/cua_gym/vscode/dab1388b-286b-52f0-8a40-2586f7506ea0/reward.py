"""
Reward Script: Undo the last three commits, reorganize changes into two logically grouped commits
Task ID: vscode_git_066
Domain: vs_code (git operations)
Scoring:
  Component 1: Exactly 2 commits after base commit (0.2 pts)
  Component 2: First newer commit message is "Refactor API endpoint handlers" (0.2 pts)
  Component 3: First newer commit only touches api.py (0.2 pts)
  Component 4: Second newer commit message is "Update tests and documentation" (0.2 pts)
  Component 5: Second newer commit only touches tests/docs (0.2 pts)
"""

import os
import subprocess

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_066'
PROJECT_DIR = os.path.join(WORKDIR, 'project')

# The base commit message (the first/oldest commit expected to be preserved)
BASE_COMMIT_MSG_PATTERN = 'Initial project structure'

# Expected reorganized commit messages
EXPECTED_COMMIT1_MSG = 'Refactor API endpoint handlers'
EXPECTED_COMMIT2_MSG = 'Update tests and documentation'

# Expected files per commit
EXPECTED_COMMIT1_FILES = {'api.py'}
EXPECTED_COMMIT2_FILES = {'docs/README.md', 'tests/test_api.py'}


def get_git_log(project_dir):
    """Return list of (hash, message) for all commits, newest first."""
    result = subprocess.run(
        ['git', '-C', project_dir, 'log', '--format=%H|||%s'],
        capture_output=True, text=True
    )
    commits = []
    for line in result.stdout.strip().splitlines():
        if '|||' in line:
            h, msg = line.split('|||', 1)
            commits.append((h.strip(), msg.strip()))
    return commits


def get_commit_files(project_dir, commit_hash):
    """Return the set of files changed in a given commit."""
    result = subprocess.run(
        ['git', '-C', project_dir, 'diff-tree', '--no-commit-id', '-r', '--name-only', commit_hash],
        capture_output=True, text=True
    )
    files = set()
    for line in result.stdout.strip().splitlines():
        line = line.strip()
        if line:
            files.add(line)
    return files


def verify_task(project_dir):
    """
    Verify task completion: the last 3 bad commits have been replaced by
    2 logically reorganized commits.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Sanity check: git repo exists
    if not os.path.isdir(os.path.join(project_dir, '.git')):
        print(f"CRITICAL: {project_dir} is not a git repository")
        print("REWARD: 0.0")
        return 0.0

    # Get commit log
    try:
        commits = get_git_log(project_dir)
    except Exception as e:
        print(f"CRITICAL: Cannot read git log: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not commits:
        print("CRITICAL: No commits found")
        print("REWARD: 0.0")
        return 0.0

    # Find the base commit (the initial project structure commit)
    base_idx = None
    for i, (h, msg) in enumerate(commits):
        if BASE_COMMIT_MSG_PATTERN.lower() in msg.lower():
            base_idx = i
            break

    if base_idx is None:
        print(f"CRITICAL: Could not find base commit containing '{BASE_COMMIT_MSG_PATTERN}'")
        print("REWARD: 0.0")
        return 0.0

    # Commits after the base commit (newer commits that were reorganized)
    new_commits = commits[:base_idx]  # commits[0] is newest
    print(f"INFO: Found {len(new_commits)} commit(s) after base commit")
    for h, msg in new_commits:
        print(f"  - [{h[:7]}] {msg}")

    # Component 1: Exactly 2 commits after the base commit (0.2 pts)
    # Initial state has 3 bad commits; golden state should have 2 reorganized commits
    try:
        if len(new_commits) == 2:
            print(f"PASS: Component 1 — Exactly 2 reorganized commits found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected 2 commits after base, found {len(new_commits)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Only proceed with ordering checks if we have exactly 2 commits
    if len(new_commits) >= 1:
        # Commit 1 (oldest of the new commits) = new_commits[-1] (index from newest)
        # But task says: commit 1 = API changes (oldest), commit 2 = tests+docs (newest)
        # git log returns newest first, so:
        #   new_commits[0] = newest = "Update tests and documentation"
        #   new_commits[1] = older  = "Refactor API endpoint handlers"
        # However, we should check by matching message, not just position.

        # Find commit matching "Refactor API endpoint handlers"
        api_commit = None
        tests_commit = None
        for h, msg in new_commits:
            if EXPECTED_COMMIT1_MSG.lower() in msg.lower():
                api_commit = (h, msg)
            elif EXPECTED_COMMIT2_MSG.lower() in msg.lower():
                tests_commit = (h, msg)

        # Component 2: Commit message "Refactor API endpoint handlers" exists (0.2 pts)
        try:
            if api_commit is not None:
                print(f"PASS: Component 2 — Found commit '{api_commit[1]}' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — No commit containing '{EXPECTED_COMMIT1_MSG}' found")
                # Print actual messages for debug
                for h, msg in new_commits:
                    print(f"  Actual: [{h[:7]}] {msg}")
        except Exception as e:
            print(f"ERROR: Component 2 — {e}")

        # Component 3: "Refactor API endpoint handlers" commit only touches api.py (0.2 pts)
        try:
            if api_commit is not None:
                api_files = get_commit_files(project_dir, api_commit[0])
                if api_files == EXPECTED_COMMIT1_FILES:
                    print(f"PASS: Component 3 — API commit only touches api.py (files: {api_files}) (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 3 — Expected files {EXPECTED_COMMIT1_FILES}, found {api_files}")
            else:
                print(f"FAIL: Component 3 — Cannot check files, API commit not found")
        except Exception as e:
            print(f"ERROR: Component 3 — {e}")

        # Component 4: Commit message "Update tests and documentation" exists (0.2 pts)
        try:
            if tests_commit is not None:
                print(f"PASS: Component 4 — Found commit '{tests_commit[1]}' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 — No commit containing '{EXPECTED_COMMIT2_MSG}' found")
                for h, msg in new_commits:
                    print(f"  Actual: [{h[:7]}] {msg}")
        except Exception as e:
            print(f"ERROR: Component 4 — {e}")

        # Component 5: "Update tests and documentation" commit only touches tests/docs (0.2 pts)
        try:
            if tests_commit is not None:
                tests_files = get_commit_files(project_dir, tests_commit[0])
                if tests_files == EXPECTED_COMMIT2_FILES:
                    print(f"PASS: Component 5 — Tests/docs commit only touches {tests_files} (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 5 — Expected files {EXPECTED_COMMIT2_FILES}, found {tests_files}")
            else:
                print(f"FAIL: Component 5 — Cannot check files, tests/docs commit not found")
        except Exception as e:
            print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
if not os.path.isdir(PROJECT_DIR):
    print(f"Project directory not found: {PROJECT_DIR}")
    print("REWARD: 0.0")
else:
    verify_task(PROJECT_DIR)
