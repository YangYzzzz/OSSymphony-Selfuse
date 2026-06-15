"""
Reward Script: Stash only auth.py changes while keeping routes.py and models.py modified
Task ID: vscode_git_030
Domain: vs_code (git operations)
Scoring:
  - Component 1 (0.5): auth.py has no local modifications (changes were stashed)
  - Component 2 (0.5): git stash exists and contains only auth.py changes

Note: The requirement that routes.py and models.py remain modified is a PRE-CONDITION
that is true in BOTH initial and golden environments (all three files were modified
from the start). It cannot be used as a scoring component. It is verified as a
sub-condition embedded in Component 2 below.
"""

import os
import subprocess

REPO_PATH = '/home/user/webapp'
TASK_ID = 'vscode_git_030'


def run_git(cmd_args, cwd=REPO_PATH):
    """Run a git command and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        ['git'] + cmd_args,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def verify_task():
    """
    Verify that auth.py changes were selectively stashed:
      1. auth.py shows no modifications in working directory (0.5 pts)
      2. A stash entry exists containing only auth.py changes,
         AND routes.py / models.py remain modified (0.5 pts)
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Guard: ensure the repo exists
    if not os.path.isdir(os.path.join(REPO_PATH, '.git')):
        print(f"CRITICAL: {REPO_PATH} is not a git repository")
        print("REWARD: 0.0")
        return 0.0

    # --- Component 1: auth.py is clean in working directory (0.5 points) ---
    # After selective stash, git diff HEAD -- auth.py should produce no output.
    # This FAILS on initial_env (auth.py still modified) and PASSES on golden_env.
    try:
        rc, stdout, stderr = run_git(['diff', '--name-only', 'HEAD', '--', 'auth.py'])
        if rc != 0:
            print(f"FAIL: Component 1 — git diff failed: {stderr}")
        elif stdout == '':
            print("PASS: Component 1 — auth.py is clean (no working-directory modifications) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — auth.py still shows modifications (expected clean after stash)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --- Component 2: stash exists with only auth.py, routes.py/models.py still modified (0.5 points) ---
    # This compound check verifies:
    #   (a) a stash entry exists  → only true after the stash operation
    #   (b) the stash contains only auth.py changes  → confirms selective stash
    #   (c) routes.py and models.py are STILL modified  → confirms they were not stashed
    # This FAILS on initial_env (no stash) and PASSES on golden_env.
    try:
        rc_list, stash_list, _ = run_git(['stash', 'list'])
        if rc_list != 0 or stash_list == '':
            print("FAIL: Component 2 — no git stash entry found")
        else:
            # (b) check stash contents touch only auth.py
            rc_show, stash_files, _ = run_git(['stash', 'show', '--name-only'])
            if rc_show != 0:
                print(f"FAIL: Component 2 — could not inspect stash: {stash_files}")
            else:
                stashed_files = [f.strip() for f in stash_files.splitlines() if f.strip()]
                if stashed_files != ['auth.py']:
                    print(f"FAIL: Component 2 — stash contains unexpected files: {stashed_files} (expected: ['auth.py'])")
                else:
                    # (c) routes.py and models.py still modified
                    _, routes_diff, _ = run_git(['diff', '--name-only', 'HEAD', '--', 'routes.py'])
                    _, models_diff, _ = run_git(['diff', '--name-only', 'HEAD', '--', 'models.py'])
                    routes_modified = routes_diff.strip() == 'routes.py'
                    models_modified = models_diff.strip() == 'models.py'
                    if routes_modified and models_modified:
                        print("PASS: Component 2 — stash has only auth.py changes; routes.py and models.py still modified (0.5 pts)")
                        total_score += 0.5
                    else:
                        if not routes_modified:
                            print(f"FAIL: Component 2 — routes.py is not modified (should remain modified)")
                        if not models_modified:
                            print(f"FAIL: Component 2 — models.py is not modified (should remain modified)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
