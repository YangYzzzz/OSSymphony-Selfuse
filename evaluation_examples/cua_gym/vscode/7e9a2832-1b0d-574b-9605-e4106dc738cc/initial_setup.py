"""
Initial Setup: Create python-data-validation project with only src/__init__.py
Task ID: vscode_gf4_068
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_068'
PROJECT_DIR = f'{WORKDIR}/projects/python-data-validation'

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
    # Create project directory structure - only src/__init__.py
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)

    # Create src/__init__.py with a minimal docstring
    with open(f'{PROJECT_DIR}/src/__init__.py', 'w') as f:
        f.write('"""Python Data Validation Library."""\n')

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Contents: src/__init__.py only')

    # Verify no venv exists
    venv_path = f'{PROJECT_DIR}/venv'
    if os.path.exists(venv_path):
        import shutil
        shutil.rmtree(venv_path)
        print('Removed pre-existing venv')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
