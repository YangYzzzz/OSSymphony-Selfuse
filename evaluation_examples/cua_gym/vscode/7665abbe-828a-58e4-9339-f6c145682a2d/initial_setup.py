"""
Initial Setup: Inline variable 'baseUrl' task - create pre-task JavaScript file
Task ID: vscode_rrt_035
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_035'
PROJECT_DIR = f'{WORKDIR}/projects/client'
OUTPUT = f'{PROJECT_DIR}/api.js'


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
    # Create project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Write the initial JavaScript file with baseUrl variable
    content = """\
const baseUrl = 'https://api.example.com/v2';

async function getUsers() {
    return fetch(`${baseUrl}/users`);
}

async function getProducts() {
    return fetch(`${baseUrl}/products`);
}

async function getOrders() {
    return fetch(`${baseUrl}/orders`);
}
"""
    with open(OUTPUT, 'w') as f:
        f.write(content)

    print(f'Initial file created: {OUTPUT}')

    # Open VSCode with the file, cursor will be at beginning (line 1)
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
