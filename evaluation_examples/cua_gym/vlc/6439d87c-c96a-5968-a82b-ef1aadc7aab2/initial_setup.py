"""
Initial Setup: Enable minimal interface mode in VLC
Task ID: vlcset_004
Domain: vlc

Creates the initial state: VLC open with default (full) interface mode.
qt-minimal-view must be 0 (default/normal mode).
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
    # Step 1: Kill any running VLC so we can safely edit vlcrc
    subprocess.run(["pkill", "-f", "vlc"], capture_output=True)
    time.sleep(2)

    # Step 2: Ensure vlcrc directory exists
    os.makedirs(os.path.dirname(VLCRC_PATH), exist_ok=True)

    # Step 3: Ensure vlcrc exists (VLC may not have been run yet)
    if not os.path.exists(VLCRC_PATH):
        # Run VLC briefly to generate default vlcrc, then kill it
        env = os.environ.copy()
        env["DISPLAY"] = ":0"
        env["VLC_VERBOSE"] = "-1"
        proc = subprocess.Popen(
            ["vlc", "--intf", "dummy", "--play-and-exit"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env,
        )
        time.sleep(3)
        subprocess.run(["pkill", "-f", "vlc"], capture_output=True)
        time.sleep(2)

    # Step 4: Set qt-minimal-view=0 (ensure default full interface)
    if os.path.exists(VLCRC_PATH):
        set_vlcrc_option("qt-minimal-view", "0")
        print("Set qt-minimal-view=0 in vlcrc")
    else:
        # Create minimal vlcrc with the setting
        with open(VLCRC_PATH, "w") as f:
            f.write("qt-minimal-view=0\n")
        print("Created vlcrc with qt-minimal-view=0")

    # Step 5: Launch VLC with no media (default full interface)
    launch_gui("vlc", delay_sec=3.0)
    print("GUI_READY: launched VLC with DISPLAY=:0 in default full interface mode")


create_initial()
