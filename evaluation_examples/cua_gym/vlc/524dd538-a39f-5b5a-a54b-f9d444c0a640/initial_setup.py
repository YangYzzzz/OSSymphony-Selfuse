"""
Initial Setup: Extract audio from MP4 using VLC CLI
Task ID: vlcconv_015
Domain: vlc

Creates a realistic MP4 video file with H.264+AAC audio at ~/Videos/
and opens a terminal for the agent to use cvlc for audio extraction.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vlcconv_015'
VIDEO_DIR = f'{WORKDIR}/Videos'
VIDEO_FILE = f'{VIDEO_DIR}/Lecture_History_Ep7.mp4'


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
    os.makedirs(VIDEO_DIR, exist_ok=True)

    # Ensure output directory does NOT exist (negative constraint)
    output_dir = f'{WORKDIR}/Documents/Lecture_Audio'
    if os.path.exists(output_dir):
        import shutil
        shutil.rmtree(output_dir)

    # Generate a realistic MP4 test video with audio (~30 seconds, 720p, H.264+AAC)
    # Using ffmpeg to create a video with test pattern and sine wave audio
    # We make it 30s to keep it manageable but enough to verify conversion
    subprocess.run([
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'testsrc=duration=30:size=1280x720:rate=30',
        '-f', 'lavfi', '-i', 'sine=frequency=440:duration=30',
        '-c:v', 'libx264', '-preset', 'fast', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '128k',
        '-shortest',
        VIDEO_FILE
    ], check=True, capture_output=True)

    print(f'Source video created: {VIDEO_FILE}')

    # Verify the file exists and has reasonable size
    size = os.path.getsize(VIDEO_FILE)
    print(f'Video file size: {size} bytes')

    # Verify output directory and file do NOT exist (task precondition)
    assert not os.path.exists(output_dir), f'Output dir should not exist: {output_dir}'
    output_file = f'{output_dir}/Lecture_History_Ep7_audio.mp3'
    assert not os.path.exists(output_file), f'Output file should not exist: {output_file}'

    # Open a terminal for the agent to work with
    launch_gui('bash -c "DISPLAY=:0 gnome-terminal"', delay_sec=2.0)
    print('GUI_READY: launched terminal with DISPLAY=:0')


create_initial()
