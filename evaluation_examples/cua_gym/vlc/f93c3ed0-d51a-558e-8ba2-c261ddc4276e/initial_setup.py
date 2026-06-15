"""
Initial Setup: Add media files to VLC and rearrange playlist
Task ID: vlc_playlist_076
Domain: vlc

Creates ~/Music/Morning_Routine/ with 5 MP3 files and launches VLC with empty playlist.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vlc_playlist_076'
MUSIC_DIR = f'{WORKDIR}/Music/Morning_Routine'

TRACKS = [
    'alarm_tone.mp3',
    'yoga_flow.mp3',
    'breakfast_jazz.mp3',
    'meditation.mp3',
    'news_briefing.mp3',
]


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    env["VLC_VERBOSE"] = "-1"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # Create music directory
    os.makedirs(MUSIC_DIR, exist_ok=True)

    # Generate 5 distinct silent MP3 files with slightly different durations
    # so they are distinguishable
    durations = {
        'alarm_tone.mp3': 3,
        'yoga_flow.mp3': 5,
        'breakfast_jazz.mp3': 4,
        'meditation.mp3': 6,
        'news_briefing.mp3': 4,
    }

    for track in TRACKS:
        filepath = os.path.join(MUSIC_DIR, track)
        dur = durations[track]
        # Generate a silent mp3 with a unique duration
        subprocess.run([
            'ffmpeg', '-y', '-f', 'lavfi', '-i',
            f'anullsrc=r=44100:cl=mono',
            '-t', str(dur), '-q:a', '9',
            filepath
        ], check=True, capture_output=True)
        print(f'Created: {filepath}')

    # Kill any existing VLC
    subprocess.run(['pkill', '-f', 'vlc'], capture_output=True)
    time.sleep(2)

    # Launch VLC with empty playlist and HTTP interface enabled
    launch_gui('vlc --extraintf=http --http-password=password', delay_sec=3.0)
    print('GUI_READY: VLC launched with empty playlist and DISPLAY=:0')


create_initial()
