"""
Reward Script: Change VLC interface language to French
Task ID: vlcset_001
Domain: vlc
Scoring:
  Component 1 (0.5): language key is present and uncommented in vlcrc
  Component 2 (0.5): language value is exactly 'fr'
"""

import os
import re

VLCRC_PATH = os.path.expanduser("~/.config/vlc/vlcrc")


def get_vlcrc_option(key: str, default=None):
    """Read an uncommented vlcrc option value. Returns default if key is commented or missing."""
    try:
        with open(VLCRC_PATH, "r") as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR: Cannot read vlcrc: {e}")
        return default

    for line in content.split("\n"):
        stripped = line.strip()
        # Skip comments and empty lines
        if stripped.startswith("#") or not stripped:
            continue
        # Match exact key= to avoid partial matches (e.g., audio-language vs language)
        if re.match(rf'^{re.escape(key)}=', stripped):
            return stripped.split("=", 1)[-1].strip()
    return default


def verify_task():
    """
    Verify that VLC interface language has been changed to French.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: vlcrc file must exist
    if not os.path.exists(VLCRC_PATH):
        print(f"CRITICAL: vlcrc not found at {VLCRC_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: language key is present and uncommented in vlcrc (0.5 points)
    # In the initial state, language is commented out (default/Auto).
    # The task requires setting it to a specific language.
    try:
        language_value = get_vlcrc_option("language")
        if language_value is not None and language_value != "":
            print(f"PASS: Component 1 -- language key is set to '{language_value}' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 -- language key is not set or empty (value: {language_value})")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: language value is exactly 'fr' (0.5 points)
    # The task specifically requires French (Francais), which is 'fr' in VLC.
    try:
        language_value = get_vlcrc_option("language")
        if language_value is not None and language_value == "fr":
            print(f"PASS: Component 2 -- language is 'fr' (French) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 -- expected 'fr', found '{language_value}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
