"""
Reward Script: Tag MP3 files with correct ID3 artist and title metadata
Task ID: osworld_multi_apps_misc_025
Domain: os (MP3 metadata / file tagging)
Scoring:
  - Component 1: Taylor Swift - Shake It Off has artist='Taylor Swift', title='Shake It Off' (0.25)
  - Component 2: Ed Sheeran - Shape of You has artist='Ed Sheeran', title='Shape of You' (0.25)
  - Component 3: Billie Eilish - Bad Guy has artist='Billie Eilish', title='Bad Guy' (0.25)
  - Component 4: Adele - Rolling in the Deep has artist='Adele', title='Rolling in the Deep' (0.25)
Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_misc_025'
MUSIC_DIR = '/home/user/Music'

# Expected tags: (filename, expected_artist, expected_title)
EXPECTED_TAGS = [
    ('Taylor Swift - Shake It Off.mp3', 'Taylor Swift', 'Shake It Off'),
    ('Ed Sheeran - Shape of You.mp3', 'Ed Sheeran', 'Shape of You'),
    ('Billie Eilish - Bad Guy.mp3', 'Billie Eilish', 'Bad Guy'),
    ('Adele - Rolling in the Deep.mp3', 'Adele', 'Rolling in the Deep'),
]


def get_id3_tags(file_path):
    """
    Read ID3 artist (TPE1) and title (TIT2) tags from an MP3 file.
    Returns (artist, title) or (None, None) if tags are absent or unreadable.
    """
    try:
        from mutagen.id3 import ID3, ID3NoHeaderError
        try:
            tags = ID3(file_path)
            artist_tag = tags.get('TPE1')
            title_tag = tags.get('TIT2')
            artist = str(artist_tag) if artist_tag is not None else None
            title = str(title_tag) if title_tag is not None else None
            return artist, title
        except ID3NoHeaderError:
            # File has no ID3 header — tags are absent
            return None, None
    except ImportError:
        raise RuntimeError("mutagen library is not available; cannot verify ID3 tags")


def verify_task():
    """
    Verify that all four MP3 files in ~/Music have the correct ID3 artist
    and title tags set based on their filenames.
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0
    component_weight = 0.25  # 4 files × 0.25 = 1.0

    # Pre-condition gate: Music directory must exist
    if not os.path.isdir(MUSIC_DIR):
        print(f"CRITICAL: Music directory not found at {MUSIC_DIR}")
        print("REWARD: 0.0")
        return 0.0

    for filename, expected_artist, expected_title in EXPECTED_TAGS:
        file_path = os.path.join(MUSIC_DIR, filename)

        # Pre-condition: the MP3 file itself must exist
        if not os.path.isfile(file_path):
            print(f"FAIL: File not found — {filename}")
            continue

        # Component: verify artist AND title tags match expected values
        try:
            actual_artist, actual_title = get_id3_tags(file_path)

            artist_ok = (actual_artist == expected_artist)
            title_ok = (actual_title == expected_title)

            if artist_ok and title_ok:
                msg = f"PASS: {filename} — artist='{actual_artist}', title='{actual_title}' ({component_weight} pts)"
                print(msg)
                total_score += component_weight
            else:
                details = []
                if not artist_ok:
                    details.append(
                        f"artist: expected='{expected_artist}', got='{actual_artist}'"
                    )
                if not title_ok:
                    details.append(
                        f"title: expected='{expected_title}', got='{actual_title}'"
                    )
                print(f"FAIL: {filename} — {'; '.join(details)}")

        except RuntimeError as e:
            print(f"ERROR: {filename} — {e}")
        except Exception as e:
            print(f"ERROR: {filename} — unexpected error: {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
