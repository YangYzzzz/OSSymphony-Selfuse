"""
Initial Setup: Build review playlist from multiple project folders
Task ID: vlc_playlist_061
Domain: vlc

Creates test MP4 files in ~/Videos/Project_A/finals/ and ~/Videos/Project_B/finals/,
then launches VLC with an empty playlist.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vlc_playlist_061'

# Directory structure
PROJECT_A_DIR = os.path.join(WORKDIR, 'Videos', 'Project_A', 'finals')
PROJECT_B_DIR = os.path.join(WORKDIR, 'Videos', 'Project_B', 'finals')

# Files to create
PROJECT_A_FILES = ['scene1_final.mp4', 'scene2_final.mp4', 'scene3_final.mp4']
PROJECT_B_FILES = ['intro_final.mp4', 'outro_final.mp4']


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


def create_test_video(path, duration=3, color='blue'):
    """Create a short test MP4 video using ffmpeg."""
    color_map = {
        'blue': '0x0000FF',
        'red': '0xFF0000',
        'green': '0x00FF00',
        'yellow': '0xFFFF00',
        'cyan': '0x00FFFF',
    }
    hex_color = color_map.get(color, '0x0000FF')
    subprocess.run([
        'ffmpeg', '-y', '-f', 'lavfi', '-i',
        f'color=c={hex_color}:s=320x240:d={duration}:r=24',
        '-pix_fmt', 'yuv420p',
        '-an',
        path
    ], check=True, capture_output=True)


def create_initial():
    # Create directory structure
    os.makedirs(PROJECT_A_DIR, exist_ok=True)
    os.makedirs(PROJECT_B_DIR, exist_ok=True)

    # Create test video files in Project_A/finals/
    colors_a = ['blue', 'red', 'green']
    for i, fname in enumerate(PROJECT_A_FILES):
        fpath = os.path.join(PROJECT_A_DIR, fname)
        if not os.path.exists(fpath):
            create_test_video(fpath, duration=3, color=colors_a[i])
            print(f'Created: {fpath}')

    # Create test video files in Project_B/finals/
    colors_b = ['yellow', 'cyan']
    for i, fname in enumerate(PROJECT_B_FILES):
        fpath = os.path.join(PROJECT_B_DIR, fname)
        if not os.path.exists(fpath):
            create_test_video(fpath, duration=3, color=colors_b[i])
            print(f'Created: {fpath}')

    # Ensure no pre-existing playlist file
    playlist_path = os.path.join(WORKDIR, 'Videos', 'review_queue.xspf')
    if os.path.exists(playlist_path):
        os.remove(playlist_path)
        print(f'Removed pre-existing playlist: {playlist_path}')

    # Kill any running VLC
    subprocess.run(['pkill', '-f', 'vlc'], capture_output=True)
    time.sleep(2)

    # Launch VLC with empty playlist
    launch_gui('vlc', delay_sec=3.0)
    print('GUI_READY: VLC launched with empty playlist on DISPLAY=:0')


create_initial()
