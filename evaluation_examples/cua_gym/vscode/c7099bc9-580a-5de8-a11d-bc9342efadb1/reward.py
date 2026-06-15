"""
FINAL REWARD SCRIPT - SUCCESS
Task: Whenever I tweak my Python scripts, VS Code’s Auto Save keeps firing off the program before I’m ready. How can I disable Auto Save so I can decide when to save manually?
Generated: 2025-09-11 17:32:46
Status: success
Model: azure-o3
Total Steps: 9
"""

import os
import json
import pathlib
import re
from typing import List, Dict

"""
Reward Script: Verify VS Code Auto Save is disabled
==================================================
This script inspects every relevant VS Code *settings.json* file it can find
inside the user’s HOME directory and awards a progressive score based on the
actual configuration of the **files.autoSave** setting.

Scoring rubric
--------------
1.0  ➜  All discovered settings either:
        • explicitly set  files.autoSave = "off"      OR
        • do **not** define files.autoSave (falls back to "off")
0.5  ➜  A mix of good (off / unset) and bad (on / afterDelay / …) values
0.2  ➜  Every discovered file explicitly enables Auto Save

The script prints detailed diagnostics for transparency and finally prints the
reward as:  REWARD: <score>
"""

###############################################################################
# Helper functions
###############################################################################

def parse_vscode_settings(path: pathlib.Path) -> Dict:
    """Load VS Code-style JSON that may contain // comments and trailing commas."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        print(f"    ✗ Could not read {path}: {exc}")
        return {}

    # Remove /* … */ comments
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)

    cleaned_lines = []
    for line in text.splitlines():
        stripped = line.lstrip()
        # Drop whole-line // comments
        if stripped.startswith("//"):
            continue
        # Remove inline // comments that are outside quotes (simple heuristic)
        if "//" in line:
            prefix, _ = line.split("//", 1)
            if prefix.count("\"") % 2 == 0:   # outside quoted strings
                line = prefix
        cleaned_lines.append(line)

    cleaned_text = "\n".join(cleaned_lines)
    # Drop trailing commas before } or ]
    cleaned_text = re.sub(r",\s*([}\]])", r"\1", cleaned_text)

    try:
        return json.loads(cleaned_text or "{}")
    except json.JSONDecodeError as exc:
        print(f"    ✗ JSON parse error in {path}: {exc}")
        return {}


def discover_settings_files(home: pathlib.Path) -> List[pathlib.Path]:
    """Return every VS Code settings.json file worth checking inside HOME."""
    candidates: List[pathlib.Path] = []

    # Standard product directories
    for product in ["Code", "Code - OSS", "Code - Insiders", "VSCodium"]:
        candidates.append(home / ".config" / product / "User" / "settings.json")

    # Workspace settings ( .vscode/settings.json ) up to depth 5
    for root, dirs, _ in os.walk(home):
        depth = len(pathlib.Path(root).relative_to(home).parts)
        if depth > 5:
            dirs[:] = []  # prune search
            continue
        if ".vscode" in dirs:
            candidates.append(pathlib.Path(root) / ".vscode" / "settings.json")

    # Keep only unique, existing paths
    unique_paths = []
    seen = set()
    for p in candidates:
        if p.exists() and p not in seen:
            unique_paths.append(p)
            seen.add(p)
    return unique_paths

###############################################################################
# Verification logic
###############################################################################

def verify_task() -> float:
    """Main entry: checks Auto Save configuration and returns a reward score."""

    print("Checking VS Code Auto Save configuration…\n")

    home = pathlib.Path.home()
    settings_files = discover_settings_files(home)
    print(f"Found {len(settings_files)} settings.json file(s) to inspect.")
    for p in settings_files:
        print(f" - {p}")

    # Categorise each file
    good_files = []   # Auto Save off or unset (default off)
    bad_files = []    # Auto Save explicitly on / afterDelay / etc.

    for path in settings_files:
        data = parse_vscode_settings(path)
        value = data.get("files.autoSave", None)

        if value is None:
            print(f"    files.autoSave not set in {path} (defaults to 'off')")
            good_files.append(path)
        else:
            val_normalised = str(value).strip().lower()
            print(f"    files.autoSave = '{val_normalised}' in {path}")

            if val_normalised == "off":
                good_files.append(path)
            else:
                bad_files.append((path, val_normalised))

    ############################################################################
    # Scoring
    ############################################################################

    if not bad_files:
        print("✓ No settings enable Auto Save. Verified disabled everywhere.")
        score = 1.0
    else:
        if good_files:
            print("✗ Some settings files enable Auto Save – partial credit.")
            score = 0.5
        else:
            print("✗ All discovered settings enable Auto Save – minimal credit.")
            score = 0.2

    print(f"\nFinal Score: {score}")
    print(f"REWARD: {score}")
    return score

###############################################################################
# Script entry-point (only executed when run, not on import)
###############################################################################

if __name__ == "__main__":
    verify_task()

