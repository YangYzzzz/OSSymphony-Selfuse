"""
Reward Script: Configure VLC to automatically play the next file in the directory
Task ID: vlc_playlist_053
Domain: vlc
Scoring:
  Component 1 (0.6): play-and-stop is set to 0 (disabled) — the primary change
  Component 2 (0.2): play-and-exit is explicitly set to 0 (uncommented) — ensures no exit after playback
  Component 3 (0.2): playlist-autostart remains enabled (1) AND loop/repeat are 0 — correct auto-next config
    (compound check: autostart must be active AND play-and-stop must be 0 for auto-next to work)
"""

import os
import re

VLCRC_PATH = '/home/user/.config/vlc/vlcrc'
TASK_ID = 'vlc_playlist_053'


def get_vlcrc_option(content: str, key: str, default=None):
    """
    Read a vlcrc option value from content.
    Returns default if key is commented out or missing.
    A commented line (#key=val) means "use default".
    An uncommented line (key=val) returns the value.
    """
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("#") or not stripped:
            continue
        # Match exact key= to avoid partial matches (e.g. play-and-exit vs play-and-exit-title)
        if stripped.startswith(f"{key}="):
            return stripped.split("=", 1)[-1].strip()
    return default


def is_option_uncommented(content: str, key: str) -> bool:
    """
    Check if a vlcrc option line exists and is uncommented (active).
    Returns True if there's an uncommented line starting with key=.
    """
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("#") or not stripped:
            continue
        if stripped.startswith(f"{key}="):
            return True
    return False


def verify_task():
    """
    Verify VLC is configured to auto-play next file in directory.
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

    # Component 1: play-and-stop is set to 0 (disabled) — 0.6 points
    # Initial state has play-and-stop=1 (stop after current file).
    # Golden state has play-and-stop=0 (continue to next file).
    # This is THE core task change.
    try:
        play_and_stop = get_vlcrc_option(content, "play-and-stop", default="1")
        if str(play_and_stop) == "0":
            print(f"PASS: Component 1 — play-and-stop=0 (disabled, allows auto-next) (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 — play-and-stop={play_and_stop}, expected 0")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: play-and-exit is explicitly set to 0 (uncommented) — 0.2 points
    # Initial state has #play-and-exit=0 (commented out).
    # Golden state has play-and-exit=0 (uncommented, explicitly disabled).
    # This ensures VLC doesn't quit after playback finishes.
    try:
        is_uncommented = is_option_uncommented(content, "play-and-exit")
        play_and_exit_val = get_vlcrc_option(content, "play-and-exit", default=None)
        if is_uncommented and str(play_and_exit_val) == "0":
            print(f"PASS: Component 2 — play-and-exit=0 (explicitly set, VLC won't exit) (0.2 pts)")
            total_score += 0.2
        else:
            if not is_uncommented:
                print(f"FAIL: Component 2 — play-and-exit is commented out (not explicitly set)")
            else:
                print(f"FAIL: Component 2 — play-and-exit={play_and_exit_val}, expected 0")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correct auto-next configuration compound check — 0.2 points
    # Verifies that: play-and-stop=0 AND playlist-autostart=1 AND loop=0 AND repeat=0
    # This compound check ensures the full "play next in folder" configuration is correct.
    # Only awards points when play-and-stop=0 (task change) is part of the passing condition.
    try:
        play_and_stop_val = get_vlcrc_option(content, "play-and-stop", default="1")
        autostart_val = get_vlcrc_option(content, "playlist-autostart", default="1")
        loop_val = get_vlcrc_option(content, "loop", default="0")
        repeat_val = get_vlcrc_option(content, "repeat", default="0")

        conditions = {
            "play-and-stop=0": str(play_and_stop_val) == "0",
            "playlist-autostart=1": str(autostart_val) == "1",
            "loop=0 (no infinite loop)": str(loop_val) == "0",
            "repeat=0 (no repeat current)": str(repeat_val) == "0",
        }

        all_pass = all(conditions.values())
        if all_pass:
            print(f"PASS: Component 3 — Full auto-next config correct: {conditions} (0.2 pts)")
            total_score += 0.2
        else:
            failed = {k: v for k, v in conditions.items() if not v}
            print(f"FAIL: Component 3 — Some conditions failed: {failed}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
