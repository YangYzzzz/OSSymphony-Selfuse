"""
Initial Setup: Open VLC with Media Library not configured with any custom paths.
Task ID: vlc_playlist_040
Domain: vlc
"""

import os
import re
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vlc_playlist_040'
VLCRC_PATH = os.path.expanduser('~/.config/vlc/vlcrc')
ML_XSPF_PATH = os.path.expanduser('~/.local/share/vlc/ml.xspf')


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


def create_sample_media():
    """Create sample media files in ~/Music/ and ~/Videos/ directories."""
    music_dir = os.path.join(WORKDIR, 'Music')
    videos_dir = os.path.join(WORKDIR, 'Videos')
    os.makedirs(music_dir, exist_ok=True)
    os.makedirs(videos_dir, exist_ok=True)

    # Create sample MP3 files in Music/
    for name, duration in [('jazz_evening.mp3', '3'), ('morning_blues.mp3', '4'), ('acoustic_sunset.mp3', '5')]:
        path = os.path.join(music_dir, name)
        if not os.path.exists(path):
            subprocess.run([
                'ffmpeg', '-y', '-f', 'lavfi', '-i', f'anullsrc=r=44100:cl=mono',
                '-t', duration, '-q:a', '9', path
            ], capture_output=True)

    # Create sample MP4 files in Videos/
    for name, duration, color in [('travel_vlog.mp4', '3', 'blue'), ('cooking_tutorial.mp4', '4', 'green')]:
        path = os.path.join(videos_dir, name)
        if not os.path.exists(path):
            subprocess.run([
                'ffmpeg', '-y', '-f', 'lavfi', '-i',
                f'color=c={color}:size=320x240:duration={duration}:rate=24',
                '-f', 'lavfi', '-i', f'anullsrc=r=44100:cl=mono',
                '-t', duration, '-pix_fmt', 'yuv420p',
                '-shortest', path
            ], capture_output=True)

    print(f'Sample media created in {music_dir} and {videos_dir}')


def ensure_clean_media_library():
    """Ensure VLC Media Library has no custom scan directories configured."""
    # Kill VLC first so vlcrc changes stick
    subprocess.run(['pkill', '-f', 'vlc'], capture_output=True)
    time.sleep(2)

    # Make sure media-library is at default (disabled / commented out) in vlcrc
    if os.path.exists(VLCRC_PATH):
        with open(VLCRC_PATH, 'r') as f:
            content = f.read()
        # Ensure media-library is commented out (default = disabled)
        content = re.sub(r'^media-library=.*$', '#media-library=0', content, flags=re.MULTILINE)
        with open(VLCRC_PATH, 'w') as f:
            f.write(content)

    # Reset ml.xspf to empty (no tracked media)
    ml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<playlist xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/" version="1">
\t<title>Media Library</title>
\t<trackList>
\t</trackList>
\t<extension application="http://www.videolan.org/vlc/playlist/0">
\t</extension>
</playlist>'''
    os.makedirs(os.path.dirname(ML_XSPF_PATH), exist_ok=True)
    with open(ML_XSPF_PATH, 'w') as f:
        f.write(ml_content)

    print('Media Library reset to clean state (no custom scan directories)')


def main():
    create_sample_media()
    ensure_clean_media_library()

    # Launch VLC (empty, no file) for the agent to interact with
    launch_gui('vlc', delay_sec=3.0)
    print('GUI_READY: launched VLC with DISPLAY=:0')


main()
