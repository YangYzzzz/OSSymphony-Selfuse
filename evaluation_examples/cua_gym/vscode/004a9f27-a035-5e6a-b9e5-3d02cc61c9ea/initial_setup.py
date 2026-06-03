"""
Initial Setup: Open VSCode with empty go-scaffold project folder
Task ID: vscode_gf6_003
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_003'
PROJECT_DIR = f'{WORKDIR}/projects/go-scaffold'


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


GO_HOME = f'{WORKDIR}/go'
GO_BIN = f'{GO_HOME}/bin/go'


def install_go():
    """Install Go 1.21 to ~/go if not already available."""
    # Check if go is already installed system-wide or locally
    result = subprocess.run(['bash', '-c', 'which go'], capture_output=True, text=True)
    if result.returncode == 0:
        print(f'Go already installed at: {result.stdout.strip()}')
        return

    if os.path.exists(GO_BIN):
        print(f'Go already installed at: {GO_BIN}')
        return

    print('Installing Go 1.21 to ~/go ...')
    cmds = [
        'wget -q https://go.dev/dl/go1.21.13.linux-amd64.tar.gz -O /tmp/go.tar.gz',
        f'mkdir -p {WORKDIR}',
        f'tar -C {WORKDIR} -xzf /tmp/go.tar.gz',
        'rm -f /tmp/go.tar.gz',
    ]
    for cmd in cmds:
        subprocess.run(['bash', '-c', cmd], check=True)

    # Add to PATH via .bashrc so terminal sessions find it
    bashrc = f'{WORKDIR}/.bashrc'
    path_line = f'export PATH={GO_HOME}/bin:$PATH'
    gopath_line = f'export GOPATH={WORKDIR}/gopath'
    already = False
    if os.path.exists(bashrc):
        with open(bashrc) as f:
            content = f.read()
            if GO_HOME in content:
                already = True
    if not already:
        with open(bashrc, 'a') as f:
            f.write(f'\n# Go installation\n{path_line}\n{gopath_line}\n')

    result = subprocess.run([GO_BIN, 'version'], capture_output=True, text=True)
    print(f'Go installed: {result.stdout.strip()}')


def create_initial():
    # Install Go if needed
    install_go()

    # Create the empty project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f'Created project directory: {PROJECT_DIR}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
