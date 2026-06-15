"""
Initial Setup: Open VLC with no file loaded (splash screen only).
Task ID: vlcplay_009
Domain: vlc

Creates a test video file at /home/user/Videos/tutorial.avi,
then launches VLC without any file (showing the cone splash screen).
VLC is started with HTTP interface enabled for status verification.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vlcplay_009'
VIDEO_DIR = f'{WORKDIR}/Videos'
VIDEO_FILE = f'{VIDEO_DIR}/tutorial.avi'


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
    # Ensure Videos directory exists
    os.makedirs(VIDEO_DIR, exist_ok=True)

    # Generate a test video file (10 seconds, 640x480, with audio)
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "testsrc=duration=10:size=640x480:rate=25",
        "-f", "lavfi", "-i", "sine=frequency=440:duration=10",
        "-c:v", "libxvid", "-c:a", "libmp3lame",
        "-pix_fmt", "yuv420p",
        VIDEO_FILE
    ], check=True, capture_output=True)
    print(f'Video file created: {VIDEO_FILE}')

    # Kill any running VLC instance first
    subprocess.run(["pkill", "-f", "vlc"], capture_output=True)
    time.sleep(2)

    # Launch VLC with NO file (splash screen only), with HTTP interface for verification
    launch_gui(
        'vlc --extraintf=http --http-password=password --http-port=8080',
        delay_sec=3.0
    )
    print('GUI_READY: VLC launched with splash screen (no file loaded) with DISPLAY=:0')


create_initial()
