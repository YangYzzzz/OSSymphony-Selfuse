"""
Reward Script: Resolve merge conflict in package.json and complete merge commit
Task ID: vscode_git_052
Domain: vs_code (git)
Scoring:
  Component 1: package.json has no merge conflict markers (0.3 pts)
  Component 2: Both axios and chart.js dependencies present with correct versions in valid JSON (0.4 pts)
  Component 3: Merge commit completed -- no MERGE_HEAD and git index clean (0.3 pts)
Total: 1.0
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_052'
REPO_PATH = '/home/user/webapp'
PACKAGE_JSON_PATH = os.path.join(REPO_PATH, 'package.json')
GIT_DIR = os.path.join(REPO_PATH, '.git')


def read_git_file(rel_path):
    """Read a file from the .git directory, return stripped content or None."""
    path = os.path.join(GIT_DIR, rel_path)
    try:
        with open(path, 'r') as f:
            return f.read().strip()
    except (FileNotFoundError, IOError):
        return None


def count_git_commits():
    """Count commits by following parent chain from HEAD."""
    try:
        # Read HEAD ref
        head_content = read_git_file('HEAD')
        if head_content is None:
            return 0

        if head_content.startswith('ref: '):
            ref_path = head_content[5:]  # e.g. refs/heads/main
            head_sha = read_git_file(ref_path)
        else:
            head_sha = head_content  # detached HEAD

        if not head_sha:
            return 0
        return head_sha  # Return SHA to identify merge commit
    except Exception:
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: package.json must exist
    if not os.path.exists(PACKAGE_JSON_PATH):
        print(f"CRITICAL: package.json not found at {PACKAGE_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Read package.json content
    try:
        with open(PACKAGE_JSON_PATH, 'r') as f:
            raw_content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read package.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: No merge conflict markers in package.json (0.3 points)
    # Initial state has <<<<<<< HEAD, =======, >>>>>>> feature/analytics
    # Golden state has none of these
    try:
        conflict_markers = ['<<<<<<< HEAD', '=======', '>>>>>>> feature/analytics']
        has_conflict_marker = any(marker in raw_content for marker in conflict_markers)

        if not has_conflict_marker:
            print("PASS: Component 1 — No merge conflict markers in package.json (0.3 pts)")
            total_score += 0.3
        else:
            found_markers = [m for m in conflict_markers if m in raw_content]
            print(f"FAIL: Component 1 — Conflict markers still present in package.json: {found_markers}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Both axios and chart.js present in dependencies with correct versions (0.4 points)
    # Initial state: JSON invalid (conflict markers), missing one dependency
    # Golden state: valid JSON with both "axios": "^1.4.0" and "chart.js": "^4.3.0"
    try:
        pkg_data = json.loads(raw_content)
        deps = pkg_data.get('dependencies', {})

        axios_ok = deps.get('axios') == '^1.4.0'
        chartjs_ok = deps.get('chart.js') == '^4.3.0'

        if axios_ok and chartjs_ok:
            print(f"PASS: Component 2 — Both axios (^1.4.0) and chart.js (^4.3.0) present in dependencies (0.4 pts)")
            total_score += 0.4
        else:
            missing = []
            if not axios_ok:
                missing.append(f"axios: expected '^1.4.0', got {deps.get('axios', '<missing>')!r}")
            if not chartjs_ok:
                missing.append(f"chart.js: expected '^4.3.0', got {deps.get('chart.js', '<missing>')!r}")
            print(f"FAIL: Component 2 — Dependencies check failed: {'; '.join(missing)}")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 2 — package.json is not valid JSON (likely still has conflict markers): {e}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Merge commit completed (no MERGE_HEAD, no unmerged index entries) (0.3 points)
    # Initial state: MERGE_HEAD exists (mid-merge), git index has UU (unmerged) entries
    # Golden state: MERGE_HEAD absent, index is clean, HEAD points to a merge commit
    try:
        # Check that MERGE_HEAD does NOT exist (mid-merge indicator)
        merge_head_exists = os.path.exists(os.path.join(GIT_DIR, 'MERGE_HEAD'))

        # Check git index for unmerged entries by reading MERGE_MSG (present during merge)
        merge_msg_exists = os.path.exists(os.path.join(GIT_DIR, 'MERGE_MSG'))

        # Read the current HEAD commit SHA
        head_sha = count_git_commits()

        # Verify there's a ORIG_HEAD (set after merge completes) in the golden env
        # OR verify HEAD SHA is a merge commit by checking the commit object parents
        orig_head_exists = os.path.exists(os.path.join(GIT_DIR, 'ORIG_HEAD'))

        if not merge_head_exists and orig_head_exists:
            print(f"PASS: Component 3 — Merge commit completed: MERGE_HEAD absent, ORIG_HEAD present (merge finished) (0.3 pts)")
            total_score += 0.3
        elif not merge_head_exists and not merge_msg_exists:
            print(f"PASS: Component 3 — Merge commit completed: no MERGE_HEAD or MERGE_MSG (merge finished) (0.3 pts)")
            total_score += 0.3
        else:
            issues = []
            if merge_head_exists:
                issues.append("MERGE_HEAD exists — merge is still in progress, not committed")
            if merge_msg_exists and not orig_head_exists:
                issues.append("MERGE_MSG present but ORIG_HEAD absent — merge may not be committed")
            print(f"FAIL: Component 3 — Merge commit not completed: {'; '.join(issues)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
