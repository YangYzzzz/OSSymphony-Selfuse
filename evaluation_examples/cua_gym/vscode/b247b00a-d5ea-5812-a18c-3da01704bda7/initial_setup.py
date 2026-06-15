"""
Initial Setup: Set tab size to 4 and enable insert spaces in VSCode settings.
Task ID: vscode_we_002
Domain: vscode

Creates settings.json with editor.tabSize=2 and editor.insertSpaces=false,
then launches VSCode.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_002'

VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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
    # Ensure the VSCode User config directory exists
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Write initial settings: tabSize=2 and insertSpaces=false
    # These are the PRE-task values that the agent must change
    settings = {
        "editor.tabSize": 2,
        "editor.insertSpaces": False
    }

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'Initial settings created: {SETTINGS_PATH}')
    print(f'Contents: {json.dumps(settings, indent=2)}')

    # Launch VSCode so the GUI agent can interact with it
    launch_gui('code --no-sandbox "/home/user"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
