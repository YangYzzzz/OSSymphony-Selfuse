"""
Initial Setup: Python Dependency Injection project scaffold
Task ID: vscode_gf4_053
Domain: libreoffice_calc (actually vscode/python project)

Creates the minimal initial state:
- ~/projects/python-dependency-injection/ with only src/__init__.py
- Opens VSCode with the project folder
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_053'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'python-dependency-injection')
SRC_DIR = os.path.join(PROJECT_DIR, 'src')


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
    # Clean up any prior state
    if os.path.exists(PROJECT_DIR):
        import shutil
        shutil.rmtree(PROJECT_DIR)

    # Create project directory structure
    os.makedirs(SRC_DIR, exist_ok=True)

    # Create src/__init__.py (empty package marker)
    init_path = os.path.join(SRC_DIR, '__init__.py')
    with open(init_path, 'w') as f:
        f.write('# Python Dependency Injection Framework\n')

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  src/__init__.py exists: {os.path.exists(init_path)}')

    # Verify no venv, no other source files exist
    contents = []
    for root, dirs, files in os.walk(PROJECT_DIR):
        for fn in files:
            contents.append(os.path.relpath(os.path.join(root, fn), PROJECT_DIR))
    print(f'  Project contents: {contents}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
