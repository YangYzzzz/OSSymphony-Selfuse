"""
Reward Script: Configure VLC VA-API hardware decoding and X11/XCB video output
Task ID: vlcset_011
Domain: vlc
Scoring:
  Component 1 (0.5): avcodec-hw is set to 'vaapi'
  Component 2 (0.5): vout is set to 'xcb_x11'
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
    Verify VLC configuration changes with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: vlcrc file exists
    if not os.path.exists(VLCRC_PATH):
        print(f"CRITICAL: vlcrc not found at {VLCRC_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Hardware-accelerated decoding set to VA-API (0.5 points)
    # Task requires avcodec-hw=vaapi. In initial state this is commented out (default).
    try:
        hw_value = get_vlcrc_option("avcodec-hw")
        if hw_value is not None and hw_value.lower() == "vaapi":
            print(f"PASS: Component 1 — avcodec-hw is set to '{hw_value}' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — expected avcodec-hw='vaapi', found: '{hw_value}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Video output module set to X11/XCB (0.5 points)
    # Task requires vout=xcb_x11. In initial state this is commented out (default).
    try:
        vout_value = get_vlcrc_option("vout")
        if vout_value is not None and vout_value.lower() == "xcb_x11":
            print(f"PASS: Component 2 — vout is set to '{vout_value}' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — expected vout='xcb_x11', found: '{vout_value}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
