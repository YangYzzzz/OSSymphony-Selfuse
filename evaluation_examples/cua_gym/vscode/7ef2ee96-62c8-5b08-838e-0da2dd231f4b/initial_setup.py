"""
Initial Setup: Django REST API project scaffold
Task ID: vscode_gf4_031
Domain: vscode

Creates ~/projects/django-rest-api with only an empty requirements.txt.
Opens VSCode with the project folder.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_031'
PROJECT_DIR = f'{WORKDIR}/projects/django-rest-api'

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

    # Create empty requirements.txt
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write('')

    print(f'Initial project directory created: {PROJECT_DIR}')
    print(f'Contents: {os.listdir(PROJECT_DIR)}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
