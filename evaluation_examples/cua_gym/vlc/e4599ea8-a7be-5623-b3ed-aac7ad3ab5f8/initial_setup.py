"""
Initial Setup: Configure VLC to stop after current file with episode files
Task ID: vlc_playlist_053
Domain: vlc
"""

import os
import re
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vlc_playlist_053'
VLCRC_PATH = os.path.expanduser("~/.config/vlc/vlcrc")
VIDEOS_DIR = os.path.join(WORKDIR, 'Videos', 'series')


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


def set_vlcrc_option(key: str, value: str):
    """Set a vlcrc option. Uncomments the key if commented out."""
    with open(VLCRC_PATH, "r") as f:
        content = f.read()
    pattern = re.compile(rf'^(#?\s*){re.escape(key)}=.*$', re.MULTILINE)
    replacement = f'{key}={value}'
    if pattern.search(content):
        content = pattern.sub(replacement, content)
    else:
        content += f'\n{key}={value}\n'
    with open(VLCRC_PATH, "w") as f:
        f.write(content)


def create_episode_files():
    """Create 10 test episode video files."""
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    for i in range(1, 11):
        ep_path = os.path.join(VIDEOS_DIR, f'episode_{i:02d}.mp4')
        if not os.path.exists(ep_path):
            # Generate a short 3-second test video with episode number overlay
            subprocess.run([
                'ffmpeg', '-y',
                '-f', 'lavfi',
                '-i', f'testsrc=duration=3:size=640x480:rate=24',
                '-f', 'lavfi',
                '-i', 'anullsrc=r=44100:cl=mono',
                '-t', '3',
                '-vf', f"drawtext=text='Episode {i:02d}':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2",
                '-pix_fmt', 'yuv420p',
                '-shortest',
                ep_path
            ], capture_output=True)
    print(f'Created episode files in {VIDEOS_DIR}')


def configure_vlc_stop_after_current():
    """Configure VLC to stop after current file (initial state)."""
    # Kill VLC first to safely edit vlcrc
    subprocess.run(["pkill", "-f", "vlc"], capture_output=True)
    time.sleep(2)

    # Set play-and-stop=1 so VLC stops after the current file
    set_vlcrc_option("play-and-stop", "1")
    # Ensure playlist-autostart is on (default) but play-and-stop overrides it
    set_vlcrc_option("playlist-autostart", "1")
    # Ensure no looping
    set_vlcrc_option("loop", "0")
    set_vlcrc_option("repeat", "0")
    print('Configured VLC: play-and-stop=1 (stop after current file)')


def main():
    # Step 1: Create episode files
    create_episode_files()

    # Step 2: Configure VLC to stop after current file
    configure_vlc_stop_after_current()

    # Step 3: Launch VLC with only episode_01.mp4 (not the whole directory)
    ep1_path = os.path.join(VIDEOS_DIR, 'episode_01.mp4')
    launch_gui(f'vlc "{ep1_path}"', delay_sec=3.0)
    print(f'GUI_READY: VLC launched with {ep1_path} on DISPLAY=:0')


main()
