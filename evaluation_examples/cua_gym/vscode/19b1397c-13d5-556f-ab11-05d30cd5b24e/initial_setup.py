"""
Initial Setup: Create a Jupyter notebook with three cells in VSCode
Task ID: vscode_py_060
Domain: vs_code

Initial state: VSCode is open with no notebook. The Jupyter extension is installed.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_060'


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
    # Ensure no stale notebook exists
    notebook_path = os.path.join(WORKDIR, f'{TASK_ID}.ipynb')
    if os.path.exists(notebook_path):
        os.remove(notebook_path)

    # Ensure Jupyter extension is installed
    subprocess.run(
        ["code", "--install-extension", "ms-toolsai.jupyter"],
        capture_output=True, text=True, timeout=60
    )
    print("Jupyter extension installed/verified")

    # Also ensure Python extension is installed (needed for Jupyter kernels)
    subprocess.run(
        ["code", "--install-extension", "ms-python.python"],
        capture_output=True, text=True, timeout=60
    )
    print("Python extension installed/verified")

    # Install numpy (matplotlib intentionally NOT pre-installed to make cell 1 meaningful)
    subprocess.run(
        ["pip3", "install", "numpy"],
        capture_output=True, text=True, timeout=120
    )
    print("numpy installed")

    # Open VSCode with the home directory
    launch_gui(f'code "{WORKDIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
