"""
Initial Setup: Configure VLC hardware decoding and video output module
Task ID: vlcset_011
Domain: vlc

Initial state: VLC open with no media loaded, default settings
(hardware decoding = any/automatic, vout = default).
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


def ensure_vlcrc_default(key: str):
    """Ensure a vlcrc option is commented out (using default value)."""
    content = read_vlcrc()
    # If there's an uncommented line for this key, comment it out
    pattern = re.compile(rf'^(?!#)(\s*){re.escape(key)}=.*$', re.MULTILINE)
    if pattern.search(content):
        content = pattern.sub(lambda m: f'#{m.group(0)}', content)
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
    # Kill VLC if running (to safely modify vlcrc)
    subprocess.run(["pkill", "-f", "vlc"], capture_output=True)
    time.sleep(2)

    # Ensure hardware decoding is at default (commented out = "any"/automatic)
    ensure_vlcrc_default("avcodec-hw")
    # Ensure video output module is at default (commented out)
    ensure_vlcrc_default("vout")

    print("vlcrc ensured at default settings for avcodec-hw and vout")

    # Launch VLC with no media loaded
    launch_gui("vlc", delay_sec=2.0)
    print("GUI_READY: launched VLC with DISPLAY=:0")


create_initial()
