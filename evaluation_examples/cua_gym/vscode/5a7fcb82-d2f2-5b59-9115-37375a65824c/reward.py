"""
FINAL REWARD SCRIPT - SUCCESS
Task: The bright theme is straining my eyes during late-night coding—could you change my VS Code color scheme to the “Dracula” theme?
Generated: 2025-09-11 17:19:08
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
import json
import re
import traceback

"""
Reward Script: VS Code Dracula Theme Verification
-------------------------------------------------
This script verifies that the user has successfully changed their VS Code
colour scheme to the **“Dracula”** theme.
It awards a progressive score based on:
    • locating VS Code *settings.json* (0.2)
    • presence of the `workbench.colorTheme` key     (0.3)
    • value of that key including the word “Dracula” (0.5)
The script prints detailed diagnostics and always outputs
`REWARD: <score>` where `<score>` ∈ [0.0, 1.0].
"""

# ---------------------------------------------------------------------------
# Helper: robustly parse a settings.json file (tolerates // comments)
# ---------------------------------------------------------------------------

def _parse_settings(path):
    """Return tuple (key_present: bool, theme_value: str | None)."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        # Strip line comments beginning with // (very common in VS Code JSON)
        cleaned_lines = [ln for ln in raw.splitlines() if not ln.strip().startswith("//")]
        cleaned = "\n".join(cleaned_lines)
        try:
            data = json.loads(cleaned)
            if "workbench.colorTheme" in data:
                return True, str(data["workbench.colorTheme"])
        except Exception:
            pass  # fall back to regex below if JSON parsing fails
        # Regex fallback for non-strict JSON
        m = re.search(r"\"workbench\\.colorTheme\"\s*:\s*\"([^\"]+)\"", raw, re.I)
        if m:
            return True, m.group(1)
        return False, None
    except Exception as e:
        print(f"Error reading {path}: {e}")
        traceback.print_exc()
        return False, None

# ---------------------------------------------------------------------------
# Main verification routine
# ---------------------------------------------------------------------------

def verify_vscode_dracula_theme():
    home = os.path.expanduser("~")

    # Common locations for VS Code user settings
    candidate_dirs = [
        os.path.join(home, ".config", "Code", "User"),          # regular VS Code on Linux
        os.path.join(home, ".config", "Code - OSS", "User"),     # open-source build
        os.path.join(home, ".config", "VSCodium", "User"),      # VSCodium
        os.path.join(home, ".vscode-server", "data", "User"),   # VS Code server (SSH/WSL)
        os.path.join(home, ".vscode-server", "data", "Machine"),
    ]

    # Collect any settings.json files
    settings_files = [os.path.join(d, "settings.json") for d in candidate_dirs if os.path.isfile(os.path.join(d, "settings.json"))]

    # Light fallback search (depth ≤ 4) for unexpected install paths
    if not settings_files:
        for root, dirs, files in os.walk(home):
            depth = root.count(os.sep) - home.count(os.sep)
            if depth > 4:
                dirs[:] = []  # prune deep traversal
                continue
            if root.endswith("User") and "settings.json" in files:
                settings_files.append(os.path.join(root, "settings.json"))
                break

    total_score = 0.0

    # -------------------------------------------------------
    # 1. Settings file found? (0.2 points)
    # -------------------------------------------------------
    if settings_files:
        print(f"✓ Found settings file(s): {settings_files} (0.2 points)")
        total_score += 0.2
    else:
        print("✗ No VS Code settings.json files located — unable to verify theme")
        print(f"REWARD: {total_score}")
        return total_score  # cannot continue without settings

    # -------------------------------------------------------
    # 2. Check for workbench.colorTheme key (0.3 points)
    # 3. Verify Dracula theme value    (0.5 points)
    # -------------------------------------------------------
    key_present = False
    dracula_set = False
    last_value = None

    for path in settings_files:
        present, value = _parse_settings(path)
        print(f"Parsed {path}: present={present}, value={value}")
        if present:
            key_present = True
            last_value = value
            if value and "dracula" in value.lower():
                dracula_set = True

    if key_present:
        print("✓ workbench.colorTheme key detected (0.3 points)")
        total_score += 0.3
    else:
        print("✗ workbench.colorTheme key absent in all settings files")

    if dracula_set:
        print("✓ Dracula theme is configured (0.5 points)")
        total_score += 0.5
    else:
        if key_present:
            print(f"✗ Theme is set to '{last_value}', not Dracula (0.1 points)")
            total_score += 0.1  # some credit: a theme is set but not Dracula
        else:
            print("✗ Dracula theme not set (0 points)")

    # Ensure score never exceeds 1.0
    final_score = min(total_score, 1.0)
    print(f"Total score: {final_score}\nREWARD: {final_score}")
    return final_score

# ---------------------------------------------------------------------------
# Script entry-point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    verify_vscode_dracula_theme()
