"""
Reward Script: Configure VLC subtitle settings
Task ID: vlcset_010
Domain: vlc
Scoring:
  Component 1: subsdec-encoding set to UTF-8          — 0.30 points
  Component 2: freetype-font set to DejaVu Sans       — 0.25 points
  Component 3: freetype-fontsize set to 24             — 0.25 points
  Component 4: sub-autodetect-file explicitly enabled  — 0.20 points
  Total: 1.0
"""

import os
import re

VLCRC_PATH = os.path.expanduser("~/.config/vlc/vlcrc")
TASK_ID = "vlcset_010"


def get_vlcrc_option(content: str, key: str):
    """
    Read an ACTIVE (uncommented) vlcrc option value.
    Returns the value string if the key is set and uncommented, else None.
    """
    for line in content.split("\n"):
        stripped = line.strip()
        # Skip comments and empty lines
        if stripped.startswith("#") or not stripped:
            continue
        # Match exact key= to avoid partial matches (e.g. play-and-exit vs play-and-exit-title)
        if stripped.startswith(f"{key}="):
            return stripped.split("=", 1)[1].strip()
    return None


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
        with open(VLCRC_PATH, "r") as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read vlcrc: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Subtitle encoding set to UTF-8 (0.30 points)
    try:
        encoding_val = get_vlcrc_option(content, "subsdec-encoding")
        if encoding_val is not None and encoding_val == "UTF-8":
            print(f"PASS: Component 1 — subsdec-encoding is 'UTF-8' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — expected subsdec-encoding='UTF-8', found: '{encoding_val}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Font set to DejaVu Sans (0.25 points)
    try:
        font_val = get_vlcrc_option(content, "freetype-font")
        if font_val is not None and font_val == "DejaVu Sans":
            print(f"PASS: Component 2 — freetype-font is 'DejaVu Sans' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — expected freetype-font='DejaVu Sans', found: '{font_val}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Font size set to 24 (0.25 points)
    try:
        fontsize_val = get_vlcrc_option(content, "freetype-fontsize")
        if fontsize_val is not None and fontsize_val == "24":
            print(f"PASS: Component 3 — freetype-fontsize is '24' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — expected freetype-fontsize='24', found: '{fontsize_val}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Subtitle autodetect explicitly enabled (0.20 points)
    # The key sub-autodetect-file must be uncommented and set to 1
    try:
        autodetect_val = get_vlcrc_option(content, "sub-autodetect-file")
        if autodetect_val is not None and autodetect_val == "1":
            print(f"PASS: Component 4 — sub-autodetect-file is explicitly '1' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — expected sub-autodetect-file='1' (uncommented), found: '{autodetect_val}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
