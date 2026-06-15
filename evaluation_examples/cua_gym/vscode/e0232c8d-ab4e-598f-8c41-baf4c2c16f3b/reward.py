"""
Reward Script: Cherry-pick feature/optimization commit onto main, resolve conflict using async connections + error handling
Task ID: vscode_git_060
Domain: vs_code (git)
Scoring:
  Component 1: Cherry-pick commit exists on main branch (3rd commit on main branch) (0.35 pts)
  Component 2: db.py uses async connection pool (asyncpg, async def connection_pool) (0.35 pts)
  Component 3: Error handling preserved in async connection_pool() with asyncpg exception handling (0.30 pts)
Total: 1.0
"""

import os
import re

WORKDIR = '/home/user/webapp'
TASK_ID = 'vscode_git_060'
GIT_DIR = os.path.join(WORKDIR, '.git')


def read_git_file(relative_path):
    """Read a git internal file relative to .git directory. Returns content string or None."""
    full_path = os.path.join(GIT_DIR, relative_path)
    try:
        with open(full_path, 'r', errors='replace') as f:
            return f.read()
    except Exception:
        return None


def get_main_branch_sha():
    """Get the SHA of the tip of the main branch from git refs."""
    # Try direct ref first
    sha = read_git_file('refs/heads/main')
    if sha:
        return sha.strip()
    # Try packed-refs
    packed = read_git_file('packed-refs')
    if packed:
        for line in packed.splitlines():
            if line.endswith(' refs/heads/main'):
                return line.split()[0].strip()
    return None


def get_main_branch_commits_from_log():
    """
    Parse .git/logs/refs/heads/main or .git/logs/HEAD to count commits on main.
    Returns list of (from_sha, to_sha, action_description) tuples for commits on main.
    """
    # Try branch-specific log first
    log_content = read_git_file('logs/refs/heads/main')
    if not log_content:
        # Fall back to HEAD log, filtering for main branch commits
        log_content = read_git_file('logs/HEAD')

    if not log_content:
        return []

    commit_entries = []
    for line in log_content.strip().splitlines():
        # Format: <old_sha> <new_sha> <identity> <timestamp> <+tz> <action>
        parts = line.split('\t', 1)
        if len(parts) < 2:
            continue
        sha_part = parts[0].strip().split()
        action = parts[1].strip() if len(parts) > 1 else ''
        if len(sha_part) >= 2 and action.startswith('commit'):
            from_sha = sha_part[0]
            to_sha = sha_part[1]
            commit_entries.append((from_sha, to_sha, action))

    return commit_entries


def get_last_commit_message():
    """Read the last commit message from COMMIT_EDITMSG."""
    return read_git_file('COMMIT_EDITMSG') or ''


def get_current_branch():
    """Get the current branch from .git/HEAD."""
    head = read_git_file('HEAD')
    if head and head.startswith('ref: refs/heads/'):
        return head.replace('ref: refs/heads/', '').strip()
    return None


