"""
Initial Setup: Python async scraper project skeleton
Task ID: vscode_gf4_029
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_029'
PROJECT_DIR = f'{WORKDIR}/projects/python-async-scraper'

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

    # Create src/__init__.py (empty)
    init_path = os.path.join(src_dir, '__init__.py')
    with open(init_path, 'w') as f:
        f.write('')

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  src/__init__.py: {os.path.exists(init_path)}')

    # Verify no venv, tests, .vscode, or scraper.py exist
    for unwanted in ['venv', 'tests', '.vscode', 'src/scraper.py']:
        path = os.path.join(PROJECT_DIR, unwanted)
        if os.path.exists(path):
            print(f'WARNING: {unwanted} already exists, removing')
            if os.path.isdir(path):
                import shutil
                shutil.rmtree(path)
            else:
                os.remove(path)

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
