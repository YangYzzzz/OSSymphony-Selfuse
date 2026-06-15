"""
Reward Script: VLC Playlist Creation from Multiple Folders
Task ID: vlc_playlist_061
Domain: vlc
Scoring:
  Component 1 (0.3): XSPF file exists and is valid XML playlist
  Component 2 (0.3): Playlist contains exactly 5 tracks
  Component 3 (0.2): All 3 Project_A/finals MP4 files present
  Component 4 (0.2): All 2 Project_B/finals MP4 files present
"""

import os
from xml.etree import ElementTree

WORKDIR = '/home/user'
TASK_ID = 'vlc_playlist_061'
XSPF_PATH = os.path.join(WORKDIR, 'Videos', 'review_queue.xspf')

# Expected files from each project
PROJECT_A_FILES = {
    'scene1_final.mp4',
    'scene2_final.mp4',
    'scene3_final.mp4',
}
PROJECT_B_FILES = {
    'intro_final.mp4',
    'outro_final.mp4',
}


def extract_track_locations(xspf_path):
    """Parse an XSPF file and return list of track location URIs."""
    tree = ElementTree.parse(xspf_path)
    root = tree.getroot()
    # XSPF uses a namespace
    ns = {'xspf': 'http://xspf.org/ns/0/'}
    tracks = root.findall('.//xspf:trackList/xspf:track/xspf:location', ns)
    return [t.text for t in tracks if t.text]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: XSPF file exists and is valid XML playlist (0.3 points)
    try:
        if not os.path.exists(XSPF_PATH):
            print(f"FAIL: Component 1 — XSPF file not found at {XSPF_PATH}")
            # If file doesn't exist, no further checks are possible
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        locations = extract_track_locations(XSPF_PATH)
        print(f"PASS: Component 1 — XSPF file exists and is valid XML with {len(locations)} track(s) (0.3 pts)")
        total_score += 0.3
    except ElementTree.ParseError as e:
        print(f"FAIL: Component 1 — XSPF file exists but is not valid XML: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Extract basenames from locations for easier matching
    track_basenames = set()
    for loc in locations:
        # Location format: file:///home/user/Videos/Project_A/finals/scene1_final.mp4
        basename = os.path.basename(loc)
        track_basenames.add(basename)
    print(f"  Tracks found: {sorted(track_basenames)}")

    # Component 2: Playlist contains exactly 5 tracks (0.3 points)
    try:
        if len(locations) == 5:
            print(f"PASS: Component 2 — Playlist has exactly 5 tracks (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected 5 tracks, found {len(locations)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 3 Project_A files present (0.2 points)
    try:
        project_a_found = PROJECT_A_FILES.intersection(track_basenames)
        if project_a_found == PROJECT_A_FILES:
            print(f"PASS: Component 3 — All 3 Project_A files present (0.2 pts)")
            total_score += 0.2
        else:
            missing = PROJECT_A_FILES - project_a_found
            print(f"FAIL: Component 3 — Missing Project_A files: {missing}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: All 2 Project_B files present (0.2 points)
    try:
        project_b_found = PROJECT_B_FILES.intersection(track_basenames)
        if project_b_found == PROJECT_B_FILES:
            print(f"PASS: Component 4 — All 2 Project_B files present (0.2 pts)")
            total_score += 0.2
        else:
            missing = PROJECT_B_FILES - project_b_found
            print(f"FAIL: Component 4 — Missing Project_B files: {missing}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
