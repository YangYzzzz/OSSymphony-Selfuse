"""
Reward Script: Enable minimal interface mode in VLC
Task ID: vlcset_004
Domain: vlc
Scoring:
  Component 1 (0.7 pts): qt-minimal-view is set to "1" (uncommented, active)
  Component 2 (0.3 pts): The setting persists correctly in vlcrc (value is exactly "1",
                          not a different truthy value, and the key is properly formatted)
"""

import os
import re

VLCRC_PATH = os.path.expanduser("~/.config/vlc/vlcrc")
TASK_ID = "vlcset_004"


def get_vlcrc_option(key: str, default: str = None) -> str:
    """Read a vlcrc option value. Returns default if key is commented or missing."""
    try:
        with open(VLCRC_PATH, "r") as f:
            content = f.read()
    except Exception:
        return default
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("#") or not stripped:
            continue
        # Match exact key= to avoid partial matches
        if stripped.startswith(f"{key}="):
            return stripped.split("=", 1)[-1].strip()
    return default


def verify_task():
    """
    Verify that VLC minimal interface mode is enabled.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: vlcrc file must exist
    if not os.path.exists(VLCRC_PATH):
        print(f"CRITICAL: vlcrc not found at {VLCRC_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: qt-minimal-view is actively set to "1" (0.7 points)
    # This is the core task requirement: enable minimal interface mode
    # Default value is "0" (full mode), so this FAILS on initial_env
    try:
        value = get_vlcrc_option("qt-minimal-view")
        if value is not None and value == "1":
            print(f"PASS: Component 1 — qt-minimal-view is set to '1' (0.7 pts)")
            total_score += 0.7
        else:
            print(f"FAIL: Component 1 — qt-minimal-view expected '1', found: '{value}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Strict validation — the key is uncommented and exactly "1" (0.3 points)
    # Verify by reading the raw file to ensure the line is properly formatted
    # (not commented out, not a different truthy value like "2" or "true")
    try:
        with open(VLCRC_PATH, "r") as f:
            content = f.read()
        # Find all lines matching qt-minimal-view (both commented and uncommented)
        pattern = re.compile(r'^(#?\s*)qt-minimal-view=(.*)$', re.MULTILINE)
        matches = pattern.findall(content)
        if matches:
            # Check that there is at least one uncommented line with value "1"
            active_minimal_lines = [
                (prefix, val) for prefix, val in matches
                if not prefix.strip().startswith("#") and val.strip() == "1"
            ]
            if len(active_minimal_lines) > 0:
                print(f"PASS: Component 2 — vlcrc contains active 'qt-minimal-view=1' line (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — no active 'qt-minimal-view=1' line found in vlcrc")
                print(f"  Found matches: {matches}")
        else:
            print(f"FAIL: Component 2 — qt-minimal-view key not found in vlcrc at all")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
