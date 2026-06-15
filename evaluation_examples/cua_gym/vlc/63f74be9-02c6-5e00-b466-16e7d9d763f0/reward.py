"""
Reward Script: VLC recording and snapshot directory configuration
Task ID: vlcset_014
Domain: vlc
Scoring:
  - Component 1: input-record-path set to /home/user/Recordings (0.35)
  - Component 2: snapshot-path set to /home/user/Screenshots (0.35)
  - Component 3: snapshot-format set to png (0.30)
"""

import os
import re

VLCRC_PATH = os.path.expanduser("~/.config/vlc/vlcrc")
TASK_ID = "vlcset_014"


def read_vlcrc() -> str:
    """Read the vlcrc configuration file."""
    with open(VLCRC_PATH, "r") as f:
        return f.read()


def get_vlcrc_option(key: str, default: str = None) -> str:
    """
    Read an UNCOMMENTED vlcrc option value.
    Returns default if the key is commented out or missing.
    Matches exact 'key=' to avoid partial key matches.
    """
    content = read_vlcrc()
    for line in content.split("\n"):
        stripped = line.strip()
        # Skip commented lines and empty lines
        if stripped.startswith("#") or not stripped:
            continue
        # Match exact key= prefix to avoid false positives
        if stripped.startswith(f"{key}="):
            return stripped.split("=", 1)[-1].strip()
    return default


def verify_task():
    """
    Verify VLC configuration changes with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: vlcrc file must exist
    if not os.path.exists(VLCRC_PATH):
        print(f"CRITICAL: vlcrc not found at {VLCRC_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Recording directory set to /home/user/Recordings (0.35 points)
    try:
        record_path = get_vlcrc_option("input-record-path")
        expected_record = "/home/user/Recordings"
        if record_path is not None and record_path == expected_record:
            print(f"PASS: Component 1 -- input-record-path is '{record_path}' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 -- expected input-record-path='{expected_record}', found: '{record_path}'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Snapshot directory set to /home/user/Screenshots (0.35 points)
    try:
        snapshot_path = get_vlcrc_option("snapshot-path")
        expected_snapshot = "/home/user/Screenshots"
        if snapshot_path is not None and snapshot_path == expected_snapshot:
            print(f"PASS: Component 2 -- snapshot-path is '{snapshot_path}' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 -- expected snapshot-path='{expected_snapshot}', found: '{snapshot_path}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Snapshot format set to png (0.30 points)
    try:
        snapshot_format = get_vlcrc_option("snapshot-format")
        expected_format = "png"
        if snapshot_format is not None and snapshot_format == expected_format:
            print(f"PASS: Component 3 -- snapshot-format is '{snapshot_format}' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 -- expected snapshot-format='{expected_format}', found: '{snapshot_format}'")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
