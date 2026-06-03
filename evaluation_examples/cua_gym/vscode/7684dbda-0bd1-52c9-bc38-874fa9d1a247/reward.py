"""
FINAL REWARD SCRIPT - SUCCESS
Task: Since I updated VS Code, the Python extension keeps missing my virtualenv; could you help me roll it back to version 2023.16.0?
Generated: 2025-09-11 15:24:04
Status: success
Model: azure-o3
Total Steps: 12
"""

import os
import re
from pathlib import Path

# Target Python-extension version required by the task
TARGET_VERSION = "2023.16.0"

# -------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------

def _parse_version(version_str: str):
    """Convert a version string to a tuple of ints for comparison.
    Non-digit characters are treated as separators. The tuple is padded
    to four components so different length versions compare properly.
    """
    cleaned = re.sub(r"[^0-9.]", ".", version_str)
    parts = [int(p) for p in cleaned.split(".") if p]
    while len(parts) < 4:
        parts.append(0)
    return tuple(parts)


def _compare_versions(a, b):
    """Return 1 if a>b, -1 if a<b, 0 if equal (a, b are tuples)."""
    for x, y in zip(a, b):
        if x > y:
            return 1
        if x < y:
            return -1
    return 0


def _find_python_extension_dirs():
    """Locate VS Code Python-extension directories in common roots."""
    roots = [
        Path.home() / ".vscode" / "extensions",
        Path.home() / ".vscode-insiders" / "extensions",
        Path.home() / ".vscode-server" / "extensions",
        Path.home() / ".vscode-server-insiders" / "extensions",
    ]
    dirs = []
    pattern = re.compile(r"ms-python\.python-[0-9]")
    for root in roots:
        if root.exists():
            for child in root.iterdir():
                if child.is_dir() and pattern.match(child.name):
                    dirs.append(child)
    return dirs

# -------------------------------------------------------------
# Verification logic (progressive scoring)
# -------------------------------------------------------------

def verify_task():
    print("--- Verifying VS Code Python Extension Rollback ---")

    python_dirs = _find_python_extension_dirs()
    if not python_dirs:
        print("✗ No Python extension directories found.")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found {len(python_dirs)} candidate directorie(s):")
    for d in python_dirs:
        print("  •", d)

    target_tuple = _parse_version(TARGET_VERSION)
    target_present = False
    newer_versions = []

    for d in python_dirs:
        ver_str = d.name.split("ms-python.python-")[-1]
        cmp = _compare_versions(_parse_version(ver_str), target_tuple)
        if cmp == 0:
            target_present = True
        elif cmp == 1:
            newer_versions.append(ver_str)

    score = 0.0

    # Requirement 1 – target version installed (0.6 pts)
    if target_present:
        print(f"✓ Target version {TARGET_VERSION} detected (0.6 pts)")
        score += 0.6
    else:
        print(f"✗ Target version {TARGET_VERSION} NOT found (0 pts)")

    # Requirement 2 – no newer versions present (0.4 pts)
    if not newer_versions:
        if target_present:
            print("✓ No newer versions present (0.4 pts)")
            score += 0.4
        else:
            print("No newer versions, but target missing (0 pts)")
    else:
        print("✗ Newer versions present:", ", ".join(newer_versions), "(0 pts)")

    score = min(score, 1.0)
    print("----------------------------------------------------")
    print("REWARD:", score)
    return score


if __name__ == "__main__":
    verify_task()
