"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m juggling a bunch of Jupyter notebooks and datasets for my machine-learning experiment—could you help me save my current VS Code workspace as “data-science” inside /home/user/analytics/ so I can reopen it later?
Generated: 2025-09-11 14:24:07
Status: success
Model: azure-o3
Total Steps: 9
"""

import os
import pathlib
import json
import re


def _load_json_lenient(path: pathlib.Path):
    """Load JSON from a file, stripping simple // comments if necessary."""
    with path.open("r", encoding="utf-8") as f:
        raw_text = f.read()

    # Strip out // comments that VS Code sometimes inserts
    cleaned = re.sub(r"//.*", "", raw_text)
    return json.loads(cleaned)


def verify_vscode_workspace():
    """Verify that the VS Code workspace has been saved as requested.

    Scoring rubric (progressive):
      0.25  –  /home/user/analytics directory exists
      0.25  –  data-science.code-workspace file exists inside that directory
      0.25  –  File contains syntactically valid JSON (after stripping // comments)
      0.25  –  JSON has a non-empty "folders" list
      +0.05 –  Bonus for each of the keys {settings, extensions, launch} that is present
                (capped so the final score never exceeds 1.0)
    """

    total_score = 0.0
    max_score = 1.0  # Absolute maximum

    analytics_dir = pathlib.Path("/home/user/analytics")
    workspace_file = analytics_dir / "data-science.code-workspace"

    print("--- VS Code Workspace Verification ---")
    print(f"Expected directory : {analytics_dir}")
    print(f"Expected workspace : {workspace_file}\n")

    # 1. Directory existence (0.25)
    if analytics_dir.exists() and analytics_dir.is_dir():
        total_score += 0.25
        print("✓ analytics directory exists (0.25)")
    else:
        print("✗ analytics directory is missing – cannot continue")
        print(f"REWARD: {total_score}")
        return total_score

    # 2. Workspace file existence (0.25)
    if workspace_file.exists() and workspace_file.is_file():
        total_score += 0.25
        print("✓ data-science.code-workspace file found (0.25)")
    else:
        print("✗ Workspace file not found – stopping early")
        print(f"REWARD: {total_score}")
        return total_score

    # 3. File parses as JSON (0.25)
    try:
        data = _load_json_lenient(workspace_file)
        total_score += 0.25
        print("✓ Workspace JSON parsed successfully (0.25)")
    except Exception as exc:
        print(f"✗ Failed to parse JSON: {exc}")
        print(f"REWARD: {total_score}")
        return total_score

    # 4. Non-empty "folders" list (0.25)
    folders = []
    if isinstance(data, dict):
        folders = data.get("folders", [])

    if isinstance(folders, list) and len(folders) > 0:
        total_score += 0.25
        print("✓ \"folders\" key present with entries (0.25)")
    else:
        print("✗ \"folders\" key missing or empty – no points awarded here")

    # 5. Bonus for extra configuration (0.05 each, capped by max_score)
    bonus_keys = {"settings", "extensions", "launch"}
    for key in bonus_keys:
        if isinstance(data, dict) and key in data:
            if total_score + 0.05 <= max_score:
                total_score += 0.05
            print(f"✓ Bonus: key '{key}' present (+0.05)")

    final_score = min(total_score, max_score)

    print(f"\nTotal computed score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_vscode_workspace()
