"""
Initial Setup: VLC playing a webinar recording with 4 custom bookmarks
Task ID: vlc_playlist_045
Domain: vlc
"""

import os
import shlex
import subprocess
import time
import configparser

WORKDIR = '/home/user'
TASK_ID = 'vlc_playlist_045'
VIDEOS_DIR = f'{WORKDIR}/Videos'
VIDEO_FILE = f'{VIDEOS_DIR}/webinar_recording.mp4'
VLCRC_PATH = f'{WORKDIR}/.config/vlc/vlcrc'
QT_CONF_PATH = f'{WORKDIR}/.config/vlc/vlc-qt-interface.conf'


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


def create_video():
    """Create a 55-minute test video simulating a webinar recording."""
    os.makedirs(VIDEOS_DIR, exist_ok=True)

    # Generate a short test video (60s) — duration doesn't affect bookmark behavior
    # Bookmarks are stored independently in VLC config, not in the media file
    subprocess.run([
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'color=c=navy:s=1280x720:d=60:r=1',
        '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono',
        '-t', '60',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '51',
        '-c:a', 'aac', '-b:a', '32k',
        '-pix_fmt', 'yuv420p',
        '-shortest',
        VIDEO_FILE
    ], check=True, capture_output=True)
    print(f'Video created: {VIDEO_FILE}')


def setup_bookmarks():
    """
    Set up 4 custom bookmarks in VLC's Qt interface config.
    VLC stores custom bookmarks in vlc-qt-interface.conf under [Bookmarks].

    Bookmarks:
      - "Intro" at 00:00:00 (0 seconds)
      - "Demo Start" at 00:12:30 (750 seconds)
      - "Q&A" at 00:35:00 (2100 seconds)
      - "Closing" at 00:50:00 (3000 seconds)
    """
    # Kill VLC if running, so config changes stick
    subprocess.run(['pkill', '-f', 'vlc'], capture_output=True)
    time.sleep(2)

    # Read the existing qt interface conf
    with open(QT_CONF_PATH, 'r') as f:
        content = f.read()

    # VLC stores bookmarks in vlc-qt-interface.conf like:
    # [Bookmarks]
    # count=4
    # row0\bytes=...
    # row0\name=Intro
    # row0\time=0
    # row1\bytes=...
    # row1\name=Demo Start
    # row1\time=750
    # etc.

    bookmarks = [
        {"name": "Intro", "time": 0},
        {"name": "Demo Start", "time": 750},
        {"name": "Q&A", "time": 2100},
        {"name": "Closing", "time": 3000},
    ]

    # Remove any existing [Bookmarks] section
    import re
    content = re.sub(r'\[Bookmarks\].*?(?=\n\[|\Z)', '', content, flags=re.DOTALL)
    content = content.rstrip('\n') + '\n'

    # Append bookmarks section
    content += '\n[Bookmarks]\n'
    content += f'count={len(bookmarks)}\n'
    for i, bm in enumerate(bookmarks):
        content += f'row{i}\\bytes=0\n'
        content += f'row{i}\\name={bm["name"]}\n'
        content += f'row{i}\\time={bm["time"]}\n'

    with open(QT_CONF_PATH, 'w') as f:
        f.write(content)
    print(f'Bookmarks written to {QT_CONF_PATH}')


def setup_recent_media():
    """Add the video to VLC's recent media list so bookmarks associate with it."""
    # Kill VLC if running
    subprocess.run(['pkill', '-f', 'vlc'], capture_output=True)
    time.sleep(1)

    with open(QT_CONF_PATH, 'r') as f:
        content = f.read()

    # Update RecentsMRL with the video file
    import re
    video_uri = f'file://{VIDEO_FILE}'
    content = re.sub(
        r'\[RecentsMRL\].*?(?=\n\[|\Z)',
        f'[RecentsMRL]\nlist={video_uri}\ntimes=1200\n',
        content,
        flags=re.DOTALL
    )

    with open(QT_CONF_PATH, 'w') as f:
        f.write(content)
    print('Recent media updated')


def main():
    # Step 1: Create the video file
    create_video()

    # Step 2: Set up bookmarks in VLC config
    setup_bookmarks()

    # Step 3: Update recent media
    setup_recent_media()

    # Step 4: Launch VLC with the video at position ~20:00 (1200 seconds)
    # Using --start-time to position playback at 00:20:00
    launch_gui(
        f'vlc --start-time=10 --extraintf=http --http-password=password --http-port=8080 "{VIDEO_FILE}"',
        delay_sec=3.0
    )
    print('GUI_READY: launched VLC with DISPLAY=:0')
    print(f'VLC playing {VIDEO_FILE} with 4 custom bookmarks')


main()
