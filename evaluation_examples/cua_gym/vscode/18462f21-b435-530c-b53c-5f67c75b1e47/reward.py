"""
Reward Script: Git stash with descriptive message via VSCode Source Control
Task ID: vscode_gf2_023
Domain: vscode
Scoring:
  Component 1: At least one git stash exists (0.3 points)
  Component 2: Stash message contains 'WIP: navbar update' (0.4 points)
  Component 3: Stash includes changes to frontend/src/App.jsx (0.3 points)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_023'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'full-stack-app')


def run_git(args_str):
    """Run a git command in the project directory via os.popen and return stdout."""
    cmd = f'cd {PROJECT_DIR} && git {args_str}'
    with os.popen(cmd) as f:
        return f.read().strip()


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: project directory exists and is a git repo
    if not os.path.isdir(os.path.join(PROJECT_DIR, '.git')):
        print(f"CRITICAL: {PROJECT_DIR} is not a git repository")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: At least one git stash exists (0.3 points)
    try:
        stash_list_output = run_git('stash list')
        stash_lines = [line for line in stash_list_output.split('\n') if line.strip()]
        if len(stash_lines) > 0:
            print(f"PASS: Component 1 — {len(stash_lines)} stash(es) found (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 1 — No stashes found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Stash message contains 'WIP: navbar update' (0.4 points)
    try:
        stash_list_output = run_git('stash list')
        matching_lines = [line for line in stash_list_output.split('\n')
                          if 'WIP: navbar update' in line]
        if len(matching_lines) > 0:
            print(f"PASS: Component 2 — Stash with message 'WIP: navbar update' found: {matching_lines[0].strip()} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — No stash with message 'WIP: navbar update'. Stash list: {stash_list_output}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Stash includes changes to frontend/src/App.jsx (0.3 points)
    try:
        stash_list_output = run_git('stash list')
        stash_lines = [line for line in stash_list_output.split('\n') if line.strip()]
        matched_stash_idx = -1
        for i in range(len(stash_lines)):
            show_output = run_git(f'stash show stash@{{{i}}}')
            if 'frontend/src/App.jsx' in show_output:
                matched_stash_idx = i
                break
        if matched_stash_idx >= 0:
            print(f"PASS: Component 3 — Stash stash@{{{matched_stash_idx}}} includes changes to frontend/src/App.jsx (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 3 — No stash includes changes to frontend/src/App.jsx")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
