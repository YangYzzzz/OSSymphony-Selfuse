"""
Initial Setup: Open VLC with default language settings (Auto/English)
Task ID: vlcset_001
Domain: vlc
"""

import os
import re
import shlex
import subprocess
import time

VLCRC_PATH = os.path.expanduser("~/.config/vlc/vlcrc")
WORKDIR = '/home/user'
TASK_ID = 'vlcset_001'


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


def kill_vlc():
    """Kill VLC if running."""
    subprocess.run(["pkill", "-f", "vlc"], capture_output=True)
    time.sleep(2)


def ensure_language_auto():
    """Ensure VLC language is set to Auto (default) by commenting out any language= line."""
    if not os.path.exists(VLCRC_PATH):
        print(f"vlcrc not found at {VLCRC_PATH}")
        return

    with open(VLCRC_PATH, "r") as f:
        content = f.read()

    # Comment out any active language= line (but not audio-language, sub-language, etc.)
    # We need to match standalone 'language=' not preceded by '-'
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        stripped = line.strip()
        # Match 'language=...' but not 'audio-language=', 'sub-language=', etc.
        if stripped.startswith('language='):
            new_lines.append('#' + line)
            print(f"Commented out: {stripped}")
        else:
            new_lines.append(line)

    with open(VLCRC_PATH, "w") as f:
        f.write('\n'.join(new_lines))

    print("Language set to Auto (default)")


def create_initial():
    # Step 1: Kill VLC before modifying config
    kill_vlc()

    # Step 2: Ensure language is Auto (comment out any language= line)
    ensure_language_auto()

    # Step 3: Launch VLC with no media (empty player)
    launch_gui('vlc --extraintf=http --http-password=password', delay_sec=3.0)
    print("GUI_READY: VLC launched with DISPLAY=:0, language=Auto (English)")


create_initial()
