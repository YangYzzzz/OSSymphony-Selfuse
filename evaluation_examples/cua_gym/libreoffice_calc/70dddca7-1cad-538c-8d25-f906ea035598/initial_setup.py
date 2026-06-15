"""
Initial Setup: MP3 files with no ID3 tags in ~/Music/Party
Task ID: osworld_multi_apps_misc_031
Domain: os / multi_apps_misc

Creates ~/Music/Party/ with 4 minimal MP3 files that have NO artist/title tags.
The agent must use Kid3 or MusicBrainz Picard to add tags from filenames.
"""

import os
import shlex
import subprocess
import sys
import time

# Ensure mutagen is available on the VM
subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "mutagen"],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

WORKDIR = '/home/user'
MUSIC_DIR = f'{WORKDIR}/Music/Party'

# Track list: (filename, artist, title) - filenames only used for creation; NO tags
TRACKS = [
    "DJ Snake - Taki Taki.mp3",
    "Calvin Harris - This Is What You Came For.mp3",
    "Martin Garrix - Animals.mp3",
    "Avicii - Wake Me Up.mp3",
]


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_minimal_mp3(filepath: str):
    """
    Create a minimal valid MP3 file with no ID3 tags.
    The file contains a valid MPEG audio frame header so apps can recognise it.
    """
    # A minimal valid MP3 frame (MPEG1, Layer3, 128kbps, 44100Hz, stereo)
    # Frame header bytes: 0xFF 0xFB 0x90 0x00 followed by 413 zero bytes
    # Total frame size for 128kbps/44100Hz = 417 bytes
    frame_header = bytes([0xFF, 0xFB, 0x90, 0x00])
    frame_body = bytes(413)  # silence
    mp3_data = frame_header + frame_body

    # Write multiple frames to make a small but valid file (~10 frames)
    with open(filepath, 'wb') as f:
        for _ in range(10):
            f.write(mp3_data)


def create_initial():
    # Create directory
    os.makedirs(MUSIC_DIR, exist_ok=True)
    print(f'Created directory: {MUSIC_DIR}')

    # Create MP3 files with NO tags
    for filename in TRACKS:
        filepath = os.path.join(MUSIC_DIR, filename)
        create_minimal_mp3(filepath)
        print(f'  Created (no tags): {filepath}')

    # Verify no tags are present using mutagen (best effort)
    try:
        from mutagen.mp3 import MP3
        from mutagen.id3 import ID3NoHeaderError
        for filename in TRACKS:
            filepath = os.path.join(MUSIC_DIR, filename)
            audio = MP3(filepath)
            tags = audio.tags
            if tags is None:
                print(f'  Confirmed no tags: {filename}')
            else:
                print(f'  WARNING: unexpected tags found in {filename}: {tags.keys()}')
    except Exception as e:
        print(f'Tag verification skipped: {e}')

    print(f'\nAll MP3 files created in {MUSIC_DIR} with no ID3 tags.')

    # GUI-ready startup: open Nautilus file manager pointing to ~/Music/Party
    # so the agent can see the files and launch Kid3 or Picard
    launch_gui(f'nautilus "{MUSIC_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus file manager with DISPLAY=:0')


create_initial()
