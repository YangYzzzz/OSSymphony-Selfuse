"""
Reward Script: Configure VLC subtitle yellow font color and font size 20
Task ID: vlcset_006
Domain: vlc
Scoring:
  Component 1 (0.5 pts): freetype-color set to yellow (16776960)
  Component 2 (0.5 pts): freetype-fontsize set to 20
"""

import os
import re

VLCRC_PATH = os.path.expanduser("~/.config/vlc/vlcrc")
TASK_ID = "vlcset_006"

# Yellow in VLC's integer color format: 0xFFFF00 = 16776960
EXPECTED_COLOR = "16776960"
EXPECTED_FONTSIZE = "20"


def read_vlcrc():
    """Read the vlcrc file content."""
    with open(VLCRC_PATH, "r") as f:
        return f.read()


def get_vlcrc_option(content, key, default=None):
    """
    Read an ACTIVE (uncommented) vlcrc option value.
    Returns default if the key is commented out or missing.
    """
    for line in content.split("\n"):
        stripped = line.strip()
        # Skip comments and empty lines
        if stripped.startswith("#") or not stripped:
            continue
        # Match exact key= to avoid partial matches
        if stripped.startswith(f"{key}="):
            return stripped.split("=", 1)[-1].strip()
    return default


def verify_task():
    """
    Verify VLC subtitle configuration with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: vlcrc file must exist
    if not os.path.exists(VLCRC_PATH):
        print(f"CRITICAL: vlcrc not found at {VLCRC_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        content = read_vlcrc()
    except Exception as e:
        print(f"CRITICAL: Cannot read vlcrc: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Subtitle font color is yellow (0.5 points)
    # Yellow = 0xFFFF00 = 16776960 in VLC integer format
    # Default (white) = 0xFFFFFF = 16777215
    try:
        color_val = get_vlcrc_option(content, "freetype-color")
        if color_val is not None and str(color_val) == EXPECTED_COLOR:
            print(f"PASS: Component 1 -- freetype-color is {color_val} (yellow) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 -- expected freetype-color={EXPECTED_COLOR}, found: {color_val}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Subtitle font size is 20 (0.5 points)
    # Default is 0 (commented out, meaning "use relative size")
    try:
        fontsize_val = get_vlcrc_option(content, "freetype-fontsize")
        if fontsize_val is not None and str(fontsize_val) == EXPECTED_FONTSIZE:
            print(f"PASS: Component 2 -- freetype-fontsize is {fontsize_val} (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 -- expected freetype-fontsize={EXPECTED_FONTSIZE}, found: {fontsize_val}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
