"""
Reward Script: Configure multi-root workspace with frontend and backend folders
Task ID: vscode_stu_059
Domain: vs_code
Scoring:
  Component 1 (0.3): A .code-workspace file exists somewhere under /home/user
  Component 2 (0.4): The workspace file contains both required folder paths
  Component 3 (0.3): The workspace file is valid JSON with proper multi-root structure
"""

import os
import json
import glob
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_059'

REQUIRED_FOLDERS = {
    '/home/user/webdev/frontend',
    '/home/user/webdev/backend',
}

# Normalize a folder path for comparison: expand ~, resolve, strip trailing slash
def normalize_path(p):
    p = p.strip()
    p = os.path.expanduser(p)
    p = os.path.normpath(p)
    return p


def find_workspace_files():
    """Find all .code-workspace files under /home/user (non-recursive in common locations)."""
    candidates = []
    # Search in home directory and common subdirectories
    for pattern in [
        os.path.join(WORKDIR, '*.code-workspace'),
        os.path.join(WORKDIR, '*', '*.code-workspace'),
        os.path.join(WORKDIR, 'Desktop', '*.code-workspace'),
        os.path.join(WORKDIR, 'Documents', '*.code-workspace'),
        os.path.join(WORKDIR, 'webdev', '*.code-workspace'),
        os.path.join(WORKDIR, '.config', 'Code', 'User', '*.code-workspace'),
    ]:
        candidates.extend(glob.glob(pattern))
    return list(set(candidates))


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Find workspace files
    ws_files = find_workspace_files()
    print(f"INFO: Found .code-workspace files: {ws_files}")

    if not ws_files:
        print("FAIL: No .code-workspace file found under /home/user")
        print("REWARD: 0.0")
        return 0.0

    # Try each workspace file — use the best scoring one
    best_score = 0.0
    best_file = None

    for ws_path in ws_files:
        score = 0.0

        # Component 1: Workspace file exists (0.3 points)
        if os.path.isfile(ws_path):
            print(f"PASS: Component 1 — workspace file exists: {ws_path} (0.3 pts)")
            score += 0.3
        else:
            print(f"FAIL: Component 1 — workspace file not accessible: {ws_path}")

        # Component 2: Contains both required folder paths (0.4 points)
        try:
            with open(ws_path, 'r') as f:
                content = f.read()
            # Strip JSONC comments before parsing
            cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            ws_data = json.loads(cleaned)

            folders = ws_data.get('folders', [])
            if not isinstance(folders, list):
                print(f"FAIL: Component 2 — 'folders' is not a list in {ws_path}")
            else:
                actual_paths = set()
                for folder in folders:
                    if isinstance(folder, dict) and 'path' in folder:
                        actual_paths.add(normalize_path(folder['path']))

                print(f"INFO: Actual folder paths (normalized): {actual_paths}")
                print(f"INFO: Required folder paths: {REQUIRED_FOLDERS}")

                matched = REQUIRED_FOLDERS.issubset(actual_paths)
                if matched:
                    print(f"PASS: Component 2 — both required folders present (0.4 pts)")
                    score += 0.4
                else:
                    missing = REQUIRED_FOLDERS - actual_paths
                    print(f"FAIL: Component 2 — missing folders: {missing}")

        except (json.JSONDecodeError, IOError) as e:
            print(f"ERROR: Component 2 — could not parse {ws_path}: {e}")

        # Component 3: Valid multi-root workspace structure (0.3 points)
        try:
            with open(ws_path, 'r') as f:
                content = f.read()
            cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            ws_data = json.loads(cleaned)

            folders = ws_data.get('folders', [])
            if isinstance(folders, list) and len(folders) >= 2:
                # Check that all folder entries have 'path' key
                all_valid = all(
                    isinstance(f, dict) and 'path' in f
                    for f in folders
                )
                if all_valid:
                    print(f"PASS: Component 3 — valid multi-root structure with {len(folders)} folders (0.3 pts)")
                    score += 0.3
                else:
                    print(f"FAIL: Component 3 — some folder entries missing 'path' key")
            else:
                print(f"FAIL: Component 3 — need >= 2 folders for multi-root, found {len(folders) if isinstance(folders, list) else 'N/A'}")

        except (json.JSONDecodeError, IOError) as e:
            print(f"ERROR: Component 3 — could not parse {ws_path}: {e}")

        if score > best_score:
            best_score = score
            best_file = ws_path

    total_score = best_score
    final_score = min(total_score, 1.0)
    print(f"\nBest workspace file: {best_file}")
    print(f"Score: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
