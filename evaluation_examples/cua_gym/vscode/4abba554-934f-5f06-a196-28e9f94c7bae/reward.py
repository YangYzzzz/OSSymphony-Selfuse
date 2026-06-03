"""
FINAL REWARD SCRIPT - SUCCESS
Task: I'm pairing with an Italian teammate this week, so I need all the VS Code menus and messages in Italian—how can I switch the editor’s display language to Italian?
Generated: 2025-09-11 18:44:20
Status: success
Model: azure-o3
Total Steps: 6
"""

import json
import re
import pathlib

"""
Reward Verification Script: VS Code Italian Language Setup

This script verifies that Visual Studio Code is configured to display its UI in
Italian. It awards up to 1.0 points based on two concrete checks:

1. VS Code’s user-level locale.json sets the editor locale to Italian (0.5 pts)
2. The Italian language-pack extension is installed in the user’s extensions
   directory (0.5 pts)

A progressive score (0.0 – 1.0) is returned, granting partial credit when only
one of the two requirements is satisfied. All verification steps rely on actual
file-system inspection—no hard-coded “true” values or natural-condition points
are used.
"""

###########################################################################
# Helper: load JSON while stripping // and /* */ comments (VS Code allows them)
###########################################################################

def _load_json_strip_comments(path: pathlib.Path):
    """Return a Python object from a JSON file, after stripping JS-style comments."""
    try:
        raw = path.read_text(encoding="utf-8")
    except Exception as exc:
        print(f"    Error reading {path}: {exc}")
        return None

    # Remove block comments /*  */
    raw = re.sub(r"/\*.*?\*/", "", raw, flags=re.S)
    # Remove line comments // ...
    raw = re.sub(r"//.*", "", raw)

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"    JSON decode error in {path}: {exc}")
        return None

###########################################################################
# Check 1: locale.json sets Italian locale
###########################################################################

def _check_locale_italian() -> bool:
    """Return True if any known VS Code locale.json file sets locale to Italian."""
    home = pathlib.Path.home()
    candidate_paths = [
        home / ".config/Code/User/locale.json",
        home / ".config/Code - Insiders/User/locale.json",
        home / ".config/Code - OSS/User/locale.json",
        home / ".config/VSCodium/User/locale.json",
        home / ".vscode/locale.json",  # portable scenario
    ]

    for loc_path in candidate_paths:
        if not loc_path.exists():
            continue
        data = _load_json_strip_comments(loc_path)
        if not isinstance(data, dict):
            continue
        locale_val = str(data.get("locale", "")).lower()
        if locale_val.startswith("it"):  # covers "it" or "it-IT"
            print(f"✓ Italian locale configured in {loc_path} (locale='{locale_val}')")
            return True
        else:
            print(f"    Found locale='{locale_val}' in {loc_path}, not Italian")
    print("✗ Italian locale not configured in any known locale.json file")
    return False

###########################################################################
# Check 2: Italian language-pack extension installed
###########################################################################

def _check_language_pack_installed() -> bool:
    """Return True if an Italian language-pack extension directory is present."""
    home = pathlib.Path.home()
    ext_dirs = [
        home / ".vscode/extensions",
        home / ".vscode-insiders/extensions",
        home / ".vscode-oss/extensions",
        home / ".vscode-remote/extensions",
    ]

    for base in ext_dirs:
        if not base.exists():
            continue
        for entry in base.iterdir():
            if entry.is_dir() and "language-pack-it" in entry.name.lower():
                print(f"✓ Italian language pack extension found: {entry}")
                return True
    print("✗ Italian language pack extension not found in VS Code extension directories")
    return False

###########################################################################
# Main verification entry-point
###########################################################################

def verify_task_completion() -> float:
    """Compute and print the progressive reward score (0.0 – 1.0)."""
    total_score = 0.0

    # Each successful check contributes 0.5 points
    if _check_locale_italian():
        total_score += 0.5
    if _check_language_pack_installed():
        total_score += 0.5

    # Clamp and round the final score
    final_score = round(min(total_score, 1.0), 2)

    # Summary output (required by evaluation harness)
    print(f"Total Score: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score

# Execute when run as a standalone script
if __name__ == "__main__":
    verify_task_completion()

