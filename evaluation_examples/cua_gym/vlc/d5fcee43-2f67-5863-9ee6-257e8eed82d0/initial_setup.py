"""
Initial Setup: Create source MP4 video file for ffmpeg conversion task.
Task ID: vlcconv_007
Domain: vlc
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vlcconv_007'
VIDEOS_DIR = f'{WORKDIR}/Videos'
SOURCE_FILE = f'{VIDEOS_DIR}/Travel_Vlog_Paris.mp4'


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
    # Ensure Videos directory exists
    os.makedirs(VIDEOS_DIR, exist_ok=True)

    # Ensure Desktop exists
    os.makedirs(f'{WORKDIR}/Desktop', exist_ok=True)

    # Remove any pre-existing AVI on Desktop (must NOT be there initially)
    avi_path = f'{WORKDIR}/Desktop/Travel_Vlog_Paris.avi'
    if os.path.exists(avi_path):
        os.remove(avi_path)

    # Generate a realistic ~12-second 1080p test video with audio
    # Using ffmpeg lavfi sources: color bars video + sine wave audio
    # This simulates a travel vlog video at 1080p H.264 + AAC
    subprocess.run([
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i',
        'testsrc2=duration=12:size=1920x1080:rate=30',
        '-f', 'lavfi', '-i',
        'sine=frequency=440:duration=12',
        '-c:v', 'libx264', '-preset', 'ultrafast',
        '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '128k',
        '-shortest',
        SOURCE_FILE
    ], check=True, capture_output=True)

    print(f'Source video created: {SOURCE_FILE}')

    # Verify the file
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries',
         'stream=codec_name,width,height,codec_type',
         '-of', 'default=noprint_wrappers=1', SOURCE_FILE],
        capture_output=True, text=True
    )
    print(f'Source video info:\n{result.stdout}')

    # Open a terminal for the user (the task says to use ffmpeg from terminal)
    launch_gui('bash -c "cd /home/user && xfce4-terminal"', delay_sec=2.0)
    print('GUI_READY: launched terminal with DISPLAY=:0')


create_initial()
