"""
Reward Script: Add ~/Music/ and ~/Videos/ as VLC Media Library scan directories
Task ID: vlc_playlist_040
Domain: vlc
Scoring:
  Component 1 (0.3): media-library enabled in vlcrc
  Component 2 (0.35): ~/Music/ listed in ml.xspf
  Component 3 (0.35): ~/Videos/ listed in ml.xspf
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vlc_playlist_040'

VLCRC_PATH = os.path.expanduser('~/.config/vlc/vlcrc')
ML_XSPF_PATH = os.path.expanduser('~/.local/share/vlc/ml.xspf')


def get_vlcrc_option(key, default=None):
    """Read a vlcrc option value. Returns default if key is commented or missing."""
    try:
        with open(VLCRC_PATH, 'r') as f:
            content = f.read()
        for line in content.split('\n'):
            stripped = line.strip()
            if stripped.startswith('#') or not stripped:
                continue
            if f'{key}=' in stripped:
                return stripped.split('=', 1)[-1].strip()
        return default
    except Exception:
        return default


def parse_ml_xspf_locations():
    """Parse ml.xspf and return list of track location URIs."""
    locations = []
    try:
        with open(ML_XSPF_PATH, 'r') as f:
            content = f.read()
        # Use regex to extract all <location>...</location> values
        pattern = re.compile(r'<location>(.*?)</location>', re.DOTALL)
        locations = [m.strip() for m in pattern.findall(content)]
    except FileNotFoundError:
        print(f"INFO: ml.xspf not found at {ML_XSPF_PATH}")
    except Exception as e:
        print(f"ERROR: Failed to parse ml.xspf: {e}")
    return locations


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: media-library is enabled in vlcrc (0.3 points)
    # In initial_env this is commented out (#media-library=0), meaning default/disabled.
    # In golden_env this should be uncommented and set to 1.
    try:
        ml_value = get_vlcrc_option('media-library')
        if ml_value is not None and str(ml_value) == '1':
            print(f"PASS: Component 1 -- media-library=1 in vlcrc (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 -- media-library option is '{ml_value}' (expected '1')")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Parse ml.xspf once for Components 2 and 3
    locations = parse_ml_xspf_locations()
    print(f"INFO: ml.xspf locations found: {locations}")

    # Component 2: ~/Music/ is a scan directory in ml.xspf (0.35 points)
    try:
        music_found = any('Music' in loc and loc.startswith('file:///home/user/') for loc in locations)
        if music_found:
            print(f"PASS: Component 2 -- ~/Music/ found in Media Library (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 -- ~/Music/ not found in Media Library locations")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: ~/Videos/ is a scan directory in ml.xspf (0.35 points)
    try:
        videos_found = any('Videos' in loc and loc.startswith('file:///home/user/') for loc in locations)
        if videos_found:
            print(f"PASS: Component 3 -- ~/Videos/ found in Media Library (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 3 -- ~/Videos/ not found in Media Library locations")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
