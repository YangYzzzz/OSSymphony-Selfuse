"""
Initial Setup: Python Network Scanner project skeleton
Task ID: vscode_gf4_048
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_048'
PROJECT_DIR = f'{WORKDIR}/projects/python-network-scanner'

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
    # Create project directory structure
    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)

    # Create src/__init__.py (the only file that should exist initially)
    init_path = os.path.join(src_dir, '__init__.py')
    with open(init_path, 'w') as f:
        f.write('"""Python Network Scanner package."""\n')

    print(f'Project structure created at: {PROJECT_DIR}')
    print(f'  src/__init__.py exists: {os.path.exists(init_path)}')

    # Ensure no venv exists
    venv_path = os.path.join(PROJECT_DIR, 'venv')
    if os.path.exists(venv_path):
        import shutil
        shutil.rmtree(venv_path)
        print('Removed existing venv')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
