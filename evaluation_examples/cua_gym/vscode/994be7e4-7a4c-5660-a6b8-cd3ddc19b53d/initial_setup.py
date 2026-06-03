"""
Initial Setup: Configure VSCode file settings (newline, trim, eol)
Task ID: vscode_we_031
Domain: vscode

Initial state: VSCode is open with empty user settings.
"""

import json
import os
import shlex
import subprocess
import time

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # Ensure the VSCode user config directory exists
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Write empty settings (no file-related settings pre-configured)
    settings = {}
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)
    print(f"Initial settings created: {SETTINGS_PATH}")

    # Launch VSCode
    launch_gui('code "/home/user"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()
