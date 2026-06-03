"""
Reward Script: Cherry-pick commit (Add logging utility) from 'feature/utils' onto 'hotfix/logging'
Task ID: vscode_git_028
Domain: vs_code (git operations)
Scoring:
  Component 1 (0.4): utils/logger.py exists on hotfix/logging branch (file was cherry-picked)
  Component 2 (0.3): HEAD commit message on hotfix/logging matches cherry-pick message
  Component 3 (0.3): utils/logger.py contains expected functions (content integrity check)

No subprocess usage — git internals are read via Python zlib/file I/O directly.
"""

import os
import zlib

PROJECT_DIR = '/home/user/project'
TASK_ID = 'vscode_git_028'
EXPECTED_COMMIT_MSG = 'Add logging utility with rotating file handler support'


def read_git_object(git_dir, sha):
    """
    Read and decompress a git object by its SHA.
    Returns (obj_type, content_bytes) or (None, None) on error.
    """
    obj_path = os.path.join(git_dir, 'objects', sha[:2], sha[2:])
    try:
        with open(obj_path, 'rb') as f:
            data = zlib.decompress(f.read())
        null_idx = data.index(b'\x00')
        header = data[:null_idx].decode('utf-8', errors='replace')
        content = data[null_idx + 1:]
        obj_type = header.split()[0]
        return obj_type, content
    except Exception as e:
        return None, None


def get_current_branch(git_dir):
    """Read the current branch name from .git/HEAD."""
    try:
        head_path = os.path.join(git_dir, 'HEAD')
        with open(head_path, 'r') as f:
            content = f.read().strip()
        # Format: "ref: refs/heads/<branch>"
        if content.startswith('ref: refs/heads/'):
            return content[len('ref: refs/heads/'):]
        return None
    except Exception:
        return None


def get_branch_head_sha(git_dir, branch_name):
    """Get the HEAD commit SHA for a branch."""
    try:
        ref_path = os.path.join(git_dir, 'refs', 'heads', branch_name)
        with open(ref_path, 'r') as f:
            return f.read().strip()
    except Exception:
        return None


def get_commit_message(git_dir, sha):
    """
    Extract the commit message (first line of body) from a git commit object.
    Returns the message string or None on error.
    """
    obj_type, content = read_git_object(git_dir, sha)
    if obj_type != 'commit' or content is None:
        return None
    try:
        text = content.decode('utf-8', errors='replace')
        # Commit format: headers\n\ncommit message\n
        # Split on double newline to get message
        parts = text.split('\n\n', 1)
        if len(parts) < 2:
            return None
        message = parts[1].strip()
        # Return first line (subject)
        return message.split('\n')[0].strip()
    except Exception:
        return None


def verify_task():
    """
    Verify that the logging utility commit was cherry-picked onto hotfix/logging.
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0
    git_dir = os.path.join(PROJECT_DIR, '.git')

    # Precondition gate: project must be a git repository
    if not os.path.isdir(git_dir):
        print(f"CRITICAL: {PROJECT_DIR} is not a git repository (no .git dir)")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: must be on hotfix/logging branch
    current_branch = get_current_branch(git_dir)
    if current_branch != 'hotfix/logging':
        print(f"CRITICAL: Not on hotfix/logging branch (found: {current_branch})")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: On branch '{current_branch}', proceeding with verification.")

    # Get HEAD SHA for hotfix/logging
    head_sha = get_branch_head_sha(git_dir, 'hotfix/logging')
    if not head_sha:
        print("CRITICAL: Cannot resolve HEAD SHA for hotfix/logging")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: hotfix/logging HEAD SHA: {head_sha}")

    # Component 1: utils/logger.py exists on hotfix/logging branch (0.4 points)
    # Fails on initial (no utils/logger.py in working tree), passes on golden (cherry-pick added it)
    try:
        logger_path = os.path.join(PROJECT_DIR, 'utils', 'logger.py')
        if os.path.isfile(logger_path):
            print("PASS: Component 1 — utils/logger.py exists on hotfix/logging branch (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — utils/logger.py not found at {logger_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: HEAD commit message matches the cherry-picked commit message (0.3 points)
    # Fails on initial (HEAD msg is "hotfix: improve startup output..."), passes on golden
    try:
        head_msg = get_commit_message(git_dir, head_sha)
        if head_msg == EXPECTED_COMMIT_MSG:
            print(f"PASS: Component 2 — HEAD commit message matches: '{head_msg}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected HEAD message '{EXPECTED_COMMIT_MSG}', found '{head_msg}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: utils/logger.py contains expected functions from cherry-picked commit (0.3 points)
    # Fails on initial (file doesn't exist), passes on golden (cherry-pick brought the correct content)
    try:
        logger_path = os.path.join(PROJECT_DIR, 'utils', 'logger.py')
        if os.path.isfile(logger_path):
            with open(logger_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            has_get_logger = 'def get_logger(' in content
            has_setup_file_logger = 'def setup_file_logger(' in content
            has_log_exception = 'def log_exception(' in content
            has_rotating_handler = 'RotatingFileHandler' in content
            if has_get_logger and has_setup_file_logger and has_log_exception and has_rotating_handler:
                print("PASS: Component 3 — utils/logger.py contains expected functions: "
                      "get_logger, setup_file_logger, log_exception, RotatingFileHandler (0.3 pts)")
                total_score += 0.3
            else:
                missing = []
                if not has_get_logger:
                    missing.append('get_logger')
                if not has_setup_file_logger:
                    missing.append('setup_file_logger')
                if not has_log_exception:
                    missing.append('log_exception')
                if not has_rotating_handler:
                    missing.append('RotatingFileHandler')
                print(f"FAIL: Component 3 — utils/logger.py missing expected symbols: {missing}")
        else:
            print("FAIL: Component 3 — utils/logger.py does not exist (cherry-pick not performed)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
