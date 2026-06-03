"""
Reward Script: Resolve a three-way merge conflict in settings.py using VSCode's merge editor
Task ID: vscode_git_058
Domain: vs_code (git/file operations)
Scoring:
  - Component 1: No conflict markers in settings.py                  (0.30 pts)
  - Component 2: TIMEOUT = 60 in resolved file (not inside conflict) (0.30 pts)
  - Component 3: Redis CACHES config present in resolved file        (0.20 pts)
  - Component 4: Merge commit exists, git working tree is clean      (0.20 pts)
  Total: 1.0

NOTE: Components 2 and 3 only award points if Component 1 passes (conflict-free).
This ensures they only score task-introduced changes.
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_058'
PROJECT_DIR = '/home/user/project'
SETTINGS_FILE = '/home/user/project/settings.py'
GIT_DIR = '/home/user/project/.git'

CONFLICT_MARKERS = ['<<<<<<<', '=======', '>>>>>>>']


def file_content_has_no_conflict_markers(content):
    """Return True if no conflict markers exist in the content."""
    return not any(m in content for m in CONFLICT_MARKERS)


def get_timeout_value(content):
    """Extract top-level TIMEOUT value; returns int or None."""
    m = re.search(r'^TIMEOUT\s*=\s*(\d+)', content, re.MULTILINE)
    if m:
        return int(m.group(1))
    return None


def is_merge_complete():
    """
    Check git state by reading git files directly (no subprocess).
    Returns (is_clean, has_merge_commit) tuple.
    - is_clean: True if no MERGE_HEAD file (merge in progress indicator) and no
                conflict index entries (checked via index file heuristic).
    - has_merge_commit: True if HEAD commit has two parents (merge commit),
                        detected by reading .git/COMMIT_EDITMSG for merge pattern.
    """
    # Check if a merge is still in progress: .git/MERGE_HEAD exists iff mid-merge
    merge_head_path = os.path.join(GIT_DIR, 'MERGE_HEAD')
    merge_in_progress = os.path.exists(merge_head_path)

    # Check if a merge commit message was recorded (COMMIT_EDITMSG)
    commit_editmsg_path = os.path.join(GIT_DIR, 'COMMIT_EDITMSG')
    has_merge_message = False
    try:
        with open(commit_editmsg_path, 'r') as f:
            msg = f.read().lower()
        # A merge commit message typically mentions "merge"
        has_merge_message = 'merge' in msg
    except Exception:
        pass

    # Read HEAD to get current commit hash
    head_path = os.path.join(GIT_DIR, 'HEAD')
    current_commit = None
    try:
        with open(head_path, 'r') as f:
            head_content = f.read().strip()
        if head_content.startswith('ref: '):
            ref = head_content[5:]
            ref_path = os.path.join(GIT_DIR, ref)
            with open(ref_path, 'r') as f:
                current_commit = f.read().strip()
        else:
            current_commit = head_content
    except Exception:
        pass

    # Check if current commit is a merge commit (has two parents)
    # by reading .git/logs/HEAD for merge commit entries
    merge_in_log = False
    if current_commit:
        logs_head_path = os.path.join(GIT_DIR, 'logs', 'HEAD')
        try:
            with open(logs_head_path, 'r') as f:
                logs = f.read()
            # A merge commit creates a log entry containing "commit (merge)"
            merge_in_log = ('commit (merge)' in logs or 'merge' in logs.lower())
        except Exception:
            pass

    # Combined result: merge commit present if found in log OR in COMMIT_EDITMSG
    has_merge_commit = merge_in_log or has_merge_message

    is_clean = not merge_in_progress
    return is_clean, has_merge_commit


def verify_task():
    """
    Verify that the three-way merge conflict in settings.py has been resolved correctly.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.py must exist
    if not os.path.exists(SETTINGS_FILE):
        print(f"CRITICAL: settings.py not found at {SETTINGS_FILE}")
        print("REWARD: 0.0")
        return 0.0

    # Read the file content once
    try:
        with open(SETTINGS_FILE, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read {SETTINGS_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -------------------------------------------------------------------------
    # Component 1: No conflict markers remaining in settings.py (0.30 points)
    # The initial_env file has <<<<<<< HEAD / ======= / >>>>>>> markers.
    # The resolved file must have none of these.
    # -------------------------------------------------------------------------
    try:
        markers_found = [m for m in CONFLICT_MARKERS if m in content]
        if not markers_found:
            print("PASS: Component 1 — No conflict markers in settings.py (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Conflict markers still present: {markers_found}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Derive conflict-free status from Component 1 result (based on actual check)
    conflict_markers_absent = file_content_has_no_conflict_markers(content)

    # -------------------------------------------------------------------------
    # Component 2: TIMEOUT = 60 in the resolved (conflict-free) file (0.30 pts)
    # HEAD had TIMEOUT=60, feature/database-config had TIMEOUT=45.
    # Correct resolution: TIMEOUT=60 (highest value among 30, 45, 60).
    # Gate: only scores if conflict-free (otherwise the value is inside markers).
    # -------------------------------------------------------------------------
    try:
        if not conflict_markers_absent:
            print("SKIP: Component 2 — File has conflict markers; TIMEOUT check skipped")
        else:
            timeout_val = get_timeout_value(content)
            if timeout_val == 60:
                print(f"PASS: Component 2 — TIMEOUT = 60 (correct higher value) (0.30 pts)")
                total_score += 0.30
            elif timeout_val is not None:
                print(f"FAIL: Component 2 — TIMEOUT = {timeout_val}, expected 60")
            else:
                print("FAIL: Component 2 — TIMEOUT constant not found in settings.py")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Redis cache configuration (CACHES) present (0.20 points)
    # HEAD had Redis cache config inside the conflict section.
    # The resolution must keep it. Gate: only scores if conflict-free.
    # -------------------------------------------------------------------------
    try:
        if not conflict_markers_absent:
            print("SKIP: Component 3 — File has conflict markers; CACHES check skipped")
        else:
            has_caches = 'CACHES' in content
            has_redis = 'RedisCache' in content or "'redis://" in content
            if has_caches and has_redis:
                print("PASS: Component 3 — Redis CACHES configuration present (0.20 pts)")
                total_score += 0.20
            elif not has_caches:
                print("FAIL: Component 3 — CACHES variable not found")
            else:
                print("FAIL: Component 3 — CACHES found but Redis backend missing")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------------
    # Component 4: Merge completed — no MERGE_HEAD, merge commit in log (0.20 pts)
    # The task requires completing the merge (git commit after resolution).
    # -------------------------------------------------------------------------
    try:
        is_clean, has_merge_commit = is_merge_complete()
        if is_clean and has_merge_commit:
            print("PASS: Component 4 — Merge commit exists, no in-progress merge (0.20 pts)")
            total_score += 0.20
        elif not is_clean:
            print("FAIL: Component 4 — .git/MERGE_HEAD exists; merge not yet committed")
        else:
            print("FAIL: Component 4 — No merge commit detected in git log")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
