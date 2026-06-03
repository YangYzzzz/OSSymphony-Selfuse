"""
Initial Setup: VLC advanced settings - audio desync, network caching, file caching
Task ID: vlcset_013
Domain: vlc

Ensures VLC is at default settings and opens VLC with no media loaded.
"""

import os
import re
import shlex
import subprocess
import time

VLCRC_PATH = os.path.expanduser("~/.config/vlc/vlcrc")


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


def reset_vlcrc_option_to_default(key: str):
    """Comment out a vlcrc option to restore its default value."""
    with open(VLCRC_PATH, "r") as f:
        content = f.read()
    # Match uncommented key=value and comment it out
    pattern = re.compile(rf'^(?!#)(\s*{re.escape(key)}=.*)$', re.MULTILINE)
    content = pattern.sub(r'#\1', content)
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
    # Kill any running VLC first to safely modify vlcrc
    subprocess.run(["pkill", "-f", "vlc"], capture_output=True)
    time.sleep(2)

    # Ensure vlcrc exists (VLC creates it on first run)
    if not os.path.exists(VLCRC_PATH):
        os.makedirs(os.path.dirname(VLCRC_PATH), exist_ok=True)
        # Run VLC briefly to generate default vlcrc
        env = os.environ.copy()
        env["DISPLAY"] = ":0"
        proc = subprocess.Popen(
            ["vlc", "--intf", "dummy", "--play-and-exit"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env,
        )
        time.sleep(3)
        subprocess.run(["pkill", "-f", "vlc"], capture_output=True)
        time.sleep(2)

    # Ensure all target settings are at default (commented out)
    reset_vlcrc_option_to_default("audio-desync")
    reset_vlcrc_option_to_default("network-caching")
    reset_vlcrc_option_to_default("file-caching")

    print("Initial vlcrc configured with default settings")

    # Launch VLC with no media
    launch_gui('vlc', delay_sec=2.0)
    print('GUI_READY: VLC launched with DISPLAY=:0')


create_initial()
