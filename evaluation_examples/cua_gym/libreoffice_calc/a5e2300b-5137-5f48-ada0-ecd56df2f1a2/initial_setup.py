"""
Initial Setup: Create ~/Music directory with 4 MP3 files that have no metadata tags.
Task ID: osworld_multi_apps_misc_025
Domain: os / multi_apps
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
MUSIC_DIR = f'{WORKDIR}/Music'

# MP3 files to create (named in 'Artist - Title.mp3' format, but NO ID3 tags)
MP3_FILES = [
    'Taylor Swift - Shake It Off.mp3',
    'Ed Sheeran - Shape of You.mp3',
    'Billie Eilish - Bad Guy.mp3',
    'Adele - Rolling in the Deep.mp3',
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


def create_minimal_mp3(path: str):
    """
    Create a minimal valid MP3 file with NO ID3 tags.
    A valid MP3 consists of at least one MPEG audio frame.
    This creates a silent 1-frame MP3 with no metadata.
    """
    # Minimal valid MP3 frame: MPEG1 Layer3, 128kbps, 44100Hz, stereo, no ID3 header
    # Frame sync: 0xFFFA (MPEG1, Layer3, no CRC)
    # This is a single silent MP3 frame header + silence data
    # Frame header bytes: FF FB 90 00 (MPEG1, Layer3, 128kbps, 44100Hz, stereo)
    # followed by 413 bytes of silence (zero-padded frame data)
    frame_header = bytes([0xFF, 0xFB, 0x90, 0x00])
    # MPEG1 Layer3 frame at 128kbps, 44100Hz = 417 bytes total (4 header + 413 data)
    frame_data = bytes(413)
    mp3_data = frame_header + frame_data

    with open(path, 'wb') as f:
        f.write(mp3_data)


def create_initial():
    # Create ~/Music directory
    os.makedirs(MUSIC_DIR, exist_ok=True)
    print(f'Created directory: {MUSIC_DIR}')

    # Create MP3 files with NO metadata tags
    for filename in MP3_FILES:
        filepath = os.path.join(MUSIC_DIR, filename)
        create_minimal_mp3(filepath)
        print(f'Created MP3 (no tags): {filepath}')

    # Verify no ID3 tags exist on any file
    try:
        from mutagen.id3 import ID3, ID3NoHeaderError
        for filename in MP3_FILES:
            filepath = os.path.join(MUSIC_DIR, filename)
            try:
                tags = ID3(filepath)
                # If we get here, tags exist — strip them
                tags.delete(filepath)
                print(f'Stripped existing tags from: {filepath}')
            except ID3NoHeaderError:
                pass  # Good — no tags
    except ImportError:
        pass  # mutagen not available on VM, files are already tag-free

    print('All MP3 files created without ID3 metadata tags.')

    # GUI-ready startup: Open Nautilus (File Manager) showing ~/Music folder
    launch_gui(f'nautilus "{MUSIC_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus file manager showing ~/Music with DISPLAY=:0')


create_initial()
