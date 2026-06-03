"""
FINAL REWARD SCRIPT - SUCCESS
Task: Play web radio http://icecast.example.com:8000/stream.mp3 using VLC.
Generated: 2025-09-13 11:15:34
Status: success
Model: azure-o3
Total Steps: 12
"""

import os
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple

def locate_status_xml(max_depth: int = 6) -> List[str]:
    """Locate all status.xml files within a restricted set of base directories.
    The evaluator saves a snapshot of VLC's HTTP status page as status.xml – we
    need to find the newest copy of that file.  To avoid an expensive full
    filesystem walk, we only look inside a handful of likely locations and
    limit search depth.
    """
    candidate_bases = [
        os.path.expanduser("~"),  # e.g. /home/user
        "/tmp",                  # evaluator often stores artefacts here
        "/home",                 # fallback – still limited depth
        os.getcwd(),              # current working dir, just in case
    ]

    status_paths: List[str] = []
    for base in candidate_bases:
        base = os.path.abspath(base)
        if not os.path.isdir(base):
            continue

        for root, dirs, files in os.walk(base):
            # prune deep sub-trees to keep the search cheap
            if root[len(base):].count(os.sep) > max_depth:
                dirs[:] = []
                continue

            if "status.xml" in files:
                status_paths.append(os.path.join(root, "status.xml"))

    # newest first – evaluator usually touches the file right before scoring
    status_paths.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return status_paths


def parse_status(path: str) -> Tuple[str, Dict[str, str]]:
    """Return (state, meta_dict) extracted from a VLC status.xml file."""
    try:
        tree = ET.parse(path)
        root = tree.getroot()

        # Playback state ------------------------------------------------------
        state_elem = root.find("state")
        state = state_elem.text.strip().lower() if state_elem is not None and state_elem.text else ""

        # Meta information ----------------------------------------------------
        meta: Dict[str, str] = {}
        for cat in root.findall(".//category[@name='meta']"):
            for info in cat.findall("info"):
                key = (info.attrib.get("name") or "").lower()
                meta[key] = (info.text or "").strip()

        return state, meta
    except Exception as exc:
        print(f"✗ Error parsing status.xml ({path}): {exc}")
        return "", {}


def verify_playback() -> float:
    """Verify that VLC is playing the expected web-radio stream.

    Scoring rules (progressive):
      • 0.5  if VLC state == 'playing'
      • 0.5  if the stream source matches the expected URL / filename suffix
      → 1.0  total for full success
    """
    EXPECTED_URL = "http://icecast.example.com:8000/stream.mp3"
    EXPECTED_FILENAME_SUFFIX = "stream.mp3"

    status_paths = locate_status_xml()
    print(f"Found status.xml candidates: {status_paths}")

    if not status_paths:
        print("✗ No status.xml file found – cannot verify playback")
        print("REWARD: 0.0")
        return 0.0

    status_path = status_paths[0]  # newest
    print(f"Using status file: {status_path}")

    state, meta = parse_status(status_path)

    total_score = 0.0

    # ----------------------------------------------------------------------
    # 1) Playback state must be 'playing'
    # ----------------------------------------------------------------------
    if state == "playing":
        total_score += 0.5
        print("✓ VLC state is PLAYING (0.5)")
    else:
        print(f"✗ VLC state is '{state}' (expected 'playing') (0 points)")

    # ----------------------------------------------------------------------
    # 2) Stream source must match
    # ----------------------------------------------------------------------
    match = False
    url_meta = meta.get("url", "")
    if url_meta:
        print(f"URL meta found: {url_meta}")
        if url_meta.endswith(EXPECTED_URL):
            match = True

    if not match:
        filename_meta = meta.get("filename", "")
        if filename_meta:
            print(f"Filename meta found: {filename_meta}")
            if filename_meta.endswith(EXPECTED_FILENAME_SUFFIX):
                match = True

    if match:
        total_score += 0.5
        print("✓ Stream source matches expected URL/filename (0.5)")
    else:
        print("✗ Stream source does NOT match expected URL/filename (0 points)")

    # ----------------------------------------------------------------------
    final_score = round(min(total_score, 1.0), 2)
    print(f"Total score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_playback()

