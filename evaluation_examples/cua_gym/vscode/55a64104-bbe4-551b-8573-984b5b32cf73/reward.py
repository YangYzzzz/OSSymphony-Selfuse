"""
Reward Script: Stage Selected Ranges - Partial Git Commit
Task ID: vscode_rf_033
Domain: vscode
Scoring:
  Component 1 (0.30): api.js has staged changes (appears in git staged area)
  Component 2 (0.30): Hunk 1 (auth bug fix) is present in the staged diff
  Component 3 (0.25): Hunk 3 (error message update) is present in the staged diff
  Component 4 (0.15): Hunk 2 (WIP caching feature) is NOT in staged diff but IS in unstaged diff
"""

import os

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'backend')
TASK_ID = 'vscode_rf_033'


def run_git_command(args):
    """Run a git command in the project directory and return stdout."""
    import subprocess as _sp
    result = _sp.run(
        ['git'] + args,
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stdout, result.stderr, result.returncode


def verify_task():
    """
    Verify that hunks 1 and 3 of api.js are staged while hunk 2 remains unstaged.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: project directory exists
    if not os.path.isdir(PROJECT_DIR):
        print(f"CRITICAL: Project directory not found: {PROJECT_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: it is a git repo
    if not os.path.isdir(os.path.join(PROJECT_DIR, '.git')):
        print(f"CRITICAL: Not a git repository: {PROJECT_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: api.js has staged changes (0.30 points)
    # In initial_env there are NO staged changes. In golden_env, api.js should be staged.
    try:
        stdout, stderr, rc = run_git_command(['diff', '--cached', '--name-only'])
        staged_files = [f.strip() for f in stdout.strip().split('\n') if f.strip()]
        if 'api.js' in staged_files:
            print(f"PASS: Component 1 - api.js has staged changes (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 - api.js not in staged files. Staged files: {staged_files}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Hunk 1 (auth bug fix - token extraction) is in staged diff (0.30 points)
    # The staged diff should contain the Bearer token extraction fix:
    #   const authHeader = req.headers['authorization'];
    #   const token = authHeader && authHeader.split(' ')[1];
    try:
        stdout, stderr, rc = run_git_command(['diff', '--cached'])
        staged_diff = stdout

        # Check for the auth fix signature in the staged diff
        has_auth_header_var = "authHeader = req.headers['authorization']" in staged_diff or 'authHeader = req.headers["authorization"]' in staged_diff
        has_bearer_split = "authHeader.split(' ')[1]" in staged_diff or "authHeader.split(\" \")[1]" in staged_diff or "authHeader &&" in staged_diff

        if has_auth_header_var and has_bearer_split:
            print(f"PASS: Component 2 - Hunk 1 (auth bug fix) found in staged diff (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 - Auth bug fix not found in staged diff. "
                  f"authHeader var: {has_auth_header_var}, bearer split: {has_bearer_split}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Hunk 3 (error message update) is in staged diff (0.25 points)
    # The staged diff should contain the updated error message:
    #   'Unable to complete order processing. Please try again later.'
    try:
        stdout, stderr, rc = run_git_command(['diff', '--cached'])
        staged_diff = stdout

        has_new_error_msg = 'Unable to complete order processing' in staged_diff
        if has_new_error_msg:
            print(f"PASS: Component 3 - Hunk 3 (error message update) found in staged diff (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 - Error message update not found in staged diff")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Selective staging - hunks 1&3 are staged while hunk 2 is NOT (0.15 points)
    # This verifies partial staging: there must be BOTH staged and unstaged changes for api.js,
    # with the caching feature specifically remaining unstaged.
    try:
        stdout_staged, _, _ = run_git_command(['diff', '--cached', '--name-only'])
        stdout_unstaged_names, _, _ = run_git_command(['diff', '--name-only'])
        staged_files = [f.strip() for f in stdout_staged.strip().split('\n') if f.strip()]
        unstaged_files = [f.strip() for f in stdout_unstaged_names.strip().split('\n') if f.strip()]

        # api.js must appear in BOTH staged AND unstaged (partial staging)
        api_in_both = 'api.js' in staged_files and 'api.js' in unstaged_files

        if not api_in_both:
            print(f"FAIL: Component 4 - api.js must be in both staged and unstaged (partial staging). "
                  f"staged: {staged_files}, unstaged: {unstaged_files}")
        else:
            # Additionally verify the unstaged diff contains the caching feature
            stdout_unstaged_diff, _, _ = run_git_command(['diff'])
            cache_markers = ['redis.get', 'cacheKey', 'redis.setex']
            cache_in_unstaged = any(marker in stdout_unstaged_diff for marker in cache_markers)

            stdout_staged_diff, _, _ = run_git_command(['diff', '--cached'])
            cache_in_staged = any(marker in stdout_staged_diff for marker in cache_markers)

            if cache_in_unstaged and not cache_in_staged:
                print(f"PASS: Component 4 - Partial staging correct: caching hunk unstaged, other hunks staged (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 - Caching feature staging wrong. "
                      f"In staged: {cache_in_staged}, in unstaged: {cache_in_unstaged}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
