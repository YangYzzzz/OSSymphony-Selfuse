"""
FINAL REWARD SCRIPT - SUCCESS
Task: The room is really bright today and my current dark interface is hard to see—could you change VS Code to the “Solarized Light” color theme?
Generated: 2025-09-11 16:38:15
Status: success
Model: azure-o3
Total Steps: 3
"""

import os
import json
import traceback

def verify_vscode_theme():
    """Reward script to verify that VS Code is using the `Solarized Light` color theme.

    Scoring breakdown (adds up to 1.0):
        • 0.2 – A VS Code settings.json file is found in a standard location.
        • 0.3 – The key "workbench.colorTheme" exists in that settings file.
        • 0.5 – The value of "workbench.colorTheme" is exactly "Solarized Light" (case-insensitive).
    """

    # Common locations for VS Code user-level settings
    candidate_paths = [
        os.path.expanduser("~/.config/Code/User/settings.json"),      # Standard VS Code (Linux)
        os.path.expanduser("~/.config/Code - OSS/User/settings.json"),# OSS build
        os.path.expanduser("~/.vscode/settings.json")                 # Portable / fallback
    ]

    total_score = 0.0
    max_score = 1.0

    settings_found      = False
    theme_key_found     = False
    correct_theme_set   = False

    chosen_path  = None
    settings_data = None

    # Locate and parse the first existing settings.json
    for path in candidate_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    settings_found = True
                    chosen_path = path
                    settings_data = data
                    # Check for the theme key and value
                    if "workbench.colorTheme" in data:
                        theme_key_found = True
                        if str(data["workbench.colorTheme"]).strip().lower() == "solarized light".lower():
                            correct_theme_set = True
                    break  # Stop after first valid settings.json
            except Exception as e:
                print(f"Error reading {path}: {e}")
                traceback.print_exc()
                continue

    # Progressive scoring based on actual verification
    if settings_found:
        print(f"✓ VS Code settings file found: {chosen_path}")
        total_score += 0.2
    else:
        print("✗ No VS Code settings file found in expected locations.")
        print("REWARD: 0.0")
        return 0.0  # Early exit – cannot proceed without settings

    if theme_key_found:
        print("✓ 'workbench.colorTheme' key present in settings.json")
        total_score += 0.3
    else:
        print("✗ 'workbench.colorTheme' key not found in settings.json")

    if correct_theme_set:
        print("✓ VS Code color theme is set to 'Solarized Light'")
        total_score += 0.5
    else:
        if theme_key_found:
            print(f"✗ VS Code color theme is NOT set to 'Solarized Light'. Found: '{settings_data.get('workbench.colorTheme')}'")

    # Cap the score at max_score
    total_score = min(total_score, max_score)

    print(f"Total score: {total_score}/{max_score}")
    print(f"REWARD: {total_score}")
    return total_score

if __name__ == "__main__":
    verify_vscode_theme()
