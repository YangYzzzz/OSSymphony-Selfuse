"""
Initial Setup: Open VSCode with empty go-distributed-counter project folder
Task ID: vscode_gf4_044
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_044'
PROJECT_DIR = f'{WORKDIR}/projects/go-distributed-counter'


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
    """Install Go 1.21 if not already installed."""
    result = subprocess.run(['which', 'go'], capture_output=True, text=True)
    if result.returncode == 0:
        print('Go already installed')
        return

    print('Installing Go 1.21...')
    go_dir = os.path.expanduser('~/go-sdk')
    commands = [
        'wget -q https://go.dev/dl/go1.21.13.linux-amd64.tar.gz -O /tmp/go.tar.gz',
        f'mkdir -p {go_dir}',
        f'tar -C {go_dir} --strip-components=1 -xzf /tmp/go.tar.gz',
        'rm /tmp/go.tar.gz',
    ]
    for cmd in commands:
        subprocess.run(cmd, shell=True, check=True)

    # Add to PATH for current process and persist for user
    go_bin = f'{go_dir}/bin'
    os.environ['PATH'] = f'{go_bin}:' + os.environ.get('PATH', '')
    bashrc = os.path.expanduser('~/.bashrc')
    with open(bashrc, 'a') as f:
        f.write(f'\nexport PATH={go_bin}:$PATH\nexport GOROOT={go_dir}\n')
    profile = os.path.expanduser('~/.profile')
    with open(profile, 'a') as f:
        f.write(f'\nexport PATH={go_bin}:$PATH\nexport GOROOT={go_dir}\n')
    print('Go 1.21 installed successfully')


def create_initial():
    # Install Go
    install_go()

    # Create empty project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f'Created project directory: {PROJECT_DIR}')

    # Open VSCode with the empty project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
