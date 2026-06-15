"""
FINAL REWARD SCRIPT - SUCCESS
Task: Our project’s style guide caps line length at 85 characters—could you show me how to add a vertical ruler at that mark in VS Code?
Generated: 2025-09-11 18:16:25
Status: success
Model: azure-o3
Total Steps: 13
"""

import json
import re
import pathlib
from typing import List, Any

# -------------------------------------------------------------
# VS Code Vertical Ruler Verification Script
# -------------------------------------------------------------
# This script awards up to 1.0 points for correctly configuring
# a vertical ruler at column 85 in VS Code.  Partial credit is
# given if a ruler is configured but not at the correct column.
# -------------------------------------------------------------

# ------------- Helper functions --------------------------------

def _strip_jsonc_comments(text: str) -> str:
    """Remove // and /* */ comments so the text becomes valid JSON."""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)   # block comments
    text = re.sub(r"//.*", "", text)                            # line comments
    return text


def _load_jsonc(path: pathlib.Path) -> Any:
    """Load a VS Code settings file that may contain comments (JSONC)."""
    raw = path.read_text(encoding="utf-8", errors="ignore")
    cleaned = _strip_jsonc_comments(raw)
    # Remove simple trailing commas that break json.loads
    cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)
    return json.loads(cleaned)


def _extract_ruler_columns(value) -> List[int]:
    """Return a list of ruler columns encoded in an editor.rulers value."""
    cols: List[int] = []
    if isinstance(value, int):
        cols.append(value)
    elif isinstance(value, str) and value.strip().isdigit():
        cols.append(int(value.strip()))
    elif isinstance(value, list):
        for item in value:
            cols.extend(_extract_ruler_columns(item))
    elif isinstance(value, dict):
        # Object form: {"column": 80, "color": "#ff0000"}
        col = value.get("column")
        cols.extend(_extract_ruler_columns(col))
    return cols


def _locate_settings_files() -> List[pathlib.Path]:
    """Find all relevant VS Code settings.json files (user & workspace)."""
    home = pathlib.Path.home()
    candidates: List[pathlib.Path] = [
        home / ".config" / "Code" / "User" / "settings.json",             # Stable
        home / ".config" / "Code - Insiders" / "User" / "settings.json",  # Insiders
    ]

    # Any workspace settings.json inside a .vscode folder under the home dir
    for p in home.rglob("settings.json"):
        if ".vscode" in p.parts:
            candidates.append(p)

    # Deduplicate & keep only existing files
    unique: List[pathlib.Path] = []
    seen = set()
    for c in candidates:
        if c.exists():
            try:
                resolved = c.resolve()
            except Exception:
                resolved = c
            if resolved not in seen:
                seen.add(resolved)
                unique.append(resolved)
    return unique

# ------------- Main verification logic -------------------------

def verify_task() -> float:
    """Verify that a vertical ruler at column 85 exists in any settings.json."""
    settings_files = _locate_settings_files()
    print(f"Discovered {len(settings_files)} potential settings.json files to inspect")

    rulers_property_found = False  # Did we see any editor.rulers property?
    ruler85_found = False          # Did any property contain column 85?

    for settings_path in settings_files:
        try:
            data = _load_jsonc(settings_path)
        except Exception as e:
            print(f"✗ Could not parse {settings_path}: {e}")
            continue

        if "editor.rulers" in data:
            val = data["editor.rulers"]
            columns = _extract_ruler_columns(val)
            print(f"✓ {settings_path}: editor.rulers -> {val} | parsed columns: {columns}")
            rulers_property_found = True
            if 85 in columns:
                ruler85_found = True
        else:
            print(f"{settings_path}: no editor.rulers property present")

    # Progressive scoring
    score = 0.0
    if rulers_property_found:
        score += 0.5
    else:
        print("✗ No editor.rulers property found in any inspected settings.json file")

    if ruler85_found:
        score += 0.5
    else:
        print("✗ A ruler at column 85 was NOT found in any settings.json file")

    score = min(score, 1.0)
    print(f"REWARD: {score}")
    return score

# ------------- Entry point -------------------------------------

if __name__ == "__main__":
    verify_task()
