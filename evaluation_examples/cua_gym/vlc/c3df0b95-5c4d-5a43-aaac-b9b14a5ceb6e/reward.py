"""
FINAL REWARD SCRIPT - SUCCESS
Task: Play movie file /media/user/ExternalDrive/action_film.avi from mounted USB.
Generated: 2025-09-13 09:02:06
Status: success
Model: azure-o3
Total Steps: 15
"""

import os
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Tuple, Dict, Optional

"""
Reward Script – VLC Playback Verification
Task: "Play movie file /media/user/ExternalDrive/action_film.avi from mounted USB."

Scoring (0-1 range):
  • 0.5 – VLC is in state == "playing" (read from status.xml)
  • 0.5 – The media playing matches the required file (filename/url suffix check)

Key Features:
  • Robust status.xml discovery (env var, common paths, shallow recursive search)
  • Strict XML parsing and meta extraction
  • No points for natural conditions (e.g., merely finding status.xml)
  • Detailed printouts for every verification step
  • Returns exactly 1.0 only when all requirements are satisfied
"""

def find_status_xml() -> Optional[str]:
    """Locate the status.xml file produced by the evaluator getter."""
    # 1. Environment variable override
    env_path = os.environ.get("STATUS_XML")
    if env_path and Path(env_path).is_file():
        return env_path

    # 2. Common direct locations
    home = Path.home()
    direct_candidates = [
        home / "status.xml",
        home / ".config" / "vlc" / "status.xml",
        Path("/tmp/status.xml"),
    ]
    for cand in direct_candidates:
        if cand.is_file():
            return str(cand)

    # 3. Shallow recursive search in $HOME and /tmp (depth ≤ 4)
    search_roots = [home, Path("/tmp")]
    for root in search_roots:
        root = Path(root)
        if not root.exists():
            continue
        for path in root.rglob("status.xml"):
            depth = len(path.relative_to(root).parts)
            if depth <= 4:
                return str(path)
    return None


def parse_status_xml(xml_path: str) -> Tuple[str, Dict[str, str]]:
    """Return (state, meta_dict) from VLC status.xml."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    state = (root.findtext("state") or "").strip()

    meta: Dict[str, str] = {}
    for info in root.iter("info"):
        name = info.attrib.get("name")
        if name:
            meta[name] = (info.text or "").strip()
    return state, meta


def verify_playback(expected_media: str) -> float:
    max_score = 1.0
    score = 0.0

    print("Searching for status.xml ...")
    status_path = find_status_xml()
    if not status_path:
        print("✗ status.xml not found – cannot verify playback")
        return 0.0
    print(f"✓ Found status.xml at: {status_path}")

    # Parse XML safely
    try:
        state, meta = parse_status_xml(status_path)
    except Exception as exc:
        print(f"✗ Failed to parse status.xml: {exc}")
        return 0.0

    # Requirement 1: VLC in 'playing' state
    if state.lower() == "playing":
        print("✓ VLC state is 'playing' (0.5 points)")
        score += 0.5
    else:
        print(f"✗ VLC state is '{state}', expected 'playing'")

    # Requirement 2: Correct media file is playing
    expected_basename = os.path.basename(expected_media)
    matched = False
    for key in ("filename", "url"):
        value = meta.get(key, "")
        if not value:
            continue
        if value.endswith(expected_media) or os.path.basename(value) == expected_basename:
            matched = True
            print(f"✓ Meta field '{key}' matches expected media (0.5 points)")
            break
        else:
            print(f"- Meta field '{key}' does not match: {value}")
    if matched:
        score += 0.5
    else:
        print("✗ No meta field matched the expected media")

    final_score = min(score, max_score)
    print(f"Computed reward: {final_score} / {max_score}")
    return final_score


def main():
    expected_path = "/media/user/ExternalDrive/action_film.avi"
    reward = verify_playback(expected_path)
    print(f"REWARD: {reward}")


if __name__ == "__main__":
    main()

