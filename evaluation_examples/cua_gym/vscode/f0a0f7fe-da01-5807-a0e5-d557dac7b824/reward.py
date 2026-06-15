"""
Reward Script: Git worktree workflow with VSCode
Task ID: vscode_gf6_017
Domain: vscode
Scoring:
  - Component 1: Worktree list has 3 entries (0.15)
  - Component 2: Hotfix worktree exists on correct branch (0.15)
  - Component 3: Feature worktree exists on correct branch (0.15)
  - Component 4: Hotfix tokens.py uses time.time_ns() (0.20)
  - Component 5: Feature dashboard/views.py has DashboardView class (0.20)
  - Component 6: Workspace file references all 3 folders (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_017'

MAIN_REPO = os.path.join(WORKDIR, 'projects', 'git-worktree-workflow')
HOTFIX_DIR = os.path.join(WORKDIR, 'projects', 'git-worktree-workflow-hotfix')
FEATURE_DIR = os.path.join(WORKDIR, 'projects', 'git-worktree-workflow-feature')
WORKSPACE_FILE = os.path.join(WORKDIR, 'projects', 'projects.code-workspace')


def get_git_worktree_list():
    """Parse git worktree list output by reading .git/worktrees directory."""
    worktrees = []
    # The main repo is always a worktree
    git_dir = os.path.join(MAIN_REPO, '.git')
    if os.path.isdir(git_dir):
        # Check for linked worktrees
        worktrees_dir = os.path.join(git_dir, 'worktrees')
        # Main worktree always counts
        worktrees.append(MAIN_REPO)
        if os.path.isdir(worktrees_dir):
            for name in os.listdir(worktrees_dir):
                wt_path = os.path.join(worktrees_dir, name)
                if os.path.isdir(wt_path):
                    # Read the gitdir file to find the worktree path
                    gitdir_file = os.path.join(wt_path, 'gitdir')
                    if os.path.exists(gitdir_file):
                        with open(gitdir_file) as f:
                            # gitdir points to the .git file in the worktree
                            gt = f.read().strip()
                            wt_root = os.path.dirname(gt)
                            worktrees.append(wt_root)
    return worktrees


def get_worktree_branch(worktree_path):
    """Get the branch checked out in a worktree."""
    git_file = os.path.join(worktree_path, '.git')
    if os.path.isfile(git_file):
        # Linked worktree: .git is a file pointing to the main repo's worktrees dir
        with open(git_file) as f:
            content = f.read().strip()
        # Format: gitdir: /path/to/main/.git/worktrees/<name>
        if content.startswith('gitdir:'):
            wt_git_dir = content.split(':', 1)[1].strip()
            head_file = os.path.join(wt_git_dir, 'HEAD')
            if os.path.exists(head_file):
                with open(head_file) as f:
                    head = f.read().strip()
                if head.startswith('ref: refs/heads/'):
                    return head[len('ref: refs/heads/'):]
    elif os.path.isdir(git_file):
        # Main worktree
        head_file = os.path.join(git_file, 'HEAD')
        if os.path.exists(head_file):
            with open(head_file) as f:
                head = f.read().strip()
            if head.startswith('ref: refs/heads/'):
                return head[len('ref: refs/heads/'):]
    return None


def verify_task():
    """Verify task completion with progressive scoring."""
    total_score = 0.0

    # Component 1: Worktree list has 3 entries (0.15 points)
    # Initial env has only 1 worktree; golden should have 3
    try:
        worktrees = get_git_worktree_list()
        wt_count = len(worktrees)
        if wt_count >= 3:
            print(f"PASS: Component 1 — worktree count is {wt_count} (>= 3) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — expected >= 3 worktrees, found {wt_count}: {worktrees}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Hotfix worktree exists with branch hotfix/fix-auth-token (0.15 points)
    try:
        if os.path.isdir(HOTFIX_DIR):
            branch = get_worktree_branch(HOTFIX_DIR)
            if branch == 'hotfix/fix-auth-token':
                print(f"PASS: Component 2 — hotfix worktree on branch '{branch}' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — hotfix worktree branch is '{branch}', expected 'hotfix/fix-auth-token'")
        else:
            print(f"FAIL: Component 2 — hotfix worktree directory does not exist: {HOTFIX_DIR}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Feature worktree exists with branch feature/new-dashboard (0.15 points)
    try:
        if os.path.isdir(FEATURE_DIR):
            branch = get_worktree_branch(FEATURE_DIR)
            if branch == 'feature/new-dashboard':
                print(f"PASS: Component 3 — feature worktree on branch '{branch}' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — feature worktree branch is '{branch}', expected 'feature/new-dashboard'")
        else:
            print(f"FAIL: Component 3 — feature worktree directory does not exist: {FEATURE_DIR}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Hotfix tokens.py uses time.time_ns() instead of time.time() (0.20 points)
    # In initial env, tokens.py has time.time(); golden should have time.time_ns()
    try:
        hotfix_tokens = os.path.join(HOTFIX_DIR, 'auth', 'tokens.py')
        if os.path.exists(hotfix_tokens):
            with open(hotfix_tokens) as f:
                content = f.read()
            # Check that time.time_ns() is used (the fix)
            has_time_ns = 'time.time_ns()' in content
            # Check that the old time.time() pattern is NOT present in the timestamp line
            # We need to be careful: time.time() is a substring of time.time_ns()
            # Look for standalone time.time() (not time.time_ns())
            has_old_time = bool(re.search(r'time\.time\(\)', content))
            if has_time_ns and not has_old_time:
                print(f"PASS: Component 4 — hotfix tokens.py uses time.time_ns() (0.20 pts)")
                total_score += 0.20
            elif has_time_ns and has_old_time:
                print(f"PARTIAL: Component 4 — tokens.py has time.time_ns() but also time.time() (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 — tokens.py does not use time.time_ns(). Has time.time_ns(): {has_time_ns}")
        else:
            print(f"FAIL: Component 4 — hotfix tokens.py not found at {hotfix_tokens}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Feature dashboard/views.py exists with DashboardView class (0.20 points)
    # In initial env, dashboard/ only has __init__.py; golden should have views.py with DashboardView
    try:
        feature_views = os.path.join(FEATURE_DIR, 'dashboard', 'views.py')
        if os.path.exists(feature_views):
            with open(feature_views) as f:
                content = f.read()
            # Check for class DashboardView definition
            if re.search(r'class\s+DashboardView', content):
                print(f"PASS: Component 5 — dashboard/views.py has DashboardView class (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 5 — dashboard/views.py exists but no DashboardView class found")
        else:
            print(f"FAIL: Component 5 — dashboard/views.py not found at {feature_views}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Workspace file references all 3 folders (0.15 points)
    # In initial env, no workspace file exists; golden should have one with all 3 paths
    try:
        if os.path.exists(WORKSPACE_FILE):
            with open(WORKSPACE_FILE) as f:
                ws = json.load(f)
            folders = ws.get('folders', [])
            folder_paths = [f.get('path', '') for f in folders]

            # Check that all 3 worktree paths are referenced
            has_main = any('git-worktree-workflow' in p and 'hotfix' not in p and 'feature' not in p for p in folder_paths)
            has_hotfix = any('git-worktree-workflow-hotfix' in p for p in folder_paths)
            has_feature = any('git-worktree-workflow-feature' in p for p in folder_paths)

            if has_main and has_hotfix and has_feature:
                print(f"PASS: Component 6 — workspace file references all 3 folders (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 6 — workspace missing folders. main={has_main}, hotfix={has_hotfix}, feature={has_feature}. Paths: {folder_paths}")
        else:
            # Also check in the main repo directory
            alt_workspace = os.path.join(MAIN_REPO, 'projects.code-workspace')
            if os.path.exists(alt_workspace):
                with open(alt_workspace) as f:
                    ws = json.load(f)
                folders = ws.get('folders', [])
                folder_paths = [f.get('path', '') for f in folders]
                has_main = any('git-worktree-workflow' in p and 'hotfix' not in p and 'feature' not in p for p in folder_paths)
                has_hotfix = any('git-worktree-workflow-hotfix' in p for p in folder_paths)
                has_feature = any('git-worktree-workflow-feature' in p for p in folder_paths)
                if has_main and has_hotfix and has_feature:
                    print(f"PASS: Component 6 — workspace file at alt path references all 3 folders (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 6 — alt workspace missing folders. Paths: {folder_paths}")
            else:
                print(f"FAIL: Component 6 — workspace file not found at {WORKSPACE_FILE} or {alt_workspace}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
