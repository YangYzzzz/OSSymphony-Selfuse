"""
Initial Setup: Multi-app task - VLC frame extraction and GIMP image processing
Task ID: osworld_multi_apps_media_image_008
Domain: multi_apps (VLC + GIMP)

Creates:
  - /home/user/videos/documentary.mp4  (5-minute test video)
  - /home/user/frames/                 (empty directory)

Does NOT create: any frame_N.png, bw_N.png, or documentary_storyboard.gif
(those are the agent's task)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_media_image_008'
VIDEOS_DIR = f'{WORKDIR}/videos'
FRAMES_DIR = f'{WORKDIR}/frames'
VIDEO_PATH = f'{VIDEOS_DIR}/documentary.mp4'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # Create required directories
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    os.makedirs(FRAMES_DIR, exist_ok=True)
    print(f'Directories created: {VIDEOS_DIR}, {FRAMES_DIR}')

    # Remove any pre-existing output files to ensure clean state
    for fname in ['frame_1.png', 'frame_2.png', 'frame_3.png', 'frame_4.png', 'frame_5.png',
                  'bw_1.png', 'bw_2.png', 'bw_3.png', 'bw_4.png', 'bw_5.png',
                  'documentary_storyboard.gif']:
        fpath = os.path.join(FRAMES_DIR, fname)
        if os.path.exists(fpath):
            os.remove(fpath)
            print(f'Removed pre-existing file: {fpath}')

    # Generate a 5-minute (300 second) documentary-style test video using ffmpeg
    # Use a nature/documentary-like pattern with varied scenes using color palette
    # The video has visible scene changes to make frame extraction meaningful
    if not os.path.exists(VIDEO_PATH) or os.path.getsize(VIDEO_PATH) < 1000:
        print(f'Creating {VIDEO_PATH} ...')
        result = subprocess.run([
            'ffmpeg', '-y',
            # Generate a 300-second video with testsrc2 (more realistic looking than testsrc)
            '-f', 'lavfi',
            '-i', 'testsrc2=duration=300:size=640x480:rate=24',
            # Add silent audio track
            '-f', 'lavfi',
            '-i', 'anullsrc=r=44100:cl=stereo',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-c:a', 'aac',
            '-t', '300',
            VIDEO_PATH
        ], capture_output=True, text=True, timeout=120)

        if result.returncode != 0:
            print(f'ffmpeg error: {result.stderr[-500:]}')
            # Fallback: try simpler color video
            result2 = subprocess.run([
                'ffmpeg', '-y',
                '-f', 'lavfi',
                '-i', 'color=c=blue:duration=300:size=640x480:rate=24',
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-t', '300',
                VIDEO_PATH
            ], capture_output=True, text=True, timeout=120)
            if result2.returncode != 0:
                print(f'Fallback ffmpeg error: {result2.stderr[-500:]}')
                raise RuntimeError('Failed to create documentary.mp4')
        print(f'Video created: {VIDEO_PATH}')
    else:
        print(f'Video already exists: {VIDEO_PATH}')

    # Verify video duration is approximately 5 minutes
    probe = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1', VIDEO_PATH],
        capture_output=True, text=True
    )
    if probe.returncode == 0:
        duration = float(probe.stdout.strip())
        print(f'Video duration: {duration:.1f} seconds')
    else:
        print('Could not probe video duration (ffprobe not available)')

    # Verify frames directory is empty (no frames should exist at start)
    frames_contents = os.listdir(FRAMES_DIR)
    if frames_contents:
        print(f'WARNING: frames dir not empty: {frames_contents}')
    else:
        print(f'Frames directory is clean: {FRAMES_DIR}')

    print(f'Initial state ready:')
    print(f'  Video: {VIDEO_PATH}')
    print(f'  Frames dir (empty): {FRAMES_DIR}')

    # GUI-ready startup: open VLC with the documentary video
    launch_gui(f'vlc "{VIDEO_PATH}"', delay_sec=2.0)
    print('GUI_READY: launched VLC with documentary.mp4 (DISPLAY=:0)')


create_initial()
