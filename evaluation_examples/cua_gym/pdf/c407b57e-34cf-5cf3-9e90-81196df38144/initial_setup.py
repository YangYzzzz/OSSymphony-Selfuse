"""
Initial Setup: Create directory for bibliography PDF task
Task ID: pdf_res_071
Domain: pdf

Initial state: No file at /home/user/papers/bibliography.pdf.
Just create the papers directory and open a terminal so the agent
can use reportlab to create the PDF.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_071'
OUTPUT_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{OUTPUT_DIR}/bibliography.pdf'


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
    # Create the output directory (the file itself must NOT exist yet)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Make sure the target file does NOT exist (negative constraint)
    if os.path.exists(OUTPUT):
        os.remove(OUTPUT)

    print(f'Initial state prepared: directory {OUTPUT_DIR} exists, no bibliography.pdf')

    # Open a terminal so the agent can work
    launch_gui('bash -c "cd /home/user/papers && exec bash"', delay_sec=1.0)
    # Also open the file manager to show the papers directory
    launch_gui(f'nautilus "{OUTPUT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')


create_initial()
