"""
Reward Script: Swap the positions of the first and last tracks in my VLC playlist.
Task ID: vlc_playlist_062
Domain: vlc
Scoring:
  Component 1 (0.35): First track is finale.mp3
  Component 2 (0.35): Last track is opening_act.mp3
  Component 3 (0.30): Middle tracks unchanged (set1, set2, set3, encore)
"""

import os
from xml.etree import ElementTree

WORKDIR = '/home/user'
TASK_ID = 'vlc_playlist_062'
PLAYLIST_FILE = os.path.join(WORKDIR, f'{TASK_ID}.xspf')

# XSPF namespace
NS = {'xspf': 'http://xspf.org/ns/0/'}


def extract_track_filenames(file_path):
    """Parse XSPF playlist and return ordered list of track filenames."""
    tree = ElementTree.parse(file_path)
    root = tree.getroot()
    tracks = root.findall('.//xspf:trackList/xspf:track', NS)
    filenames = []
    for track in tracks:
        location = track.find('xspf:location', NS)
        if location is not None and location.text:
            # Extract filename from file:///path/to/file.mp3
            fname = os.path.basename(location.text)
            filenames.append(fname)
    return filenames


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load and parse the playlist
    try:
        filenames = extract_track_filenames(file_path)
        print(f"INFO: Found {len(filenames)} tracks: {filenames}")
    except Exception as e:
        print(f"CRITICAL: Cannot parse playlist {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must have exactly 6 tracks
    if len(filenames) != 6:
        print(f"FAIL: Expected 6 tracks, found {len(filenames)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: First track is finale.mp3 (0.35 points)
    # In the initial state, position 0 is opening_act.mp3, so this only passes after the swap.
    try:
        if filenames[0] == 'finale.mp3':
            print(f"PASS: Component 1 — First track is finale.mp3 (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — Expected first track 'finale.mp3', found '{filenames[0]}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Last track is opening_act.mp3 (0.35 points)
    # In the initial state, position 5 is finale.mp3, so this only passes after the swap.
    try:
        if filenames[5] == 'opening_act.mp3':
            print(f"PASS: Component 2 — Last track is opening_act.mp3 (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — Expected last track 'opening_act.mp3', found '{filenames[5]}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Middle tracks unchanged — set1, set2, set3, encore (0.30 points)
    # In the initial state, these middle tracks are already in the same positions,
    # but this component is compound: it only awards points if at least one of the
    # swap checks above also passed (ensuring we are scoring the swap, not the precondition).
    try:
        expected_middle = ['set1.mp3', 'set2.mp3', 'set3.mp3', 'encore.mp3']
        actual_middle = filenames[1:5]
        if actual_middle == expected_middle:
            # Only award if at least one swap component passed (prevents initial_env from scoring)
            if total_score > 0:
                print(f"PASS: Component 3 — Middle tracks unchanged: {actual_middle} (0.30 pts)")
                total_score += 0.30
            else:
                print(f"SKIP: Component 3 — Middle tracks correct but no swap detected, no points awarded")
        else:
            print(f"FAIL: Component 3 — Expected middle tracks {expected_middle}, found {actual_middle}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(PLAYLIST_FILE):
    print(f"File not found: {PLAYLIST_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(PLAYLIST_FILE)
