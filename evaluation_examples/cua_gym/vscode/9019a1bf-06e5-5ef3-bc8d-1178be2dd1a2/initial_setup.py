"""
Initial Setup: Open VSCode with an empty Go project directory
Task ID: vscode_gf4_004
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_004'
PROJECT_DIR = f'{WORKDIR}/projects/go-service'


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
    # Create the empty project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Check if Go is installed (non-fatal if missing)
    go_paths = ['/usr/local/go/bin/go', '/usr/bin/go', '/snap/bin/go']
    go_bin = None
    for p in go_paths:
        if os.path.exists(p):
            go_bin = p
            break
    if go_bin:
        result = subprocess.run([go_bin, 'version'], capture_output=True, text=True)
        print(f'Go version: {result.stdout.strip()}')
    else:
        # Try PATH
        result = subprocess.run(['which', 'go'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f'Go found at: {result.stdout.strip()}')
        else:
            print('Warning: Go not found in expected locations')

    # Verify the directory is empty (no go.mod, main.go, or .vscode)
    for item in ['go.mod', 'main.go', '.vscode']:
        path = os.path.join(PROJECT_DIR, item)
        if os.path.exists(path):
            if os.path.isdir(path):
                import shutil
                shutil.rmtree(path)
            else:
                os.remove(path)
            print(f'Removed pre-existing {item}')

    print(f'Empty project directory created: {PROJECT_DIR}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
