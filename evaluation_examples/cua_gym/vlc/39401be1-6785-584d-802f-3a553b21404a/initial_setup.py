"""
Initial Setup: VLC playlist with 3 local tracks, playback stopped.
Task ID: vlc_playlist_047
Domain: vlc
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vlc_playlist_047'

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

    # Create 3 short silent MP3 files as local tracks
    tracks = ["local_song1.mp3", "local_song2.mp3", "local_song3.mp3"]
    for track in tracks:
        track_path = os.path.join(WORKDIR, track)
        if not os.path.exists(track_path):
            subprocess.run([
                "ffmpeg", "-y", "-f", "lavfi",
                "-i", "anullsrc=r=44100:cl=mono",
                "-t", "3", "-q:a", "9",
                track_path
            ], capture_output=True, check=True)
            print(f"Created: {track_path}")

    # Create an M3U playlist with the 3 local tracks
    playlist_path = os.path.join(WORKDIR, f"{TASK_ID}.m3u")
    with open(playlist_path, "w") as f:
        f.write("#EXTM3U\n")
        for track in tracks:
            f.write(f"#EXTINF:3,{track}\n")
            f.write(f"{os.path.join(WORKDIR, track)}\n")
    print(f"Playlist created: {playlist_path}")

    # Launch VLC with the playlist in stopped/paused mode
    launch_gui(
        f'vlc --no-play-and-pause --no-play-and-exit "{playlist_path}"',
        delay_sec=3.0
    )
    print("GUI_READY: launched VLC with playlist on DISPLAY=:0")

create_initial()
