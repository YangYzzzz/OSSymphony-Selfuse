"""
FINAL REWARD SCRIPT - SUCCESS
Task: Running pytest keeps sprinkling “.pytest_cache” folders all over my project at /home/user/projects/my_app, and they crowd the Explorer view. How can I hide every “.pytest_cache” folder so they don’t show up in VS Code’s sidebar?
Generated: 2025-09-11 16:48:59
Status: success
Model: azure-o3
Total Steps: 3
"""

import json
import re
import os
from pathlib import Path

"""
Reward script for verifying that the VS Code sidebar is configured to hide all
".pytest_cache" folders in the workspace at /home/user/projects/my_app.

Verification strategy:
1. Look for VS Code settings.json files that can influence folder visibility.
   • Workspace-specific file:   /home/user/projects/my_app/.vscode/settings.json
   • Typical user-level files: ~/.config/Code/User/settings.json, etc.
2. Parse each settings.json (handle JSON with comments) and inspect two keys
   that control visibility in the Explorer sidebar:
      a) "files.exclude"
      b) "search.exclude"
3. The task is considered 100 % complete when BOTH of these dictionaries contain
   at least one pattern that matches "*.pytest_cache*" (e.g. "**/.pytest_cache")
   and that pattern evaluates to True (not False).
   • files.exclude match  -> 0.6 points
   • search.exclude match -> 0.4 points
4. The script prints detailed diagnostics and finally prints
   "REWARD: <score>" where <score> is a float between 0.0 and 1.0.

This progressive scoring ensures partial credit if only one of the two excludes
is configured. A perfect configuration earns exactly 1.0.
"""

def _strip_json_comments(text: str) -> str:
    """Remove // and /* */ comments from VS Code JSONC files."""
    # Remove // line comments
    text = re.sub(r"//.*", "", text)
    # Remove /* block comments */
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return text


def _load_settings(path: Path):
    """Load a settings.json file, returning a dict or None on error."""
    try:
        raw = path.read_text(encoding="utf-8")
        cleaned = _strip_json_comments(raw)
        return json.loads(cleaned)
    except Exception as exc:
        print(f"✗ Could not parse {path}: {exc}")
        return None


def _find_settings_files(project_root: Path):
    """Return a list of workspace and user settings.json paths that exist."""
    files = [project_root / ".vscode" / "settings.json"]

    home = Path.home()
    user_paths = [
        home / ".config" / "Code" / "User" / "settings.json",
        home / ".config" / "Code - OSS" / "User" / "settings.json",
        home / ".vscode" / "settings.json",
        home / ".vscode-oss" / "settings.json",
        home / ".vscode-user-data" / "User" / "settings.json",
    ]
    files.extend(user_paths)
    return [p for p in files if p.exists()]


def _pattern_matches(pattern: str) -> bool:
    """Return True if pattern clearly targets .pytest_cache folders."""
    return ".pytest_cache" in pattern


def verify_task() -> float:
    project_root = Path("/home/user/projects/my_app")
    if not project_root.exists():
        print("✗ Project root not found; verification failed.")
        print("REWARD: 0.0")
        return 0.0

    settings_files = _find_settings_files(project_root)
    print(f"Found {len(settings_files)} settings.json file(s) to inspect.")

    files_exclude_ok = False
    search_exclude_ok = False

    for sf in settings_files:
        data = _load_settings(sf)
        if data is None:
            continue

        print(f"Inspecting {sf}")
        # Check files.exclude
        files_exclude = data.get("files.exclude", {})
        if isinstance(files_exclude, dict):
            for pattern, value in files_exclude.items():
                if _pattern_matches(pattern) and value is not False:
                    files_exclude_ok = True
                    print(f"  ✓ files.exclude hides '{pattern}' (value={value})")
        # Check search.exclude (keeps sidebar tidy in many setups)
        search_exclude = data.get("search.exclude", {})
        if isinstance(search_exclude, dict):
            for pattern, value in search_exclude.items():
                if _pattern_matches(pattern) and value is not False:
                    search_exclude_ok = True
                    print(f"  ✓ search.exclude hides '{pattern}' (value={value})")

    # Progressive scoring
    score = 0.0
    if files_exclude_ok:
        score += 0.6
    else:
        print("✗ No suitable .pytest_cache pattern found in files.exclude")

    if search_exclude_ok:
        score += 0.4
    else:
        print("✗ No suitable .pytest_cache pattern found in search.exclude")

    # Clamp to [0,1]
    score = min(score, 1.0)
    print(f"Final score: {score}")
    print(f"REWARD: {score}")
    return score


if __name__ == "__main__":
    verify_task()
