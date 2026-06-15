"""
Initial Setup: Open VSCode with empty go-stream-processor project
Task ID: vscode_gf4_092
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_092'
PROJECT_DIR = f'{WORKDIR}/projects/go-stream-processor'
GO_VERSION = '1.21.13'
GO_TAR = f'go{GO_VERSION}.linux-amd64.tar.gz'
GO_URL = f'https://go.dev/dl/{GO_TAR}'
GO_ROOT = f'{WORKDIR}/go-sdk'
GO_BIN = f'{GO_ROOT}/go/bin/go'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    # Ensure Go is in PATH for VSCode
    env["PATH"] = f"{GO_ROOT}/go/bin:" + env.get("PATH", "")
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def install_go():
    """Install Go if not already present."""
    if os.path.exists(GO_BIN):
        print('Go already installed')
        return
    print(f'Installing Go {GO_VERSION}...')
    os.makedirs(GO_ROOT, exist_ok=True)
    subprocess.run(['wget', '-q', GO_URL, '-O', f'/tmp/{GO_TAR}'], check=True)
    subprocess.run(['tar', '-C', GO_ROOT, '-xzf', f'/tmp/{GO_TAR}'], check=True)
    os.remove(f'/tmp/{GO_TAR}')

    # Add Go to PATH in bashrc for the user
    bashrc = os.path.expanduser('~/.bashrc')
    with open(bashrc, 'a') as f:
        f.write(f'\nexport PATH="{GO_ROOT}/go/bin:$PATH"\n')
        f.write('export GOPATH="$HOME/go"\n')

    # Verify
    result = subprocess.run([GO_BIN, 'version'], capture_output=True, text=True)
    print(f'Installed: {result.stdout.strip()}')


def create_initial():
    # Install Go
    install_go()

    # Create empty project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f'Created project directory: {PROJECT_DIR}')

    # Verify Go is available
    result = subprocess.run([GO_BIN, 'version'], capture_output=True, text=True)
    print(f'Go version: {result.stdout.strip()}')

    # Launch VSCode with the empty project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
