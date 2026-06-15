"""
Reward Script: Generate monorepo.code-workspace with all three packages
Task ID: vscode_gf3_015
Domain: vscode
Scoring:
  Component 1 (0.3): Workspace file exists and is valid JSON
  Component 2 (0.3): Has "folders" key with exactly 3 entries
  Component 3 (0.4): All three package paths present (frontend, backend, shared)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_015'

# The workspace file should be at /home/user/projects/monorepo/monorepo.code-workspace
WORKSPACE_PATH = os.path.join(WORKDIR, 'projects', 'monorepo', 'monorepo.code-workspace')

# Required package folders - these may be relative or absolute paths
REQUIRED_PACKAGES = {'frontend', 'backend', 'shared'}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: workspace file must exist
    if not os.path.exists(WORKSPACE_PATH):
        print(f"CRITICAL: Workspace file not found: {WORKSPACE_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Workspace file is valid JSON (0.3 points)
    workspace_data = None
    try:
        with open(WORKSPACE_PATH, 'r') as f:
            workspace_data = json.load(f)
        if isinstance(workspace_data, dict):
            print(f"PASS: Component 1 - Workspace file is valid JSON dict (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 - Workspace file is valid JSON but not a dict, type: {type(workspace_data)}")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 1 - Workspace file is not valid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    if workspace_data is None or not isinstance(workspace_data, dict):
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Has "folders" key with exactly 3 entries (0.3 points)
    try:
        folders = workspace_data.get('folders', None)
        if folders is not None and isinstance(folders, list) and len(folders) == 3:
            print(f"PASS: Component 2 - 'folders' has exactly 3 entries (0.3 pts)")
            total_score += 0.3
        elif folders is not None and isinstance(folders, list):
            print(f"FAIL: Component 2 - 'folders' has {len(folders)} entries, expected 3")
        else:
            print(f"FAIL: Component 2 - 'folders' key missing or not a list")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: All three required package paths present (0.4 points)
    try:
        folders = workspace_data.get('folders', [])
        if not isinstance(folders, list):
            print(f"FAIL: Component 3 - 'folders' is not a list")
        else:
            # Extract paths from folder entries
            folder_paths = []
            for entry in folders:
                if isinstance(entry, dict) and 'path' in entry:
                    folder_paths.append(entry['path'])

            # Check each required package is represented in the paths
            # The path could be relative (e.g., "packages/frontend") or absolute
            found_packages = set()
            for path_str in folder_paths:
                for pkg in REQUIRED_PACKAGES:
                    if pkg in path_str:
                        found_packages.add(pkg)

            if found_packages == REQUIRED_PACKAGES:
                print(f"PASS: Component 3 - All 3 packages found: {found_packages} (0.4 pts)")
                total_score += 0.4
            else:
                missing = REQUIRED_PACKAGES - found_packages
                print(f"FAIL: Component 3 - Missing packages: {missing}. Found paths: {folder_paths}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
