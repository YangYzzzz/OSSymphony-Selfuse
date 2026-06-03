"""
Initial Setup: Set up environment for requests library (pre-task state)
Task ID: osworld_multi_apps_vscode_env_setup_002
Domain: os

Initial state:
  - Chrome is open
  - Terminal is available
  - /home/user/requests does NOT exist
"""

import os
import shlex
import shutil
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_env_setup_002'


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
    # Ensure /home/user/requests does NOT exist (clean pre-task state)
    requests_dir = os.path.join(WORKDIR, 'requests')
    if os.path.exists(requests_dir):
        shutil.rmtree(requests_dir)
        print(f'Removed existing {requests_dir} to ensure clean initial state')
    else:
        print(f'Confirmed: {requests_dir} does not exist (clean initial state)')

    # GUI-ready startup: open Chrome (as specified in context: Chrome is open)
    launch_gui('google-chrome --new-window https://github.com/psf/requests', delay_sec=3.0)
    print('GUI_READY: Launched Chrome with DISPLAY=:0')

    print(f'Initial state ready:')
    print(f'  - {requests_dir}: does not exist')
    print(f'  - Chrome: open')
    print(f'  - Terminal: available')


create_initial()
