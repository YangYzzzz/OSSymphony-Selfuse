"""
Reward Script: Open tutorial.avi in VLC and set playback speed to 0.5x
Task ID: vlcplay_009
Domain: vlc
Scoring:
  Component 1: tutorial.avi is loaded in VLC playlist (0.4 pts)
  Component 2: Playback rate is 0.5x (0.6 pts)
"""

import time
import requests
from xml.etree import ElementTree

VLC_HOST = "localhost"
VLC_PORT = 8080
VLC_PASSWORD = "password"
EXPECTED_FILENAME = "tutorial.avi"
EXPECTED_RATE = 0.5
RATE_TOLERANCE = 0.05  # allow small floating point variance


def get_vlc_status():
    """Fetch VLC status XML via HTTP interface."""
    resp = requests.get(
        f"http://{VLC_HOST}:{VLC_PORT}/requests/status.xml",
        auth=("", VLC_PASSWORD),
        timeout=5,
    )
    return ElementTree.fromstring(resp.content)


def get_vlc_playlist():
    """Fetch VLC playlist XML via HTTP interface."""
    resp = requests.get(
        f"http://{VLC_HOST}:{VLC_PORT}/requests/playlist.xml",
        auth=("", VLC_PASSWORD),
        timeout=5,
    )
    return ElementTree.fromstring(resp.content)


def ensure_playing():
    """If VLC has a file loaded but is stopped/paused, resume playback so we can read the rate."""
    try:
        status = get_vlc_status()
        state = status.find("state").text
        if state in ("stopped", "paused"):
            # Try to play current item
            playlist = get_vlc_playlist()
            # Find the current leaf or first leaf
            leaves = playlist.findall(".//leaf")
            if leaves:
                item_id = leaves[0].get("id")
                requests.get(
                    f"http://{VLC_HOST}:{VLC_PORT}/requests/status.xml?command=pl_play&id={item_id}",
                    auth=("", VLC_PASSWORD),
                    timeout=5,
                )
                time.sleep(2)
    except Exception as e:
        print(f"WARN: ensure_playing failed: {e}")


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # First, check if VLC HTTP interface is reachable at all
    try:
        status = get_vlc_status()
    except Exception as e:
        print(f"CRITICAL: Cannot reach VLC HTTP interface: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: tutorial.avi is loaded in VLC playlist (0.4 points)
    # This differentiates golden (file loaded) from initial (empty playlist).
    try:
        playlist = get_vlc_playlist()
        leaves = playlist.findall(".//leaf")
        matching_leaves = [
            leaf for leaf in leaves
            if EXPECTED_FILENAME in leaf.get("uri", "") or EXPECTED_FILENAME in leaf.get("name", "")
        ]

        if len(matching_leaves) > 0:
            print(f"PASS: Component 1 -- {EXPECTED_FILENAME} found in playlist (0.4 pts)")
            total_score += 0.4
        else:
            leaf_names = [leaf.get("name", "") for leaf in leaves]
            print(f"FAIL: Component 1 -- {EXPECTED_FILENAME} not in playlist. Found: {leaf_names}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # If file is not loaded, no point checking rate -- return early
    if total_score < 0.1:
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Before checking rate, ensure the file is playing (it may have finished
    # for short videos). We need the file playing to read the actual rate.
    ensure_playing()

    # Component 2: Playback rate is 0.5x (0.6 points)
    # On initial_env, there is no file loaded so we never reach here.
    # On golden_env, the rate should be 0.5.
    try:
        status = get_vlc_status()
        rate_elem = status.find("rate")
        if rate_elem is not None and rate_elem.text:
            actual_rate = float(rate_elem.text)
            if abs(actual_rate - EXPECTED_RATE) <= RATE_TOLERANCE:
                print(f"PASS: Component 2 -- playback rate is {actual_rate} (expected ~{EXPECTED_RATE}) (0.6 pts)")
                total_score += 0.6
            else:
                print(f"FAIL: Component 2 -- playback rate is {actual_rate}, expected ~{EXPECTED_RATE}")
        else:
            print("FAIL: Component 2 -- could not read rate from VLC status")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
