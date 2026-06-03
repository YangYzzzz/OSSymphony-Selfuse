"""
Reward Script: Fill in MP3 ID3 tags (artist and title) from filenames
Task ID: osworld_multi_apps_misc_027
Domain: os (MP3 metadata / ID3 tags)
Scoring:
  Component 1: All 6 MP3 files have correct 'artist' (TPE1) ID3 tag   — 0.50 pts
  Component 2: All 6 MP3 files have correct 'title' (TIT2) ID3 tag    — 0.50 pts
  Total: 1.0
"""

import os
import sys

WORKDIR = '/home/user'
PODCAST_DIR = os.path.join(WORKDIR, 'Music', 'Podcasts')
TASK_ID = 'osworld_multi_apps_misc_027'

# Expected ID3 tags derived from filenames: "Show Name - Episode Title.mp3"
# artist = show name (part before " - ")
# title  = episode title (part after " - ", without .mp3)
EXPECTED_TAGS = {
    'Lex Fridman Podcast - Episode 300.mp3': {
        'artist': 'Lex Fridman Podcast',
        'title': 'Episode 300',
    },
    'The Joe Rogan Experience - Episode 2000.mp3': {
        'artist': 'The Joe Rogan Experience',
        'title': 'Episode 2000',
    },
    'Huberman Lab - Sleep Toolkit.mp3': {
        'artist': 'Huberman Lab',
        'title': 'Sleep Toolkit',
    },
    'How I Built This - Airbnb.mp3': {
        'artist': 'How I Built This',
        'title': 'Airbnb',
    },
    'Hidden Brain - The Optimism Bias.mp3': {
        'artist': 'Hidden Brain',
        'title': 'The Optimism Bias',
    },
    'Radiolab - Darkode.mp3': {
        'artist': 'Radiolab',
        'title': 'Darkode',
    },
}


def verify_task():
    """
    Verify that all six MP3 files in ~/Music/Podcasts have correct
    'artist' (TPE1) and 'title' (TIT2) ID3 tags extracted from their filenames.
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Precondition: ensure the podcast directory exists and has the expected files
    if not os.path.isdir(PODCAST_DIR):
        print(f"CRITICAL: Podcast directory not found: {PODCAST_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Attempt to import mutagen for ID3 tag reading
    try:
        from mutagen.id3 import ID3, ID3NoHeaderError
    except ImportError:
        print("CRITICAL: mutagen library not available")
        print("REWARD: 0.0")
        return 0.0

    # --- Component 1: All 6 files have correct 'artist' (TPE1) tag (0.5 points) ---
    try:
        artist_pass_count = 0
        artist_total = len(EXPECTED_TAGS)

        for filename, expected in EXPECTED_TAGS.items():
            filepath = os.path.join(PODCAST_DIR, filename)
            if not os.path.isfile(filepath):
                print(f"FAIL: Component 1 — File not found: {filename}")
                continue
            try:
                tags = ID3(filepath)
                tpe1 = tags.get('TPE1')
                actual_artist = str(tpe1) if tpe1 is not None else None
                expected_artist = expected['artist']
                if actual_artist == expected_artist:
                    print(f"PASS: artist '{actual_artist}' in {filename}")
                    artist_pass_count += 1
                else:
                    print(f"FAIL: artist mismatch in {filename}: expected={expected_artist!r}, found={actual_artist!r}")
            except ID3NoHeaderError:
                print(f"FAIL: No ID3 tags in {filename}")
            except Exception as e:
                print(f"ERROR: Could not read {filename}: {e}")

        if artist_pass_count == artist_total:
            print(f"PASS: Component 1 — All {artist_total} files have correct artist tag (0.5 pts)")
            total_score += 0.5
        else:
            partial = artist_pass_count / artist_total
            print(f"FAIL: Component 1 — Only {artist_pass_count}/{artist_total} files have correct artist tag")
            # No partial credit for this component — require all-or-nothing
            # (partial completion is captured by the per-file output above)

    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --- Component 2: All 6 files have correct 'title' (TIT2) tag (0.5 points) ---
    try:
        title_pass_count = 0
        title_total = len(EXPECTED_TAGS)

        for filename, expected in EXPECTED_TAGS.items():
            filepath = os.path.join(PODCAST_DIR, filename)
            if not os.path.isfile(filepath):
                print(f"FAIL: Component 2 — File not found: {filename}")
                continue
            try:
                tags = ID3(filepath)
                tit2 = tags.get('TIT2')
                actual_title = str(tit2) if tit2 is not None else None
                expected_title = expected['title']
                if actual_title == expected_title:
                    print(f"PASS: title '{actual_title}' in {filename}")
                    title_pass_count += 1
                else:
                    print(f"FAIL: title mismatch in {filename}: expected={expected_title!r}, found={actual_title!r}")
            except ID3NoHeaderError:
                print(f"FAIL: No ID3 tags (title check) in {filename}")
            except Exception as e:
                print(f"ERROR: Could not read title in {filename}: {e}")

        if title_pass_count == title_total:
            print(f"PASS: Component 2 — All {title_total} files have correct title tag (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — Only {title_pass_count}/{title_total} files have correct title tag")

    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
