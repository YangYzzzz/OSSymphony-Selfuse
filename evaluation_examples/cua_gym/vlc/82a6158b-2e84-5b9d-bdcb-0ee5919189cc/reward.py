"""
Reward Script: Set VLC default volume level to 50%
Task ID: vlcset_002
Domain: vlc
Scoring:
  Component 1 (0.5 pts): volume-save=0 (disable "remember last volume", enabling fixed start level)
  Component 2 (0.5 pts): qt-startvolume=50 (set the audio start level to 50%)
"""

import os
import re

VLCRC_PATH = os.path.expanduser("~/.config/vlc/vlcrc")


def get_vlcrc_option(key: str, default: str = None) -> str:
    """Read a vlcrc option value. Returns default if key is commented or missing."""
    try:
        with open(VLCRC_PATH, "r") as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR: Cannot read vlcrc: {e}")
        return default

    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("#") or not stripped:
            continue
        if stripped.startswith(f"{key}="):
            return stripped.split("=", 1)[-1].strip()
    return default


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: vlcrc file must exist
    if not os.path.exists(VLCRC_PATH):
        print(f"CRITICAL: vlcrc not found at {VLCRC_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: volume-save=0 (0.5 points)
    # When "Always reset audio start level to:" is checked, volume-save is set to 0.
    # Default / initial state has volume-save=1 (remember last volume).
    try:
        volume_save = get_vlcrc_option("volume-save", "1")
        if str(volume_save) == "0":
            print(f"PASS: Component 1 - volume-save=0 (fixed start level enabled) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 - expected volume-save=0, found: {volume_save}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: qt-startvolume=50 (0.5 points)
    # The audio start level should be set to 50%.
    # This key does not exist (commented out or absent) in initial state.
    try:
        startvolume = get_vlcrc_option("qt-startvolume", None)
        if startvolume is not None and int(startvolume) == 50:
            print(f"PASS: Component 2 - qt-startvolume=50 (start volume at 50%) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 - expected qt-startvolume=50, found: {startvolume}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
