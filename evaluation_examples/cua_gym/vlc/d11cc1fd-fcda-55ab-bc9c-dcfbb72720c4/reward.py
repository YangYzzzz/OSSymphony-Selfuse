"""
Reward Script: VLC advanced settings configuration
Task ID: vlcset_013
Domain: vlc
Scoring:
  - Component 1: audio-desync = 200 (0.35 pts)
  - Component 2: network-caching = 1500 (0.35 pts)
  - Component 3: file-caching = 1000 (0.30 pts)
"""

import os

VLCRC_PATH = os.path.expanduser("~/.config/vlc/vlcrc")


def get_vlcrc_option(key, default=None):
    """
    Read a vlcrc option value. Returns default if key is commented out or missing.
    Only returns a value for uncommented (active) lines matching 'key=value'.
    """
    if not os.path.exists(VLCRC_PATH):
        return default
    with open(VLCRC_PATH, "r") as f:
        content = f.read()
    for line in content.split("\n"):
        stripped = line.strip()
        # Skip comments and empty lines
        if stripped.startswith("#") or not stripped:
            continue
        # Match exact key= to avoid partial matches (e.g., file-caching vs file-caching-ms)
        if stripped.startswith(f"{key}="):
            return stripped.split("=", 1)[1].strip()
    return default


def verify_task():
    """
    Verify VLC advanced settings configuration with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: vlcrc file must exist
    if not os.path.exists(VLCRC_PATH):
        print(f"CRITICAL: vlcrc not found at {VLCRC_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Audio desynchronization compensation = 200 (0.35 points)
    try:
        audio_desync = get_vlcrc_option("audio-desync")
        if audio_desync is not None and str(audio_desync) == "200":
            print(f"PASS: Component 1 — audio-desync is 200 (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — expected audio-desync=200, found: {audio_desync}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Network caching = 1500 (0.35 points)
    try:
        network_caching = get_vlcrc_option("network-caching")
        if network_caching is not None and str(network_caching) == "1500":
            print(f"PASS: Component 2 — network-caching is 1500 (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — expected network-caching=1500, found: {network_caching}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: File caching = 1000 (0.30 points)
    try:
        file_caching = get_vlcrc_option("file-caching")
        if file_caching is not None and str(file_caching) == "1000":
            print(f"PASS: Component 3 — file-caching is 1000 (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — expected file-caching=1000 (explicitly set), found: {file_caching}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
