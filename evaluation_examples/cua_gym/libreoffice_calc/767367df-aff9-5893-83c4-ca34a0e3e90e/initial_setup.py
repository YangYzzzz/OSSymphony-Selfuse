"""
Initial Setup: Extract 5-second clip from training_video.mp4 via VLC and convert to greyscale GIF in GIMP
Task ID: osworld_multi_apps_vlc_gimp_041
Domain: multi_apps (VLC + GIMP)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_vlc_gimp_041'
VIDEO_FILE = f'{DESKTOP}/training_video.mp4'


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

    # Create a realistic training video using ffmpeg
    # Duration: 20 seconds (enough for the 00:08 - 00:13 segment)
    # Use a colorful testsrc2 pattern that looks like a training/instructional video
    result = subprocess.run([
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", "testsrc2=duration=20:size=640x480:rate=10",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        VIDEO_FILE
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ffmpeg error: {result.stderr}")
        # Fallback: use simpler testsrc
        result2 = subprocess.run([
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", "testsrc=duration=20:size=640x480:rate=10",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            VIDEO_FILE
        ], capture_output=True, text=True)
        if result2.returncode != 0:
            print(f"Fallback ffmpeg error: {result2.stderr}")
            raise RuntimeError("Failed to create training_video.mp4")

    print(f"Video file created: {VIDEO_FILE}")

    # Verify the video was created and has sufficient duration
    probe = subprocess.run([
        "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", VIDEO_FILE
    ], capture_output=True, text=True)
    if probe.returncode == 0:
        print(f"Video duration: {probe.stdout.strip()} seconds")

    # GUI-ready startup: Open VLC with the training video and open GIMP
    # Open VLC with the training video file
    launch_gui(f'vlc "{VIDEO_FILE}"', delay_sec=2.0)

    # Open GIMP (without a specific file, ready for import)
    launch_gui('gimp', delay_sec=2.0)

    print('GUI_READY: launched VLC and GIMP with DISPLAY=:0')


create_initial()
