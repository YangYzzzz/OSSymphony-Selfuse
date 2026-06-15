"""
Reward Script: Recover accidental commit by moving it from main to feature/payments
Task ID: vscode_git_072
Domain: vs_code (git operations)
Scoring:
  - Component 1: feature/payments branch exists (0.3 pts)
  - Component 2: feature/payments branch has the 'Add payment validation' commit
                 with payment.py changes (0.4 pts)
  - Component 3: main branch does NOT have the payment validation changes
                 (reset to only initial project structure) (0.3 pts)
Total: 1.0
"""

import os
import subprocess

PROJECT_DIR = '/home/user/project'


def run_git(args, cwd=PROJECT_DIR):
    """Run a git command and return stdout. Raises on non-zero exit."""
    result = subprocess.run(
        ['git'] + args,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def verify_task():
    """
    Verify the git branch recovery task:
    1. feature/payments branch exists
    2. feature/payments has the 'Add payment validation' commit with payment changes
    3. main branch has been reset and does NOT contain payment validation changes
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: project directory and git repo exist
    if not os.path.isdir(PROJECT_DIR):
        print(f"CRITICAL: Project directory not found: {PROJECT_DIR}")
        print("REWARD: 0.0")
        return 0.0

    rc, stdout, stderr = run_git(['rev-parse', '--is-inside-work-tree'])
    if rc != 0:
        print(f"CRITICAL: {PROJECT_DIR} is not a git repository: {stderr}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: feature/payments branch exists (0.3 points)
    # This FAILS on initial_env (only main) and PASSES on golden_env
    try:
        rc, branches_out, _ = run_git(['branch', '--list', 'feature/payments'])
        feature_branch_exists = rc == 0 and 'feature/payments' in branches_out
        if feature_branch_exists:
            print("PASS: Component 1 — branch 'feature/payments' exists (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 1 — branch 'feature/payments' does not exist")
    except Exception as e:
        print(f"ERROR: Component 1 — could not check branch: {e}")

    # Component 2: feature/payments branch has the 'Add payment validation'
    #              commit which modifies payment.py (0.4 points)
    # This FAILS on initial_env (branch doesn't exist) and PASSES on golden_env
    try:
        if not feature_branch_exists:
            print("FAIL: Component 2 — skipped because feature/payments does not exist")
        else:
            # Check commit log on feature/payments for the required commit message
            rc, log_out, _ = run_git(['log', '--oneline', 'feature/payments'])
            has_payment_commit = 'add payment validation' in log_out.lower()

            if not has_payment_commit:
                print(f"FAIL: Component 2 — 'Add payment validation' commit not found on feature/payments. Log: {log_out}")
            else:
                # Also verify the commit actually modifies payment.py (not just message match)
                # Get the commit hash for 'Add payment validation' on feature/payments
                rc2, log_hash, _ = run_git([
                    'log', '--oneline', '--all',
                    '--grep=Add payment validation',
                    'feature/payments'
                ])
                if rc2 != 0 or not log_hash:
                    print("FAIL: Component 2 — could not find commit hash for 'Add payment validation'")
                else:
                    commit_hash = log_hash.split()[0]
                    # Check that payment.py is in the changed files of this commit
                    rc3, show_out, _ = run_git(['show', '--name-only', '--format=', commit_hash])
                    if 'payment.py' in show_out:
                        print(f"PASS: Component 2 — feature/payments has 'Add payment validation' commit ({commit_hash}) modifying payment.py (0.4 pts)")
                        total_score += 0.4
                    else:
                        print(f"FAIL: Component 2 — commit {commit_hash} on feature/payments does not modify payment.py. Changed files: {show_out}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: main branch does NOT have payment validation changes (0.3 points)
    # The main branch should be reset to only 'Initial project structure',
    # meaning payment.py on main should NOT contain 'PaymentValidationError' or
    # the validate_card method introduced in 'Add payment validation'.
    # This FAILS on initial_env (payment changes ARE on main) and PASSES on golden_env
    try:
        # Check if payment.py on main branch contains PaymentValidationError
        # (a class introduced specifically in the 'Add payment validation' commit)
        rc, payment_content, _ = run_git(['show', 'main:payment.py'])
        if rc != 0:
            print(f"FAIL: Component 3 — could not read payment.py from main: {payment_content}")
        else:
            # PaymentValidationError is introduced in the payment validation commit
            # It should NOT be present on main after the reset
            payment_validation_on_main = 'PaymentValidationError' in payment_content
            validate_card_on_main = 'validate_card' in payment_content

            if payment_validation_on_main or validate_card_on_main:
                print(
                    f"FAIL: Component 3 — main branch still has payment validation changes. "
                    f"PaymentValidationError={'found' if payment_validation_on_main else 'not found'}, "
                    f"validate_card={'found' if validate_card_on_main else 'not found'}"
                )
            else:
                # Also confirm main only has one commit (the initial project structure)
                rc2, main_log, _ = run_git(['log', '--oneline', 'main'])
                commit_count = len([l for l in main_log.splitlines() if l.strip()])
                if commit_count == 1 and 'initial project structure' in main_log.lower():
                    print(f"PASS: Component 3 — main branch reset to 'Initial project structure' only ({commit_count} commit, no payment changes) (0.3 pts)")
                    total_score += 0.3
                elif commit_count > 1:
                    print(f"FAIL: Component 3 — main branch has {commit_count} commits (expected 1 after reset). Log: {main_log}")
                else:
                    # payment changes not on main, but commit structure might be unusual
                    print(f"PASS: Component 3 — main branch does not have payment validation changes (0.3 pts)")
                    total_score += 0.3
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
