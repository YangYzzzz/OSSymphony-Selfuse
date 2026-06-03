"""
Initial Setup: Set up default formatters for JSON, HTML, JavaScript, and CSS
Task ID: vscode_code_013
Domain: vs_code

Creates an initial VSCode settings.json with only editor.fontSize set,
no default formatters configured (as the task requires adding them).
"""

import json
import os
import shlex
import subprocess
import time

HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
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

    # Initial state: only fontSize configured, no formatter settings
    initial_settings = {
        "editor.fontSize": 14
    }

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(initial_settings, f, indent=4)

    print(f'Initial settings.json created: {SETTINGS_PATH}')
    print(f'Contents: {json.dumps(initial_settings, indent=4)}')

    # GUI-ready startup: open VSCode so the agent can interact with it
    launch_gui('code', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
