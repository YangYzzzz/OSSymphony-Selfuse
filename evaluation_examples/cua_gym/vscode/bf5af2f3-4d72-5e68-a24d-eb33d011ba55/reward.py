"""
Reward Script: Revert replica count hunk in deployment.yaml via VSCode inline diff editor
Task ID: vscode_ops_051
Domain: vscode
Scoring:
  - Component 1 (0.40): replicas reverted to 3 in working copy
  - Component 2 (0.30): deployment.yaml has unstaged changes in git
  - Component 3 (0.30): the unstaged diff only changes replicas (selective revert)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_051'
REPO_DIR = os.path.join(WORKDIR, TASK_ID)
DEPLOY_FILE = os.path.join(REPO_DIR, 'deployment.yaml')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: deployment.yaml must exist
    if not os.path.exists(DEPLOY_FILE):
        print(f"CRITICAL: deployment.yaml not found at {DEPLOY_FILE}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(DEPLOY_FILE, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read {DEPLOY_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: replicas is 3 in the working copy (0.40 points)
    # In initial_env, replicas is 5 (from the last commit). After revert, it should be 3.
    try:
        replicas_match = re.search(r'^\s*replicas:\s*(\d+)', content, re.MULTILINE)
        if replicas_match:
            replica_count = int(replicas_match.group(1))
            if replica_count == 3:
                print(f"PASS: Component 1 -- replicas is 3 (reverted from 5) (0.40 pts)")
                total_score += 0.40
            else:
                print(f"FAIL: Component 1 -- expected replicas: 3, found replicas: {replica_count}")
        else:
            print("FAIL: Component 1 -- no 'replicas:' field found in deployment.yaml")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: deployment.yaml has unstaged changes (0.30 points)
    # Reverting a hunk in the inline diff editor creates an unstaged modification.
    # In initial_env, working tree is clean (no unstaged changes).
    try:
        git_dir = os.path.join(REPO_DIR, '.git')
        if os.path.isdir(git_dir):
            git_diff_names = os.popen(f'cd {REPO_DIR} && git diff --name-only 2>/dev/null').read().strip()
            if 'deployment.yaml' in git_diff_names:
                print(f"PASS: Component 2 -- deployment.yaml has unstaged changes (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 -- deployment.yaml has no unstaged changes (git diff --name-only: '{git_diff_names}')")
        else:
            print(f"FAIL: Component 2 -- .git directory not found at {git_dir}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: The unstaged diff only touches replicas, not the image tag (0.30 points)
    # This verifies selective revert: only the replica hunk was reverted, not the image hunk.
    # In initial_env, there is no diff at all, so this fails.
    try:
        git_dir = os.path.join(REPO_DIR, '.git')
        if os.path.isdir(git_dir):
            git_diff = os.popen(f'cd {REPO_DIR} && git diff -- deployment.yaml 2>/dev/null').read().strip()
            if git_diff:
                # The diff should contain the replicas change (5 -> 3)
                has_replica_change = ('+  replicas: 3' in git_diff or '+  replicas:  3' in git_diff) and \
                                    ('-  replicas: 5' in git_diff or '-  replicas:  5' in git_diff)
                # The diff should NOT contain image tag changes
                has_image_change = 'web-frontend:v2.1.0' in git_diff or 'version: v2.1.0' in git_diff
                if has_replica_change and not has_image_change:
                    print(f"PASS: Component 3 -- diff only reverts replicas, image tag untouched (0.30 pts)")
                    total_score += 0.30
                elif has_replica_change and has_image_change:
                    print(f"FAIL: Component 3 -- diff also reverts image tag (should only revert replicas)")
                else:
                    print(f"FAIL: Component 3 -- diff does not show expected replicas revert. Diff:\n{git_diff}")
            else:
                print(f"FAIL: Component 3 -- no diff found for deployment.yaml (no unstaged changes)")
        else:
            print(f"FAIL: Component 3 -- .git directory not found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
