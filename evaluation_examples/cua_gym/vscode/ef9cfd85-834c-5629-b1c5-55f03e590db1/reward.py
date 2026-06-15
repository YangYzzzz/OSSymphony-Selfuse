"""
FINAL REWARD SCRIPT - SUCCESS
Task: I'm collaborating on a project and need quick access to our common assets. How can I add the folder located at “/home/user/shared” to my current VS Code workspace?
Generated: 2025-09-11 14:35:23
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
import json
import glob


def _normalize_path(path_str: str, workspace_dir: str) -> str:
    """Return an absolute, normalized path for a folder entry coming from a
    VS Code *.code-workspace file.  If the entry is relative, it is resolved
    relative to the workspace file location (VS Code behaviour)."""
    if os.path.isabs(path_str):
        return os.path.normpath(os.path.abspath(path_str))
    return os.path.normpath(os.path.abspath(os.path.join(workspace_dir, path_str)))


def verify_vscode_workspace(shared_folder: str = "/home/user/shared",
                             search_root: str = "/home/user") -> float:
    """Verify that at least one VS Code workspace under *search_root* contains
    *shared_folder* as a folder entry.

    Scoring (progressive):
        0.7 – *shared_folder* present in any workspace file
        0.3 – that workspace also contains at least one other folder entry
    The function prints detailed diagnostics and returns a score between 0.0
    and 1.0.
    """

    shared_folder = os.path.normpath(os.path.abspath(shared_folder))
    print(f"Target shared folder absolute path: {shared_folder}")

    # Locate every *.code-workspace file below search_root
    workspace_files = glob.glob(os.path.join(search_root, "**", "*.code-workspace"),
                                recursive=True)
    print(f"Found {len(workspace_files)} .code-workspace file(s) under {search_root}.")

    found_shared = False        # Did we ever see the shared folder?
    found_extra  = False        # Was there at least one other folder beside shared?

    for wf in workspace_files:
        print(f"\nInspecting workspace file: {wf}")
        try:
            with open(wf, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception as exc:
            print(f"   ✗ Failed to parse JSON – skipped (error: {exc})")
            continue

        folders_section = data.get("folders", [])
        print(f"   Contains {len(folders_section)} folder entrie(s).")

        # Normalise all folder paths declared in this workspace file
        normalised_paths = []
        for entry in folders_section:
            # VS Code allows either a plain string or an object with a "path" key
            if isinstance(entry, str):
                path_value = entry
            elif isinstance(entry, dict):
                path_value = entry.get("path") or entry.get("name")
            else:
                continue  # unsupported structure – ignore
            abs_path = _normalize_path(path_value, os.path.dirname(wf))
            normalised_paths.append(abs_path)

        for p in normalised_paths:
            print(f"      - {p}")

        if shared_folder in normalised_paths:
            print("   ✓ Shared folder found in this workspace file.")
            found_shared = True
            if len(normalised_paths) > 1:
                found_extra = True
        else:
            print("   Shared folder NOT present in this workspace file.")

    # ----------------------- Scoring -----------------------
    score = 0.0
    if found_shared:
        score += 0.7
        print("✓ Requirement 1 met: Shared folder added to a workspace (0.7 points)")
    else:
        print("✗ Requirement 1 failed: Shared folder not found (0 points)")

    if found_shared and found_extra:
        score += 0.3
        print("✓ Requirement 2 met: Workspace also contains other folder(s) (0.3 points)")
    elif found_shared:
        print("✗ Requirement 2 failed: No additional folder entries (0 points)")

    score = round(min(score, 1.0), 2)
    print(f"Total score: {score} / 1.0")
    return score


if __name__ == "__main__":
    reward = verify_vscode_workspace()
    print(f"REWARD: {reward}")

