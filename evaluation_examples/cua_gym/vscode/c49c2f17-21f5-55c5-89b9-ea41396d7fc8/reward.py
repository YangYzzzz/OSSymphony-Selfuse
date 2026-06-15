"""
FINAL REWARD SCRIPT - SUCCESS
Task: Every time I open my legacy PHP project, VS Code floods the editor with red squiggles for syntax issues I can’t tackle right now—how can I temporarily turn off PHP syntax error reporting so I can focus on other changes?
Generated: 2025-09-11 23:37:13
Status: success
Model: azure-o3
Total Steps: 13
"""

import os
import json
import re
import pathlib

# ----------------------------- Helper Functions -----------------------------

def _strip_json_comments(text: str) -> str:
    """Remove // line comments and /* ... */ block comments from JSONC text."""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)  # block comments
    text = re.sub(r"//.*", "", text)                         # line comments
    return text


def _load_jsonc(path: str):
    """Load a VS Code JSON/JSONC settings file and return a dict or None on failure."""
    try:
        raw = pathlib.Path(path).read_text(encoding="utf-8")
    except Exception as e:
        print(f"    ✗ Could not read {path}: {e}")
        return None

    cleaned = _strip_json_comments(raw)
    # Remove trailing commas which are allowed in VS Code settings
    cleaned = re.sub(r",\s*(\]|\})", r"\1", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"    ✗ JSON decode error in {path}: {e}")
        return None


# --------------------------- Discovery Functions ---------------------------

def _candidate_settings_files(home: str):
    """Return a de-duplicated list of user & workspace VS Code settings.json files."""
    files = []

    # Common user-level settings locations (Linux focus)
    user_dirs = [
        os.path.join(home, ".config", "Code", "User"),           # VS Code
        os.path.join(home, ".config", "Code - OSS", "User"),    # Code - OSS
        os.path.join(home, ".config", "VSCodium", "User"),      # VSCodium
        os.path.join(home, ".vscode", "User"),                  # Portable/Insiders
    ]
    for d in user_dirs:
        p = os.path.join(d, "settings.json")
        if os.path.isfile(p):
            files.append(p)

    # Workspace-level settings:  .vscode/settings.json inside projects
    for dirpath, dirnames, _ in os.walk(home):
        # Skip hidden dirs for speed, but keep ".vscode" itself
        dirnames[:] = [dn for dn in dirnames if not dn.startswith(".") or dn == ".vscode"]
        if ".vscode" in dirnames:
            p = os.path.join(dirpath, ".vscode", "settings.json")
            if os.path.isfile(p):
                files.append(p)

    # De-duplicate while preserving order
    seen, unique = set(), []
    for f in files:
        if f not in seen:
            unique.append(f)
            seen.add(f)
    return unique


# --------------------------- Verification Logic ----------------------------

def verify_task(home: str = "/home/user") -> float:
    """Verify that PHP diagnostics are disabled in VS Code settings."""

    print(f"Searching for VS Code settings that disable PHP diagnostics in '{home}'…")

    settings_files = _candidate_settings_files(home)
    if not settings_files:
        print("✗ No VS Code settings.json files found – task not completed")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found {len(settings_files)} settings file(s):")
    for p in settings_files:
        print(f"  - {p}")

    # Track findings
    any_relevant_key = False        # At least one of the diagnostic keys is present
    diagnostics_disabled = False    # Any relevant key explicitly set to false

    # Inspect each settings file
    for path in settings_files:
        data = _load_jsonc(path)
        if data is None:
            continue

        # Built-in PHP validation
        if "php.validate.enable" in data:
            any_relevant_key = True
            if data.get("php.validate.enable") is False:
                diagnostics_disabled = True
                print(f"  ✓ 'php.validate.enable' is false in {path}")
            else:
                print(f"    'php.validate.enable' is {data.get('php.validate.enable')} in {path}")

        # Intelephense diagnostics (most common PHP language server)
        if "intelephense.diagnostics.enable" in data:
            any_relevant_key = True
            if data.get("intelephense.diagnostics.enable") is False:
                diagnostics_disabled = True
                print(f"  ✓ 'intelephense.diagnostics.enable' is false in {path}")
            else:
                print(f"    'intelephense.diagnostics.enable' is {data.get('intelephense.diagnostics.enable')} in {path}")

    # --------------------------- Scoring Rules ---------------------------
    # 0.0  – No relevant settings found
    # 0.3  – At least one diagnostic-related key present (effort shown)
    # 1.0  – Any diagnostic key explicitly set to false (PHP squiggles disabled)

    score = 0.0
    if any_relevant_key:
        score += 0.3
    if diagnostics_disabled:
        score += 0.7

    score = min(score, 1.0)  # Safety cap

    if score == 1.0:
        print("✓ PHP diagnostics have been disabled – full completion")
    elif score == 0.3:
        print("✗ Diagnostic keys present but still enabled – partial completion (0.3)")
    else:
        print("✗ No evidence of disabling diagnostics – task incomplete")

    print(f"REWARD: {score}")
    return score


# ----------------------------- Script Entrypoint ----------------------------
if __name__ == "__main__":
    verify_task("/home/user")
