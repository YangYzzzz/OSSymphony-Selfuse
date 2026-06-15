"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’ve been refactoring a large TypeScript project for hours, and the default light theme is really straining my eyes—could you help me switch VS Code to the “Cobalt2” color theme instead?
Generated: 2025-09-11 16:25:47
Status: success
Model: azure-o3
Total Steps: 9
"""

import os
import re
import json
import pathlib

"""
Reward Script – VS Code “Cobalt2” Theme Verification

This script verifies that the user has successfully switched Visual Studio Code to the
“Cobalt2” colour theme.  Two concrete conditions are checked:

1. VS Code settings.json (any common location) contains a workbench.colorTheme
   entry whose value matches /Cobalt2/i  →  0.8 points (major requirement)
2. A Cobalt2-related extension directory is present in one of the standard
   VS Code extension folders                           →  0.2 points (supporting)

Progressive scoring is applied and the final score (0.0-1.0) is printed as
“REWARD: <score>”.
"""

def _strip_json_comments(text: str) -> str:
    """Remove // and /*…*/ comments so that JSONC becomes valid JSON."""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)  # block comments
    text = re.sub(r"//.*", "", text)                    # line comments
    return text


def _settings_paths() -> list[pathlib.Path]:
    """Return plausible VS Code settings.json paths (deduplicated)."""
    h = pathlib.Path.home()
    paths = [
        h / ".config" / "Code" / "User" / "settings.json",
        h / ".config" / "Code - OSS" / "User" / "settings.json",
        h / ".config" / "Code - Insiders" / "User" / "settings.json",
        h / ".vscode" / "data" / "user-data" / "User" / "settings.json",  # portable mode
    ]
    # Catch any other *Code*/User/settings.json variants
    paths.extend(h.glob(".config/*Code*/User/settings.json"))

    seen, unique = set(), []
    for p in paths:
        if p not in seen:
            unique.append(p)
            seen.add(p)
    return unique


def _theme_is_cobalt2(value: str) -> bool:
    return bool(re.search(r"cobalt\s*2", value, re.I) or re.search(r"cobalt2", value, re.I))


def _check_theme_setting() -> bool:
    """True if *any* VS Code settings.json sets colour theme to Cobalt2."""
    for path in _settings_paths():
        if not path.exists():
            continue
        raw = path.read_text(encoding="utf-8", errors="ignore")
        cleaned = _strip_json_comments(raw)
        try:
            data = json.loads(cleaned)
            theme_val = data.get("workbench.colorTheme")
            if theme_val and _theme_is_cobalt2(str(theme_val)):
                print(f"✓ Cobalt2 theme found in settings: {path} → {theme_val}")
                return True
            elif theme_val:
                print(f"Found different theme ('{theme_val}') in {path}")
        except json.JSONDecodeError as e:
            # Fallback: regex search in raw JSONC if parsing failed
            if re.search(r"\"workbench\\.colorTheme\"\s*:\s*\"[^\"]*cobalt2[^\"]*\"", raw, re.I):
                print(f"✓ Cobalt2 theme detected via regex in settings: {path}")
                return True
            else:
                print(f"Warning: could not parse {path}: {e}")
    print("✗ Cobalt2 theme not set in any recognised settings.json file")
    return False


def _check_cobalt_extension() -> bool:
    """True if a directory for the Cobalt2 theme extension exists."""
    h = pathlib.Path.home()
    ext_dirs = [
        h / ".vscode" / "extensions",        # normal desktop
        h / ".vscode-server" / "extensions",  # remote / WSL / SSH
        h / ".config" / "Code" / "extensions", # occasionally used path
    ]
    for ext_dir in ext_dirs:
        if ext_dir.exists():
            for d in ext_dir.iterdir():
                if d.is_dir() and re.search(r"cobalt2|wesbos\.theme-cobalt2", d.name, re.I):
                    print(f"✓ Cobalt2 extension directory found: {d}")
                    return True
    print("✗ Cobalt2 extension directory not found in expected locations")
    return False


def verify_task() -> float:
    print("Verifying VS Code configuration for the ‘Cobalt2’ colour theme…\n")
    theme_ok = _check_theme_setting()
    ext_ok   = _check_cobalt_extension()

    # Progressive scoring
    score = 0.0
    if theme_ok:
        score += 0.8  # major requirement (theme applied)
    if ext_ok:
        score += 0.2  # supporting requirement (extension installed)

    score = round(min(score, 1.0), 2)

    print("\nVerification summary:")
    print(f"  Theme correctly set : {theme_ok}")
    print(f"  Extension installed: {ext_ok}\n")
    print(f"REWARD: {score}")
    return score


if __name__ == "__main__":
    verify_task()
