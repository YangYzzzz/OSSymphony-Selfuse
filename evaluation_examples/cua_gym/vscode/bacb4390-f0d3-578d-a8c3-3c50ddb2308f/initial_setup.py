"""
Initial Setup: Add timeout parameter to fetch_data function
Task ID: vscode_rrt_040
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_040'
PROJECT_DIR = f'{WORKDIR}/projects/api'


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

    # --- fetcher.py (initial: NO timeout parameter) ---
    fetcher_content = '''\
def fetch_data(url, headers=None):
    import requests
    resp = requests.get(url, headers=headers)
    return resp.json()
'''
    with open(os.path.join(PROJECT_DIR, 'fetcher.py'), 'w') as f:
        f.write(fetcher_content)
    print(f'Created: {PROJECT_DIR}/fetcher.py')

    # --- main.py ---
    main_content = '''\
from fetcher import fetch_data

result1 = fetch_data('https://api.example.com/users')
result2 = fetch_data('https://api.example.com/items', headers={'Auth': 'token123'})
'''
    with open(os.path.join(PROJECT_DIR, 'main.py'), 'w') as f:
        f.write(main_content)
    print(f'Created: {PROJECT_DIR}/main.py')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
