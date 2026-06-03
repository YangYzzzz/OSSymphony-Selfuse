"""
Initial Setup: Open VSCode with ~/projects/python-openapi project skeleton
Task ID: vscode_gf6_062
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_062'
PROJECT_DIR = f'{WORKDIR}/projects/python-openapi'

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
    # Ensure project directory structure exists
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)

    # Create empty __init__.py so src is a package (if not already there)
    init_path = f'{PROJECT_DIR}/src/__init__.py'
    if not os.path.isfile(init_path):
        with open(init_path, 'w') as f:
            f.write('')

    # Create venv if not present (using --without-pip since python3-venv pkg may be missing)
    venv_dir = f'{PROJECT_DIR}/venv'
    if not os.path.isdir(venv_dir):
        subprocess.run(
            ['python3', '-m', 'venv', '--without-pip', venv_dir],
            check=True, capture_output=True, text=True
        )
    print(f'Project structure verified at {PROJECT_DIR}')

    # Make sure no task-completed artifacts exist (clean state)
    for path in [
        f'{PROJECT_DIR}/src/main.py',
        f'{PROJECT_DIR}/openapi.json',
        f'{PROJECT_DIR}/.vscode/tasks.json',
    ]:
        if os.path.exists(path):
            os.remove(path)
            print(f'Removed pre-existing: {path}')

    # Verify initial state
    assert os.path.isdir(f'{PROJECT_DIR}/src'), 'src/ directory missing'
    assert os.path.isdir(f'{PROJECT_DIR}/venv'), 'venv/ directory missing'
    assert not os.path.exists(f'{PROJECT_DIR}/src/main.py'), 'src/main.py should not exist yet'
    assert not os.path.exists(f'{PROJECT_DIR}/openapi.json'), 'openapi.json should not exist yet'
    print('Initial state verified: venv/ (empty), src/ (empty), no main.py, no openapi.json')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
