"""
Initial Setup: VSCode with empty python-pipeline-dsl project skeleton
Task ID: vscode_gf4_094
Domain: libreoffice_calc (actually vscode/python project)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_094'
PROJECT_DIR = f'{WORKDIR}/projects/python-pipeline-dsl'

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
    src_dsl_dir = os.path.join(PROJECT_DIR, 'src', 'dsl')
    os.makedirs(src_dsl_dir, exist_ok=True)

    # Create src/__init__.py
    with open(os.path.join(PROJECT_DIR, 'src', '__init__.py'), 'w') as f:
        f.write('')

    # Create src/dsl/__init__.py
    with open(os.path.join(PROJECT_DIR, 'src', 'dsl', '__init__.py'), 'w') as f:
        f.write('')

    print(f'Initial project created at: {PROJECT_DIR}')

    # Verify structure
    for root, dirs, files in os.walk(PROJECT_DIR):
        level = root.replace(PROJECT_DIR, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f'{subindent}{file}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
