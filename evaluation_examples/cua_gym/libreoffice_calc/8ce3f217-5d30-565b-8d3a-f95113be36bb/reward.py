"""
Reward Script: Partial hunk staging and selective commit in VSCode
Task ID: vscode_gf1_023
Domain: vscode (git operations)
Scoring:
  Component 1 (0.3): Commit with correct message exists (beyond initial)
  Component 2 (0.4): Committed diff contains only the bug fix hunk
  Component 3 (0.3): Bug fix is NOT in unstaged diff AND logging/debug changes ARE unstaged
"""

import os

WORKDIR = '/home/user/projects/webapp'


def run_git(cmd):
    """Run a git command in WORKDIR and return (stdout, returncode)."""
    full_cmd = f"cd {WORKDIR} && {cmd}"
    stream = os.popen(full_cmd)
    output = stream.read().strip()
    rc = stream.close()  # None means success (rc=0)
    return output, (rc or 0)


def verify_task():
    """
    Verify that only the bug fix hunk was staged and committed,
    while logging and debug changes remain unstaged.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: repo exists
    if not os.path.isdir(os.path.join(WORKDIR, '.git')):
        print("CRITICAL: No git repo found at " + WORKDIR)
        print("REWARD: 0.0")
        return 0.0

    # Get commit log
    log_output, rc = run_git("git log --oneline")
    if rc != 0:
        print("CRITICAL: git log failed")
        print("REWARD: 0.0")
        return 0.0

    commits = log_output.strip().split('\n')
    print(f"INFO: Found {len(commits)} commit(s): {log_output}")

    # Component 1: A commit with message "Fix order processing validation bug" exists
    # beyond the initial commit (0.3 points)
    try:
        msg_check, _ = run_git('git log --oneline --grep="Fix order processing validation bug"')
        if msg_check.strip() and len(commits) >= 2:
            print(f"PASS: Component 1 — Commit with correct message found: {msg_check.strip()} (0.3 pts)")
            total_score += 0.3
        else:
            if not msg_check.strip():
                print(f"FAIL: Component 1 — No commit with message 'Fix order processing validation bug' found")
            else:
                print(f"FAIL: Component 1 — Only {len(commits)} commit(s); expected new commit beyond initial")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The committed diff contains the bug fix changes and excludes other hunks (0.4 points)
    try:
        if len(commits) >= 2:
            commit_diff, _ = run_git("git diff HEAD~1 HEAD")

            has_discount_fix = ("discount_pct < 0 or order.discount_pct > 100" in commit_diff or
                                "Discount must be between 0 and 100" in commit_diff)
            has_quantity_check = ("item.quantity <= 0" in commit_diff or
                                 "Quantity must be positive" in commit_diff)
            has_logging_import = ("import logging" in commit_diff or "logging.getLogger" in commit_diff)
            has_debug_comments = ("DEBUG: shipping rate" in commit_diff or "DEBUG: base_rates" in commit_diff)

            sub_score = 0.0
            if has_discount_fix:
                sub_score += 0.15
                print(f"  PASS: Discount validation fix present in commit")
            else:
                print(f"  FAIL: Discount validation fix NOT in commit diff")

            if has_quantity_check:
                sub_score += 0.15
                print(f"  PASS: Quantity check present in commit")
            else:
                print(f"  FAIL: Quantity check NOT in commit diff")

            if not has_logging_import:
                sub_score += 0.05
                print(f"  PASS: Logging import correctly excluded from commit")
            else:
                print(f"  FAIL: Logging import was included in commit (should be excluded)")

            if not has_debug_comments:
                sub_score += 0.05
                print(f"  PASS: Debug comments correctly excluded from commit")
            else:
                print(f"  FAIL: Debug comments were included in commit (should be excluded)")

            if sub_score > 0:
                print(f"PASS: Component 2 — Bug fix commit content verified ({sub_score} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 2 — Commit diff does not contain expected bug fix changes")
        else:
            print(f"FAIL: Component 2 — No new commit to check diff against")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Bug fix is NOT in unstaged diff (committed) AND logging/debug
    # changes ARE still in unstaged diff (0.3 points — compound, all-or-nothing)
    # Key discriminator: in initial_env the bug fix IS still unstaged, so this fails.
    try:
        unstaged_diff, _ = run_git("git diff")

        # The bug fix hunk should NOT be in unstaged diff (it was committed)
        bugfix_still_unstaged = ("Discount must be between 0 and 100" in unstaged_diff or
                                 "discount_pct < 0 or order.discount_pct > 100" in unstaged_diff)

        # Logging and debug changes SHOULD still be in unstaged diff
        has_logging_unstaged = ("import logging" in unstaged_diff and "logger.info" in unstaged_diff)
        has_debug_unstaged = ("DEBUG: shipping rate" in unstaged_diff or "DEBUG: base_rates" in unstaged_diff)

        bugfix_absent = not bugfix_still_unstaged
        print(f"  {'PASS' if bugfix_absent else 'FAIL'}: Bug fix {'absent from' if bugfix_absent else 'still in'} unstaged diff")
        print(f"  {'PASS' if has_logging_unstaged else 'FAIL'}: Logging changes {'remain' if has_logging_unstaged else 'missing from'} unstaged diff")
        print(f"  {'PASS' if has_debug_unstaged else 'FAIL'}: Debug comments {'remain' if has_debug_unstaged else 'missing from'} unstaged diff")

        # ALL three must hold for the component to pass (compound check)
        if bugfix_absent and has_logging_unstaged and has_debug_unstaged:
            print(f"PASS: Component 3 — Working tree state correct: bug fix committed, other changes remain (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Working tree state incorrect (all sub-checks must pass)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
