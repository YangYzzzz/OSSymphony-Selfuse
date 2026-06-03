"""
FINAL REWARD SCRIPT - SUCCESS
Task: Our team’s style guide caps line length at 140 characters; can you help me add a ruler at the 140-character mark in VS Code so I can stay within that limit?
Generated: 2025-09-11 16:55:33
Status: success
Model: azure-o3
Total Steps: 13
"""

import pathlib
import re
from typing import List

"""
Reward Verification Script — VS Code 140-Character Ruler
-------------------------------------------------------
This script checks that Visual Studio Code is configured to show a 
ruler at column 140, as required by the task instructions.

Scoring (progressive):
• +0.4 points  – at least one rulers array ("editor.rulers" or nested 
  "rulers") is defined in any relevant settings.json file.
• +0.6 points  – value 140 appears in one of those arrays.

A perfect configuration therefore yields a score of 1.0.

Files inspected:
1. User settings:
   ~/.config/Code/User/settings.json
   ~/.config/Code - Insiders/User/settings.json
   ~/.config/VSCodium/User/settings.json
2. All workspace-level .vscode/settings.json files under the user’s 
   home directory.

JSONC comments (// or /* … */) are stripped before parsing so that 
commented settings are handled correctly.
"""

# ─────────────────────────── Helper Functions ──────────────────────────── #

def _strip_comments(text: str) -> str:
    """Remove line (// …) and block (/* … */) comments from JSONC."""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)  # block comments
    text = re.sub(r"(^|[^:])//.*", r"\1", text, flags=re.MULTILINE)  # line comments
    return text


def _extract_rulers(clean_content: str) -> List[int]:
    """Return a list of integer ruler columns found in the given text."""
    rulers: List[int] = []
    # Matches "editor.rulers": [ … ]  OR  "rulers": [ … ]
    pattern = r'"(?:editor\\.rulers|editor\.rulers|rulers)"\s*:\s*\[(.*?)\]'
    for match in re.finditer(pattern, clean_content, flags=re.DOTALL | re.IGNORECASE):
        inside = match.group(1)
        nums = re.findall(r"\b\d+\b", inside)
        rulers.extend(map(int, nums))
    return rulers


# ───────────────────────── File Discovery Logic ────────────────────────── #

def _discover_settings_files() -> List[pathlib.Path]:
    """Return a list of potential VS Code settings.json files."""
    home = pathlib.Path.home()
    candidates: List[pathlib.Path] = []

    # Standard user settings
    for user_path in [
        home / ".config" / "Code" / "User" / "settings.json",
        home / ".config" / "Code - Insiders" / "User" / "settings.json",
        home / ".config" / "VSCodium" / "User" / "settings.json",
    ]:
        if user_path.exists():
            candidates.append(user_path)

    # Workspace-level .vscode/settings.json files
    for path in home.rglob('settings.json'):
        if '.vscode' in path.parts and path not in candidates:
            candidates.append(path)

    return candidates


# ─────────────────────────── Verification ─────────────────────────────── #

def verify_task() -> float:
    """Verify task completion and return a score in the range [0.0, 1.0]."""
    settings_files = _discover_settings_files()
    print(f"Scanning {len(settings_files)} settings files…")

    prop_found = False      # Any rulers property present
    ruler_140_found = False # 140-column ruler present

    for file in settings_files:
        try:
            raw_text = file.read_text(encoding='utf-8', errors='ignore')
        except Exception as exc:
            print(f"⚠️  Cannot read {file}: {exc}")
            continue

        cleaned = _strip_comments(raw_text)
        rulers = _extract_rulers(cleaned)

        if rulers:
            prop_found = True
            print(f"✓ Rulers in {file}: {rulers}")
            if 140 in rulers:
                ruler_140_found = True
        else:
            print(f"✗ No rulers defined in {file}")

    # Progressive scoring
    score = 0.0
    if prop_found:
        score += 0.4
    if ruler_140_found:
        score += 0.6
    score = min(score, 1.0)

    print(f"prop_found={prop_found}, ruler_140_found={ruler_140_found}")
    print(f"REWARD: {score}")
    return score

# Execute verification when run as a standalone script
if __name__ == '__main__':
    verify_task()
