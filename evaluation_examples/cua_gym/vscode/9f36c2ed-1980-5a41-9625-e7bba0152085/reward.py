"""
FINAL REWARD SCRIPT - SUCCESS
Task: I keep forgetting to hit save while refactoring my TypeScript project—could you set VS Code to automatically save any file changes after 3 seconds of inactivity?
Generated: 2025-09-11 16:46:29
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
import json
import re
import pathlib
from typing import List, Optional

"""
Reward Verification Script for VS Code Auto-Save Configuration
=============================================================
Verifies that Visual Studio Code is configured to automatically save file
changes *after 3 seconds of inactivity* (i.e.            
  files.autoSave      == "afterDelay" **and**
  files.autoSaveDelay == 3000
)

The script inspects user-level and workspace-level settings.json files located
inside the current user's home directory.  Progressive scoring is applied:
    • 1.0 – Both settings correctly configured in at least one file
    • 0.6 – autoSave is "afterDelay" but delay is incorrect/missing
    • 0.4 – delay is 3000 but autoSave mode incorrect/missing
    • 0.3 / 0.2 – partial presence of settings with wrong values
    • ≤0.1 – little to no progress

The final line prints "REWARD: X.X" where X.X ∈ [0.0, 1.0].
"""

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _strip_json_comments(raw: str) -> str:
    """Remove // comments and trailing commas so json.loads succeeds."""
    without_comments = re.sub(r"//.*", "", raw)
    cleaned = re.sub(r",\s*([}\]])", r"\1", without_comments)
    return cleaned


def _load_settings(path: pathlib.Path) -> Optional[dict]:
    """Load a VS Code settings.json file into a dict (tolerates comments)."""
    try:
        return json.loads(_strip_json_comments(path.read_text()))
    except Exception as e:
        print(f"✗ Could not parse {path}: {e}")
        return None


def _discover_settings_files(home: pathlib.Path) -> List[pathlib.Path]:
    """Gather plausible VS Code settings.json paths under the user's home."""
    fixed = [
        home / ".config/Code/User/settings.json",          # Standard VS Code
        home / ".config/Code - OSS/User/settings.json",    # OSS build
        home / ".vscode/settings.json",                    # VS Code folder in home
    ]

    # Also search workspace .vscode/settings.json (depth-limited for speed)
    max_depth, max_files = 4, 50
    for root, dirs, files in os.walk(home):
        rel_depth = len(pathlib.Path(root).relative_to(home).parts)
        if rel_depth > max_depth:
            dirs[:] = []               # prune deep traversal
            continue
        if "settings.json" in files and ".vscode" in root.split(os.sep):
            fixed.append(pathlib.Path(root) / "settings.json")
            if len(fixed) >= max_files:
                break
    return [p for p in fixed if p.exists()]

# ---------------------------------------------------------------------------
# Core verification logic
# ---------------------------------------------------------------------------

def verify_vscode_autosave() -> float:
    home = pathlib.Path.home()
    settings_files = _discover_settings_files(home)
    print(f"Discovered {len(settings_files)} settings file(s) to inspect.\n")

    autosave_afterdelay = False
    delay_3000 = False
    autosave_any = False
    delay_any = False

    for path in settings_files:
        data = _load_settings(path)
        if data is None:
            continue

        auto_val = data.get("files.autoSave")
        delay_val = data.get("files.autoSaveDelay")

        print(f"Inspecting {path} -> files.autoSave={auto_val!r}, files.autoSaveDelay={delay_val!r}")

        if auto_val is not None:
            autosave_any = True
        if delay_val is not None:
            delay_any = True

        if isinstance(auto_val, str) and auto_val.lower() == "afterdelay":
            autosave_afterdelay = True
        if isinstance(delay_val, (int, float)) and abs(delay_val - 3000) < 1:
            delay_3000 = True

    # -------------------- Scoring --------------------
    score = 0.0

    if autosave_afterdelay and delay_3000:
        print("\n✓ Auto-save correctly set to 'afterDelay' with 3000 ms delay.")
        score = 1.0
    else:
        if autosave_afterdelay:
            print("\n✓ 'afterDelay' mode found, but delay incorrect/missing.")
            score += 0.6
        elif autosave_any:
            print("\n✗ Auto-save mode set but not 'afterDelay'.")
            score += 0.3
        else:
            print("\n✗ No auto-save mode configured.")

        if delay_3000:
            print("✓ Correct 3000 ms delay found, but auto-save mode incorrect/missing.")
            score += 0.4
        elif delay_any:
            print("✗ files.autoSaveDelay present but not 3000 ms.")
            score += 0.2
        else:
            print("✗ No delay setting configured.")

        score = min(score, 0.9)  # cap partial credit

    print(f"\nREWARD: {score}")
    return score


if __name__ == "__main__":
    verify_vscode_autosave()
