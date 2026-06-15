"""
Initial Setup: Configure VLC subtitle settings (yellow color, font size 20)
Task ID: vlcset_006
Domain: vlc

VLC is open with no media loaded. Subtitle settings are at defaults
(white color, default size).
"""

import os
import re
import shlex
import subprocess
import time

VLCRC_PATH = os.path.expanduser("~/.config/vlc/vlcrc")


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
    # Kill VLC if running so we can safely modify vlcrc
    subprocess.run(["pkill", "-f", "vlc"], capture_output=True)
    time.sleep(2)

    # Ensure subtitle settings are at defaults by commenting out any
    # active freetype-color and freetype-fontsize lines
    with open(VLCRC_PATH, "r") as f:
        content = f.read()

    # Comment out freetype-color if uncommented (default = 16777215 = white)
    content = re.sub(
        r'^(freetype-color=.*)$',
        r'#\1',
        content,
        flags=re.MULTILINE
    )
    # Comment out freetype-fontsize if uncommented (default = 0 = auto)
    content = re.sub(
        r'^(freetype-fontsize=.*)$',
        r'#\1',
        content,
        flags=re.MULTILINE
    )

    with open(VLCRC_PATH, "w") as f:
        f.write(content)

    print("Initial vlcrc configured with default subtitle settings (white, default size)")

    # Launch VLC with no media loaded
    launch_gui('vlc', delay_sec=2.0)
    print('GUI_READY: launched VLC with DISPLAY=:0')


create_initial()
