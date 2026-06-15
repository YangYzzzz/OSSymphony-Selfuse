"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m tidying up my Python project and need to add both “/home/user/src” and “/home/user/tests” to my VS Code workspace, but can you show me how to keep the “.pytest_cache” folder hidden so it doesn’t clutter the Explorer?
Generated: 2025-09-11 23:45:31
Status: success
Model: azure-o3
Total Steps: 17
"""

import os
import json
import pathlib
from typing import List


def load_json(path: pathlib.Path):
    """Safely load a JSON file and return the parsed object or None on error."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:
        print(f"✗ Could not parse JSON {path}: {exc}")
        return None


def collect_workspace_files(root: pathlib.Path, max_depth: int = 3) -> List[pathlib.Path]:
    """Return a list of *.code-workspace files found below *root* (limited by *max_depth*)."""
    workspaces: List[pathlib.Path] = []
    for current_root, dirs, files in os.walk(root):
        depth = len(pathlib.Path(current_root).relative_to(root).parts)
        if depth > max_depth:
            # prune search for efficiency
            dirs[:] = []
            continue
        for file in files:
            if file.endswith(".code-workspace"):
                workspaces.append(pathlib.Path(current_root) / file)
    return workspaces


def normalize(p: str) -> str:
    """Return an absolute, resolved POSIX path string for consistent comparison."""
    return pathlib.Path(p).expanduser().resolve().as_posix()


def verify_task() -> float:
    """Verify that the workspace lists /home/user/src & /home/user/tests and hides .pytest_cache."""
    user_home = pathlib.Path("/home/user")

    print("Scanning for VS Code workspace files …")
    workspace_files = collect_workspace_files(user_home)
    print(f"Found {len(workspace_files)} workspace file(s): {workspace_files}")

    # Requirements to check
    required_folders = {
        "/home/user/src": False,
        "/home/user/tests": False,
    }
    pytest_cache_hidden = False

    # -------------------------------------------
    # Inspect every *.code-workspace file found
    # -------------------------------------------
    for ws_path in workspace_files:
        print(f"\nChecking workspace file: {ws_path}")
        data = load_json(ws_path)
        if not isinstance(data, dict):
            continue

        # 1️⃣  Folder entries
        for folder in data.get("folders", []):
            folder_path = folder.get("path") if isinstance(folder, dict) else folder
            if not isinstance(folder_path, str):
                continue
            abs_path = normalize(folder_path)
            for target in required_folders:
                if abs_path == normalize(target):
                    required_folders[target] = True

        # 2️⃣  .pytest_cache exclusion in settings
        settings = data.get("settings", {})
        if isinstance(settings, dict):
            for exclude_key in ("files.exclude", "explorer.exclude"):
                exclude_cfg = settings.get(exclude_key)
                if isinstance(exclude_cfg, dict):
                    if exclude_cfg.get("**/.pytest_cache") is True:
                        pytest_cache_hidden = True

    # If exclusion not found inside workspace file, check global settings.json
    if not pytest_cache_hidden:
        global_settings = user_home / ".vscode" / "settings.json"
        if global_settings.exists():
            print(f"\nChecking global settings: {global_settings}")
            data = load_json(global_settings)
            if isinstance(data, dict):
                for exclude_key in ("files.exclude", "explorer.exclude"):
                    exclude_cfg = data.get(exclude_key)
                    if isinstance(exclude_cfg, dict):
                        if exclude_cfg.get("**/.pytest_cache") is True:
                            pytest_cache_hidden = True
                            break

    # ----------------
    # Scoring section
    # ----------------
    score = 0.0

    # Each required folder present → +0.25 (total 0.5)
    for folder_path, present in required_folders.items():
        if present:
            print(f"✓ Workspace contains folder: {folder_path}")
            score += 0.25
        else:
            print(f"✗ Workspace missing folder: {folder_path}")

    # .pytest_cache exclusion → +0.5
    if pytest_cache_hidden:
        print("✓ .pytest_cache is hidden/excluded in Explorer")
        score += 0.5
    else:
        print("✗ .pytest_cache is NOT excluded from Explorer")

    final_score = min(score, 1.0)
    print(f"\nTotal Score: {final_score} / 1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task()

