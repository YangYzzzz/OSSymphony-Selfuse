"""
Initial Setup: Create directory structure for certificate PDF creation task
Task ID: pdf_gf3_009
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_009'
DOCUMENTS_DIR = f'{WORKDIR}/documents'


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
    # Create the documents directory if it doesn't exist
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    print(f'Directory created: {DOCUMENTS_DIR}')

    # Verify certificate.pdf does NOT exist (task is to create it from scratch)
    cert_path = f'{DOCUMENTS_DIR}/certificate.pdf'
    if os.path.exists(cert_path):
        os.remove(cert_path)
        print(f'Removed pre-existing certificate: {cert_path}')

    # Open a terminal in the documents directory so the user can work
    launch_gui('bash -c "cd /home/user/documents && xterm"', delay_sec=1.0)

    # Also open the file manager to show the documents directory
    launch_gui(f'nautilus "{DOCUMENTS_DIR}"', delay_sec=2.0)

    print(f'Initial state ready: {DOCUMENTS_DIR} exists, certificate.pdf does NOT exist')
    print('GUI_READY: launched terminal and file manager with DISPLAY=:0')


create_initial()
