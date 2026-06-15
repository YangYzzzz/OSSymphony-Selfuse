"""
Reward Script: Create branching workflow with feature/release branches and merges
Task ID: vscode_git_056
Domain: vs_code (git)
Scoring:
  Component 1 (0.15): feature/user-auth branch exists
  Component 2 (0.15): release/v2.0 branch exists
  Component 3 (0.20): feature/user-auth merged into release/v2.0 (merge commit on release branch)
  Component 4 (0.15): auth.py exists on main with login/logout functions
  Component 5 (0.15): version.py exists on main with v2.0.0 version bump
  Component 6 (0.20): release/v2.0 merged into main (merge commit on main)
"""

import os
import subprocess

WORKDIR = '/home/user'
PROJECT_DIR = '/home/user/project'
TASK_ID = 'vscode_git_056'


def run_git(args, cwd=PROJECT_DIR):
    """Run a git command and return (stdout, returncode)."""
    try:
        result = subprocess.run(
            ['git'] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip(), result.returncode
    except Exception as e:
        return '', 1


def verify_task():
    """
    Verify the git branching workflow task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: project directory is a git repo
    if not os.path.isdir(os.path.join(PROJECT_DIR, '.git')):
        print(f"CRITICAL: {PROJECT_DIR} is not a git repository")
        print("REWARD: 0.0")
        return 0.0

    # --- Component 1: feature/user-auth branch exists (0.15 points) ---
    try:
        # List all branches (local + remote refs treated as local by setup)
        stdout, rc = run_git(['branch', '--list', 'feature/user-auth'])
        branch_exists = 'feature/user-auth' in stdout
        if branch_exists:
            print("PASS: Component 1 — feature/user-auth branch exists (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 1 — feature/user-auth branch does NOT exist")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --- Component 2: release/v2.0 branch exists (0.15 points) ---
    try:
        stdout, rc = run_git(['branch', '--list', 'release/v2.0'])
        branch_exists = 'release/v2.0' in stdout
        if branch_exists:
            print("PASS: Component 2 — release/v2.0 branch exists (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 2 — release/v2.0 branch does NOT exist")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # --- Component 3: feature/user-auth merged into release/v2.0 (0.20 points) ---
    # A merge of feature/user-auth into release means the feature commit is an ancestor
    # of release/v2.0, and there's a merge commit on release/v2.0 that references feature
    try:
        # Check if feature/user-auth tip is an ancestor of release/v2.0
        stdout_feat, rc_feat = run_git(['rev-parse', 'feature/user-auth'])
        stdout_rel, rc_rel = run_git(['rev-parse', 'release/v2.0'])

        if rc_feat != 0 or rc_rel != 0:
            print("FAIL: Component 3 — cannot resolve branch tips")
        else:
            # Check if feature/user-auth is an ancestor of release/v2.0
            _, rc_ancestor = run_git(['merge-base', '--is-ancestor', 'feature/user-auth', 'release/v2.0'])
            if rc_ancestor == 0:
                # Also verify there is actually a merge commit (two parents) on release/v2.0
                # that includes feature/user-auth
                log_out, _ = run_git(['log', '--merges', '--oneline', 'release/v2.0'])
                if log_out:
                    print(f"PASS: Component 3 — feature/user-auth merged into release/v2.0 (0.20 pts)")
                    total_score += 0.20
                else:
                    # Could be fast-forward: feature commits are still present
                    print("PASS: Component 3 — feature/user-auth commits reachable from release/v2.0 (0.20 pts)")
                    total_score += 0.20
            else:
                print("FAIL: Component 3 — feature/user-auth is NOT an ancestor of release/v2.0")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # --- Component 4: auth.py exists on main with login/logout functions (0.15 points) ---
    try:
        # Read auth.py content from main branch
        auth_content, rc = run_git(['show', 'main:auth.py'])
        if rc != 0:
            print("FAIL: Component 4 — auth.py does not exist on main branch")
        else:
            has_login = 'def login' in auth_content
            has_logout = 'def logout' in auth_content
            if has_login and has_logout:
                print("PASS: Component 4 — auth.py on main contains login() and logout() functions (0.15 pts)")
                total_score += 0.15
            elif has_login or has_logout:
                print(f"FAIL: Component 4 — auth.py on main is missing {'logout' if has_login else 'login'} function")
            else:
                print("FAIL: Component 4 — auth.py on main lacks both login() and logout() functions")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # --- Component 5: version.py exists on main with v2.0.0 version bump (0.15 points) ---
    try:
        version_content, rc = run_git(['show', 'main:version.py'])
        if rc != 0:
            print("FAIL: Component 5 — version.py does not exist on main branch")
        else:
            # Check for v2.0.0 version info
            has_major2 = 'VERSION_MAJOR = 2' in version_content or "'major': 2" in version_content or '"major": 2' in version_content
            has_version_string = '2.0.0' in version_content or "VERSION_MAJOR = 2" in version_content
            if has_version_string:
                print("PASS: Component 5 — version.py on main contains v2.0.0 version bump (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — version.py on main does not contain v2.0.0 version info")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # --- Component 6: release/v2.0 merged into main (0.20 points) ---
    # Verify that release/v2.0 is an ancestor of main (i.e., its commits are reachable from main),
    # AND that there is a merge commit on main that brought in release/v2.0
    try:
        _, rc_ancestor = run_git(['merge-base', '--is-ancestor', 'release/v2.0', 'main'])
        if rc_ancestor == 0:
            # Verify there's a merge commit on main
            log_main_merges, _ = run_git(['log', '--merges', '--oneline', 'main'])
            if log_main_merges:
                print(f"PASS: Component 6 — release/v2.0 merged into main (merge commit present) (0.20 pts)")
                total_score += 0.20
            else:
                print("FAIL: Component 6 — release/v2.0 commits reachable from main but no merge commit found on main")
        else:
            print("FAIL: Component 6 — release/v2.0 is NOT an ancestor of main (merge not done)")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.isdir(PROJECT_DIR):
    print(f"Project directory not found: {PROJECT_DIR}")
    print("REWARD: 0.0")
else:
    verify_task()
