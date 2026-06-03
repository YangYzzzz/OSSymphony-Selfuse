"""
Reward Script: Delete all custom bookmarks in VLC
Task ID: vlc_playlist_045
Domain: vlc
Scoring:
  Component 1 (0.5): Bookmark count is 0 in vlc-qt-interface.conf
  Component 2 (0.3): No individual bookmark row entries exist
  Component 3 (0.2): Media file still present (playback not disrupted)
"""

import os
import re
import configparser

WORKDIR = '/home/user'
TASK_ID = 'vlc_playlist_045'
QT_CONF_PATH = os.path.join(WORKDIR, '.config', 'vlc', 'vlc-qt-interface.conf')


def verify_task():
    """
    Verify that all custom bookmarks have been deleted from VLC.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: vlc-qt-interface.conf must exist
    if not os.path.exists(QT_CONF_PATH):
        print(f"CRITICAL: Config file not found: {QT_CONF_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(QT_CONF_PATH, 'r') as f:
            conf_content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read config file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Bookmark count is 0 (0.5 points)
    # In initial_env, count=4. In golden_env, count=0.
    try:
        # Parse the [Bookmarks] section for count value
        count_match = re.search(r'\[Bookmarks\]\s*\n(?:.*\n)*?count=(\d+)', conf_content)
        if count_match:
            bookmark_count = int(count_match.group(1))
            if bookmark_count == 0:
                print(f"PASS: Component 1 -- Bookmark count is 0 (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 1 -- Expected bookmark count=0, found count={bookmark_count}")
        else:
            # If [Bookmarks] section doesn't exist or count key is missing,
            # that also means no bookmarks (section removed entirely)
            if '[Bookmarks]' not in conf_content:
                print(f"PASS: Component 1 -- [Bookmarks] section removed entirely (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 1 -- [Bookmarks] section exists but count key not found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: No individual bookmark row entries (0.3 points)
    # In initial_env, there are row0\name=Intro, row1\name=Demo Start, etc.
    # In golden_env, these should all be absent.
    try:
        # Find any rowN\name= or rowN\time= or rowN\bytes= entries in the Bookmarks section
        bookmark_rows = re.findall(r'row\d+\\(?:name|time|bytes)=', conf_content)
        if len(bookmark_rows) == 0:
            print(f"PASS: Component 2 -- No bookmark row entries found (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- Found {len(bookmark_rows)} bookmark row entries: {bookmark_rows[:6]}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Media file still present (0.2 points)
    # Verify the video file still exists, confirming playback was not disrupted
    # This checks that the task was done without breaking the media setup.
    # In initial_env, the file exists but bookmarks also exist (so Component 1+2 fail).
    # We need this to differentiate from a scenario where someone deleted the whole VLC config.
    # Score this ONLY if bookmarks are actually gone (compound check).
    try:
        media_path = os.path.join(WORKDIR, 'Videos', 'webinar_recording.mp4')
        media_exists = os.path.exists(media_path)
        # Compound: media exists AND bookmarks section reflects deletion
        # This component is meaningful because it confirms selective bookmark deletion
        # rather than wholesale config or media destruction.
        # Only award if count == 0 (prevents scoring on initial_env)
        if media_exists and total_score >= 0.5:
            print(f"PASS: Component 3 -- Media file exists and bookmarks cleared (0.2 pts)")
            total_score += 0.2
        elif not media_exists:
            print(f"FAIL: Component 3 -- Media file not found at {media_path}")
        else:
            print(f"FAIL: Component 3 -- Media exists but bookmarks not cleared (compound check)")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
