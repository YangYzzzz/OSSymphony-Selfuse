"""
Initial Setup: VLC with default recording and snapshot settings
Task ID: vlcset_014
Domain: vlc
"""

import os
import re
import shlex
import subprocess
import time

VLCRC_PATH = os.path.expanduser("~/.config/vlc/vlcrc")
WORKDIR = '/home/user'

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

def ensure_defaults():
    """Ensure vlcrc has default (commented-out) snapshot and record settings."""
    # Kill VLC first to prevent it from overwriting vlcrc on exit
    subprocess.run(["pkill", "-f", "vlc"], capture_output=True)
    time.sleep(2)

    # Read vlcrc
    with open(VLCRC_PATH, "r") as f:
        content = f.read()

    # Ensure these keys are commented out (default state)
    keys_to_comment = ["input-record-path", "snapshot-path", "snapshot-format"]
    for key in keys_to_comment:
        # If there's an uncommented line, comment it out
        pattern = re.compile(rf'^(?!#)(\s*{re.escape(key)}=.*)$', re.MULTILINE)
        content = pattern.sub(r'#\1', content)

    with open(VLCRC_PATH, "w") as f:
        f.write(content)

    print("vlcrc defaults ensured (snapshot/record keys commented out)")

def create_directories():
    """Create the target directories so agent doesn't have to."""
    os.makedirs(f'{WORKDIR}/Recordings', exist_ok=True)
    os.makedirs(f'{WORKDIR}/Screenshots', exist_ok=True)
    print(f"Created directories: {WORKDIR}/Recordings, {WORKDIR}/Screenshots")

def main():
    ensure_defaults()
    create_directories()

    # Launch VLC with no media (just the player window)
    launch_gui('vlc', delay_sec=2.0)
    print('GUI_READY: VLC launched with DISPLAY=:0, no media loaded')

main()
