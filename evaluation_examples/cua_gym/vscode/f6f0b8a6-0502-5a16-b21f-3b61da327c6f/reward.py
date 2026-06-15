"""
FINAL REWARD SCRIPT - SUCCESS
Task: I keep forgetting to hit save while working on my React project—could you set VS Code to automatically save my files 5 seconds after I stop typing?
Generated: 2025-09-11 18:36:33
Status: success
Model: azure-o3
Total Steps: 5
"""

import os
import json
import re
from pathlib import Path

"""
Reward Script: Verify VS Code is configured to auto-save files
5 seconds after the user stops typing.

Success Criteria (progressive scoring):
1. files.autoSave is set to "afterDelay"  → 0.5 pts
2. files.autoSaveDelay equals 5000        → 0.5 pts
Returns a float from 0.0 to 1.0.
Prints detailed diagnostics and the final score as
"REWARD: X.X" (required by evaluation harness).
"""

def _load_jsonc(file_path: Path):
    """Load a VS Code JSON with comments (jsonc)."""
    try:
        text = file_path.read_text(encoding="utf-8")
        # Strip // line comments
        text = re.sub(r"//.*", "", text)
        # Strip /* block comments */
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
        # Remove trailing commas before }} or ]
        text = re.sub(r",\s*([}\]])", r"\1", text)
        text = text.strip()
        return json.loads(text) if text else {}
    except Exception as exc:
        print(f"   ! Failed to parse {file_path}: {exc}")
        return None

def _discover_settings_files(max_depth: int = 6):
    """Return a list of existing VS Code settings.json locations (user + workspace)."""
    home = Path.home()
    common_user_paths = [
        home / ".config" / "Code" / "User" / "settings.json",
        home / ".config" / "Code - OSS" / "User" / "settings.json",
        home / ".config" / "Code - Insiders" / "User" / "settings.json",
        home / ".config" / "VSCodium" / "User" / "settings.json",
        home / ".vscode-oss" / "User" / "settings.json",
    ]

    candidates = [p for p in common_user_paths if p.exists()]

    # Search for workspace .vscode/settings.json files (shallow scan)
    for root, dirs, files in os.walk(home):
        depth = len(Path(root).relative_to(home).parts)
        if depth > max_depth:
            dirs[:] = []  # prune deeper paths
            continue
        if "settings.json" in files and Path(root).name in {".vscode", "User"}:
            candidates.append(Path(root) / "settings.json")

    # De-duplicate while preserving order
    seen = set()
    unique = []
    for p in candidates:
        rp = str(p.resolve())
        if rp not in seen:
            unique.append(p)
            seen.add(rp)
    return unique

def verify_vscode_autosave():
    print("Checking VS Code auto-save configuration…")
    settings_files = _discover_settings_files()
    print(f"Discovered {len(settings_files)} settings.json file(s).")

    autosave_after_delay = False
    delay_is_5000 = False

    for path in settings_files:
        data = _load_jsonc(path)
        if data is None:
            continue  # skip unreadable files
        auto_val = data.get("files.autoSave")
        delay_val = data.get("files.autoSaveDelay")
        print(f"- {path}: files.autoSave={auto_val} | files.autoSaveDelay={delay_val}")

        if isinstance(auto_val, str) and auto_val.lower() == "afterdelay":
            autosave_after_delay = True
        if delay_val is not None:
            try:
                if int(delay_val) == 5000:
                    delay_is_5000 = True
            except (ValueError, TypeError):
                pass

    # Progressive scoring
    score = 0.0
    if autosave_after_delay:
        score += 0.5
        print("✓ 'files.autoSave' is set to 'afterDelay' (0.5)")
    else:
        print("✗ 'files.autoSave' is NOT set to 'afterDelay'")

    if delay_is_5000:
        score += 0.5
        print("✓ 'files.autoSaveDelay' is 5000 ms (0.5)")
    else:
        print("✗ 'files.autoSaveDelay' is NOT 5000 ms")

    final_score = round(min(score, 1.0), 2)
    print(f"REWARD: {final_score}")
    return final_score

# Execute when run as a script
if __name__ == "__main__":
    verify_vscode_autosave()
