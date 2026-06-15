"""
Initial Setup: Go Feature Flags project skeleton
Task ID: vscode_gf6_095
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_095'
PROJECT_DIR = f'{WORKDIR}/projects/go-feature-flags'

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
    """Install Go 1.21 if not already present."""
    go_bin = os.path.expanduser('~/go-sdk/go/bin/go')
    # Check common locations
    for path in ['/usr/local/go/bin/go', '/usr/bin/go', '/snap/bin/go', go_bin]:
        if os.path.isfile(path):
            print(f'Go already installed at {path}')
            return
    print('Installing Go 1.21 to ~/go-sdk ...')
    go_sdk = os.path.expanduser('~/go-sdk')
    os.makedirs(go_sdk, exist_ok=True)
    subprocess.run([
        'bash', '-c',
        f'wget -q https://go.dev/dl/go1.21.13.linux-amd64.tar.gz -O /tmp/go.tar.gz '
        f'&& tar -C {go_sdk} -xzf /tmp/go.tar.gz '
        f'&& rm /tmp/go.tar.gz'
    ], check=True)
    # Add to PATH for this process and future shells
    os.environ['PATH'] = f'{go_sdk}/go/bin:' + os.environ.get('PATH', '')
    bashrc = os.path.expanduser('~/.bashrc')
    with open(bashrc, 'a') as f:
        f.write(f'\nexport PATH={go_sdk}/go/bin:$PATH\n')
    print('Go 1.21 installed successfully')

def create_initial():
    # Install Go
    install_go()

    # Create project directory structure
    os.makedirs(f'{PROJECT_DIR}/pkg', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/internal', exist_ok=True)

    # Create go.mod
    go_mod_content = """module github.com/user/go-feature-flags

go 1.21
"""
    with open(f'{PROJECT_DIR}/go.mod', 'w') as f:
        f.write(go_mod_content)

    print(f'Initial project structure created at: {PROJECT_DIR}')

    # Verify structure
    for root, dirs, files in os.walk(PROJECT_DIR):
        level = root.replace(PROJECT_DIR, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f'{subindent}{file}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
