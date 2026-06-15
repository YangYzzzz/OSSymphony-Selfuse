"""
Reward Script: Git Archaeology Investigation - trace process_order() evolution
Task ID: vscode_git_069
Domain: vs_code
Scoring:
  - Component 1: investigation_report.md exists with substantial content (0.30 pts)
  - Component 2: All 4 authors (alice, bob, charlie, dave) are mentioned (0.30 pts)
  - Component 3: Correct commit hashes referenced for each iteration (0.20 pts)
  - Component 4: Correct iteration-to-author attribution documented (0.20 pts)
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user/project'
TASK_ID = 'vscode_git_069'
REPORT_PATH = os.path.join(WORKDIR, 'investigation_report.md')

# Expected commit hashes (abbreviated) from git log on golden VM
# These are the canonical commits from the 5 iterations:
# Iteration 1 (alice - initial): 2c5674e
# Iteration 2 (bob - error handling): 372585c
# Iteration 3 (charlie - async refactor): eeef481
# Iteration 4 (alice - caching): 2b5b29c
# Iteration 5 (dave - race condition fix): 2bda0b4
EXPECTED_COMMITS = ['2c5674e', '372585c', 'eeef481', '2b5b29c', '2bda0b4']

# Expected authors for each iteration
ITERATION_AUTHORS = {
    1: 'alice',   # Initial implementation
    2: 'bob',     # Error handling
    3: 'charlie', # Async refactor
    4: 'alice',   # Caching
    5: 'dave',    # Race condition fix
}

# All 4 unique authors that must appear in the report
REQUIRED_AUTHORS = {'alice', 'bob', 'charlie', 'dave'}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: investigation_report.md exists with substantial content (0.30 pts)
    # This component FAILS on initial_env (file doesn't exist) and PASSES on golden_env
    try:
        if not os.path.exists(REPORT_PATH):
            print(f"FAIL: Component 1 — investigation_report.md not found at {REPORT_PATH}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        with open(REPORT_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

        if len(content.strip()) < 100:
            print(f"FAIL: Component 1 — investigation_report.md exists but is nearly empty ({len(content)} chars)")
        else:
            # Must mention process_order to be a valid investigation report
            if 'process_order' in content.lower():
                print(f"PASS: Component 1 — investigation_report.md found with {len(content)} chars, references process_order (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 1 — investigation_report.md exists but does not mention process_order")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 4 authors mentioned in the report (0.30 pts)
    # This component FAILS on initial_env (file doesn't exist) and PASSES on golden_env
    try:
        if not os.path.exists(REPORT_PATH):
            print(f"FAIL: Component 2 — report file not found, cannot check authors")
        else:
            with open(REPORT_PATH, 'r', encoding='utf-8') as f:
                content = f.read().lower()

            authors_found = set()
            for author in REQUIRED_AUTHORS:
                if author in content:
                    authors_found.add(author)

            authors_missing = REQUIRED_AUTHORS - authors_found

            if not authors_missing:
                print(f"PASS: Component 2 — All 4 required authors found: {sorted(authors_found)} (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 — Missing authors: {sorted(authors_missing)}, found: {sorted(authors_found)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correct commit hashes referenced (0.20 pts)
    # Checks that the report includes actual commit hashes from git log
    # This component FAILS on initial_env (file doesn't exist) and PASSES on golden_env
    try:
        if not os.path.exists(REPORT_PATH):
            print(f"FAIL: Component 3 — report file not found, cannot check commits")
        else:
            with open(REPORT_PATH, 'r', encoding='utf-8') as f:
                content = f.read()

            commits_found = []
            for commit_hash in EXPECTED_COMMITS:
                # Check for the short hash (7 chars) anywhere in the report
                if commit_hash in content:
                    commits_found.append(commit_hash)

            if len(commits_found) >= 4:
                print(f"PASS: Component 3 — {len(commits_found)}/5 commit hashes found: {commits_found} (0.20 pts)")
                total_score += 0.20
            elif len(commits_found) >= 2:
                print(f"PARTIAL: Component 3 — Only {len(commits_found)}/5 commit hashes found: {commits_found} (partial credit not awarded, need 4+)")
            else:
                print(f"FAIL: Component 3 — Only {len(commits_found)}/5 commit hashes found: {commits_found}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Correct iteration-to-author attribution (0.20 pts)
    # Verifies the key attributions are correctly documented:
    # - alice for initial implementation (iteration 1)
    # - bob for error handling (iteration 2)
    # - charlie for async refactor (iteration 3)
    # - dave for race condition fix (iteration 5)
    # This component FAILS on initial_env (file doesn't exist) and PASSES on golden_env
    try:
        if not os.path.exists(REPORT_PATH):
            print(f"FAIL: Component 4 — report file not found, cannot check attribution")
        else:
            with open(REPORT_PATH, 'r', encoding='utf-8') as f:
                content = f.read().lower()

            attribution_checks = []

            # Check alice associated with initial implementation
            alice_initial = bool(
                re.search(r'alice.{0,200}initial', content, re.DOTALL) or
                re.search(r'initial.{0,200}alice', content, re.DOTALL)
            )
            attribution_checks.append(('alice/initial', alice_initial))

            # Check bob associated with error handling/validation
            bob_error = bool(
                re.search(r'bob.{0,200}(error|validat)', content, re.DOTALL) or
                re.search(r'(error|validat).{0,200}bob', content, re.DOTALL)
            )
            attribution_checks.append(('bob/error-handling', bob_error))

            # Check charlie associated with async
            charlie_async = bool(
                re.search(r'charlie.{0,200}async', content, re.DOTALL) or
                re.search(r'async.{0,200}charlie', content, re.DOTALL)
            )
            attribution_checks.append(('charlie/async', charlie_async))

            # Check dave associated with race condition or lock
            dave_race = bool(
                re.search(r'dave.{0,200}(race|lock)', content, re.DOTALL) or
                re.search(r'(race|lock).{0,200}dave', content, re.DOTALL)
            )
            attribution_checks.append(('dave/race-condition', dave_race))

            passing_checks = [name for name, passed in attribution_checks if passed]
            failing_checks = [name for name, passed in attribution_checks if not passed]

            if len(passing_checks) >= 4:
                print(f"PASS: Component 4 — All 4 attribution checks passed: {passing_checks} (0.20 pts)")
                total_score += 0.20
            elif len(passing_checks) >= 3:
                print(f"PARTIAL: Component 4 — {len(passing_checks)}/4 attribution checks passed: {passing_checks}, failed: {failing_checks}")
            else:
                print(f"FAIL: Component 4 — Only {len(passing_checks)}/4 attribution checks passed, failed: {failing_checks}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
