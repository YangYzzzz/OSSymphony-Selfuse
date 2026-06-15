"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m working on /home/user/plots/analysis.py and want every matplotlib chart to appear right inside the VS Code editor, not in a separate window—what setting should I tweak in the Python extension to make the plots render inline?
Generated: 2025-09-11 23:49:02
Status: success
Model: azure-o3
Total Steps: 15
"""

import os
import json
from typing import List, Tuple

def _load_json(path: str):
    """Safely load JSON and return a dict or None."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"  ✗ Could not read valid JSON from {path}: {e}")
        return None

def _collect_settings_files(workspace_dir: str) -> List[str]:
    """Return a de-duplicated, ordered list of possible VS Code settings.json files.

    Precedence (first wins):
      1. Workspace-level   <workspace>/.vscode/settings.json
      2. Nested workspaces inside the main workspace (any sub-folder that
         contains a .vscode/settings.json)
      3. User-level VS Code settings (Linux paths)
    """
    candidates: List[str] = []

    # 1) Main workspace settings
    candidates.append(os.path.join(workspace_dir, ".vscode", "settings.json"))

    # 2) Any nested .vscode folders inside the workspace
    for root, dirs, files in os.walk(workspace_dir):
        if os.path.basename(root) == ".vscode":
            candidates.append(os.path.join(root, "settings.json"))

    # 3) User-level settings (most common Linux paths)
    candidates.extend(
        [
            os.path.expanduser("~/.vscode/settings.json"),
            os.path.expanduser("~/.config/Code/User/settings.json"),
            os.path.expanduser("~/.vscode-server/data/Machine/settings.json"),
        ]
    )

    # De-duplicate while preserving order
    seen = set()
    ordered: List[str] = []
    for p in candidates:
        if p not in seen:
            seen.add(p)
            ordered.append(p)
    return ordered

def _get_effective_backend(workspace_dir: str) -> Tuple[str, str, List[str]]:
    """Return (backend_value, source_file, checked_files).  backend_value is None if not found."""
    files = _collect_settings_files(workspace_dir)
    for path in files:
        if os.path.isfile(path):
            data = _load_json(path)
            if isinstance(data, dict) and "python.plotting.backend" in data:
                return str(data["python.plotting.backend"]).strip(), path, files
    return None, None, files

def verify_task() -> float:
    """Verify that python.plotting.backend is set to 'inline'.  Return a progressive score 0-1."""
    workspace_dir = "/home/user/plots"

    backend_value, source_file, checked_files = _get_effective_backend(workspace_dir)

    print("Checked settings files in order of precedence:")
    for p in checked_files:
        print("  -", p)

    score = 0.0

    # Give points only for *actual* achievements
    if backend_value is None:
        print("✗ 'python.plotting.backend' setting not found in any settings file")
    else:
        score += 0.5  # key exists – half the work done
        print(f"✓ Found 'python.plotting.backend' in {source_file}: '{backend_value}' (0.5)")
        if backend_value.lower() == "inline":
            score += 0.5  # correct value – task fully completed
            print("✓ Backend correctly set to 'inline' (0.5)")
        else:
            print("✗ Backend value is not 'inline' (no additional points)")

    final_score = round(min(score, 1.0), 2)
    print(f"REWARD: {final_score}")
    return final_score

if __name__ == "__main__":
    verify_task()
