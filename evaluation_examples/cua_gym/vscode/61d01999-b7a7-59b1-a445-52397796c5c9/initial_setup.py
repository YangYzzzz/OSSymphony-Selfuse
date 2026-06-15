"""
Initial Setup: Python Task Queue project with only .env file
Task ID: vscode_gf4_041
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_041'
PROJECT_DIR = f'{WORKDIR}/projects/python-task-queue'


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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create .env file with REDIS_URL
    env_content = "REDIS_URL=redis://localhost:6379/0\n"
    with open(os.path.join(PROJECT_DIR, '.env'), 'w') as f:
        f.write(env_content)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  .env file with REDIS_URL')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
