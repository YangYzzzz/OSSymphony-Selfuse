"""
Reward Script: Find and play deep_focus_03 in VLC playlist
Task ID: vlc_playlist_048
Domain: vlc
Scoring:
  - Component 1 (0.5 pts): VLC is playing a deep_focus track (partial match)
  - Component 2 (0.5 pts): Exact track is deep_focus_03.mp3
"""

import requests
from xml.etree import ElementTree

TASK_ID = 'vlc_playlist_048'
VLC_HTTP_HOST = 'localhost'
VLC_HTTP_PORT = 8080
VLC_HTTP_PASSWORD = 'password'


def get_vlc_status():
    """Fetch VLC status XML via HTTP interface."""
    resp = requests.get(
        f'http://{VLC_HTTP_HOST}:{VLC_HTTP_PORT}/requests/status.xml',
        auth=('', VLC_HTTP_PASSWORD),
        timeout=5
    )
    return ElementTree.fromstring(resp.content)


def get_current_filename(tree):
    """Extract the current filename from VLC status XML."""
    # Check multiple meta paths for robustness
    for xpath in [
        'information/category[@name="meta"]/info[@name="filename"]',
        'information/category[@name="meta"]/info[@name="title"]',
    ]:
        elem = tree.find(xpath)
        if elem is not None and elem.text:
            return elem.text.strip()
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: VLC HTTP interface is accessible
    try:
        tree = get_vlc_status()
    except Exception as e:
        print(f"CRITICAL: Cannot connect to VLC HTTP interface: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get current playback state
    state_elem = tree.find('state')
    if state_elem is None:
        print("CRITICAL: No state element in VLC status XML")
        print("REWARD: 0.0")
        return 0.0

    state = state_elem.text
    filename = get_current_filename(tree)
    print(f"VLC state: {state}")
    print(f"Current filename: {filename}")

    # Component 1: VLC is playing a deep_focus track (0.5 points)
    # This checks both that VLC is actively playing AND that the track
    # belongs to the deep_focus family -- verifies the user searched for
    # and navigated to the correct family of tracks.
    try:
        if state in ('playing', 'paused') and filename and 'deep_focus' in filename.lower():
            print(f"PASS: Component 1 -- VLC is playing a deep_focus track: {filename} (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 -- Expected a playing deep_focus track, "
                  f"found state={state}, filename={filename}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Exact track match -- deep_focus_03.mp3 (0.5 points)
    # This verifies the user found the EXACT correct track, not just any
    # deep_focus track. The filename must be deep_focus_03.mp3.
    try:
        if filename and filename.strip() == 'deep_focus_03.mp3':
            print(f"PASS: Component 2 -- Exact track match: deep_focus_03.mp3 (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 -- Expected deep_focus_03.mp3, found: {filename}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
