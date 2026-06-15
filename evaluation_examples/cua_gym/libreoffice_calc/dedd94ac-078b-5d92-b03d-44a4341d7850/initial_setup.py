"""
Initial Setup: Open VSCode with empty go-raft-consensus project folder
Task ID: vscode_gf4_062
Domain: vscode (Go project)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_062'
PROJECT_DIR = f'{WORKDIR}/projects/go-raft-consensus'
GO_VERSION = '1.21.13'
GO_ROOT = f'{WORKDIR}/go-sdk'
GO_BIN = f'{GO_ROOT}/bin/go'

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

def run_cmd(cmd, check=True):
    print(f'$ {cmd}')
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())
    if check and result.returncode != 0:
        raise RuntimeError(f'Command failed with code {result.returncode}: {cmd}')
    return result

def install_go():
    """Install Go into user home directory."""
    if os.path.exists(GO_BIN):
        result = run_cmd(f'{GO_BIN} version')
        return

    print(f'Installing Go {GO_VERSION} to {GO_ROOT}...')
    run_cmd(f'wget -q https://go.dev/dl/go{GO_VERSION}.linux-amd64.tar.gz -O /tmp/go.tar.gz')
    os.makedirs(GO_ROOT, exist_ok=True)
    run_cmd(f'tar -C "{WORKDIR}" -xzf /tmp/go.tar.gz')
    # tar extracts to {WORKDIR}/go, rename to go-sdk
    if os.path.exists(f'{WORKDIR}/go') and not os.path.exists(GO_ROOT):
        os.rename(f'{WORKDIR}/go', GO_ROOT)
    elif os.path.exists(f'{WORKDIR}/go') and os.path.exists(GO_ROOT):
        # Merge: remove go-sdk and rename go
        import shutil
        shutil.rmtree(GO_ROOT)
        os.rename(f'{WORKDIR}/go', GO_ROOT)
    run_cmd('rm -f /tmp/go.tar.gz')

    # Add to PATH in .bashrc
    profile_lines = f'\nexport GOROOT={GO_ROOT}\nexport PATH=$PATH:{GO_ROOT}/bin\n'
    bashrc = f'{WORKDIR}/.bashrc'
    if os.path.exists(bashrc):
        with open(bashrc, 'r') as f:
            content = f.read()
        if GO_ROOT not in content:
            with open(bashrc, 'a') as f:
                f.write(profile_lines)

    run_cmd(f'{GO_BIN} version')
    print('Go installed successfully')

def create_initial():
    # Install Go
    install_go()

    # Create empty project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f'Created project directory: {PROJECT_DIR}')

    # Open VSCode with the empty project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
