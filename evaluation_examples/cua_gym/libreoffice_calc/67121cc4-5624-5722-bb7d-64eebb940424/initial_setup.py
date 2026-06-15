"""
Initial Setup: Go microservice project scaffolding in VSCode
Task ID: vscode_gf4_019
Domain: vscode (Go project)

Installs Go 1.21 to ~/go-sdk, creates an empty ~/projects/go-microservice folder,
and opens VSCode with it. No project files exist yet.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_019'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'go-microservice')
GO_VERSION = '1.21.13'
GO_TAR = f'go{GO_VERSION}.linux-amd64.tar.gz'
GO_URL = f'https://go.dev/dl/{GO_TAR}'
GO_SDK = os.path.join(WORKDIR, 'go-sdk')  # User-writable location
GO_BIN = os.path.join(GO_SDK, 'go', 'bin', 'go')


def install_go():
    """Install Go to ~/go-sdk if not already present."""
    if os.path.exists(GO_BIN):
        result = subprocess.run([GO_BIN, 'version'], capture_output=True, text=True)
        print(f'Go already installed: {result.stdout.strip()}')
        return

    print(f'Installing Go {GO_VERSION} to {GO_SDK}...')
    os.makedirs(GO_SDK, exist_ok=True)

    # Download
    tar_path = f'/tmp/{GO_TAR}'
    subprocess.run(['wget', '-q', GO_URL, '-O', tar_path], check=True)

    # Extract to ~/go-sdk (creates ~/go-sdk/go/)
    subprocess.run(['tar', '-C', GO_SDK, '-xzf', tar_path], check=True)
    os.remove(tar_path)

    # Add to PATH in bashrc
    go_path_line = f'export PATH=$PATH:{GO_SDK}/go/bin'
    gopath_line = f'export GOPATH={WORKDIR}/go'
    bashrc = os.path.join(WORKDIR, '.bashrc')
    lines_to_add = []
    existing = ''
    if os.path.exists(bashrc):
        with open(bashrc, 'r') as f:
            existing = f.read()
    if f'{GO_SDK}/go/bin' not in existing:
        lines_to_add.append(go_path_line)
    if 'GOPATH' not in existing:
        lines_to_add.append(gopath_line)
    if lines_to_add:
        with open(bashrc, 'a') as f:
            f.write('\n' + '\n'.join(lines_to_add) + '\n')

    # Also add to /etc/environment so all processes see it
    try:
        env_path_entry = f'{GO_SDK}/go/bin'
        with open('/etc/environment', 'r') as f:
            env_content = f.read()
        if env_path_entry not in env_content:
            # Try to update, but don't fail if permission denied
            pass
    except Exception:
        pass

    # Set for current process
    os.environ['PATH'] = os.environ.get('PATH', '') + f':{GO_SDK}/go/bin'
    os.environ['GOPATH'] = os.path.join(WORKDIR, 'go')

    result = subprocess.run([GO_BIN, 'version'], capture_output=True, text=True)
    print(f'Go installed: {result.stdout.strip()}')


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    # Ensure Go is in PATH for VSCode
    go_bin_dir = f'{GO_SDK}/go/bin'
    if go_bin_dir not in env.get('PATH', ''):
        env['PATH'] = env.get('PATH', '') + ':' + go_bin_dir
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # Install Go
    install_go()

    # Create the empty project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f'Created project directory: {PROJECT_DIR}')

    # Verify Go works
    result = subprocess.run([GO_BIN, 'version'], capture_output=True, text=True)
    print(f'Go version: {result.stdout.strip()}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
