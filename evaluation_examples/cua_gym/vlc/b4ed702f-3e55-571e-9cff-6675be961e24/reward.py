"""
FINAL REWARD SCRIPT - SUCCESS
Task: Stream live radio from http://stream.live365.com/a12345 using VLC.
Generated: 2025-09-13 12:08:11
Status: success
Model: azure-o3
Total Steps: 6
"""

import os
import glob
import xml.etree.ElementTree as ET

"""
Reward script for verifying the VLC task:
"Stream live radio from http://stream.live365.com/a12345 using VLC."

Verification requirements (per task context):
1. Parse the status.xml file produced by VLC’s HTTP interface.
2. Ensure <state> equals "playing".
3. Ensure one of the <info name="filename"> or <info name="url"> entries ends
   with the expected stream URL suffix (case-insensitive).

Scoring (binary in this case, but progressive logic retained):
• +0.5 if playback state is correctly "playing".
• +0.5 if the stream URL/filename suffix matches.
A perfect run yields 1.0.

This script searches common locations for status.xml, performs the checks, and
prints the final score in the required "REWARD: X.X" format.
"""

EXPECTED_SUFFIX = "stream.live365.com/a12345".lower()


def find_status_xml() -> str | None:
    """Locate status.xml in a set of plausible locations used by the harness."""
    # Environment override (useful for tests) ---------------------------------
    env_path = os.environ.get("STATUS_XML_PATH")
    if env_path and os.path.isfile(env_path):
        return env_path

    # Common fixed paths -------------------------------------------------------
    fixed_candidates = [
        "status.xml",  # current working directory
        os.path.join(os.getcwd(), "status.xml"),
        os.path.expanduser("~/status.xml"),
        os.path.expanduser("~/.config/vlc/status.xml"),
        "/tmp/status.xml",
        os.path.join("/tmp", "vlc", "status.xml"),
    ]
    for path in fixed_candidates:
        if os.path.isfile(path):
            return path

    # Fallback shallow glob under $HOME (depth ≤2) ----------------------------
    home = os.path.expanduser("~")
    for pattern in [os.path.join(home, "*", "status.xml"),
                    os.path.join(home, "*", "*", "status.xml")]:
        for path in glob.glob(pattern):
            if os.path.isfile(path):
                return path
    return None


def verify_playback(xml_path: str, expected_suffix: str) -> float:
    """Verify VLC playback state and URL/filename suffix. Return score ∈ [0,1]."""
    score = 0.0
    max_score = 1.0

    # --- Parse XML -----------------------------------------------------------
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        print(f"✓ Parsed XML from {xml_path}")
    except Exception as exc:
        print(f"✗ Failed to parse status.xml ({exc})")
        print("REWARD: 0.0")
        return 0.0

    # --- Check <state> -------------------------------------------------------
    state_elem = root.find("state")
    if state_elem is not None and (state_elem.text or "").strip().lower() == "playing":
        print("✓ Playback state is 'playing'")
        score += 0.5
    else:
        print("✗ Playback state is NOT 'playing'")

    # --- Check URL/filename suffix ------------------------------------------
    matched = False
    for info in root.iter("info"):
        if info.get("name") in ("filename", "url"):
            value = (info.text or "").strip().lower()
            # Tolerate a trailing slash on the stored value
            if value.endswith("/") and not expected_suffix.endswith("/"):
                value = value[:-1]
            if value.endswith(expected_suffix):
                matched = True
                print(f"✓ Found matching {info.get('name')}: {value}")
                break
    if matched:
        score += 0.5
    else:
        print(f"✗ No 'filename' or 'url' ends with '{expected_suffix}'")

    final_score = min(score, max_score)
    print(f"Total score: {final_score}/{max_score}")
    return final_score


def main() -> float:
    xml_path = find_status_xml()
    if not xml_path:
        print("✗ status.xml file not found – cannot verify playback")
        print("REWARD: 0.0")
        return 0.0

    reward = verify_playback(xml_path, EXPECTED_SUFFIX)
    print(f"REWARD: {reward}")
    return reward


if __name__ == "__main__":
    main()

