"""
Reward Script: VSCode Source Control - Git Stash, Branch Switch, and Stash Apply
Task ID: vscode_ops_084
Domain: vscode
Scoring:
  Component 1: Stash exists with correct message 'WIP: nginx config updates' (0.35 pts)
  Component 2: Reflog shows checkout to 'hotfix' branch (0.30 pts)
  Component 3: Currently on 'main' branch AND reflog shows return from hotfix (0.20 pts)
  Component 4: Working directory has changes AND stash exists (stash applied) (0.15 pts)
"""

import os

WORKDIR = '/home/user'
REPO_DIR = os.path.join(WORKDIR, 'workspace')
TASK_ID = 'vscode_ops_084'


def run_git(args: str) -> str:
    """Run a git command in the repo directory and return stdout."""
    stream = os.popen(f'git -C {REPO_DIR} {args} 2>/dev/null')
    output = stream.read().strip()
    stream.close()
    return output


def has_stash_with_message(stash_output: str, message: str) -> bool:
    """Check if any stash entry contains the given message."""
    return any(message in line for line in stash_output.split('\n') if line)


def has_reflog_entry(reflog_output: str, pattern: str) -> bool:
    """Check if any reflog line contains the given pattern."""
    return any(pattern in line for line in reflog_output.split('\n') if line)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: repo directory exists
    if not os.path.isdir(os.path.join(REPO_DIR, '.git')):
        print(f"CRITICAL: No git repository found at {REPO_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Stash exists with correct message 'WIP: nginx config updates' (0.35 pts)
    # Initial env has NO stash entries. Golden env has one with the right message.
    try:
        stash_list = run_git('stash list')
        if stash_list and has_stash_with_message(stash_list, 'WIP: nginx config updates'):
            print(f"PASS: Component 1 - Stash with message 'WIP: nginx config updates' found (0.35 pts)")
            total_score += 0.35
        elif stash_list:
            print(f"FAIL: Component 1 - Stash entries exist but none with message 'WIP: nginx config updates'. Entries: {stash_list}")
        else:
            print(f"FAIL: Component 1 - No stash entries found")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Reflog shows checkout to 'hotfix' branch (0.30 pts)
    # Initial env reflog has no branch switches. Golden env shows checkout to hotfix.
    try:
        reflog = run_git('reflog')
        if has_reflog_entry(reflog, 'to hotfix'):
            print(f"PASS: Component 2 - Reflog shows checkout to 'hotfix' branch (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 - No reflog entry showing checkout to 'hotfix'. Reflog:\n{reflog}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Currently on 'main' branch AND reflog shows return from hotfix (0.20 pts)
    # This verifies the agent switched back to main after visiting hotfix.
    # Initial env is on main but reflog has no branch switches.
    try:
        current_branch = run_git('branch --show-current')
        reflog = run_git('reflog')

        if current_branch == 'main' and has_reflog_entry(reflog, 'checkout: moving from hotfix to main'):
            print(f"PASS: Component 3 - On 'main' branch with reflog showing return from hotfix (0.20 pts)")
            total_score += 0.20
        elif current_branch == 'main':
            print(f"FAIL: Component 3 - On 'main' branch but no reflog entry showing return from hotfix")
        else:
            print(f"FAIL: Component 3 - Current branch is '{current_branch}', expected 'main'")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Working directory changes restored AND stash exists (0.15 pts)
    # Both envs have working dir changes, but only golden has a stash.
    # This component requires BOTH conditions: stash exists AND changes are in working dir.
    # On initial_env: changes exist but no stash -> FAIL (stash condition fails)
    # On golden_env: changes exist AND stash exists -> PASS (stash was applied)
    try:
        diff_stat = run_git('diff --stat')
        stash_list_2 = run_git('stash list')

        has_nginx = 'nginx.conf' in diff_stat
        has_docker = 'docker-compose.yml' in diff_stat
        has_correct_stash = bool(stash_list_2) and 'WIP: nginx config updates' in stash_list_2

        if has_nginx and has_docker and has_correct_stash:
            print(f"PASS: Component 4 - Working dir changes restored with stash present (0.15 pts)")
            total_score += 0.15
        else:
            details = []
            if not has_nginx:
                details.append("nginx.conf not modified in working dir")
            if not has_docker:
                details.append("docker-compose.yml not modified in working dir")
            if not has_correct_stash:
                details.append("no stash with correct message found")
            print(f"FAIL: Component 4 - {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
