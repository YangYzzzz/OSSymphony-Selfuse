"""
FINAL REWARD SCRIPT - SUCCESS
Task: I keep forgetting to save my edits while coding and it's causing me to lose work—can you help me turn on VS Code’s auto-save feature with a 2-second delay?
Generated: 2025-09-11 17:21:20
Status: success
Model: azure-o3
Total Steps: 1
"""

import os
import json
import re
import pathlib
from typing import Tuple


def extract_settings_info(text: str) -> Tuple[str, int]:
    """Extract `files.autoSave` and `files.autoSaveDelay` values from a VS Code settings.json string.

    Returns (autoSaveValue, autoSaveDelay). Either value can be None if not found.
    The function first tries to parse the text as JSON (after stripping line comments),
    then falls back to regex extraction to cover malformed-JSON cases.
    """
    # Strip simple //-style comments for JSON parsing
    no_comments = re.sub(r"//.*", "", text)

    auto_save_val = None
    auto_save_delay = None

    # Attempt JSON parsing
    try:
        data = json.loads(no_comments)
        auto_save_val = data.get("files.autoSave")
        auto_save_delay = data.get("files.autoSaveDelay")
    except Exception:
        pass  # Ignore JSON errors; fall back to regex searches below

    # Fallback regex search for files.autoSave
    if auto_save_val is None:
        m = re.search(r'"files\\.autoSave"\s*:\s*"([^"]+)"', text)
        if m:
            auto_save_val = m.group(1)

    # Fallback regex search for files.autoSaveDelay
    if auto_save_delay is None:
        m = re.search(r'"files\\.autoSaveDelay"\s*:\s*(\d+)', text)
        if m:
            try:
                auto_save_delay = int(m.group(1))
            except ValueError:
                pass

    return auto_save_val, auto_save_delay


def find_settings_files() -> list:
    """Locate plausible VS Code settings.json files inside the user’s HOME directory."""
    home = pathlib.Path.home()
    candidates = []

    # Standard user-level settings paths for various VS Code builds
    for rel_path in [
        ".config/Code/User/settings.json",          # Regular VS Code
        ".config/Code - OSS/User/settings.json",    # VS Code OSS
        ".config/Code - Insiders/User/settings.json",  # Insiders build
        ".vscode-oss/user-data/User/settings.json",    # Flatpak variant
    ]:
        p = home / rel_path
        if p.is_file():
            candidates.append(p)

    # Workspace settings: search depth-limited inside HOME for *.vscode/settings.json
    for path in home.rglob("settings.json"):
        # Limit search depth for performance & relevance (≤3 levels below HOME)
        if len(path.parts) - len(home.parts) <= 3 and path.is_file():
            candidates.append(path)

    # Deduplicate paths while preserving order
    unique = []
    seen = set()
    for p in candidates:
        if p not in seen:
            unique.append(p)
            seen.add(p)
    return unique


def verify_vscode_autosave() -> float:
    """Verify that VS Code auto-save is enabled with a 2-second delay.

    Scoring:
    • 0.5 points – ‘files.autoSave’ is set to ‘afterDelay’ in any relevant settings.json.
    • 0.5 points – AND ‘files.autoSaveDelay’ is exactly 2000 (milliseconds).
    Returns a float between 0.0 and 1.0 and prints a detailed breakdown.
    """
    print("Starting verification of VS Code auto-save settings…")
    settings_files = find_settings_files()
    print(f"Found {len(settings_files)} candidate settings.json files to inspect.")

    auto_save_correct = False
    delay_correct = False

    for file in settings_files:
        try:
            text = file.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"⚠️  Could not read {file}: {e}")
            continue

        auto_save_val, auto_save_delay = extract_settings_info(text)
        print(f"Inspecting {file}: autoSave={auto_save_val}, delay={auto_save_delay}")

        # Check conditions
        if auto_save_val == "afterDelay":
            auto_save_correct = True
            if isinstance(auto_save_delay, int) and auto_save_delay == 2000:
                delay_correct = True
                print("✓ Correct auto-save value AND correct 2-second delay found.")
                break  # Full score achieved; no need to inspect further
            else:
                print("✓ Auto-save enabled but delay incorrect or missing.")
        else:
            print("⨯ Auto-save not set to ‘afterDelay’ in this file.")

    # Progressive scoring
    score = 0.0
    if auto_save_correct:
        score += 0.5
    if auto_save_correct and delay_correct:
        score += 0.5

    # Results summary
    print("\n--- Scoring Summary ---")
    print(f"Auto-save set to ‘afterDelay’: {auto_save_correct}  -> {'0.5' if auto_save_correct else '0.0'}")
    print(f"2-second delay (2000 ms):     {delay_correct}  -> {'0.5' if delay_correct else '0.0'}")
    print(f"Total score: {score}")
    print(f"REWARD: {score}")

    return score


if __name__ == "__main__":
    verify_vscode_autosave()
