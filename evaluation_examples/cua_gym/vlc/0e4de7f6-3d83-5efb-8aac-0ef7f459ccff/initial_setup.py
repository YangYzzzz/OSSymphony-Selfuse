"""
Initial Setup: Add directories to VLC's Media Library scan list
Task ID: vlc_playlist_078
Domain: vlc

Creates three directories with media content, enables media library in vlcrc,
and launches VLC with default (empty) media library scan paths.
"""

import os
import re
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vlc_playlist_078'
VLCRC_PATH = os.path.expanduser("~/.config/vlc/vlcrc")
ML_XSPF_PATH = os.path.expanduser("~/.local/share/vlc/ml.xspf")

# Directories to create with media content
DIRS = [
    os.path.join(WORKDIR, "Music", "Albums"),
    os.path.join(WORKDIR, "Music", "Singles"),
    os.path.join(WORKDIR, "Videos", "Music_Videos"),
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


def create_directories_with_content():
    """Create the three directories and populate them with small audio/video files."""
    for d in DIRS:
        os.makedirs(d, exist_ok=True)

    # Create small silent audio files using ffmpeg
    audio_files = [
        (os.path.join(WORKDIR, "Music", "Albums", "track01_sunrise.mp3"), "5"),
        (os.path.join(WORKDIR, "Music", "Albums", "track02_moonlight.mp3"), "4"),
        (os.path.join(WORKDIR, "Music", "Albums", "track03_starfall.mp3"), "3"),
        (os.path.join(WORKDIR, "Music", "Singles", "single_summer_breeze.mp3"), "5"),
        (os.path.join(WORKDIR, "Music", "Singles", "single_winter_chill.mp3"), "4"),
    ]

    video_files = [
        (os.path.join(WORKDIR, "Videos", "Music_Videos", "sunrise_official_mv.mp4"), "3"),
        (os.path.join(WORKDIR, "Videos", "Music_Videos", "moonlight_live_session.mp4"), "3"),
    ]

    for filepath, duration in audio_files:
        if not os.path.exists(filepath):
            subprocess.run([
                "ffmpeg", "-y", "-f", "lavfi", "-i",
                f"anullsrc=r=44100:cl=mono",
                "-t", duration, "-q:a", "9", filepath
            ], capture_output=True)

    for filepath, duration in video_files:
        if not os.path.exists(filepath):
            subprocess.run([
                "ffmpeg", "-y", "-f", "lavfi", "-i",
                f"testsrc=duration={duration}:size=320x240:rate=15",
                "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=mono",
                "-t", duration, "-pix_fmt", "yuv420p",
                "-shortest", filepath
            ], capture_output=True)

    print("Created directories and media content:")
    for d in DIRS:
        files = os.listdir(d)
        print(f"  {d}: {files}")


def reset_media_library():
    """Ensure media library is empty (no custom scan paths) - the initial state."""
    # Reset ml.xspf to empty
    ml_dir = os.path.dirname(ML_XSPF_PATH)
    os.makedirs(ml_dir, exist_ok=True)
    with open(ML_XSPF_PATH, 'w') as f:
        f.write("""<?xml version="1.0" encoding="UTF-8"?>
<playlist xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/" version="1">
\t<title>Media Library</title>
\t<trackList>
\t</trackList>
\t<extension application="http://www.videolan.org/vlc/playlist/0">
\t</extension>
</playlist>""")
    print(f"Reset {ML_XSPF_PATH} to empty media library")


def setup_vlcrc():
    """Ensure vlcrc has media-library enabled but NO custom scan paths."""
    # Kill VLC first to avoid it overwriting our changes
    subprocess.run(["pkill", "-f", "vlc"], capture_output=True)
    time.sleep(2)

    with open(VLCRC_PATH, "r") as f:
        content = f.read()

    # Enable media-library
    pattern = re.compile(r'^(#?\s*)media-library=.*$', re.MULTILINE)
    if pattern.search(content):
        content = pattern.sub('media-library=1', content)
    else:
        content += '\nmedia-library=1\n'

    with open(VLCRC_PATH, "w") as f:
        f.write(content)
    print("vlcrc: media-library enabled, no custom scan paths set")


def main():
    create_directories_with_content()

    # Kill VLC before modifying config (bitter lesson #1)
    subprocess.run(["pkill", "-f", "vlc"], capture_output=True)
    time.sleep(2)

    setup_vlcrc()
    reset_media_library()

    # Launch VLC
    launch_gui('vlc', delay_sec=2.0)
    print('GUI_READY: launched VLC with DISPLAY=:0')


main()
