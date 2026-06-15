"""
Reward Script: Change VLC playback speed to 1.5x
Task ID: vlcplay_004
Domain: vlc
Scoring:
  Component 1 (0.6 pts): Playback rate is approximately 1.5x (within 0.05 tolerance)
  Component 2 (0.4 pts): Playback rate is closer to 1.5 than to 1.0 (directional check)
"""

import requests
from xml.etree import ElementTree

VLC_HOST = "localhost"
VLC_PORT = 8080
VLC_PASSWORD = "password"
EXPECTED_RATE = 1.5
TOLERANCE = 0.05


def get_vlc_rate():
    """Fetch the current playback rate from VLC HTTP interface."""
    resp = requests.get(
        f"http://{VLC_HOST}:{VLC_PORT}/requests/status.xml",
        auth=("", VLC_PASSWORD),
        timeout=10,
    )
    root = ElementTree.fromstring(resp.content)
    rate_elem = root.find("rate")
    if rate_elem is None or rate_elem.text is None:
        return None
    return float(rate_elem.text)


def verify_task():
    """
    Verify that VLC playback speed is set to 1.5x.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Fetch the current rate from VLC
    try:
        rate = get_vlc_rate()
    except Exception as e:
        print(f"CRITICAL: Cannot connect to VLC HTTP interface: {e}")
        print("REWARD: 0.0")
        return 0.0

    if rate is None:
        print("CRITICAL: Could not parse rate from VLC status XML")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Current VLC playback rate: {rate}")

    # Component 1: Playback rate is approximately 1.5x (0.6 points)
    # This checks that the rate is within TOLERANCE of 1.5.
    # Fails on initial_env (rate=1.0), passes on golden_env (rate~1.5).
    try:
        diff = abs(rate - EXPECTED_RATE)
        if diff <= TOLERANCE:
            print(f"PASS: Component 1 - Rate {rate:.4f} is within {TOLERANCE} of {EXPECTED_RATE} (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 - Rate {rate:.4f} differs from {EXPECTED_RATE} by {diff:.4f} (tolerance: {TOLERANCE})")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Rate is significantly closer to 1.5 than to 1.0 (0.4 points)
    # This provides partial credit for rates between 1.0 and 1.5.
    # At rate=1.0: dist_to_target=0.5, dist_to_initial=0.0 -> fails
    # At rate=1.5: dist_to_target=0.0, dist_to_initial=0.5 -> passes
    try:
        dist_to_target = abs(rate - EXPECTED_RATE)
        dist_to_initial = abs(rate - 1.0)
        # Rate must be meaningfully closer to 1.5 than to 1.0
        # We require dist_to_initial > dist_to_target + 0.1 to avoid edge cases
        if dist_to_initial > dist_to_target + 0.1:
            print(f"PASS: Component 2 - Rate {rate:.4f} is closer to {EXPECTED_RATE} (dist={dist_to_target:.4f}) than to 1.0 (dist={dist_to_initial:.4f}) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 - Rate {rate:.4f} is not significantly closer to {EXPECTED_RATE} than to 1.0 (dist_target={dist_to_target:.4f}, dist_initial={dist_to_initial:.4f})")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
