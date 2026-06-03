"""
FINAL REWARD SCRIPT - SUCCESS
Task: The constant Pylint pop-ups are distracting me while I refactor my Django project—how can I temporarily turn off the Pylint extension in VS Code without uninstalling it?
Generated: 2025-09-11 11:51:32
Status: success
Model: azure-o3
Total Steps: 14
"""

"""
Reward script for VS Code task: Temporarily disable Pylint extension without uninstalling.

Scoring criteria (progressive):
 1. Pylint extension is still installed under ~/.vscode/extensions         (0.3 pts)
 2. At least one workspace .vscode/settings.json sets
    "python.linting.pylintEnabled": false                                (0.5 pts)
 3. A workspace .vscode/extensions.json lists the Pylint extension under
    the "disabled" array                                                 (0.2 pts)

A perfect score (1.0) is achieved when all three conditions are satisfied.
The script awards **no points** for natural conditions (e.g., mere existence
of a workspace); points are granted ONLY when task-specific changes are
verified.
"""
import json
import pathlib
import re
from typing import List

# ------------------------ Helper Functions ------------------------ #

def strip_json_comments(text: str) -> str:
    """Remove // comments so JSON can be parsed reliably."""
    return re.sub(r"//.*", "", text)

def find_pylint_extensions() -> List[pathlib.Path]:
    """Locate VS Code extension directories that look like Pylint."""
    ext_root = pathlib.Path.home() / ".vscode" / "extensions"
    if not ext_root.exists():
        return []
    return [p for p in ext_root.iterdir() if p.is_dir() and "pylint" in p.name.lower()]

def workspaces_settings_with_pylint_disabled() -> List[pathlib.Path]:
    """Find .vscode/settings.json files where python.linting.pylintEnabled == false."""
    matches = []
    for settings_path in pathlib.Path.home().rglob("settings.json"):
        if settings_path.parent.name != ".vscode":
            continue  # only workspace-level settings
        try:
            raw = settings_path.read_text(encoding="utf-8")
        except Exception:
            continue
        cleaned = strip_json_comments(raw)
        try:
            data = json.loads(cleaned or "{}")
        except json.JSONDecodeError:
            continue
        val = data.get("python.linting.pylintEnabled")
        if (isinstance(val, bool) and val is False) or (
            isinstance(val, str) and val.strip().lower() == "false"
        ):
            matches.append(settings_path)
    return matches

def extensions_json_disabling_pylint() -> List[pathlib.Path]:
    """Find .vscode/extensions.json files that list ms-python.pylint under "disabled"."""
    disabled_files = []
    for ext_file in pathlib.Path.home().rglob("extensions.json"):
        if ext_file.parent.name != ".vscode":
            continue
        try:
            raw = ext_file.read_text(encoding="utf-8")
        except Exception:
            continue
        cleaned = strip_json_comments(raw)
        try:
            data = json.loads(cleaned or "{}")
        except json.JSONDecodeError:
            continue
        disabled_list = data.get("disabled") or []
        if isinstance(disabled_list, list):
            if any(isinstance(entry, str) and "pylint" in entry.lower() for entry in disabled_list):
                disabled_files.append(ext_file)
    return disabled_files

# ---------------------- Verification Routine ---------------------- #

def verify_task() -> float:
    print("--- Verifying VS Code task: Temporarily disable Pylint extension ---")
    total_score = 0.0

    # Requirement 1 – Pylint extension still installed (0.3)
    pylint_dirs = find_pylint_extensions()
    if pylint_dirs:
        print(f"✓ Pylint extension installed: {[p.name for p in pylint_dirs]} (0.3)")
        total_score += 0.3
    else:
        print("✗ No Pylint extension found in ~/.vscode/extensions (0 pts)")

    # Requirement 2 – Workspace settings disable Pylint (0.5)
    disabled_settings_files = workspaces_settings_with_pylint_disabled()
    if disabled_settings_files:
        print("✓ Workspace settings.json disables Pylint (0.5)")
        for path in disabled_settings_files:
            print(f"  - {path}")
        total_score += 0.5
    else:
        print("✗ No settings.json with python.linting.pylintEnabled=false found (0 pts)")

    # Requirement 3 – extensions.json marks Pylint as disabled (0.2)
    disabled_extension_files = extensions_json_disabling_pylint()
    if disabled_extension_files:
        print("✓ extensions.json lists ms-python.pylint as disabled (0.2)")
        for path in disabled_extension_files:
            print(f"  - {path}")
        total_score += 0.2
    else:
        print("✗ No extensions.json found that disables Pylint (0 pts)")

    # Final score
    final_score = round(min(total_score, 1.0), 2)
    print(f"Total Score: {final_score:.2f} / 1.0")
    print(f"REWARD: {final_score}")
    return final_score

if __name__ == "__main__":
    verify_task()

