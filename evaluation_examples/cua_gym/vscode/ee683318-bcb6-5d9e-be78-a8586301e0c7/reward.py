"""
Reward Script: Create a workspace file configuring a multi-root workspace with custom folder names
Task ID: vscode_file_069
Domain: vs_code
Scoring:
  Component 1 (0.35 pts): workspace.code-workspace file exists at /home/user/projects/ and is valid JSON
  Component 2 (0.35 pts): folders array contains both correct paths (my-frontend-app, my-backend-api)
  Component 3 (0.30 pts): each folder entry has correct custom display names (Frontend, Backend)
"""

import os
import json

WORKDIR = '/home/user/projects'
TASK_ID = 'vscode_file_069'
WORKSPACE_PATH = os.path.join(WORKDIR, 'workspace.code-workspace')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: workspace.code-workspace exists and is valid JSON (0.35 points)
    # This FAILS on initial_env (file does not exist) and PASSES on golden_env (file created by task)
    workspace_data = None
    try:
        if not os.path.exists(file_path):
            print(f"FAIL: Component 1 — workspace file not found at {file_path}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        with open(file_path, 'r') as f:
            workspace_data = json.load(f)

        if workspace_data is not None:
            print(f"PASS: Component 1 — workspace file exists and is valid JSON (0.35 pts)")
            total_score += 0.35

    except json.JSONDecodeError as e:
        print(f"FAIL: Component 1 — workspace file exists but is not valid JSON: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: folders array contains both expected paths (0.35 points)
    # Verifies that the multi-root workspace has both project directories configured
    try:
        folders = workspace_data.get('folders', [])
        actual_paths = [folder.get('path', '') for folder in folders]

        expected_paths = {'my-frontend-app', 'my-backend-api'}
        found_paths = set(actual_paths) & expected_paths

        if found_paths == expected_paths:
            print(f"PASS: Component 2 — both folder paths found: {sorted(found_paths)} (0.35 pts)")
            total_score += 0.35
        else:
            missing = expected_paths - found_paths
            print(f"FAIL: Component 2 — missing folder paths: {missing}, found: {actual_paths}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: each folder has correct custom display names (0.30 points)
    # Verifies that custom names "Frontend" and "Backend" are set — the core requirement
    try:
        folders = workspace_data.get('folders', [])

        # Build a mapping from path -> name
        path_to_name = {folder.get('path', ''): folder.get('name', '') for folder in folders}

        frontend_name_ok = path_to_name.get('my-frontend-app', '') == 'Frontend'
        backend_name_ok = path_to_name.get('my-backend-api', '') == 'Backend'

        if frontend_name_ok and backend_name_ok:
            print(f"PASS: Component 3 — both custom names correct: my-frontend-app='Frontend', my-backend-api='Backend' (0.30 pts)")
            total_score += 0.30
        else:
            if not frontend_name_ok:
                actual_fe = path_to_name.get('my-frontend-app', '<missing>')
                print(f"FAIL: Component 3 — my-frontend-app name expected 'Frontend', found: '{actual_fe}'")
            if not backend_name_ok:
                actual_be = path_to_name.get('my-backend-api', '<missing>')
                print(f"FAIL: Component 3 — my-backend-api name expected 'Backend', found: '{actual_be}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
# verify_task handles the case where the file does not exist (returns 0.0)
verify_task(WORKSPACE_PATH)
