"""
Initial Setup: VLC + GIMP multi-app task - extract clip and convert to GIF
Task ID: osworld_multi_apps_vlc_gimp_035
Domain: multi_apps (VLC + GIMP)

Creates 'animation.mp4' on the Desktop as a short animated video.
The agent must:
  1. Use VLC to extract a 5-second clip (00:05 - 00:10) from animation.mp4
  2. Import frames into GIMP
  3. Reduce color palette to 64 colors
  4. Export as 'animation_clip.gif'
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_vlc_gimp_035'
OUTPUT_VIDEO = f'{DESKTOP}/animation.mp4'


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
    # Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)

    # Remove any pre-existing animation_clip.gif (task output must not exist yet)
    clip_gif = f'{DESKTOP}/animation_clip.gif'
    if os.path.exists(clip_gif):
        os.remove(clip_gif)
        print(f'Removed pre-existing: {clip_gif}')

    # Generate animation.mp4 using ffmpeg - a colorful animated video of at least 15 seconds
    # Use testsrc2 which produces vibrant animated color patterns
    print('Generating animation.mp4 ...')
    subprocess.run([
        'ffmpeg', '-y',
        '-f', 'lavfi',
        '-i', 'testsrc2=duration=20:size=320x240:rate=10',
        '-pix_fmt', 'yuv420p',
        '-c:v', 'libx264',
        '-crf', '23',
        OUTPUT_VIDEO
    ], check=True, capture_output=True)
    print(f'Created: {OUTPUT_VIDEO}')

    # Verify the video was created
    if os.path.exists(OUTPUT_VIDEO):
        size = os.path.getsize(OUTPUT_VIDEO)
        print(f'animation.mp4 size: {size} bytes')
    else:
        raise RuntimeError('Failed to create animation.mp4')

    # GUI-ready startup: open VLC with animation.mp4
    print('Launching VLC with animation.mp4 ...')
    launch_gui(f'vlc "{OUTPUT_VIDEO}"', delay_sec=2.0)
    print('GUI_READY: launched VLC with animation.mp4 on DISPLAY=:0')


create_initial()
