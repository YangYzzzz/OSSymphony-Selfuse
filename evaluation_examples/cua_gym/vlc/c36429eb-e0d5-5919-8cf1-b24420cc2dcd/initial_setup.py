"""
Initial Setup: VLC playing video at normal speed (1.0x)
Task ID: vlcplay_004
Domain: vlc

Creates a test video at /home/user/Videos/tutorial.avi,
launches VLC with HTTP interface at normal speed, seeks to ~0:30.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vlcplay_004'
VIDEO_DIR = f'{WORKDIR}/Videos'
VIDEO_PATH = f'{VIDEO_DIR}/tutorial.avi'


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
    # Kill any existing VLC instances
    subprocess.run(["pkill", "-f", "vlc"], capture_output=True)
    time.sleep(2)

    # Create Videos directory
    os.makedirs(VIDEO_DIR, exist_ok=True)

    # Generate a 600-second test video (tutorial-style with color bars)
    # Long duration prevents video from finishing during evaluation
    # Force regenerate to ensure correct duration
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", "testsrc=duration=600:size=640x480:rate=25",
        "-f", "lavfi",
        "-i", "sine=frequency=440:duration=600:sample_rate=44100",
        "-c:v", "libxvid", "-q:v", "5",
        "-c:a", "libmp3lame", "-b:a", "128k",
        VIDEO_PATH,
    ], check=True, capture_output=True)
    print(f"Video created: {VIDEO_PATH}")

    # Launch VLC with HTTP interface enabled, starting at 30 seconds, normal speed
    launch_gui(
        f'vlc --extraintf=http --http-password=password --http-port=8080 '
        f'--start-time=30 --no-video-title-show '
        f'"{VIDEO_PATH}"',
        delay_sec=4.0,
    )
    print("GUI_READY: VLC launched with DISPLAY=:0, playing tutorial.avi at 0:30, 1.0x speed")


create_initial()
