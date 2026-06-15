"""
FINAL REWARD SCRIPT - SUCCESS
Task: I've been staring at the default colors all day—could you help me switch VS Code to the “Material Theme” so the interface is easier on my eyes?
Generated: 2025-09-11 17:39:05
Status: success
Model: azure-o3
Total Steps: 6
"""

import os
import json
import re

"""
Reward Script: Verify VS Code is switched to the “Material Theme”.

Scoring rubric (progressive):
• 0.7 pts – VS Code’s workbench.colorTheme is set to any theme that contains the word “Material” (case-insensitive)
• 0.3 pts – At least one installed extension folder whose name contains “material” (case-insensitive)

The script searches common locations for VS Code’s settings.json and the extensions folder.
It prints detailed diagnostics and finishes with a single line:  
    REWARD: X.X
where X.X ∈ {0.0 … 1.0}
"""

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def find_settings_file():
    """Return the first VS Code settings.json found in common paths, else None."""
    home = os.path.expanduser("~")
    candidates = [
        os.path.join(home, ".config", "Code", "User", "settings.json"),          # Linux (Microsoft build)
        os.path.join(home, ".config", "Code - OSS", "User", "settings.json"),    # Linux OSS build
        os.path.join(home, ".config", "VSCodium", "User", "settings.json"),     # VSCodium
        os.path.join(home, ".vscode", "settings.json"),                           # Portable / devcontainer
        os.path.join(home, "AppData", "Roaming", "Code", "User", "settings.json"),  # Windows
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    return None


def theme_is_material(settings_path):
    """Return (True, theme_value) if the current theme contains the word ‘material’."""
    try:
        with open(settings_path, "r", encoding="utf-8") as fp:
            data = json.load(fp)
    except Exception as exc:
        print(f"✗ Error reading/parsing settings.json: {exc}")
        return False, None

    theme_value = data.get("workbench.colorTheme")
    if theme_value and "material" in theme_value.lower():
        return True, theme_value
    return False, theme_value


def material_extension_installed():
    """Return (True, path) if an extension folder name contains ‘material’."""
    home = os.path.expanduser("~")
    ext_dirs = [
        os.path.join(home, ".vscode", "extensions"),        # Microsoft build (Linux/Win/Mac)
        os.path.join(home, ".vscode-oss", "extensions"),    # OSS build
        os.path.join(home, ".vscode-server", "extensions"), # Remote server install
    ]
    for ext_dir in ext_dirs:
        if os.path.isdir(ext_dir):
            for entry in os.listdir(ext_dir):
                if re.search(r"material", entry, re.IGNORECASE):
                    return True, os.path.join(ext_dir, entry)
    return False, None

# ---------------------------------------------------------------------------
# Main verification routine
# ---------------------------------------------------------------------------

def verify_task():
    total_score = 0.0  # progressive score
    max_score   = 1.0

    # 1) Verify theme
    settings_path = find_settings_file()
    if settings_path:
        print(f"✓ Found settings.json at: {settings_path}")
        theme_ok, theme_val = theme_is_material(settings_path)
        if theme_ok:
            print(f"✓ workbench.colorTheme is set to '{theme_val}' (Material detected) (+0.7)")
            total_score += 0.7
        else:
            print(f"✗ workbench.colorTheme is not a Material variant (current: {theme_val}) (+0.0)")
    else:
        print("✗ Could not locate VS Code settings.json (+0.0)")

    # 2) Verify extension presence
    ext_ok, ext_path = material_extension_installed()
    if ext_ok:
        print(f"✓ Material-related extension found: {ext_path} (+0.3)")
        total_score += 0.3
    else:
        print("✗ No Material-related extension found (+0.0)")

    # Cap score to 1.0
    total_score = min(total_score, max_score)

    print(f"REWARD: {total_score}")
    return total_score

# ---------------------------------------------------------------------------
# Execute verification when run as script
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    verify_task()
