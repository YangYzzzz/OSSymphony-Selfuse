"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m working on a Python project in /home/user/webapp, and all the “.mypy_cache” folders are cluttering the Explorer view—how can I hide every “.mypy_cache” directory so they no longer appear in the sidebar?
Generated: 2025-09-11 18:24:14
Status: success
Model: azure-o3
Total Steps: 3
"""

import os
import json
import re
import pathlib

"""
Reward Script: Verify that every “.mypy_cache” directory is hidden in VS Code’s
Explorer sidebar for the workspace /home/user/webapp.

Scoring Logic (progressive):
1. Workspace-level .vscode/settings.json (project-specific) — up to 1.0 pts
     • 1.0 pts  if `.mypy_cache` is excluded via  files.exclude  (preferred)
     • 0.7 pts  if excluded via secondary keys (files.watcherExclude / search.exclude / explorer.exclude)
2. User-level settings.json (in ~/.config/Code*/User/) — same scoring as above, but only
   counted if workspace file is missing or provides lower score.

The highest score found (workspace or user) becomes the reward, capped at 1.0.
A score of 0.0 means the exclusion rule was not found anywhere.
"""

# --------------------------- Helper Functions --------------------------- #

def load_json(path: pathlib.Path):
    """Load a JSON file, stripping simple // comments if present."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        # Naïvely strip // comments (handles single-line comments)
        content = re.sub(r"//.*", "", content)
        return json.loads(content)
    except Exception as exc:
        print(f"Error loading {path}: {exc}")
        return None

def pattern_in_exclude(exclude_dict):
    """Return True if any pattern containing '.mypy_cache' is enabled."""
    if not isinstance(exclude_dict, dict):
        return False
    for pattern, enabled in exclude_dict.items():
        if ".mypy_cache" in pattern and bool(enabled):
            return True
    return False

def score_settings_file(path: pathlib.Path):
    """Return a score for a settings.json file regarding .mypy_cache exclusion."""
    data = load_json(path)
    if not data:
        return 0.0

    # Primary key
    if "files.exclude" in data and pattern_in_exclude(data["files.exclude"]):
        print(f"✓ .mypy_cache excluded via files.exclude in {path}")
        return 1.0

    # Secondary keys (partial credit)
    for key in ("files.watcherExclude", "search.exclude", "explorer.exclude"):
        if key in data and pattern_in_exclude(data[key]):
            print(f"✓ .mypy_cache excluded via {key} in {path} (partial)")
            return 0.7

    # Nothing found
    return 0.0

# --------------------------- Main Verification --------------------------- #

def verify_hide_mypy_cache():
    project_root = pathlib.Path("/home/user/webapp")
    workspace_settings = project_root / ".vscode" / "settings.json"

    # Potential user-level settings locations for VS Code / Code-OSS / VSCodium
    user_settings_paths = [
        pathlib.Path.home() / ".config" / "Code" / "User" / "settings.json",
        pathlib.Path.home() / ".config" / "Code - OSS" / "User" / "settings.json",
        pathlib.Path.home() / ".config" / "VSCodium" / "User" / "settings.json",
    ]

    total_score = 0.0

    # 1. Check workspace settings (preferred)
    if workspace_settings.exists():
        total_score = max(total_score, score_settings_file(workspace_settings))
    else:
        print("Workspace settings.json not found")

    # 2. Check user-level settings only if higher score can be achieved
    if total_score < 1.0:
        for path in user_settings_paths:
            if path.exists():
                total_score = max(total_score, score_settings_file(path))
                if total_score == 1.0:
                    break  # cannot get higher than 1.0

    # Final reporting
    if total_score == 0.0:
        print("✗ No valid exclusion for .mypy_cache found")
    print(f"Final score: {total_score}")
    print(f"REWARD: {total_score}")
    return total_score

# --------------------------- Script Entry Point -------------------------- #

if __name__ == "__main__":
    verify_hide_mypy_cache()
