"""
Reward Script: Stage only the changes in lines 10-25 of api_handler.py as a hunk
Task ID: vscode_git_023
Domain: vs_code
Scoring:
  Component 1: api_handler.py has staged changes (git index differs from HEAD) — 0.3 pts
  Component 2: The staged hunk is ONLY the new users endpoint (list_users function, ~10 additions, 0 deletions) — 0.4 pts
  Component 3: The other two hunks (validate_request and authenticate) remain unstaged — 0.3 pts
"""

import os
import subprocess

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_023'
REPO_PATH = '/home/user/backend'


def run_git(args, cwd=REPO_PATH):
    """Run a git command and return (stdout, returncode)."""
    result = subprocess.run(
        ['git'] + args,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout, result.returncode


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    The task requires:
    1. Stage ONLY the hunk covering lines 10-25 (new users endpoint / list_users function)
    2. Leave the other two hunks (validate_request refactor, authenticate update) unstaged
    """
    total_score = 0.0

    # Precondition: repo exists
    if not os.path.isdir(REPO_PATH):
        print(f"CRITICAL: Repository not found at {REPO_PATH}")
        print("REWARD: 0.0")
        return 0.0

    if not os.path.isdir(os.path.join(REPO_PATH, '.git')):
        print(f"CRITICAL: Not a git repository: {REPO_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: api_handler.py has staged changes (git index != HEAD) — 0.3 points
    # This FAILS on initial_env (nothing staged) and PASSES on golden_env (hunk staged)
    try:
        staged_diff, rc = run_git(['diff', '--staged', '--name-only'])
        staged_files = [f.strip() for f in staged_diff.strip().splitlines() if f.strip()]
        if 'api_handler.py' in staged_files:
            print(f"PASS: Component 1 — api_handler.py has staged changes (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — api_handler.py is NOT in staged changes (staged files: {staged_files})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The staged hunk is ONLY the new users endpoint (list_users function)
    # The staged diff should show only additions (no deletions), specifically the
    # list_users function body (10 added lines), not the validate_request or authenticate changes — 0.4 points
    try:
        staged_diff_content, rc = run_git(['diff', '--staged', 'api_handler.py'])
        if staged_diff_content:
            # Count added/removed lines
            added_lines = [l for l in staged_diff_content.splitlines() if l.startswith('+') and not l.startswith('+++')]
            removed_lines = [l for l in staged_diff_content.splitlines() if l.startswith('-') and not l.startswith('---')]
            # The new users endpoint hunk adds exactly 10 lines and removes 0
            # Check for presence of list_users function in staged content
            has_list_users = 'def list_users' in staged_diff_content
            has_no_validate_changes = 'missing = [f for f in required_fields' not in staged_diff_content
            has_no_authenticate_changes = 'import hmac' not in staged_diff_content and 'base64.b64decode' not in staged_diff_content
            # Staged diff should have 10 insertions and 0 deletions (only the new endpoint hunk)
            num_added = len(added_lines)
            num_removed = len(removed_lines)
            if (has_list_users and has_no_validate_changes and has_no_authenticate_changes
                    and num_removed == 0 and 8 <= num_added <= 12):
                print(f"PASS: Component 2 — Staged hunk is ONLY the list_users endpoint "
                      f"(+{num_added} lines, -{num_removed} lines) (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — Staged hunk mismatch:")
                print(f"  has_list_users={has_list_users}, has_no_validate_changes={has_no_validate_changes}, "
                      f"has_no_authenticate_changes={has_no_authenticate_changes}, "
                      f"added={num_added}, removed={num_removed}")
        else:
            print(f"FAIL: Component 2 — No staged diff content for api_handler.py")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The other two hunks remain unstaged (validate_request and authenticate)
    # The unstaged diff should still contain the validate_request and authenticate changes — 0.3 points
    # This FAILS on initial_env (no staged changes, so unstaged diff includes ALL three hunks —
    # but we need to confirm that validate_request and authenticate changes are specifically unstaged)
    # On initial_env: nothing is staged, so the whole diff is unstaged (initial scores 0.0 because
    # Component 1 fails and Components 2+3 gate on Component 1 passing).
    # On golden_env: validate_request + authenticate changes remain unstaged.
    try:
        unstaged_diff, rc = run_git(['diff', 'api_handler.py'])
        if unstaged_diff:
            has_validate_unstaged = ('missing = [f for f in required_fields' in unstaged_diff
                                     or "Missing required fields" in unstaged_diff)
            has_authenticate_unstaged = ('import hmac' in unstaged_diff
                                         or 'base64.b64decode' in unstaged_diff)
            # Also confirm the list_users function is NOT in the unstaged diff
            # (it should already be staged and thus not appear in unstaged)
            list_users_still_unstaged = 'def list_users' in unstaged_diff

            if (has_validate_unstaged and has_authenticate_unstaged and not list_users_still_unstaged):
                print(f"PASS: Component 3 — validate_request and authenticate hunks remain unstaged, "
                      f"list_users is fully staged (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Unstaged diff mismatch:")
                print(f"  has_validate_unstaged={has_validate_unstaged}, "
                      f"has_authenticate_unstaged={has_authenticate_unstaged}, "
                      f"list_users_still_unstaged={list_users_still_unstaged}")
        else:
            print(f"FAIL: Component 3 — No unstaged diff for api_handler.py (all changes staged?)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
