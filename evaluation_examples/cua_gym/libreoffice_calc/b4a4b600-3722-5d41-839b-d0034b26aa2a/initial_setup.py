"""
Initial Setup: MP3 files with blank metadata in ~/Music/Podcasts
Task ID: osworld_multi_apps_misc_027
Domain: os (MP3 ID3 tag manipulation)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PODCASTS_DIR = f'{WORKDIR}/Music/Podcasts'

# The six MP3 filenames (no ID3 tags initially)
MP3_FILES = [
    'Lex Fridman Podcast - Episode 300.mp3',
    'The Joe Rogan Experience - Episode 2000.mp3',
    'Huberman Lab - Sleep Toolkit.mp3',
    'How I Built This - Airbnb.mp3',
    'Hidden Brain - The Optimism Bias.mp3',
    'Radiolab - Darkode.mp3',
]

# Minimal valid MP3 file: ID3v2.3 header with no frames + silent MPEG audio frame
# This is a tiny but valid MP3 binary (ID3 header + one silent MPEG frame)
# ID3v2 header: "ID3" + version 2.3.0 + flags 0x00 + size 0 (syncsafe)
# followed by a minimal silent MPEG audio frame
MINIMAL_MP3_BYTES = bytes([
    # ID3v2.3 header (no frames, size=0)
    0x49, 0x44, 0x33,  # "ID3"
    0x03, 0x00,        # version 2.3, revision 0
    0x00,              # flags
    0x00, 0x00, 0x00, 0x00,  # size = 0 (syncsafe integer)
    # MPEG Layer 3 silent frame header: 0xFFFA (MPEG1, Layer3, 128kbps, 44100Hz, stereo)
    0xFF, 0xFB, 0x90, 0x00,
    # Zero-padded silent audio data (417 bytes for 128kbps frame at 44100Hz)
] + [0x00] * 413)


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


def create_initial():
    # Create the Podcasts directory
    os.makedirs(PODCASTS_DIR, exist_ok=True)
    print(f'Created directory: {PODCASTS_DIR}')

    for filename in MP3_FILES:
        filepath = os.path.join(PODCASTS_DIR, filename)
        # Write minimal MP3 file with NO ID3 tags
        # We write a plain file with no tags at all
        with open(filepath, 'wb') as f:
            f.write(MINIMAL_MP3_BYTES)
        print(f'Created: {filepath}')

    # Verify: use python mutagen to strip any accidentally created tags
    try:
        from mutagen.id3 import ID3NoHeaderError
        from mutagen.mp3 import MP3
        for filename in MP3_FILES:
            filepath = os.path.join(PODCASTS_DIR, filename)
            try:
                from mutagen.id3 import ID3
                tags = ID3(filepath)
                # If tags exist, delete them all
                tags.delete(filepath)
                print(f'Cleared existing tags from: {filename}')
            except ID3NoHeaderError:
                pass  # No tags — exactly what we want
    except ImportError:
        print('mutagen not available for tag verification; files written without tags')

    print(f'\nInitial state created:')
    print(f'  Directory: {PODCASTS_DIR}')
    print(f'  Files: {len(MP3_FILES)} MP3 files with no ID3 tags')

    # GUI-ready startup: open Nautilus file manager at the Podcasts directory
    launch_gui(f'nautilus "{PODCASTS_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus at Podcasts directory with DISPLAY=:0')


create_initial()
