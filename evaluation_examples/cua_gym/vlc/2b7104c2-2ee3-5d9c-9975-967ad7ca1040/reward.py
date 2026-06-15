"""
Reward Script: VLC Playlist Project Handoff
Task ID: vlc_playlist_080
Domain: vlc
Scoring:
  Component 1 (0.30) — M3U playlist exists with all 8 tracks
  Component 2 (0.30) — XSPF playlist exists with all 8 tracks
  Component 3 (0.20) — Repeat-all mode enabled in vlcrc (loop=1)
  Component 4 (0.20) — Tracks in correct sorted order (01 through 08)
"""

import os
import re
from xml.etree import ElementTree

WORKDIR = '/home/user'
TASK_ID = 'vlc_playlist_080'
DELIVERY_DIR = os.path.join(WORKDIR, 'Videos', 'Final_Delivery')
M3U_PATH = os.path.join(DELIVERY_DIR, 'delivery_manifest.m3u')
XSPF_PATH = os.path.join(DELIVERY_DIR, 'delivery_manifest.xspf')
VLCRC_PATH = os.path.join(WORKDIR, '.config', 'vlc', 'vlcrc')

# The 8 expected filenames in sorted order
EXPECTED_FILES = [
    '01_opening.mp4',
    '02_brand_intro.mp4',
    '03_product_demo.mp4',
    '04_testimonials.mp4',
    '05_features.mp4',
    '06_pricing.mp4',
    '07_call_to_action.mp4',
    '08_credits.mp4',
]


def parse_m3u_tracks(filepath):
    """Parse an M3U file and return list of track filenames (basenames) in order."""
    tracks = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # This is a file path line
                tracks.append(os.path.basename(line))
    except Exception as e:
        print(f"ERROR: Cannot read M3U file: {e}")
    return tracks


def parse_xspf_tracks(filepath):
    """Parse an XSPF file and return list of track filenames (basenames) in order."""
    tracks = []
    try:
        tree = ElementTree.parse(filepath)
        root = tree.getroot()
        # XSPF uses namespace
        ns = {'xspf': 'http://xspf.org/ns/0/'}
        for track in root.findall('.//xspf:trackList/xspf:track', ns):
            location = track.find('xspf:location', ns)
            if location is not None and location.text:
                # location is like file:///home/user/Videos/Final_Delivery/01_opening.mp4
                path = location.text.replace('file://', '')
                tracks.append(os.path.basename(path))
    except Exception as e:
        print(f"ERROR: Cannot parse XSPF file: {e}")
    return tracks


def get_vlcrc_option(key):
    """Read an uncommented vlcrc option. Returns None if commented or missing."""
    try:
        with open(VLCRC_PATH, 'r') as f:
            for line in f:
                stripped = line.strip()
                if stripped.startswith('#') or not stripped:
                    continue
                if stripped.startswith(f'{key}='):
                    return stripped.split('=', 1)[1].strip()
    except Exception as e:
        print(f"ERROR: Cannot read vlcrc: {e}")
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: M3U playlist exists with all 8 tracks (0.30 points)
    try:
        if not os.path.exists(M3U_PATH):
            print(f"FAIL: Component 1 -- M3U file not found at {M3U_PATH}")
        else:
            m3u_tracks = parse_m3u_tracks(M3U_PATH)
            m3u_basenames = set(m3u_tracks)
            expected_set = set(EXPECTED_FILES)
            if expected_set.issubset(m3u_basenames) and len(m3u_tracks) >= 8:
                print(f"PASS: Component 1 -- M3U has all 8 tracks ({m3u_tracks}) (0.30 pts)")
                total_score += 0.30
            else:
                missing = expected_set - m3u_basenames
                print(f"FAIL: Component 1 -- M3U missing tracks: {missing}, found: {m3u_basenames}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: XSPF playlist exists with all 8 tracks (0.30 points)
    try:
        if not os.path.exists(XSPF_PATH):
            print(f"FAIL: Component 2 -- XSPF file not found at {XSPF_PATH}")
        else:
            xspf_tracks = parse_xspf_tracks(XSPF_PATH)
            xspf_basenames = set(xspf_tracks)
            expected_set = set(EXPECTED_FILES)
            if expected_set.issubset(xspf_basenames) and len(xspf_tracks) >= 8:
                print(f"PASS: Component 2 -- XSPF has all 8 tracks ({xspf_tracks}) (0.30 pts)")
                total_score += 0.30
            else:
                missing = expected_set - xspf_basenames
                print(f"FAIL: Component 2 -- XSPF missing tracks: {missing}, found: {xspf_basenames}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Repeat-all mode enabled in vlcrc (0.20 points)
    # "Repeat all" in VLC means loop=1 (loop the playlist).
    # repeat=1 means repeat the current item. The task says "repeat all" which is loop.
    # We check loop=1 as the primary indicator of "repeat all" mode.
    try:
        loop_val = get_vlcrc_option('loop')
        if loop_val == '1':
            print(f"PASS: Component 3 -- loop=1 (repeat all enabled) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 -- expected loop=1, found loop={loop_val}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Tracks in correct sorted order (01 through 08) (0.20 points)
    # Check order in BOTH playlist files. At least one must have correct order.
    try:
        m3u_ordered = (parse_m3u_tracks(M3U_PATH) == EXPECTED_FILES) if os.path.exists(M3U_PATH) else False
        xspf_ordered = (parse_xspf_tracks(XSPF_PATH) == EXPECTED_FILES) if os.path.exists(XSPF_PATH) else False

        if m3u_ordered or xspf_ordered:
            print(f"PASS: Component 4 -- Tracks in correct sorted order 01-08 (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 -- Tracks not in correct sorted order")
            if os.path.exists(M3U_PATH):
                print(f"  M3U order: {parse_m3u_tracks(M3U_PATH)}")
            if os.path.exists(XSPF_PATH):
                print(f"  XSPF order: {parse_xspf_tracks(XSPF_PATH)}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
