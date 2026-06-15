"""
Initial Setup: Go Event Sourcing project skeleton
Task ID: vscode_gf6_089
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_089'
PROJECT_DIR = f'{WORKDIR}/projects/go-event-sourcing'

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
    """Install Go 1.21 to ~/go-sdk if not already installed."""
    go_root = os.path.expanduser('~/go-sdk/go')
    go_bin = os.path.join(go_root, 'bin', 'go')
    if os.path.exists(go_bin):
        print('Go already installed')
        return

    print('Installing Go 1.21...')
    sdk_dir = os.path.expanduser('~/go-sdk')
    os.makedirs(sdk_dir, exist_ok=True)
    subprocess.run(
        f'curl -sL https://go.dev/dl/go1.21.13.linux-amd64.tar.gz | tar -C {sdk_dir} -xzf -',
        shell=True, check=True
    )

    # Add to PATH in profile so it persists
    profile_lines = f'\nexport GOROOT={go_root}\nexport PATH=$PATH:{go_root}/bin\n'
    bashrc = os.path.expanduser('~/.bashrc')
    with open(bashrc, 'a') as f:
        f.write(profile_lines)

    # Also write to .profile for non-interactive shells
    profile = os.path.expanduser('~/.profile')
    with open(profile, 'a') as f:
        f.write(profile_lines)

    # Verify
    result = subprocess.run([go_bin, 'version'], capture_output=True, text=True)
    print(f'Go installed: {result.stdout.strip()}')

def create_project():
    """Create the Go project skeleton with go.mod and empty directories."""
    # Create directory structure
    os.makedirs(f'{PROJECT_DIR}/pkg', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/internal', exist_ok=True)

    # Create go.mod
    go_mod_content = """module github.com/user/go-event-sourcing

go 1.21
"""
    with open(f'{PROJECT_DIR}/go.mod', 'w') as f:
        f.write(go_mod_content)

    print(f'Project created at {PROJECT_DIR}')

def setup_initial():
    install_go()
    create_project()

    # Open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

setup_initial()
