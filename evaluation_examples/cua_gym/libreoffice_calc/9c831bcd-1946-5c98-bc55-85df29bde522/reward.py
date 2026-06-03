"""
Reward Script: VSCode Git Feature Branch Workflow
Task ID: vscode_gf2_017
Domain: vscode (git operations)
Scoring:
  Component 1: feature/dark-mode branch exists locally (0.15 pts)
  Component 2: HEAD is on feature/dark-mode branch (0.15 pts)
  Component 3: App.css contains an added comment (0.20 pts)
  Component 4: Commit with message 'WIP: begin dark mode styles' on feature/dark-mode (0.25 pts)
  Component 5: feature/dark-mode pushed to origin (remote tracking branch exists) (0.25 pts)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_017'
REPO_PATH = os.path.join(WORKDIR, 'projects', 'react-app')
APP_CSS_PATH = os.path.join(REPO_PATH, 'src', 'App.css')


def run_git(args: str) -> str:
    """Run a git command in the repo and return stdout."""
    import subprocess
    result = subprocess.run(
        f'git -C {REPO_PATH} {args}',
        shell=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stdout.strip()


def verify_task():
    total_score = 0.0

    # Precondition: repo exists
    if not os.path.isdir(os.path.join(REPO_PATH, '.git')):
        print(f"CRITICAL: Git repo not found at {REPO_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: feature/dark-mode branch exists locally (0.15 pts)
    try:
        branches = run_git('branch')
        branch_names = [b.strip().lstrip('* ') for b in branches.splitlines()]
        if 'feature/dark-mode' in branch_names:
            print("PASS: Component 1 -- feature/dark-mode branch exists locally (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- feature/dark-mode branch not found. Branches: {branch_names}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: HEAD is on feature/dark-mode (0.15 pts)
    try:
        current_branch = run_git('rev-parse --abbrev-ref HEAD')
        if current_branch == 'feature/dark-mode':
            print("PASS: Component 2 -- HEAD is on feature/dark-mode (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 -- Current branch is '{current_branch}', expected 'feature/dark-mode'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: App.css contains an added comment (0.20 pts)
    # In the initial state, App.css has no comment lines. The task asks to "add a comment".
    try:
        if os.path.exists(APP_CSS_PATH):
            with open(APP_CSS_PATH, 'r') as f:
                css_content = f.read()
            # CSS comments are /* ... */ or // (non-standard but sometimes used)
            # Check for CSS block comments that weren't in the original
            # The original file had NO comment lines at all
            comment_pattern = re.findall(r'/\*.*?\*/', css_content, re.DOTALL)
            if len(comment_pattern) > 0:
                print(f"PASS: Component 3 -- App.css contains {len(comment_pattern)} comment(s) (0.20 pts)")
                total_score += 0.20
            else:
                # Also check for // style comments
                line_comments = [l for l in css_content.splitlines() if l.strip().startswith('//')]
                if line_comments:
                    print(f"PASS: Component 3 -- App.css contains {len(line_comments)} line comment(s) (0.20 pts)")
                    total_score += 0.20
                else:
                    print("FAIL: Component 3 -- No comments found in App.css")
        else:
            print(f"FAIL: Component 3 -- App.css not found at {APP_CSS_PATH}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Commit with message 'WIP: begin dark mode styles' exists on feature/dark-mode (0.25 pts)
    try:
        # Check if the branch exists before querying its log
        branch_exists = 'feature/dark-mode' in [b.strip().lstrip('* ') for b in run_git('branch').splitlines()]
        if branch_exists:
            log_output = run_git('log feature/dark-mode --format=%s')
            commit_messages = log_output.splitlines()
            # Look for the exact or close match of the commit message
            found = any('WIP: begin dark mode styles' in msg for msg in commit_messages)
            if found:
                print("PASS: Component 4 -- Commit 'WIP: begin dark mode styles' found on feature/dark-mode (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 -- Commit message not found. Messages on branch: {commit_messages}")
        else:
            print("FAIL: Component 4 -- feature/dark-mode branch does not exist, cannot check commits")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: feature/dark-mode pushed to origin (remote tracking branch exists) (0.25 pts)
    try:
        remote_branches = run_git('branch -r')
        remote_names = [b.strip() for b in remote_branches.splitlines()]
        if any('origin/feature/dark-mode' in name for name in remote_names):
            print("PASS: Component 5 -- origin/feature/dark-mode remote branch exists (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 5 -- origin/feature/dark-mode not found. Remote branches: {remote_names}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.isdir(REPO_PATH):
    print(f"Repo not found: {REPO_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
