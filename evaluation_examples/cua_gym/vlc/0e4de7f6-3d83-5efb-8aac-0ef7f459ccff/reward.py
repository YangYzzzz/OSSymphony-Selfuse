"""
Reward Script: Add three directories to VLC Media Library scan list
Task ID: vlc_playlist_078
Domain: vlc
Scoring:
  - Component 1: ~/Music/Albums/ in ml.xspf (0.33 pts)
  - Component 2: ~/Music/Singles/ in ml.xspf (0.33 pts)
  - Component 3: ~/Videos/Music_Videos/ in ml.xspf (0.34 pts)
"""

import os
from xml.etree import ElementTree

WORKDIR = '/home/user'
TASK_ID = 'vlc_playlist_078'
ML_XSPF_PATH = os.path.join(WORKDIR, '.local', 'share', 'vlc', 'ml.xspf')

# The three directories that must be present as scan entries
REQUIRED_DIRS = [
    '/home/user/Music/Albums',
    '/home/user/Music/Singles',
    '/home/user/Videos/Music_Videos',
]

# Scoring weights per directory
WEIGHTS = [0.33, 0.33, 0.34]


def get_ml_locations(xspf_path):
    """Parse ml.xspf and return a set of location URIs (decoded file paths)."""
    tree = ElementTree.parse(xspf_path)
    root = tree.getroot()
    # XSPF uses a namespace
    ns = {'xspf': 'http://xspf.org/ns/0/'}
    locations = set()
    for track in root.findall('.//xspf:trackList/xspf:track/xspf:location', ns):
        if track.text:
            # Locations are stored as file:///path — extract the path
            loc = track.text
            if loc.startswith('file://'):
                loc = loc[len('file://'):]
            # Normalize: strip trailing slash
            loc = loc.rstrip('/')
            locations.add(loc)
    return locations


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: ml.xspf file must exist
    if not os.path.exists(ML_XSPF_PATH):
        print(f"CRITICAL: ml.xspf not found at {ML_XSPF_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Parse the media library playlist
    try:
        locations = get_ml_locations(ML_XSPF_PATH)
        print(f"Found {len(locations)} scan locations in ml.xspf: {locations}")
    except Exception as e:
        print(f"CRITICAL: Cannot parse ml.xspf: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: ~/Music/Albums/ in scan list (0.33 points)
    try:
        dir_path = REQUIRED_DIRS[0]
        if dir_path in locations:
            print(f"PASS: Component 1 — {dir_path} found in ML scan list (0.33 pts)")
            total_score += WEIGHTS[0]
        else:
            print(f"FAIL: Component 1 — {dir_path} not found in ML scan list")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: ~/Music/Singles/ in scan list (0.33 points)
    try:
        dir_path = REQUIRED_DIRS[1]
        if dir_path in locations:
            print(f"PASS: Component 2 — {dir_path} found in ML scan list (0.33 pts)")
            total_score += WEIGHTS[1]
        else:
            print(f"FAIL: Component 2 — {dir_path} not found in ML scan list")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: ~/Videos/Music_Videos/ in scan list (0.34 points)
    try:
        dir_path = REQUIRED_DIRS[2]
        if dir_path in locations:
            print(f"PASS: Component 3 — {dir_path} found in ML scan list (0.34 pts)")
            total_score += WEIGHTS[2]
        else:
            print(f"FAIL: Component 3 — {dir_path} not found in ML scan list")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
