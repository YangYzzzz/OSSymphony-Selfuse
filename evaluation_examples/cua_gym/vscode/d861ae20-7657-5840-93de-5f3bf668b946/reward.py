"""
Reward Script: Merge 'feature/search' into main and handle a merge conflict in search.py
Task ID: vscode_git_045
Domain: vs_code (git)
Scoring:
  Component 1: Merge commit exists with feature/search as second parent (0.4 pts)
  Component 2: search.py contains both fuzzy matching AND pagination (0.4 pts)
  Component 3: Merge commit message matches default merge message (0.2 pts)
  Total: 1.0
"""

import os
import re
import subprocess

WORKDIR = '/home/user/webapp'
TASK_ID = 'vscode_git_045'


def run_git(args, cwd=WORKDIR):
    """Run a git command and return stdout."""
    result = subprocess.run(
        ['git'] + args,
        capture_output=True,
        text=True,
        cwd=cwd
    )
    return result.stdout.strip(), result.returncode


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: ensure the webapp repo exists
    if not os.path.isdir(os.path.join(WORKDIR, '.git')):
        print(f"CRITICAL: No git repo found at {WORKDIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: HEAD is a merge commit (2 parents) and feature/search is one parent (0.4 pts)
    # This verifies the merge was actually performed
    try:
        # Get the HEAD commit object
        head_info, rc = run_git(['cat-file', '-p', 'HEAD'])
        if rc != 0:
            print(f"FAIL: Component 1 — Could not read HEAD commit")
        else:
            # Count parent lines
            parent_lines = [line for line in head_info.split('\n') if line.startswith('parent ')]
            parent_hashes = [line.split(' ')[1] for line in parent_lines]

            if len(parent_hashes) < 2:
                print(f"FAIL: Component 1 — HEAD is not a merge commit (only {len(parent_hashes)} parent(s))")
            else:
                # Verify the second parent corresponds to the feature/search branch commits
                # Check the feature/search branch tip or commits
                feature_tip, rc2 = run_git(['rev-parse', 'feature/search'])
                if rc2 != 0:
                    # Branch may not exist by name after merge, check via reflog or log
                    # Try to find any of the parents in the log with the fuzzy commit message
                    all_commits, _ = run_git(['log', '--all', '--oneline'])
                    if 'fuzzy' in all_commits.lower() or 'feature/search' in all_commits.lower():
                        print(f"PASS: Component 1 — HEAD is a merge commit with 2 parents ({len(parent_hashes)} parents)")
                        total_score += 0.4
                    else:
                        print(f"FAIL: Component 1 — Cannot find feature/search commits in history")
                else:
                    # feature/search branch still exists; verify second parent is feature tip
                    if feature_tip in parent_hashes:
                        print(f"PASS: Component 1 — HEAD is a merge commit; feature/search ({feature_tip[:7]}) is a parent")
                        total_score += 0.4
                    else:
                        # The merge may have integrated feature/search even if hash doesn't match exactly
                        # Check if any parent contains the fuzzy matching feature
                        fuzzy_parent_count = sum(
                            1 for ph in parent_hashes[1:]
                            if 'fuzzy' in run_git(['show', f'{ph}:search.py'])[0]
                        )
                        if fuzzy_parent_count > 0:
                            print(f"PASS: Component 1 — HEAD is a merge commit; a parent contains fuzzy matching (feature/search content)")
                            total_score += 0.4
                        else:
                            print(f"FAIL: Component 1 — HEAD has 2 parents but neither matches feature/search content")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: search.py in HEAD contains BOTH fuzzy matching AND pagination (0.4 pts)
    # Both changes from the conflict resolution must be present
    try:
        search_content, rc = run_git(['show', 'HEAD:search.py'])
        if rc != 0:
            print(f"FAIL: Component 2 — Could not read search.py from HEAD commit")
        else:
            # Check for fuzzy matching: presence of 'fuzzy' parameter/logic
            has_fuzzy = 'fuzzy' in search_content and 'fuzzy matching' in search_content.lower()
            # Check for pagination: presence of page/page_size parameters
            has_pagination = ('page=' in search_content or 'page_size=' in search_content) and \
                             ('page - 1' in search_content or '(page - 1)' in search_content or
                              'start = ' in search_content)

            if has_fuzzy and has_pagination:
                print(f"PASS: Component 2 — search.py contains both fuzzy matching and pagination")
                total_score += 0.4
            elif has_fuzzy:
                print(f"FAIL: Component 2 — search.py has fuzzy matching but MISSING pagination")
            elif has_pagination:
                print(f"FAIL: Component 2 — search.py has pagination but MISSING fuzzy matching")
            else:
                print(f"FAIL: Component 2 — search.py is missing both fuzzy matching and pagination")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The merge commit message is the default git merge message (0.2 pts)
    # Default: "Merge branch 'feature/search'"
    try:
        commit_msg, rc = run_git(['log', '-1', '--format=%s'])
        if rc != 0:
            print(f"FAIL: Component 3 — Could not read commit message")
        else:
            # The default merge message is "Merge branch 'feature/search'"
            expected_msg = "Merge branch 'feature/search'"
            if commit_msg.strip() == expected_msg:
                print(f"PASS: Component 3 — Commit message is default merge message: '{commit_msg}'")
                total_score += 0.2
            elif 'merge' in commit_msg.lower() and 'feature/search' in commit_msg.lower():
                # Partial match — has the right information but not exactly default
                print(f"FAIL: Component 3 — Expected '{expected_msg}', found '{commit_msg}'")
            else:
                print(f"FAIL: Component 3 — Expected '{expected_msg}', found '{commit_msg}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
