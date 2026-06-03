"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m juggling some heavily nested JavaScript functions and keep losing track of which brackets match; could you help me install the “Bracket Pair Colorizer 2” extension so each pair gets its own color?
Generated: 2025-09-11 13:37:00
Status: success
Model: azure-o3
Total Steps: 7
"""

import os
import subprocess
import shutil
import pathlib
import re
from typing import List

"""
Reward Verification Script – Bracket Pair Colorizer 2
====================================================
This script awards a *progressive* score (0.0‒1.0) for the task:
“Install the VS Code extension ‘Bracket Pair Colorizer 2’.”

Scoring
-------
• 0.2 points – VS Code CLI (`code`) is present.
• 0.8 points – Extension detected (via CLI *or* directory search).

A perfect score (1.0) is reached only when the extension is actually installed.
All checks are data-driven and falsifiable – no hard-coded success values.
"""

TARGET_SUBSTR = "bracket-pair-colorizer-2"  # case-insensitive substring
CLI_SCORE     = 0.2
EXT_SCORE     = 0.8
MAX_SCORE     = 1.0


def list_extensions_via_cli(code_path: str) -> List[str]:
    """Return list of extension IDs obtained from `code --list-extensions`."""
    try:
        res = subprocess.run(
            [code_path, "--list-extensions"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=20,
        )
        if res.returncode == 0:
            ext_ids = [ln.strip() for ln in res.stdout.splitlines() if ln.strip()]
            print(f"✓ CLI reported {len(ext_ids)} extension(s)")
            return ext_ids
        else:
            print("✗ CLI exited with status", res.returncode)
            if res.stderr:
                print("stderr:", res.stderr.strip())
    except Exception as exc:
        print("✗ Exception running CLI:", exc)
    return []


def extension_directory_search() -> bool:
    """Search standard VS Code extension directories for the target extension."""
    dirs_to_check = [
        pathlib.Path.home() / ".vscode" / "extensions",
        pathlib.Path.home() / ".vscode-server" / "extensions",
        pathlib.Path.home() / ".vscode-insiders" / "extensions",
    ]
    for base in dirs_to_check:
        if base.exists():
            print(f"Searching directory: {base}")
            for child in base.iterdir():
                if TARGET_SUBSTR in child.name.lower():
                    print(f"✓ Extension directory found: {child}")
                    return True
    return False


def verify_task() -> float:
    """Compute and return the progressive reward score."""
    score = 0.0
    extension_found = False

    # 1 – VS Code CLI presence
    code_path = shutil.which("code")
    if code_path:
        print(f"✓ VS Code CLI located at {code_path} (+{CLI_SCORE})")
        score += CLI_SCORE

        # Attempt to detect the extension via CLI
        for ext_id in list_extensions_via_cli(code_path):
            if TARGET_SUBSTR in ext_id.lower():
                extension_found = True
                print(f"✓ Extension found via CLI: {ext_id}")
                break
    else:
        print("✗ VS Code CLI ('code') not found – 0 points for CLI availability")

    # 2 – Directory fallback if CLI didn’t confirm the extension
    if not extension_found:
        extension_found = extension_directory_search()

    # 3 – Extension scoring
    if extension_found:
        print(f"✓ '{TARGET_SUBSTR}' extension is installed (+{EXT_SCORE})")
        score += EXT_SCORE
    else:
        print(f"✗ '{TARGET_SUBSTR}' extension NOT detected (+0)")

    # 4 – Finalise score
    score = min(score, MAX_SCORE)
    print("Final Score:", score)
    return score


if __name__ == "__main__":
    reward = verify_task()
    print(f"REWARD: {reward}")

