"""
Initial Setup: Create empty Node.js project structure for VSCode task
Task ID: vscode_gf4_002
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_002'
PROJECT_DIR = f'{WORKDIR}/projects/node-api'

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

    # Create empty src/index.js
    index_path = os.path.join(src_dir, 'index.js')
    with open(index_path, 'w') as f:
        f.write('')  # empty file

    # Ensure NO package.json, .env, or node_modules exist
    for item in ['package.json', '.env', 'node_modules', 'package-lock.json']:
        item_path = os.path.join(PROJECT_DIR, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            import shutil
            shutil.rmtree(item_path)

    print(f'Initial project structure created at: {PROJECT_DIR}')
    print(f'  - src/index.js (empty)')

    # Verify Node.js and npm are available
    try:
        node_check = subprocess.run(['node', '--version'], capture_output=True, text=True)
        print(f'  - Node.js: {node_check.stdout.strip()}')
    except FileNotFoundError:
        # Try with full path
        try:
            node_check = subprocess.run(['/usr/local/bin/node', '--version'], capture_output=True, text=True)
            print(f'  - Node.js: {node_check.stdout.strip()}')
        except FileNotFoundError:
            print('  - Node.js: not found in PATH (may need nvm or manual setup)')
    try:
        npm_check = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        print(f'  - npm: {npm_check.stdout.strip()}')
    except FileNotFoundError:
        print('  - npm: not found in PATH')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
