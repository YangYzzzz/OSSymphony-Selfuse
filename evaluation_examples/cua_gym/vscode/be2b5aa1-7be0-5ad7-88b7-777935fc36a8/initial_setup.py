"""
Initial Setup: VSCode FastAPI project with empty app directory
Task ID: vscode_gf4_012
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_012'
PROJECT_DIR = f'{WORKDIR}/projects/python-fastapi'

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
    # Create the project directory structure
    os.makedirs(f'{PROJECT_DIR}/app', exist_ok=True)

    # Ensure no virtual environment, tests, or launch config exist
    # (clean slate - only empty app/ directory)
    for cleanup_path in [
        f'{PROJECT_DIR}/venv',
        f'{PROJECT_DIR}/tests',
        f'{PROJECT_DIR}/.vscode',
        f'{PROJECT_DIR}/app/main.py',
        f'{PROJECT_DIR}/app/__init__.py',
    ]:
        if os.path.isdir(cleanup_path):
            import shutil
            shutil.rmtree(cleanup_path)
        elif os.path.isfile(cleanup_path):
            os.remove(cleanup_path)

    print(f'Project directory created: {PROJECT_DIR}')
    print(f'  app/ directory exists: {os.path.isdir(f"{PROJECT_DIR}/app")}')
    print(f'  venv/ exists: {os.path.isdir(f"{PROJECT_DIR}/venv")}')
    print(f'  tests/ exists: {os.path.isdir(f"{PROJECT_DIR}/tests")}')
    print(f'  .vscode/ exists: {os.path.isdir(f"{PROJECT_DIR}/.vscode")}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
