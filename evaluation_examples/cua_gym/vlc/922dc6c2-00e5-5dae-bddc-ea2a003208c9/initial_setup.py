"""
Initial Setup: Swap the positions of the first and last tracks in VLC playlist
Task ID: vlc_playlist_062
Domain: vlc

Creates 6 MP3 files and opens VLC with a playlist in the original order:
  opening_act.mp3, set1.mp3, set2.mp3, set3.mp3, encore.mp3, finale.mp3
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vlc_playlist_062'

TRACKS = [
    'opening_act.mp3',
    'set1.mp3',
    'set2.mp3',
    'set3.mp3',
    'encore.mp3',
    'finale.mp3',
]

# Each track gets a different duration and tone so they are distinguishable
TRACK_SPECS = [
    ('opening_act.mp3', 5, 'sine=f=440:r=44100'),     # A4
    ('set1.mp3',        5, 'sine=f=494:r=44100'),      # B4
    ('set2.mp3',        5, 'sine=f=523:r=44100'),      # C5
    ('set3.mp3',        5, 'sine=f=587:r=44100'),      # D5
    ('encore.mp3',      5, 'sine=f=659:r=44100'),      # E5
    ('finale.mp3',      5, 'sine=f=698:r=44100'),      # F5
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


def create_media_files():
    """Create 6 distinct MP3 files using ffmpeg."""
    for filename, duration, source in TRACK_SPECS:
        filepath = os.path.join(WORKDIR, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
        subprocess.run([
            'ffmpeg', '-y',
            '-f', 'lavfi', '-i', f'anullsrc=r=44100:cl=mono',
            '-f', 'lavfi', '-i', source,
            '-filter_complex', '[0][1]amix=inputs=2:duration=shortest',
            '-t', str(duration),
            '-q:a', '9',
            filepath,
        ], capture_output=True, check=True)
        print(f'Created: {filepath}')


def create_playlist():
    """Create an XSPF playlist file with tracks in original order."""
    playlist_path = os.path.join(WORKDIR, f'{TASK_ID}.xspf')

    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<playlist xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/" version="1">')
    lines.append('  <title>Playlist</title>')
    lines.append('  <trackList>')

    for i, track in enumerate(TRACKS):
        filepath = os.path.join(WORKDIR, track)
        lines.append(f'    <track>')
        lines.append(f'      <location>file://{filepath}</location>')
        lines.append(f'      <title>{os.path.splitext(track)[0]}</title>')
        lines.append(f'      <extension application="http://www.videolan.org/vlc/playlist/ns/0/">')
        lines.append(f'        <vlc:id>{i}</vlc:id>')
        lines.append(f'      </extension>')
        lines.append(f'    </track>')

    lines.append('  </trackList>')
    lines.append('  <extension application="http://www.videolan.org/vlc/playlist/ns/0/">')
    for i in range(len(TRACKS)):
        lines.append(f'    <vlc:item tid="{i}"/>')
    lines.append('  </extension>')
    lines.append('</playlist>')

    with open(playlist_path, 'w') as f:
        f.write('\n'.join(lines))
    print(f'Playlist created: {playlist_path}')
    return playlist_path


def main():
    # Kill any existing VLC instance
    subprocess.run(['pkill', '-f', 'vlc'], capture_output=True)
    time.sleep(2)

    # Create media files
    create_media_files()

    # Create playlist
    playlist_path = create_playlist()

    # Launch VLC with the playlist (stopped state)
    launch_gui(f'vlc --no-play-and-pause --no-play-and-exit --started-from-file "{playlist_path}"', delay_sec=3.0)
    print('GUI_READY: launched VLC with playlist on DISPLAY=:0')


main()