def verify_task():
    """
    Verify that the cherry-pick was completed successfully with conflict resolution.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: repository must exist
    if not os.path.isdir(WORKDIR):
        print(f"CRITICAL: Repository directory not found: {WORKDIR}")
        print("REWARD: 0.0")
        return 0.0

    if not os.path.isdir(GIT_DIR):
        print(f"CRITICAL: Not a git repository: {WORKDIR}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must be on main branch
    current_branch = get_current_branch()
    if current_branch != 'main':
        print(f"PRECONDITION FAIL: Expected to be on 'main' branch, found: '{current_branch}'")
        print("REWARD: 0.0")
        return 0.0
    print(f"PRECONDITION OK: On branch 'main'")

    # Precondition: no active cherry-pick in progress (CHERRY_PICK_HEAD should not exist)
    cherry_pick_head = os.path.join(GIT_DIR, 'CHERRY_PICK_HEAD')
    if os.path.exists(cherry_pick_head):
        print("PRECONDITION FAIL: Cherry-pick is still in progress (CHERRY_PICK_HEAD exists). Task not completed.")
        print("REWARD: 0.0")
        return 0.0
    print("PRECONDITION OK: No cherry-pick in progress")

    # Precondition: db.py must exist
    db_path = os.path.join(WORKDIR, 'db.py')
    if not os.path.isfile(db_path):
        print(f"CRITICAL: db.py not found at {db_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(db_path, 'r') as f:
            db_content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read db.py: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: no unresolved conflict markers in db.py
    if '<<<<<<<' in db_content or '=======' in db_content or '>>>>>>>' in db_content:
        print("PRECONDITION FAIL: db.py still contains conflict markers — cherry-pick not completed")
        print("REWARD: 0.0")
        return 0.0
    print("PRECONDITION OK: No conflict markers in db.py")

    # Component 1: A cherry-pick commit exists on main branch (0.35 pts)
    # After cherry-pick, main should have at least 3 commits.
    # We verify by counting commit entries in git logs and checking the HEAD commit message.
    try:
        main_commits = get_main_branch_commits_from_log()
        commit_count = len(main_commits)
        print(f"INFO: main branch has {commit_count} commit(s) in git log")

        last_commit_msg = get_last_commit_message()
        last_commit_lower = last_commit_msg.lower()

        print(f"INFO: Last commit message (COMMIT_EDITMSG):\n  {last_commit_msg.strip()[:200]}")

        # Cherry-pick indicators in the commit message
        cherry_indicators = [
            'cherry' in last_commit_lower,
            'async' in last_commit_lower and 'connection' in last_commit_lower,
            'cherry picked from commit' in last_commit_lower,
        ]

        # We need: >= 3 commits on main AND last commit looks like the cherry-pick
        if commit_count >= 3 and any(cherry_indicators):
            print(f"PASS: Component 1 — Cherry-pick commit found on main ({commit_count} commits, last: '{last_commit_msg.strip()[:80]}') ({0.35} pts)")
            total_score += 0.35
        elif commit_count >= 3:
            # Still check COMMIT_EDITMSG for async/refactor indicators
            async_refactor = 'refactor' in last_commit_lower and 'async' in last_commit_lower
            has_optimization = 'optimization' in last_commit_lower
            has_asyncpg_msg = 'asyncpg' in last_commit_lower
            if async_refactor or has_optimization or has_asyncpg_msg:
                print(f"PASS: Component 1 — Cherry-pick result commit found on main ({commit_count} commits) ({0.35} pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 — main has {commit_count} commits but HEAD commit doesn't look like cherry-pick. Last msg: '{last_commit_msg.strip()[:80]}'")
        else:
            print(f"FAIL: Component 1 — Expected >= 3 commits on main after cherry-pick, found {commit_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: db.py uses async connection pool (asyncpg + async def connection_pool) (0.35 pts)
    # This verifies the conflict was resolved using async connections (not sync)
    try:
        has_asyncpg_import = 'import asyncpg' in db_content
        has_async_def_connection_pool = bool(re.search(r'async\s+def\s+connection_pool\s*\(', db_content))
        has_await_asyncpg = 'await asyncpg.create_pool' in db_content
        has_no_psycopg2 = 'psycopg2' not in db_content and 'pg_pool' not in db_content

        checks = {
            'asyncpg import': has_asyncpg_import,
            'async def connection_pool()': has_async_def_connection_pool,
            'await asyncpg.create_pool': has_await_asyncpg,
            'no psycopg2/pg_pool': has_no_psycopg2,
        }

        print(f"INFO: Async connection pool checks:")
        for check_name, check_result in checks.items():
            print(f"  {'PASS' if check_result else 'FAIL'}: {check_name}")

        if all(checks.values()):
            print(f"PASS: Component 2 — db.py uses async connection pool with asyncpg ({0.35} pts)")
            total_score += 0.35
        elif has_asyncpg_import and has_async_def_connection_pool:
            # Partial async migration
            print(f"PASS: Component 2 — db.py uses async connection_pool() with asyncpg ({0.35} pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — db.py does not use async connection pool. Checks: {checks}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Error handling preserved in ASYNC connection_pool() with asyncpg exception handling (0.30 pts)
    # The resolved conflict must have: async def + try/except + asyncpg exception + RuntimeError
    # Key distinction from initial state: initial_env has sync def + psycopg2 exceptions.
    # This component requires BOTH async function AND asyncpg-compatible error handling.
    try:
        # Extract async def connection_pool() function body
        cp_func_match = re.search(
            r'async\s+def\s+connection_pool\s*\(\s*\).*?(?=\n(?:async\s+)?def\s|\Z)',
            db_content,
            re.DOTALL
        )

        if cp_func_match:
            cp_func_body = cp_func_match.group(0)
            cp_has_try = 'try:' in cp_func_body
            cp_has_except = 'except' in cp_func_body
            cp_has_raise_runtime = 'raise RuntimeError' in cp_func_body
            # asyncpg-specific error handling (not psycopg2)
            cp_has_asyncpg_except = 'asyncpg' in cp_func_body and 'except' in cp_func_body
            cp_no_psycopg2 = 'psycopg2' not in cp_func_body

            cp_checks = {
                'async def connection_pool() found': True,
                'try/except in function': cp_has_try and cp_has_except,
                'raise RuntimeError preserved': cp_has_raise_runtime,
                'asyncpg exception handling (not psycopg2)': cp_has_asyncpg_except and cp_no_psycopg2,
            }
            print(f"INFO: Async error handling checks in connection_pool():")
            for check_name, check_result in cp_checks.items():
                print(f"  {'PASS' if check_result else 'FAIL'}: {check_name}")

            if cp_has_try and cp_has_except and cp_has_asyncpg_except and cp_no_psycopg2:
                print(f"PASS: Component 3 — Error handling preserved in async connection_pool() with asyncpg exceptions ({0.30} pts)")
                total_score += 0.30
            elif cp_has_try and cp_has_except and cp_has_raise_runtime and cp_no_psycopg2:
                print(f"PASS: Component 3 — Try/except + RuntimeError preserved in async connection_pool() ({0.30} pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 3 — Error handling not properly preserved. try={cp_has_try}, except={cp_has_except}, asyncpg_except={cp_has_asyncpg_except}, no_psycopg2={cp_no_psycopg2}")
        else:
            print(f"FAIL: Component 3 — async def connection_pool() not found in db.py (cannot verify error handling)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
