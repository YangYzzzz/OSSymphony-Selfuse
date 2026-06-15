"""
Initial Setup: Extract audio from Concert_Live_2025.mp4 as OGG Vorbis
Task ID: vlcconv_005
Domain: vlc

Creates a test MP4 video with audio at ~/Videos/Concert_Live_2025.mp4
and opens it in VLC.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vlcconv_005'
VIDEOS_DIR = f'{WORKDIR}/Videos'
SOURCE_FILE = f'{VIDEOS_DIR}/Concert_Live_2025.mp4'


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
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    os.makedirs(f'{WORKDIR}/Desktop', exist_ok=True)

    # Generate a test MP4 with both video and audio tracks (~30 seconds for testing)
    # Using ffmpeg to create a test video with color bars + sine wave audio
    subprocess.run([
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'testsrc=duration=30:size=1920x1080:rate=30',
        '-f', 'lavfi', '-i', 'sine=frequency=440:duration=30',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '128k',
        '-shortest',
        SOURCE_FILE
    ], check=True, capture_output=True)
    print(f'Source video created: {SOURCE_FILE}')

    # Verify the file was created
    file_size = os.path.getsize(SOURCE_FILE)
    print(f'File size: {file_size} bytes')

    # Launch VLC with the source file
    launch_gui(f'vlc "{SOURCE_FILE}"', delay_sec=2.0)
    print('GUI_READY: launched VLC with DISPLAY=:0')


create_initial()
