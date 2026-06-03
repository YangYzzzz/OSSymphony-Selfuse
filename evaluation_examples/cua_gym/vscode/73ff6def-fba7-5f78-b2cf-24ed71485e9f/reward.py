"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m updating our project docs in Markdown and need handy shortcuts for headings and tables—can you help me install the “Markdown All in One” extension?
Generated: 2025-09-11 12:34:54
Status: success
Model: azure-o3
Total Steps: 7
"""

import os
import json
import pathlib
import subprocess
import shutil

"""
Reward Script: Verify installation of "Markdown All in One" VS Code extension

Scoring Breakdown (progressive, max 1.0):
• 0.3 – At least one directory whose name contains "markdown-all-in-one" found inside a known VS Code extensions root.
• 0.5 – package.json manifest inside that directory confirms BOTH:
           ‑ name  == "markdown-all-in-one"
           ‑ publisher contains "yzhang"
• 0.2 – Functional confirmation: manifest exposes at least one keybinding whose command
         contains "heading" or "table" (features requested by user).
• +0.1 – BONUS (capped at 1.0): extension also appears in `code --list-extensions` CLI output.

The script prints detailed diagnostics and the final line "REWARD: X.X" where X.X is the
computed score.
"""

def find_candidate_dirs() -> list[pathlib.Path]:
    """Return a list of directories whose names contain 'markdown-all-in-one' inside common VS Code extension roots."""
    home = pathlib.Path.home()
    roots = [
        home / '.vscode' / 'extensions',
        home / '.vscode-insiders' / 'extensions',
        home / '.vscode-server' / 'extensions',
        home / '.vscode-server-insiders' / 'extensions',
        home / '.vscode-test' / 'extensions',
        home / '.vscode-remote' / 'extensions',
        # Remote CLI caches can appear under these paths
        home / '.vscode-server' / 'cli',
        home / '.vscode-server-insiders' / 'cli',
    ]

    candidates: list[pathlib.Path] = []
    for root in roots:
        if not root.is_dir():
            continue

        if root.name == 'cli':  # dive deeper for cached servers
            for ext_dir in root.rglob('*'):
                if ext_dir.is_dir() and 'markdown-all-in-one' in ext_dir.name.lower():
                    candidates.append(ext_dir)
        else:  # normal desktop/server roots
            for child in root.iterdir():
                if child.is_dir() and 'markdown-all-in-one' in child.name.lower():
                    candidates.append(child)

    # de-duplicate by resolved path
    unique_dirs = list({p.resolve(): p for p in candidates}.values())
    return unique_dirs


def verify_manifest(dir_path: pathlib.Path) -> tuple[bool, bool]:
    """Return (manifest_matches_extension, keybindings_present)."""
    pkg = dir_path / 'package.json'
    if not pkg.exists():
        return False, False

    try:
        with pkg.open(encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {pkg}: {e}")
        return False, False

    name_ok = data.get('name', '').lower() == 'markdown-all-in-one'
    publisher_ok = 'yzhang' in data.get('publisher', '').lower()

    keybinding_found = False
    for kb in data.get('contributes', {}).get('keybindings', []):
        if isinstance(kb, dict):
            cmd = (kb.get('command') or '').lower()
            if 'heading' in cmd or 'table' in cmd:
                keybinding_found = True
                break

    return (name_ok and publisher_ok), keybinding_found


def verify_vscode_cli() -> bool:
    """Check if extension appears in `code --list-extensions`. Returns False if CLI unavailable."""
    code_bin = shutil.which('code') or shutil.which('code-insiders')
    if not code_bin:
        return False

    try:
        result = subprocess.run(
            [code_bin, '--list-extensions'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return False

        lines = [ln.strip().lower() for ln in result.stdout.splitlines()]
        return any(ln.startswith('yzhang.markdown-all-in-one') for ln in lines)
    except Exception:
        return False


def calculate_score() -> float:
    print("-- Verifying installation of 'Markdown All in One' VS Code extension --")

    total = 0.0
    candidates = find_candidate_dirs()

    if candidates:
        print(f"✓ Found {len(candidates)} directorie(s) containing 'markdown-all-in-one':")
        for d in candidates:
            print(f"  - {d}")
        total += 0.3
    else:
        print("✗ No directory found containing 'markdown-all-in-one'")

    manifest_ok = False
    keybindings_ok = False
    for d in candidates:
        m_ok, k_ok = verify_manifest(d)
        manifest_ok |= m_ok
        keybindings_ok |= k_ok
        if manifest_ok and keybindings_ok:
            break

    if manifest_ok:
        print("✓ Manifest confirms correct extension name & publisher (yzhang.markdown-all-in-one)")
        total += 0.5
    else:
        print("✗ Could not validate manifest for extension")

    if keybindings_ok:
        print("✓ Keybindings for headings/tables detected (functional confirmation)")
        total += 0.2
    else:
        print("✗ Expected keybindings not detected in manifest")

    # Optional extra confirmation via CLI (does not penalise if unavailable)
    if verify_vscode_cli():
        print("✓ Extension also listed via VS Code CLI --list-extensions")
        total += 0.1

    # Cap score at 1.0
    final_score = min(total, 1.0)
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    calculate_score()
