"""
Initial Setup: Take three snapshots from the concert video at timestamps 1:00, 2:00, and 3:00
Task ID: vlcplay_016
Domain: vlc

Creates:
- /home/user/Videos/concert.mp4 (a ~4-minute test video with changing visuals)
- /home/user/Pictures/Snapshots/ directory (empty, ready for agent to save snapshots)
- Launches VLC playing the concert video at 0:00
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vlcplay_016'
VIDEO_DIR = f'{WORKDIR}/Videos'
VIDEO_PATH = f'{VIDEO_DIR}/concert.mp4'
SNAPSHOT_DIR = f'{WORKDIR}/Pictures/Snapshots'


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
    # Ensure directories exist
    os.makedirs(VIDEO_DIR, exist_ok=True)
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    os.makedirs(f'{WORKDIR}/Pictures', exist_ok=True)

    # Generate a ~4-minute concert-like test video with changing colors and audio
    # Using testsrc2 for visual variety at different timestamps, plus sine wave audio
    # Duration: 240 seconds (4 minutes) to cover timestamps 1:00, 2:00, 3:00
    if not os.path.exists(VIDEO_PATH):
        subprocess.run([
            "ffmpeg", "-y",
            "-f", "lavfi", "-i",
            "testsrc2=duration=240:size=1280x720:rate=24",
            "-f", "lavfi", "-i",
            "sine=frequency=440:duration=240",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "28",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            VIDEO_PATH
        ], check=True, capture_output=True)
    print(f'Video created: {VIDEO_PATH}')

    # Verify snapshot directory is empty (no pre-existing snapshots)
    for f in os.listdir(SNAPSHOT_DIR):
        os.remove(os.path.join(SNAPSHOT_DIR, f))
    print(f'Snapshot directory ready (empty): {SNAPSHOT_DIR}')

    # Launch VLC playing the concert video
    launch_gui(f'vlc --no-video-title-show "{VIDEO_PATH}"', delay_sec=3.0)
    print('GUI_READY: VLC launched with concert.mp4 on DISPLAY=:0')


create_initial()
