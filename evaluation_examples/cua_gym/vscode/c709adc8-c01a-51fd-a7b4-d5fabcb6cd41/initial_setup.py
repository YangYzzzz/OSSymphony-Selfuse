"""
Initial Setup: Go Configuration Manager — empty project folder with VSCode open
Task ID: vscode_gf4_067
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_067'
PROJECT_DIR = f'{WORKDIR}/projects/go-configuration-manager'
GO_VERSION = '1.21.13'
GO_TAR = f'go{GO_VERSION}.linux-amd64.tar.gz'
GO_URL = f'https://go.dev/dl/{GO_TAR}'
GO_ROOT = f'{WORKDIR}/go-sdk'


def run(cmd, **kwargs):
    """Run a command, printing output."""
    print(f'  $ {cmd}')
    env = kwargs.pop('env', os.environ.copy())
    env['PATH'] = f'{GO_ROOT}/bin:' + env.get('PATH', '')
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env, **kwargs)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())
    return result


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    env['PATH'] = f'{GO_ROOT}/bin:' + env.get('PATH', '')
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def install_go():
    """Install Go if not already present."""
    check = subprocess.run(
        f'{GO_ROOT}/bin/go version', shell=True, capture_output=True, text=True
    )
    if check.returncode == 0:
        print(f'Go already installed: {check.stdout.strip()}')
        return

    print(f'Installing Go {GO_VERSION}...')
    run(f'wget -q -O /tmp/{GO_TAR} {GO_URL}')
    run(f'rm -rf {GO_ROOT}')
    run(f'mkdir -p {GO_ROOT}')
    run(f'tar -C {WORKDIR} -xzf /tmp/{GO_TAR}')
    run(f'mv {WORKDIR}/go/* {GO_ROOT}/')
    run(f'rmdir {WORKDIR}/go')
    run(f'rm /tmp/{GO_TAR}')

    # Verify
    result = run(f'{GO_ROOT}/bin/go version')
    if result.returncode != 0:
        raise RuntimeError('Go installation failed')
    print('Go installed successfully')

    # Set up profile for future shells
    profile_line = f'export PATH={GO_ROOT}/bin:$PATH'
    profile = '/home/user/.profile'
    try:
        with open(profile, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        content = ''
    if GO_ROOT not in content:
        with open(profile, 'a') as f:
            f.write(f'\n{profile_line}\n')
        print('Added Go to PATH in .profile')


def create_initial():
    # Install Go
    install_go()

    # Create the empty project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f'Created project directory: {PROJECT_DIR}')

    # Verify Go is available
    run(f'{GO_ROOT}/bin/go version')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
