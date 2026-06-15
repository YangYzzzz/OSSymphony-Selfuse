"""
Initial Setup: Create empty workspace for Maven multi-module project
Task ID: vscode_lang_074
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = f'{WORKDIR}/projects/java-multi'

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
    # Create the empty workspace directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f'Empty workspace created: {PROJECT_DIR}')

    # Verify maven is available (may not be in PATH)
    try:
        result = subprocess.run(['mvn', '--version'], capture_output=True, text=True)
        print(f'Maven version check: {result.stdout.splitlines()[0] if result.stdout else "not found"}')
    except FileNotFoundError:
        # Try common locations
        for mvn_path in ['/usr/share/maven/bin/mvn', '/opt/maven/bin/mvn', '/usr/local/bin/mvn']:
            if os.path.exists(mvn_path):
                result = subprocess.run([mvn_path, '--version'], capture_output=True, text=True)
                print(f'Maven found at {mvn_path}: {result.stdout.splitlines()[0] if result.stdout else ""}')
                break
        else:
            print('Maven not found in PATH or common locations (may need to be installed by agent)')

    # Launch VSCode with the empty workspace folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
