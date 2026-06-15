"""
Reward Script: Set up multi-remote git configuration with bare repos and push branches selectively.
Task ID: vscode_git_071
Domain: vs_code (git operations)
Scoring:
  - Component 1: Bare repos /tmp/origin.git and /tmp/backup.git exist and are valid (0.2 pts)
  - Component 2: Remotes 'origin' and 'backup' configured correctly in /home/user/project (0.2 pts)
  - Component 3: 'main' branch pushed to both remotes (0.2 pts)
  - Component 4: 'develop' branch pushed to origin only (not backup) (0.2 pts)
  - Component 5: 'experimental' branch pushed to backup only (not origin) (0.2 pts)
"""

import os
import subprocess

WORKDIR = '/home/user'
PROJECT_DIR = '/home/user/project'
ORIGIN_GIT = '/tmp/origin.git'
BACKUP_GIT = '/tmp/backup.git'
TASK_ID = 'vscode_git_071'


def run_git(args, cwd=None):
    """Run a git command and return (stdout, stderr, returncode)."""
    try:
        result = subprocess.run(
            ['git'] + args,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return '', str(e), -1


def verify_task():
    """
    Verify the multi-remote git configuration task completion.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: project directory must exist and be a git repo
    if not os.path.isdir(PROJECT_DIR):
        print(f"CRITICAL: Project directory {PROJECT_DIR} not found")
        print("REWARD: 0.0")
        return 0.0

    stdout, stderr, rc = run_git(['rev-parse', '--git-dir'], cwd=PROJECT_DIR)
    if rc != 0:
        print(f"CRITICAL: {PROJECT_DIR} is not a git repository: {stderr}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Bare repos /tmp/origin.git and /tmp/backup.git exist and are valid (0.2 pts)
    try:
        origin_is_bare = False
        backup_is_bare = False

        # Check /tmp/origin.git is a valid bare repository
        if os.path.isdir(ORIGIN_GIT):
            stdout, _, rc = run_git(['rev-parse', '--is-bare-repository'], cwd=ORIGIN_GIT)
            if rc == 0 and stdout.strip() == 'true':
                origin_is_bare = True

        # Check /tmp/backup.git is a valid bare repository
        if os.path.isdir(BACKUP_GIT):
            stdout, _, rc = run_git(['rev-parse', '--is-bare-repository'], cwd=BACKUP_GIT)
            if rc == 0 and stdout.strip() == 'true':
                backup_is_bare = True

        if origin_is_bare and backup_is_bare:
            print(f"PASS: Component 1 — Both bare repos exist: {ORIGIN_GIT} and {BACKUP_GIT} (0.2 pts)")
            total_score += 0.2
        else:
            if not origin_is_bare:
                print(f"FAIL: Component 1 — {ORIGIN_GIT} is not a valid bare repository")
            if not backup_is_bare:
                print(f"FAIL: Component 1 — {BACKUP_GIT} is not a valid bare repository")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Remotes 'origin' and 'backup' configured with correct URLs (0.2 pts)
    try:
        origin_url = None
        backup_url = None

        stdout, _, rc = run_git(['remote', 'get-url', 'origin'], cwd=PROJECT_DIR)
        if rc == 0:
            origin_url = stdout.strip()

        stdout, _, rc = run_git(['remote', 'get-url', 'backup'], cwd=PROJECT_DIR)
        if rc == 0:
            backup_url = stdout.strip()

        origin_ok = (origin_url == ORIGIN_GIT)
        backup_ok = (backup_url == BACKUP_GIT)

        if origin_ok and backup_ok:
            print(f"PASS: Component 2 — Both remotes configured: origin={origin_url}, backup={backup_url} (0.2 pts)")
            total_score += 0.2
        else:
            if not origin_ok:
                print(f"FAIL: Component 2 — 'origin' remote URL: expected {ORIGIN_GIT}, found {origin_url!r}")
            if not backup_ok:
                print(f"FAIL: Component 2 — 'backup' remote URL: expected {BACKUP_GIT}, found {backup_url!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'main' branch pushed to BOTH remotes (0.2 pts)
    try:
        # Get branches in origin.git
        stdout_origin, _, rc_o = run_git(['branch'], cwd=ORIGIN_GIT)
        origin_branches = [b.strip().lstrip('* ') for b in stdout_origin.splitlines() if b.strip()]

        # Get branches in backup.git
        stdout_backup, _, rc_b = run_git(['branch'], cwd=BACKUP_GIT)
        backup_branches = [b.strip().lstrip('* ') for b in stdout_backup.splitlines() if b.strip()]

        origin_has_main = 'main' in origin_branches
        backup_has_main = 'main' in backup_branches

        if origin_has_main and backup_has_main:
            print(f"PASS: Component 3 — 'main' branch exists in both remotes (origin branches: {origin_branches}, backup branches: {backup_branches}) (0.2 pts)")
            total_score += 0.2
        else:
            if not origin_has_main:
                print(f"FAIL: Component 3 — 'main' not found in origin remote. Branches: {origin_branches}")
            if not backup_has_main:
                print(f"FAIL: Component 3 — 'main' not found in backup remote. Branches: {backup_branches}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 'develop' branch pushed to origin ONLY (not backup) (0.2 pts)
    try:
        # Get branches in origin.git (already retrieved above but re-check fresh)
        stdout_origin, _, rc_o = run_git(['branch'], cwd=ORIGIN_GIT)
        origin_branches_4 = [b.strip().lstrip('* ') for b in stdout_origin.splitlines() if b.strip()]

        stdout_backup, _, rc_b = run_git(['branch'], cwd=BACKUP_GIT)
        backup_branches_4 = [b.strip().lstrip('* ') for b in stdout_backup.splitlines() if b.strip()]

        origin_has_develop = 'develop' in origin_branches_4
        backup_no_develop = 'develop' not in backup_branches_4

        if origin_has_develop and backup_no_develop:
            print(f"PASS: Component 4 — 'develop' pushed to origin only (not in backup) (0.2 pts)")
            total_score += 0.2
        else:
            if not origin_has_develop:
                print(f"FAIL: Component 4 — 'develop' not found in origin. Origin branches: {origin_branches_4}")
            if not backup_no_develop:
                print(f"FAIL: Component 4 — 'develop' found in backup (should NOT be there). Backup branches: {backup_branches_4}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: 'experimental' branch pushed to backup ONLY (not origin) (0.2 pts)
    try:
        # Get branches in origin.git
        stdout_origin, _, rc_o = run_git(['branch'], cwd=ORIGIN_GIT)
        origin_branches_5 = [b.strip().lstrip('* ') for b in stdout_origin.splitlines() if b.strip()]

        stdout_backup, _, rc_b = run_git(['branch'], cwd=BACKUP_GIT)
        backup_branches_5 = [b.strip().lstrip('* ') for b in stdout_backup.splitlines() if b.strip()]

        backup_has_experimental = 'experimental' in backup_branches_5
        origin_no_experimental = 'experimental' not in origin_branches_5

        if backup_has_experimental and origin_no_experimental:
            print(f"PASS: Component 5 — 'experimental' pushed to backup only (not in origin) (0.2 pts)")
            total_score += 0.2
        else:
            if not backup_has_experimental:
                print(f"FAIL: Component 5 — 'experimental' not found in backup. Backup branches: {backup_branches_5}")
            if not origin_no_experimental:
                print(f"FAIL: Component 5 — 'experimental' found in origin (should NOT be there). Origin branches: {origin_branches_5}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
