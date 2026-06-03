"""
Reward Script: VLC Playlist Reorder
Task ID: vlc_playlist_076
Domain: vlc
Scoring:
  Component 1 (0.3): Playlist contains exactly 5 tracks
  Component 2 (0.35): meditation.mp3 is first, yoga_flow.mp3 is second
  Component 3 (0.35): Remaining 3 tracks in original order (alarm_tone, breakfast_jazz, news_briefing)
"""

import requests
from xml.etree import ElementTree
import os

WORKDIR = '/home/user'
TASK_ID = 'vlc_playlist_076'

# Expected playlist order after task completion
EXPECTED_ORDER = [
    'meditation.mp3',
    'yoga_flow.mp3',
    'alarm_tone.mp3',
    'breakfast_jazz.mp3',
    'news_briefing.mp3',
]


def get_playlist_tracks(host='localhost', port=8080, password='password'):
    """Fetch the VLC playlist and return ordered list of track filenames."""
    resp = requests.get(
        f'http://{host}:{port}/requests/playlist.xml',
        auth=('', password),
        timeout=5,
    )
    root = ElementTree.fromstring(resp.content)

    # Find the Playlist node (id="1" or name="Playlist")
    playlist_node = None
    for node in root.iter('node'):
        if node.get('name') == 'Playlist':
            playlist_node = node
            break

    if playlist_node is None:
        print("FAIL: Could not find Playlist node in VLC playlist XML")
        return []

    # Extract leaf names in order
    tracks = []
    for leaf in playlist_node.findall('leaf'):
        name = leaf.get('name', '')
        if name:
            tracks.append(name)

    return tracks


def verify_task():
    """
    Verify VLC playlist reorder task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Fetch playlist from VLC HTTP interface
    try:
        tracks = get_playlist_tracks()
        print(f"INFO: Found {len(tracks)} tracks in playlist: {tracks}")
    except Exception as e:
        print(f"CRITICAL: Cannot fetch VLC playlist via HTTP interface: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Playlist has exactly 5 tracks (0.3 points)
    # This checks that all files from ~/Music/Morning_Routine/ were added.
    # On initial_env the playlist is empty, so this fails there.
    try:
        if len(tracks) == 5:
            # Also verify the correct filenames are present (any order)
            expected_names = set(EXPECTED_ORDER)
            actual_names = set(tracks)
            if expected_names == actual_names:
                print(f"PASS: Component 1 - Playlist has exactly 5 correct tracks (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 - Playlist has 5 tracks but wrong names. Expected: {expected_names}, Got: {actual_names}")
        else:
            print(f"FAIL: Component 1 - Expected 5 tracks, found {len(tracks)}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: meditation.mp3 is position 1, yoga_flow.mp3 is position 2 (0.35 points)
    # This is the core task requirement - these two tracks must be moved to the front.
    # On initial_env the playlist is empty, so this fails there.
    try:
        if len(tracks) >= 2:
            pos1_ok = (tracks[0] == 'meditation.mp3')
            pos2_ok = (tracks[1] == 'yoga_flow.mp3')
            if pos1_ok and pos2_ok:
                print(f"PASS: Component 2 - meditation.mp3 first, yoga_flow.mp3 second (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 - Position 1: {tracks[0]} (expected meditation.mp3), Position 2: {tracks[1]} (expected yoga_flow.mp3)")
        else:
            print(f"FAIL: Component 2 - Not enough tracks to verify positions (found {len(tracks)})")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Remaining tracks in original relative order (0.35 points)
    # After meditation and yoga_flow, the remaining tracks should be: alarm_tone, breakfast_jazz, news_briefing
    # This is their original filesystem order.
    # On initial_env the playlist is empty, so this fails there.
    try:
        if len(tracks) == 5:
            remaining = tracks[2:]
            expected_remaining = ['alarm_tone.mp3', 'breakfast_jazz.mp3', 'news_briefing.mp3']
            if remaining == expected_remaining:
                print(f"PASS: Component 3 - Remaining tracks in correct order: {remaining} (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 3 - Remaining tracks order: {remaining}, expected: {expected_remaining}")
        else:
            print(f"FAIL: Component 3 - Cannot verify remaining order with {len(tracks)} tracks")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
