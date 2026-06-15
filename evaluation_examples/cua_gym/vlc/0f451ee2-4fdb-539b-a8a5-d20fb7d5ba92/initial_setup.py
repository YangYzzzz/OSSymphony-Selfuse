"""
Initial Setup: Configure VLC subtitle settings for visually impaired user
Task ID: vlcset_010
Domain: vlc

Initial state: VLC open with no media loaded, subtitle settings at defaults.
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


def ensure_vlcrc_exists():
    """Make sure vlcrc directory and file exist."""
    vlcrc_dir = os.path.dirname(VLCRC_PATH)
    os.makedirs(vlcrc_dir, exist_ok=True)
    if not os.path.exists(VLCRC_PATH):
        # Launch and kill VLC once to generate default vlcrc
        launch_gui("vlc --extraintf=http --http-password=password", delay_sec=3.0)
        subprocess.run(["pkill", "-f", "vlc"], capture_output=True)
        time.sleep(2)


def verify_defaults():
    """Verify that subtitle settings are at defaults (commented out)."""
    if not os.path.exists(VLCRC_PATH):
        print("vlcrc does not exist yet")
        return

    with open(VLCRC_PATH, "r") as f:
        content = f.read()

    # Verify the relevant keys are still commented (default state)
    keys_to_check = [
        "subsdec-encoding",
        "freetype-font",
        "freetype-fontsize",
        "sub-autodetect-file",
    ]
    for key in keys_to_check:
        pattern = re.compile(rf'^{re.escape(key)}=', re.MULTILINE)
        if pattern.search(content):
            print(f"WARNING: {key} is already uncommented (not default)")
        else:
            print(f"OK: {key} is at default (commented out)")


def create_initial():
    ensure_vlcrc_exists()
    verify_defaults()

    # Kill any running VLC before launching fresh
    subprocess.run(["pkill", "-f", "vlc"], capture_output=True)
    time.sleep(2)

    # Launch VLC with no media (just the player window)
    launch_gui("vlc", delay_sec=3.0)
    print("GUI_READY: launched VLC with DISPLAY=:0, no media loaded")


create_initial()
