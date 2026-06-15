"""
Initial Setup: Create directory structure for supplementary table PDF task.
Task ID: pdf_res_089
Domain: pdf

The task asks the agent to CREATE the PDF, so the initial state has
the target directory ready but NO PDF file at the output path.
We also open a file manager to the papers directory so the agent can see
where to save the file.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_089'
PAPERS_DIR = f'{WORKDIR}/papers'


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
    # Ensure the papers directory exists
    os.makedirs(PAPERS_DIR, exist_ok=True)

    # Make sure no PDF exists at the target path
    target = os.path.join(PAPERS_DIR, 'supplementary_table.pdf')
    if os.path.exists(target):
        os.remove(target)

    print(f'Papers directory created: {PAPERS_DIR}')
    print(f'No PDF at target path (as expected for initial state)')

    # Open file manager to the papers directory so the agent sees the workspace
    launch_gui(f'nautilus "{PAPERS_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus file manager with DISPLAY=:0')


create_initial()
