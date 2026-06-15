"""
Reward Script: Pull latest changes from remote 'origin' on current branch
Task ID: vscode_gs_012
Domain: vscode
Scoring:
  Component 1 (0.4): Local main is up to date with origin/main (not behind)
  Component 2 (0.3): At least 5 commits in local history (3 new pulled commits)
  Component 3 (0.3): Specific new commit messages present (Dockerfile, pytest, CI)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_gs_012'
REPO_PATH = os.path.join(WORKDIR, 'projects', 'team-repo')


def run_git(args: str) -> str:
    """Run a git command in the repo and return stdout."""
    import io
    old_cwd = os.getcwd()
    try:
        os.chdir(REPO_PATH)
        stream = os.popen(f'git {args}')
        output = stream.read()
        return output.strip()
    finally:
        os.chdir(old_cwd)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: repo directory exists
    if not os.path.isdir(REPO_PATH):
        print(f"CRITICAL: Repo directory not found: {REPO_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: it is a git repo
    if not os.path.isdir(os.path.join(REPO_PATH, '.git')):
        print(f"CRITICAL: Not a git repo: {REPO_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Local main is up to date with origin/main (0.4 points)
    # On initial_env, branch is behind by 3 commits => FAIL
    # On golden_env, branch is up to date => PASS
    try:
        status_output = run_git('status')
        is_behind = 'Your branch is behind' in status_output
        is_up_to_date = 'Your branch is up to date' in status_output
        if is_up_to_date and not is_behind:
            print(f"PASS: Component 1 — Branch is up to date with remote (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Branch is NOT up to date. Status: {status_output[:200]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: At least 5 commits in local history (0.3 points)
    # Initial has 2 commits, golden has 5 commits after pulling 3 new ones
    try:
        log_output = run_git('log --oneline')
        commit_count = len([line for line in log_output.split('\n') if line.strip()])
        if commit_count >= 5:
            print(f"PASS: Component 2 — Found {commit_count} commits in local history (>= 5) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Only {commit_count} commits in local history, expected >= 5")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Specific new commit messages are present (0.3 points)
    # The 3 new commits should contain these keywords in their messages:
    #   - "Dockerfile" (Add Dockerfile and .dockerignore for containerized deployment)
    #   - "pytest" (Add pytest test suite for API endpoints)
    #   - "CI pipeline" or "GitHub Actions" (Add GitHub Actions CI pipeline)
    # On initial_env these commits do not exist => FAIL
    # On golden_env these commits exist => PASS
    try:
        log_output = run_git('log --format="%s"')
        found_keywords = 0
        expected_keywords = ['Dockerfile', 'pytest', 'GitHub Actions']
        for kw in expected_keywords:
            if kw.lower() in log_output.lower():
                found_keywords += 1

        if found_keywords == 3:
            print(f"PASS: Component 3 — All 3 new commit messages found in history (0.3 pts)")
            total_score += 0.3
        elif found_keywords > 0:
            partial = round(0.3 * found_keywords / 3, 2)
            print(f"PARTIAL: Component 3 — Found {found_keywords}/3 new commit messages ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — None of the 3 new commit messages found in local history")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
