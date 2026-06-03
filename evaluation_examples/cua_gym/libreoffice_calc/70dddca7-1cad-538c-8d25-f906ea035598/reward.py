"""
Reward Script: Tag MP3 files with artist and title from filename
Task ID: osworld_multi_apps_misc_031
Domain: os (audio metadata)
Scoring:
  Component 1: All 4 MP3 files have ID3v2 tags present (0.3 points)
  Component 2: All 4 files have correct TPE1 (artist) tags matching filename (0.4 points)
  Component 3: All 4 files have correct TIT2 (title) tags matching filename (0.3 points)
  Total: 1.0
"""

import os

# mutagen is available on the VM for ID3 tag reading
_mutagen_id3_module = None
try:
    import mutagen.id3 as _mutagen_id3_module
except ImportError:
    pass

MUTAGEN_AVAILABLE = _mutagen_id3_module is not None

MUSIC_DIR = '/home/user/Music/Party'

# Expected tags derived from filename pattern "Artist - Title.mp3"
EXPECTED_TAGS = {
    'Avicii - Wake Me Up.mp3': {
        'artist': 'Avicii',
        'title': 'Wake Me Up',
    },
    'Calvin Harris - This Is What You Came For.mp3': {
        'artist': 'Calvin Harris',
        'title': 'This Is What You Came For',
    },
    'DJ Snake - Taki Taki.mp3': {
        'artist': 'DJ Snake',
        'title': 'Taki Taki',
    },
    'Martin Garrix - Animals.mp3': {
        'artist': 'Martin Garrix',
        'title': 'Animals',
    },
}


def read_id3_tags_mutagen(filepath):
    """Read ID3 artist and title tags using mutagen. Returns dict with 'artist', 'title', or None if not found."""
    try:
        ID3 = _mutagen_id3_module.ID3
        ID3NoHeaderError = _mutagen_id3_module.ID3NoHeaderError
        tags = ID3(filepath)
        result = {}
        # TPE1 = Lead performer / Artist
        if 'TPE1' in tags:
            result['artist'] = str(tags['TPE1']).strip()
        else:
            result['artist'] = None
        # TIT2 = Title
        if 'TIT2' in tags:
            result['title'] = str(tags['TIT2']).strip()
        else:
            result['title'] = None
        result['has_id3'] = True
        return result
    except Exception as e:
        err_type = type(e).__name__
        if 'NoHeaderError' in err_type or 'ID3NoHeaderError' in err_type:
            return {'has_id3': False, 'artist': None, 'title': None}
        return {'has_id3': False, 'artist': None, 'title': None, 'error': str(e)}


def read_id3_tags_manual(filepath):
    """Fallback: manually parse ID3v2 tags if mutagen is not available."""
    try:
        with open(filepath, 'rb') as f:
            header = f.read(10)
            if header[:3] != b'ID3':
                return {'has_id3': False, 'artist': None, 'title': None}

            # Syncsafe integer for tag size
            size = (header[6] << 21) | (header[7] << 14) | (header[8] << 7) | header[9]
            tag_data = f.read(size)

        frames = {}
        offset = 0
        while offset < len(tag_data) - 10:
            frame_id = tag_data[offset:offset + 4].decode('latin-1', errors='ignore')
            if not frame_id.strip() or frame_id[0] == '\x00':
                break
            frame_size = int.from_bytes(tag_data[offset + 4:offset + 8], 'big')
            if frame_size == 0:
                break
            frame_data = tag_data[offset + 10:offset + 10 + frame_size]

            if frame_id in ('TIT2', 'TPE1'):
                if not frame_data:
                    offset += 10 + frame_size
                    continue
                encoding = frame_data[0]
                payload = frame_data[1:]
                if encoding == 0:
                    text = payload.decode('latin-1', errors='ignore').rstrip('\x00')
                elif encoding == 1:
                    text = payload.decode('utf-16', errors='ignore').rstrip('\x00')
                elif encoding == 3:
                    text = payload.decode('utf-8', errors='ignore').rstrip('\x00')
                else:
                    text = payload.decode('latin-1', errors='ignore').rstrip('\x00')
                frames[frame_id] = text.strip()

            offset += 10 + frame_size

        artist = frames.get('TPE1', None)
        title = frames.get('TIT2', None)
        return {'has_id3': True, 'artist': artist, 'title': title}

    except Exception as e:
        return {'has_id3': False, 'artist': None, 'title': None, 'error': str(e)}


