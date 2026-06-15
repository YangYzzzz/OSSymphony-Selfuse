"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’ve been coding late into the night and the default theme is way too bright—could you help me switch VS Code to the “Tomorrow Night Blue” color theme?
Generated: 2025-09-11 17:41:03
Status: success
Model: azure-o3
Total Steps: 1
"""

import os
import re

"""
Reward Script for Verifying VS Code Theme Change to "Tomorrow Night Blue"
===========================================================
This script checks the user's VS Code configuration to ensure that:
1. At least one VS Code `settings.json` file exists (0.2 points)
2. A `workbench.colorTheme` property is present in any of those settings files (0.4 points)
3. The theme value is exactly "Tomorrow Night Blue" (case-insensitive) (0.4 points)

A fully correct configuration yields a score of 1.0, while partial completion
receives proportionally less.  The result is printed as `REWARD: X.X` as
required.
"""

def verify_vscode_theme() -> float:
    """Return a progressive score based on how completely the task was achieved."""

    home = os.path.expanduser("~")

    # Common locations for VS Code settings.json (including Insiders / OSS / VSCodium)
    candidate_dirs = [
        os.path.join(home, ".config", "Code", "User"),
        os.path.join(home, ".config", "Code - Insiders", "User"),
        os.path.join(home, ".config", "Code - OSS", "User"),
        os.path.join(home, ".config", "VSCodium", "User"),
        os.path.join(home, ".vscode"),  # portable-mode or older installs
    ]

    # Collect all plausible settings.json paths
    settings_files = []
    for d in candidate_dirs:
        if os.path.isdir(d):
            f = os.path.join(d, "settings.json")
            if os.path.isfile(f):
                settings_files.append(f)

    # Extra: walk ~/.config for any *Code*/VSCodium settings.json missed above
    extra_root = os.path.join(home, ".config")
    for root, _dirs, files in os.walk(extra_root):
        if "settings.json" in files and ("Code" in root or "VSCodium" in root):
            settings_files.append(os.path.join(root, "settings.json"))

    # De-duplicate while preserving order
    settings_files = list(dict.fromkeys(settings_files))

    print(f"Found settings files: {settings_files}")

    total_score = 0.0

    # 1) Must have at least one settings.json relevant to VS Code
    if settings_files:
        total_score += 0.2
        print("✓ Found at least one VS Code settings.json file (0.2 points)")
    else:
        print("✗ No VS Code settings.json file found -> task likely not completed")
        print("REWARD: 0.0")
        return 0.0  # nothing else to check

    theme_property_found = False
    correct_theme_found = False

    # Regex to capture the setting regardless of whitespace/comments
    pattern = re.compile(r'"\s*workbench\.colorTheme\s*"\s*:\s*"([^"]+)"', re.IGNORECASE)

    for file_path in settings_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for raw_line in f:
                    line = raw_line.lstrip()
                    if line.startswith("//"):
                        continue  # ignore JSONC comments
                    match = pattern.search(line)
                    if match:
                        theme_property_found = True
                        value = match.group(1).strip()
                        print(f"Found theme setting in {file_path}: '{value}'")
                        if value.lower() == "tomorrow night blue".lower():
                            correct_theme_found = True
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    # 2) Has the colorTheme key been set?
    if theme_property_found:
        total_score += 0.4
        print("✓ 'workbench.colorTheme' property found (0.4 points)")
    else:
        print("✗ 'workbench.colorTheme' property not found in any settings file")

    # 3) Is it set to the correct theme?
    if correct_theme_found:
        total_score += 0.4
        print("✓ Theme is correctly set to 'Tomorrow Night Blue' (0.4 points)")
    else:
        print("✗ Theme is NOT set to 'Tomorrow Night Blue'")

    # Cap at 1.0 and round for neatness
    final_score = round(min(total_score, 1.0), 2)
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_vscode_theme()

