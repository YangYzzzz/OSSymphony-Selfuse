"""
Initial Setup: Create empty JavaScript snippet file for VSCode
Task ID: vscode_code_016
Domain: vs_code

The task asks the agent to create a custom snippet for JavaScript.
Initial state: ~/.config/Code/User/snippets/javascript.json exists but is empty ({})
"""

import os
import json
import shlex
import subprocess
import time

# VM paths — all scripts run on the VM
HOME = '/home/user'
SNIPPETS_DIR = os.path.join(HOME, '.config', 'Code', 'User', 'snippets')
SNIPPET_FILE = os.path.join(SNIPPETS_DIR, 'javascript.json')


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
    # Ensure the snippets directory exists
    os.makedirs(SNIPPETS_DIR, exist_ok=True)

    # Create empty javascript.json (just an empty object)
    with open(SNIPPET_FILE, 'w') as f:
        json.dump({}, f, indent=4)

    print(f'Initial snippet file created: {SNIPPET_FILE}')

    # GUI-ready startup: open VSCode
    # Open the snippets directory so agent can navigate to the file
    launch_gui('code --new-window', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