def read_tags(filepath):
    """Read ID3 tags using mutagen if available, else manual fallback."""
    if MUTAGEN_AVAILABLE:
        return read_id3_tags_mutagen(filepath)
    else:
        return read_id3_tags_manual(filepath)


def verify_task():
    """
    Verify that all 4 MP3 files in ~/Music/Party have correct artist and title ID3 tags.
    Progressive scoring:
      - 0.3 pts: all 4 files have ID3v2 tags present
      - 0.4 pts: all 4 files have correct artist (TPE1) tags
      - 0.3 pts: all 4 files have correct title (TIT2) tags
    Returns float 0.0 to 1.0
    """
    total_score = 0.0

    # Precondition: music directory must exist
    if not os.path.isdir(MUSIC_DIR):
        print(f"CRITICAL: Music directory not found: {MUSIC_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: all 4 files must exist
    for filename in EXPECTED_TAGS:
        path = os.path.join(MUSIC_DIR, filename)
        if not os.path.isfile(path):
            print(f"CRITICAL: Expected MP3 file not found: {filename}")
            print("REWARD: 0.0")
            return 0.0

    print(f"Precondition OK: all 4 MP3 files exist in {MUSIC_DIR}")
    print()

    # Read tags from all files
    file_tags = {}
    for filename in EXPECTED_TAGS:
        path = os.path.join(MUSIC_DIR, filename)
        tags = read_tags(path)
        file_tags[filename] = tags
        print(f"  {filename}: has_id3={tags.get('has_id3')}, artist={tags.get('artist')!r}, title={tags.get('title')!r}")

    print()

    # Component 1: All 4 files have ID3v2 tags present (0.3 points)
    # This verifies the tagging action was performed at all
    try:
        files_with_id3 = sum(1 for fn, tags in file_tags.items() if tags.get('has_id3'))
        if files_with_id3 == 4:
            print(f"PASS: Component 1 — All 4 files have ID3v2 tags (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Only {files_with_id3}/4 files have ID3v2 tags (expected 4)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 4 files have correct TPE1 (artist) tag (0.4 points)
    # Verifies artist tags match the "DJ Name" part of the filename
    try:
        artist_correct = 0
        artist_failures = []
        for filename, expected in EXPECTED_TAGS.items():
            actual_artist = file_tags[filename].get('artist')
            expected_artist = expected['artist']
            if actual_artist and actual_artist.strip() == expected_artist:
                artist_correct += 1
            else:
                artist_failures.append(
                    f"{filename}: expected artist={expected_artist!r}, got={actual_artist!r}"
                )

        if artist_correct == 4:
            print(f"PASS: Component 2 — All 4 files have correct artist (TPE1) tags (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — Only {artist_correct}/4 files have correct artist tags")
            for failure in artist_failures:
                print(f"  MISMATCH: {failure}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 4 files have correct TIT2 (title) tag (0.3 points)
    # Verifies title tags match the "Track Name" part of the filename
    try:
        title_correct = 0
        title_failures = []
        for filename, expected in EXPECTED_TAGS.items():
            actual_title = file_tags[filename].get('title')
            expected_title = expected['title']
            if actual_title and actual_title.strip() == expected_title:
                title_correct += 1
            else:
                title_failures.append(
                    f"{filename}: expected title={expected_title!r}, got={actual_title!r}"
                )

        if title_correct == 4:
            print(f"PASS: Component 3 — All 4 files have correct title (TIT2) tags (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Only {title_correct}/4 files have correct title tags")
            for failure in title_failures:
                print(f"  MISMATCH: {failure}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
