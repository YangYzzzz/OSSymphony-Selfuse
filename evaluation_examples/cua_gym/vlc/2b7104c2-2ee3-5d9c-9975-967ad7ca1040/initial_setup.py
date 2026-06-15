"""
Initial Setup: Content creator project handoff playlist
Task ID: vlc_playlist_080
Domain: vlc

Creates 8 video files in ~/Videos/Final_Delivery/, then launches VLC
with an empty playlist. Shuffle off, repeat off.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vlc_playlist_080'
DELIVERY_DIR = f'{WORKDIR}/Videos/Final_Delivery'

VIDEO_FILES = [
    '01_opening.mp4',
    '02_brand_intro.mp4',
    '03_product_demo.mp4',
    '04_testimonials.mp4',
    '05_features.mp4',
    '06_pricing.mp4',
    '07_call_to_action.mp4',
    '08_credits.mp4',
]


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
    # Kill any running VLC first
    subprocess.run(["pkill", "-f", "vlc"], capture_output=True)
    time.sleep(2)

    # Create delivery directory
    os.makedirs(DELIVERY_DIR, exist_ok=True)

    # Generate 8 short test video files using ffmpeg
    for i, fname in enumerate(VIDEO_FILES):
        filepath = os.path.join(DELIVERY_DIR, fname)
        if not os.path.exists(filepath):
            # Create a 3-second color test video with unique color per file
            hue = i * 30  # Different color for each file
            subprocess.run([
                "ffmpeg", "-y",
                "-f", "lavfi",
                "-i", f"color=c=0x{(hue*17)%256:02x}{(hue*7+50)%256:02x}{(hue*13+100)%256:02x}:size=320x240:duration=3:rate=24",
                "-f", "lavfi",
                "-i", "anullsrc=r=44100:cl=mono",
                "-t", "3",
                "-pix_fmt", "yuv420p",
                "-shortest",
                filepath
            ], capture_output=True, check=True)
            print(f'Created: {filepath}')

    # Ensure no playlist files exist in initial state
    for pf in ['delivery_manifest.m3u', 'delivery_manifest.xspf']:
        path = os.path.join(DELIVERY_DIR, pf)
        if os.path.exists(path):
            os.remove(path)

    # Launch VLC with empty playlist (no files loaded)
    # Use --no-loop and --no-random to ensure repeat off, shuffle off
    launch_gui('vlc --no-loop --no-random --no-repeat', delay_sec=3.0)
    print(f'Initial state ready: 8 video files in {DELIVERY_DIR}')
    print('GUI_READY: launched VLC with empty playlist, DISPLAY=:0')


create_initial()
