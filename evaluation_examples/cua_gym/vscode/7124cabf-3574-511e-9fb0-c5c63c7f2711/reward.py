"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’ve organized all my project folders just the way I need them—can you help me save this VS Code workspace as “myproject” under /home/user/workspaces/?
Generated: 2025-09-11 15:08:37
Status: success
Model: azure-o3
Total Steps: 1
"""

import os
import json
import pathlib
import traceback


def verify_vscode_workspace():
    """
    Reward script for task:
    "Save the current VS Code workspace as \"myproject\" under /home/user/workspaces/"

    Verification Logic & Progressive Scoring (max 1.0):
    1. Workspace file exists exactly at /home/user/workspaces/myproject.code-workspace (0.5)
    2. File is valid JSON and loads without error                  (0.3)
    3. "folders" array in JSON references real, existing folders   (up to 0.2)
       • All folders exist  -> +0.2
       • Some exist         -> +0.2 * (existing/total)
    
    The script prints detailed diagnostics and the final score as:
        REWARD: X.X
    """

    workspace_dir = pathlib.Path('/home/user/workspaces')
    expected_file = workspace_dir / 'myproject.code-workspace'

    score = 0.0
    max_score = 1.0

    print(f"Checking for workspace file at: {expected_file}")

    # Requirement 1: File existence
    if expected_file.exists() and expected_file.is_file():
        print("✓ Workspace file exists (0.5 pts)")
        score += 0.5
    else:
        print("✗ Workspace file not found – cannot proceed with further checks")
        print(f"REWARD: {score}")
        return score

    # Requirement 2: Valid JSON
    try:
        with expected_file.open('r', encoding='utf-8') as f:
            data = json.load(f)
        print("✓ JSON parsed successfully (0.3 pts)")
        score += 0.3
    except Exception as e:
        print(f"✗ Failed to parse JSON workspace file: {e}")
        print(f"REWARD: {score}")
        return score

    # Requirement 3: "folders" key and referenced paths
    folders = data.get('folders')
    if isinstance(folders, list) and folders:
        existing = 0
        for folder in folders:
            folder_path = None
            if isinstance(folder, dict):
                folder_path = folder.get('path')
            elif isinstance(folder, str):  # rare but supported
                folder_path = folder

            if folder_path is None:
                continue

            path_obj = pathlib.Path(folder_path)
            if not path_obj.is_absolute():
                # Interpret relative paths relative to workspace file location
                path_obj = (expected_file.parent / path_obj).resolve()
            if path_obj.exists():
                existing += 1

        if existing == len(folders):
            print("✓ All referenced folders exist (0.2 pts)")
            score += 0.2
        elif existing > 0:
            partial = 0.2 * (existing / len(folders))
            print(f"✓ Some folders exist ({existing}/{len(folders)}) (+{partial:.2f} pts)")
            score += partial
        else:
            print("✗ None of the referenced folders exist (0 pts)")
    else:
        print("✗ 'folders' key missing or empty in workspace JSON (0 pts)")

    # Clamp score to max
    final_score = min(score, max_score)
    print(f"Total Score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    try:
        verify_vscode_workspace()
    except Exception:
        traceback.print_exc()
        print("REWARD: 0.0")
