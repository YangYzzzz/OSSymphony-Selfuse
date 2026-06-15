"""
Reward Script: Add network stream to VLC playlist
Task ID: vlc_playlist_047
Domain: vlc
Scoring:
  Component 1 (0.3): Playlist contains exactly 4 entries (increased from 3)
  Component 2 (0.4): Network stream URL http://stream.example.com:8000/radio is present
  Component 3 (0.3): Original 3 local tracks are preserved
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vlc_playlist_047'
PLAYLIST_PATH = os.path.join(WORKDIR, f'{TASK_ID}.m3u')

EXPECTED_STREAM_URL = 'http://stream.example.com:8000/radio'
EXPECTED_LOCAL_TRACKS = [
    '/home/user/local_song1.mp3',
    '/home/user/local_song2.mp3',
    '/home/user/local_song3.mp3',
]


def parse_m3u(file_path):
    """Parse an M3U playlist and return list of track URIs."""
    tracks = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            tracks.append(line)
    return tracks


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        tracks = parse_m3u(file_path)
        print(f"INFO: Parsed {len(tracks)} tracks from playlist")
        for i, t in enumerate(tracks):
            print(f"  Track {i+1}: {t}")
    except Exception as e:
        print(f"CRITICAL: Cannot parse playlist {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Playlist contains exactly 4 entries (0.3 points)
    # Initial has 3 entries; golden should have 4 after adding the stream
    try:
        if len(tracks) == 4:
            print(f"PASS: Component 1 — Playlist has 4 entries (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Expected 4 entries, found {len(tracks)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Network stream URL is present in the playlist (0.4 points)
    # This is the core task change — adding the stream URL
    try:
        stream_found = any(EXPECTED_STREAM_URL in t for t in tracks)
        if stream_found:
            print(f"PASS: Component 2 — Network stream URL found in playlist (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — Network stream URL '{EXPECTED_STREAM_URL}' not found in playlist")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Original 3 local tracks are preserved (0.3 points)
    # Only award points if the stream URL is also present (compound check)
    # This ensures we score a task-introduced change (stream added alongside existing tracks)
    try:
        local_tracks_present = all(
            any(expected in t for t in tracks) for expected in EXPECTED_LOCAL_TRACKS
        )
        stream_present = any(EXPECTED_STREAM_URL in t for t in tracks)
        if local_tracks_present and stream_present:
            print(f"PASS: Component 3 — All 3 original local tracks preserved alongside stream (0.3 pts)")
            total_score += 0.3
        elif local_tracks_present and not stream_present:
            print(f"FAIL: Component 3 — Local tracks present but stream not added (no credit: compound check)")
        else:
            missing = [e for e in EXPECTED_LOCAL_TRACKS if not any(e in t for t in tracks)]
            print(f"FAIL: Component 3 — Missing local tracks: {missing}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(PLAYLIST_PATH):
    print(f"File not found: {PLAYLIST_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(PLAYLIST_PATH)
