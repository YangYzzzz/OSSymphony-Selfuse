"""
FINAL REWARD SCRIPT - SUCCESS
Task: My project at /home/user/dev/ is cluttered with JetBrains’ “.idea” folders that keep showing up in the Explorer. Could you help me hide every folder named “.idea” so they don’t appear in the VS Code file tree?
Generated: 2025-09-11 16:45:10
Status: success
Model: azure-o3
Total Steps: 16
"""

import json
import re
import glob
from pathlib import Path

"""
Reward script for task:
    Hide all JetBrains “.idea” folders from VS Code’s Explorer view for the project
    located at /home/user/dev.

Verification Logic
------------------
1. Locate every relevant VS-Code *settings.json* file:
   • Workspace-level:  /home/user/dev/.vscode/settings.json and any nested
     .vscode/settings.json inside that project tree.
   • User-level:       ~/.config/Code*/User/settings.json  (covers Code, Code OSS,
     VSCodium, etc.)
   • Home-level:       ~/.vscode/settings.json (rare, but supported)

2. Parse each JSONC file safely (strip // and /* */ comments) so it becomes valid JSON.

3. Look inside these setting sections, in order of importance:
      a) files.exclude
      b) explorer.exclude
      c) (fallback / partial credit) search.exclude
   and search for any glob pattern that contains “.idea” **and** is enabled (true / "true" / dict).

4. Scoring (progressive):
      • 1.0  – At least one pattern hiding “.idea” in files.exclude or explorer.exclude
                ( Explorer view really hides it )
      • 0.7  – Absent from Explorer excludes but present in search.exclude only
      • 0.0  – No exclusion found

The script prints detailed diagnostics, computes the score, prints
"REWARD: <score>", and returns the float so the grading harness can pick it up.
"""

def _load_jsonc(path: Path):
    """Load a VS Code JSON-with-comments (JSONC) safely."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"   ✗ Could not read {path}: {e}")
        return None

    # Remove /* */ block comments first
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)

    # Remove // line comments that are *outside* of string literals
    cleaned_lines = []
    for line in text.splitlines():
        if "//" in line:
            pre, _, _ = line.partition("//")
            if pre.count("\"") % 2 == 0:        # even quote count  -> outside string
                line = pre                       # strip comment part
        cleaned_lines.append(line)

    try:
        return json.loads("\n".join(cleaned_lines) or "{}")
    except json.JSONDecodeError as e:
        print(f"   ✗ JSON parse error in {path}: {e}")
        return None


def _discover_settings_files(project_root: Path) -> list[Path]:
    """Return list of workspace + user VS-Code settings.json files to inspect."""
    files: list[Path] = []

    # 1. Workspace top-level .vscode
    ws_top = project_root / ".vscode" / "settings.json"
    if ws_top.exists():
        files.append(ws_top)

    # 2. Any nested workspaces within the project tree
    for p in project_root.rglob(".vscode/settings.json"):
        if p not in files:
            files.append(p)

    # 3. User settings for all Code variants under ~/.config
    for user_dir in glob.glob(str(Path.home() / ".config" / "Code*" / "User")):
        candidate = Path(user_dir) / "settings.json"
        if candidate.exists():
            files.append(candidate)

    # 4. Home-level .vscode (occasionally used)
    home_vs = Path.home() / ".vscode" / "settings.json"
    if home_vs.exists():
        files.append(home_vs)

    return files


def _pattern_targets_idea(pattern: str) -> bool:
    return ".idea" in pattern.lower()


def _value_enabled(val) -> bool:
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.strip().lower() in {"true", "yes"}
    if isinstance(val, dict):
        return True   # dict signals conditional exclusion – still active
    return False


def _section_hides_idea(data: dict, section: str) -> bool:
    sect = data.get(section)
    if not isinstance(sect, dict):
        return False
    for pattern, value in sect.items():
        if _pattern_targets_idea(pattern) and _value_enabled(value):
            return True
    return False


def verify_hide_idea(project_root: Path = Path("/home/user/dev")) -> float:
    print("Starting verification of '.idea' exclusion in VS Code settings...\n")

    settings_files = _discover_settings_files(project_root)
    if settings_files:
        print("Settings files discovered:")
        for f in settings_files:
            print(" •", f)
    else:
        print("✗ No VS Code settings.json files found.")

    found_explorer_exclude = False  # files.exclude or explorer.exclude
    found_search_only      = False  # search.exclude only

    for path in settings_files:
        data = _load_jsonc(path)
        if data is None:
            continue

        if (_section_hides_idea(data, "files.exclude") or
                _section_hides_idea(data, "explorer.exclude")):
            found_explorer_exclude = True
            print(f"✓ '.idea' exclusion found impacting Explorer in: {path}")
        elif _section_hides_idea(data, "search.exclude"):
            # only mark if explorer-exclude was NOT found earlier
            found_search_only = True
            print(f"△ '.idea' exclusion found only in search.exclude in: {path}")

    # ---------- Progressive Scoring ----------
    if found_explorer_exclude:
        score = 1.0      # Full success – hidden from Explorer
    elif found_search_only:
        score = 0.7      # Partially addressed – hidden from search only
    else:
        score = 0.0      # Not addressed

    print(f"\nComputed score: {score}")
    return score

# ----------------------
# Entrypoint for grader
# ----------------------
if __name__ == "__main__":
    reward = verify_hide_idea()
    print(f"REWARD: {reward}")

