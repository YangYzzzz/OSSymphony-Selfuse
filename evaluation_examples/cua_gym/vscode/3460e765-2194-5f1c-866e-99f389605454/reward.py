"""
Reward Script: Set up a multi-root workspace with three projects
Task ID: vscode_lp_062
Domain: vscode
Scoring:
  - Component 1 (0.2): Workspace file is valid JSON with "folders" key
  - Component 2 (0.2): ~/projects/api is in folders array
  - Component 3 (0.2): ~/projects/web is in folders array
  - Component 4 (0.2): ~/projects/shared is in folders array
  - Component 5 (0.2): Exactly 3 folders (no extras, no duplicates)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_062'
WORKSPACE_PATH = os.path.join(WORKDIR, 'projects', 'fullstack.code-workspace')

# Required folder paths — accept both absolute and relative forms
REQUIRED_FOLDERS = {
    'api': ['/home/user/projects/api', '~/projects/api', './api', 'api'],
    'web': ['/home/user/projects/web', '~/projects/web', './web', 'web'],
    'shared': ['/home/user/projects/shared', '~/projects/shared', './shared', 'shared'],
}


def normalize_path(p):
    """Normalize a folder path for comparison."""
    p = p.rstrip('/')
    return p


def folder_matches(actual_path, accepted_variants):
    """Check if an actual path matches any accepted variant."""
    norm = normalize_path(actual_path)
    return any(normalize_path(v) == norm for v in accepted_variants)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: workspace file must exist
    if not os.path.exists(WORKSPACE_PATH):
        print(f"CRITICAL: Workspace file not found at {WORKSPACE_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid JSON with "folders" key (0.2 points)
    workspace_data = None
    try:
        with open(WORKSPACE_PATH, 'r') as f:
            content = f.read()
        # Handle JSONC (strip comments)
        cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        workspace_data = json.loads(cleaned)

        if isinstance(workspace_data, dict) and 'folders' in workspace_data:
            folders_list = workspace_data['folders']
            if isinstance(folders_list, list):
                print(f"PASS: Component 1 — Valid JSON with 'folders' key containing {len(folders_list)} entries (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 1 — 'folders' is not a list, got {type(folders_list).__name__}")
        else:
            print(f"FAIL: Component 1 — JSON missing 'folders' key")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 1 — Invalid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if workspace_data is None or 'folders' not in workspace_data:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    folders_list = workspace_data['folders']
    # Extract actual paths from folder entries
    actual_paths = []
    for entry in folders_list:
        if isinstance(entry, dict) and 'path' in entry:
            actual_paths.append(entry['path'])
        elif isinstance(entry, str):
            actual_paths.append(entry)

    # Component 2: ~/projects/api is in folders (0.2 points)
    try:
        if any(folder_matches(p, REQUIRED_FOLDERS['api']) for p in actual_paths):
            print(f"PASS: Component 2 — 'api' folder found in workspace (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — 'api' folder not found. Actual paths: {actual_paths}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: ~/projects/web is in folders (0.2 points)
    try:
        if any(folder_matches(p, REQUIRED_FOLDERS['web']) for p in actual_paths):
            print(f"PASS: Component 3 — 'web' folder found in workspace (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — 'web' folder not found. Actual paths: {actual_paths}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: ~/projects/shared is in folders (0.2 points)
    try:
        if any(folder_matches(p, REQUIRED_FOLDERS['shared']) for p in actual_paths):
            print(f"PASS: Component 4 — 'shared' folder found in workspace (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — 'shared' folder not found. Actual paths: {actual_paths}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Exactly 3 folders — no extras, no duplicates (0.2 points)
    try:
        if len(actual_paths) == 3:
            print(f"PASS: Component 5 — Exactly 3 folders in workspace (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 5 — Expected 3 folders, found {len(actual_paths)}: {actual_paths}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
