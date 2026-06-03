"""
Initial Setup: Set up FastAPI framework from GitHub
Task ID: osworld_multi_apps_vscode_env_setup_005
Domain: os / multi_apps_vscode_env_setup

Initial State:
- Chrome is open
- Terminal is available
- /home/user/fastapi does NOT exist
"""

import os
import shlex
import subprocess
import shutil
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_env_setup_005'
FASTAPI_DIR = f'{WORKDIR}/fastapi'


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
    # Ensure /home/user/fastapi does NOT exist (clean state)
    if os.path.exists(FASTAPI_DIR):
        shutil.rmtree(FASTAPI_DIR)
        print(f'Removed existing {FASTAPI_DIR}')
    else:
        print(f'{FASTAPI_DIR} does not exist - initial state is correct')

    # GUI-ready startup: open Chrome and a terminal
    # Chrome is expected to already be open according to task spec
    launch_gui('google-chrome --new-window https://github.com/tiangolo/fastapi', delay_sec=3.0)
    time.sleep(1.0)

    # Open a terminal (gnome-terminal) so user has access to CLI tools
    launch_gui('gnome-terminal', delay_sec=2.0)

    print(f'Initial state ready: {FASTAPI_DIR} does not exist')
    print('GUI_READY: Chrome opened with fastapi GitHub page, terminal opened with DISPLAY=:0')


create_initial()
