"""
Initial Setup: Academic paper title page creation task
Task ID: pdf_res_046
Domain: pdf

Initial state: No PDF file exists. The agent must create the PDF from scratch.
We ensure the /home/user/papers/ directory does NOT exist, and open a terminal
so the agent can use reportlab or other tools to create the document.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_046'
PAPERS_DIR = f'{WORKDIR}/papers'
TARGET = f'{PAPERS_DIR}/gnn_title_page.pdf'


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
    # Ensure no pre-existing file at the target path
    if os.path.exists(TARGET):
        os.remove(TARGET)
    # Remove the papers directory if it somehow exists
    if os.path.exists(PAPERS_DIR):
        import shutil
        shutil.rmtree(PAPERS_DIR)

    print(f'Initial state prepared: no file at {TARGET}')
    print(f'Directory {PAPERS_DIR} does not exist (agent must create it)')

    # Open a terminal so the agent can work
    launch_gui('bash -c "xterm -e bash"', delay_sec=1.0)
    # Also open file manager at home directory for context
    launch_gui(f'nautilus "{WORKDIR}"', delay_sec=2.0)
    print('GUI_READY: launched terminal and file manager with DISPLAY=:0')


create_initial()
