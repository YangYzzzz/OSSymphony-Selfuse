"""
Initial Setup: Fix indentation error in loop.py
Task ID: vscode_rdb_004
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rdb_004'
PROJECT_DIR = f'{WORKDIR}/projects/bugfix'
TARGET_FILE = f'{PROJECT_DIR}/loop.py'


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
    # Create the project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Write the buggy loop.py — print(i) is NOT indented inside the for loop
    buggy_content = """\
def print_numbers():
    for i in range(1, 6):
    print(i)

print_numbers()
"""
    with open(TARGET_FILE, 'w') as f:
        f.write(buggy_content)

    print(f'Initial file created: {TARGET_FILE}')

    # GUI-ready startup: open VSCode with the buggy file
    launch_gui(f'code "{TARGET_FILE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
