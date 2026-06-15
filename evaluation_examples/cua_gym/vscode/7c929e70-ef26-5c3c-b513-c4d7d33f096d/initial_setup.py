"""
Initial Setup: Open VSCode with empty go-template-engine project folder
Task ID: vscode_gf4_057
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_057'
PROJECT_DIR = f'{WORKDIR}/projects/go-template-engine'


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


def install_go():
    """Install Go 1.21 to user home if not already present."""
    go_dir = os.path.join(WORKDIR, 'go-sdk')
    go_bin = os.path.join(go_dir, 'go', 'bin', 'go')
    if os.path.exists(go_bin):
        print('Go already installed.')
        return
    print('Installing Go 1.21...')
    os.makedirs(go_dir, exist_ok=True)
    subprocess.run(
        f'wget -q https://go.dev/dl/go1.21.13.linux-amd64.tar.gz -O /tmp/go.tar.gz '
        f'&& tar -C {go_dir} -xzf /tmp/go.tar.gz '
        f'&& rm /tmp/go.tar.gz',
        shell=True, check=True,
    )
    # Add to PATH for current user
    bashrc = os.path.join(WORKDIR, '.bashrc')
    path_line = f'\nexport PATH=$PATH:{go_dir}/go/bin\nexport GOPATH={WORKDIR}/go\n'
    with open(bashrc, 'a') as f:
        f.write(path_line)
    print('Go 1.21 installed.')


def create_initial():
    # Install Go
    install_go()

    # Create the empty project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f'Created project directory: {PROJECT_DIR}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
