"""
Initial Setup: Create empty /home/user/design/ directory for floor plan PDF task.
Task ID: pdf_aw_046
Domain: pdf

The task requires the agent to CREATE a layered PDF from scratch.
Initial state: directory exists but no PDF file.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_aw_046'
DESIGN_DIR = f'{WORKDIR}/design'

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
    # Create the design directory (task says it exists but is empty)
    os.makedirs(DESIGN_DIR, exist_ok=True)
    print(f'Design directory created: {DESIGN_DIR}')

    # Verify no floor_plan.pdf exists
    pdf_path = os.path.join(DESIGN_DIR, 'floor_plan.pdf')
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        print(f'Removed existing floor_plan.pdf')

    # Open a file manager showing the empty design directory
    # so the agent can see the workspace
    launch_gui(f'nautilus "{DESIGN_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched file manager with DISPLAY=:0')

create_initial()
