"""
Initial Setup: Set VLC default volume level to 50%
Task ID: vlcset_002
Domain: vlc

Initial state: VLC is open with no media loaded. Default volume is at 100%
(volume-save=1 / default, no qt-startvolume override).
"""

import os
import re
import shlex
import subprocess
import time

VLCRC_PATH = os.path.expanduser("~/.config/vlc/vlcrc")


def read_vlcrc() -> str:
    with open(VLCRC_PATH, "r") as f:
        return f.read()


def set_vlcrc_option(key: str, value: str):
    """Set a vlcrc option. Uncomments the key if commented out."""
    content = read_vlcrc()
    pattern = re.compile(rf'^(#?\s*){re.escape(key)}=.*$', re.MULTILINE)
    replacement = f'{key}={value}'
    if pattern.search(content):
        content = pattern.sub(replacement, content)
    else:
        content += f'\n{key}={value}\n'
    with open(VLCRC_PATH, "w") as f:
        f.write(content)


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
    # Kill VLC if running (must edit vlcrc while VLC is not running)
    subprocess.run(["pkill", "-f", "vlc"], capture_output=True)
    time.sleep(2)

    # Ensure vlcrc exists
    os.makedirs(os.path.dirname(VLCRC_PATH), exist_ok=True)

    # Ensure volume-save is at default (1 = remember volume, i.e. NOT "always reset")
    # This means the "Always reset audio start level to:" checkbox is UNCHECKED
    set_vlcrc_option("volume-save", "1")

    # Ensure qt-startvolume is NOT set to 50 (remove or comment it out)
    # If it exists, set to default (which is typically 80 in VLC)
    content = read_vlcrc()
    # Remove any existing qt-startvolume line to keep it at default
    pattern = re.compile(r'^qt-startvolume=.*$', re.MULTILINE)
    if pattern.search(content):
        content = pattern.sub('#qt-startvolume=80', content)
        with open(VLCRC_PATH, "w") as f:
            f.write(content)

    print(f'Initial vlcrc configured: volume-save=1 (default), no qt-startvolume override')

    # Launch VLC with no media (just the player window)
    launch_gui('vlc', delay_sec=2.0)
    print('GUI_READY: VLC launched with DISPLAY=:0, no media loaded')


create_initial()
