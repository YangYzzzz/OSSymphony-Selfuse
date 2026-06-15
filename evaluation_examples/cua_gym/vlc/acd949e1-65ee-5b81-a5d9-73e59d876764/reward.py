"""
FINAL REWARD SCRIPT - SUCCESS
Task: Open streaming playlist /home/user/Radio/internet_stations.pls.
Generated: 2025-09-13 10:38:58
Status: success
Model: azure-o3
Total Steps: 8
"""

import glob
import os
import xml.etree.ElementTree as ET
import traceback


def verify_vlc_playback(expected_suffix: str = "internet_stations.pls") -> float:
    """Verify that VLC is currently playing the expected playlist/stream.

    Scoring (progressive):
    0.5  – VLC is in state == 'playing' (from status.xml)
    +0.5 – One of the <info name="filename|url"> or URI tags ends with the
            expected suffix (case-insensitive)
    Returns a float between 0.0 and 1.0.
    """

    print("=== VLC Playback Verification ===")

    # Locate every status.xml produced by the framework (search /home & /tmp)
    status_paths = (
        glob.glob("/home/**/*status.xml", recursive=True)
        + glob.glob("/tmp/**/*status.xml", recursive=True)
    )
    print(f"Found {len(status_paths)} status.xml file(s) to inspect")

    playing_found = False  # did we observe <state>playing</state> ?
    suffix_match_found = False  # did any meta/uri end with expected suffix?

    for path in status_paths:
        print(f"\nChecking {path}")
        try:
            tree = ET.parse(path)
            root = tree.getroot()
        except Exception as e:
            print(f"  ! Error parsing XML: {e}")
            traceback.print_exc()
            continue  # move on to next status.xml

        # --- 1. Check <state> ---
        state_elem = root.find("state")
        state_text = (
            state_elem.text.strip().lower() if state_elem is not None and state_elem.text else ""
        )
        print(f"  state: {state_text}")
        if state_text == "playing":
            playing_found = True

            # --- 2. Collect candidate meta values to match suffix ---
            candidate_values = []

            # a) <info name="filename|url">value</info>
            for info in root.findall(".//info"):
                name = (info.attrib.get("name") or "").lower()
                if name in ("filename", "url"):
                    candidate_values.append(info.text or "")

            # b) <filename>, <url>, <uri> direct tags (appear in some VLC versions)
            for tag in ("filename", "url", "uri"):
                for elem in root.findall(f".//{tag}"):
                    candidate_values.append(elem.text or "")

            print(f"  Candidate meta values: {candidate_values}")
            for value in candidate_values:
                if value.lower().endswith(expected_suffix.lower()):
                    suffix_match_found = True
                    break

        else:
            print("  Not in 'playing' state – skipping meta checks for this file")

        # EARLY EXIT: once both conditions satisfied, no need to inspect further
        if playing_found and suffix_match_found:
            break

    # --------------------- Scoring ---------------------
    score = 0.0
    if playing_found:
        score += 0.5
    if playing_found and suffix_match_found:
        score += 0.5

    # ----------------- Summary Prints -----------------
    print("\n=== Verification Summary ===")
    if playing_found:
        print("✓ VLC is in 'playing' state  (0.5 points)")
    else:
        print("✗ VLC is NOT in 'playing' state  (0 points)")

    if suffix_match_found:
        print(f"✓ Media ends with expected suffix '{expected_suffix}'  (0.5 points)")
    else:
        print(f"✗ Media does NOT end with expected suffix '{expected_suffix}'  (0 points)")

    final_score = min(score, 1.0)
    print(f"Final score: {final_score}")
    return final_score


if __name__ == "__main__":
    reward = verify_vlc_playback("internet_stations.pls")
    print(f"REWARD: {reward}")

