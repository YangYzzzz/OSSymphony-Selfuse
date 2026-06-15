"""
Reward Script: Git branch cleanup, alias creation, and VSCode task configuration
Task ID: vscode_gf6_018
Domain: vscode
Scoring:
  Component 1 (0.35): Merged branches deleted AND non-merged branch preserved AND main intact
  Component 2 (0.25): git global alias 'cleanmerged' is set to a non-empty value
  Component 3 (0.25): .vscode/tasks.json has correct task definition
  Component 4 (0.15): tasks.json is committed to the repository
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_018'
REPO_DIR = os.path.join(WORKDIR, 'projects', 'git-advanced-ops')


def run_git(args):
    """Run a git command in the repo directory and return stdout."""
    import subprocess
    result = subprocess.run(
        ['git'] + args,
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
        timeout=10
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: repo directory exists
    if not os.path.isdir(REPO_DIR):
        print(f"CRITICAL: Repository directory not found: {REPO_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Get list of local branches
    try:
        stdout, _, rc = run_git(['branch', '--list'])
        branches = [b.strip().lstrip('* ') for b in stdout.splitlines() if b.strip()]
        print(f"INFO: Local branches: {branches}")
    except Exception as e:
        print(f"CRITICAL: Cannot list branches: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Branch cleanup correct (0.35 points)
    # All 3 merged branches deleted, feature/in-progress preserved, main preserved
    # This is a single compound check: ALL sub-conditions must pass together
    try:
        merged_branches_that_should_be_gone = [
            'feature/completed-api',
            'feature/old-ui',
            'hotfix/minor-fix'
        ]
        all_merged_deleted = True
        for branch in merged_branches_that_should_be_gone:
            if branch in branches:
                all_merged_deleted = False
                print(f"  FAIL: Branch '{branch}' still exists but should be deleted")
            else:
                print(f"  OK: Branch '{branch}' is deleted")

        in_progress_preserved = 'feature/in-progress' in branches
        main_preserved = 'main' in branches

        if not in_progress_preserved:
            print(f"  FAIL: feature/in-progress was incorrectly deleted")
        if not main_preserved:
            print(f"  FAIL: main branch is missing")

        if all_merged_deleted and in_progress_preserved and main_preserved:
            print(f"PASS: Component 1 — Branch cleanup correct: merged branches deleted, non-merged and main preserved (0.35 pts)")
            total_score += 0.35
        elif all_merged_deleted:
            # Merged branches deleted but something else is wrong — partial credit
            partial = 0.25
            print(f"PARTIAL: Component 1 — Merged branches deleted but branch preservation issue ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — Not all merged branches are deleted")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: git global alias 'cleanmerged' is set (0.25 points)
    try:
        stdout, stderr, rc = run_git(['config', '--global', 'alias.cleanmerged'])
        if rc == 0 and stdout.strip():
            print(f"PASS: Component 2 — git alias cleanmerged is set: '{stdout.strip()}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — git alias cleanmerged not set (rc={rc}, stdout='{stdout}')")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: .vscode/tasks.json exists with correct task definition (0.25 points)
    try:
        tasks_path = os.path.join(REPO_DIR, '.vscode', 'tasks.json')
        if not os.path.exists(tasks_path):
            print(f"FAIL: Component 3 — .vscode/tasks.json does not exist")
        else:
            with open(tasks_path, 'r') as f:
                tasks_data = json.load(f)

            tasks_list = tasks_data.get('tasks', [])
            found_correct_task = False
            for task in tasks_list:
                label = task.get('label', '')
                command = task.get('command', '')
                # Check label matches and command references git cleanmerged
                if 'Clean Merged Branches' in label and 'cleanmerged' in command:
                    found_correct_task = True
                    break

            if found_correct_task:
                print(f"PASS: Component 3 — tasks.json has 'Git: Clean Merged Branches' task with 'git cleanmerged' command (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — tasks.json exists but missing correct task definition. Tasks: {[t.get('label') for t in tasks_list]}")
    except json.JSONDecodeError as e:
        print(f"ERROR: Component 3 — tasks.json is not valid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: tasks.json is committed to the repository (0.15 points)
    try:
        # Check if .vscode/tasks.json is tracked by git (appears in git ls-files)
        stdout, stderr, rc = run_git(['ls-files', '.vscode/tasks.json'])
        if stdout.strip() == '.vscode/tasks.json':
            # Also verify it's not just staged but actually committed
            status_out, _, _ = run_git(['status', '--porcelain', '.vscode/tasks.json'])
            if not status_out.strip():
                print(f"PASS: Component 4 — tasks.json is committed to the repository (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — tasks.json is staged but not committed (status: '{status_out.strip()}')")
        else:
            print(f"FAIL: Component 4 — tasks.json is not tracked by git (ls-files: '{stdout.strip()}')")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
