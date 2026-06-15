"""
Initial Setup: VSCode with empty project directory for Vite React+TS initialization
Task ID: vscode_web_093
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_093'
PROJECT_DIR = f'{WORKDIR}/projects/new-app'
SUDO_PASS = 'password'


def run_cmd(cmd, shell=True, timeout=300):
    """Run a shell command and print output."""
    result = subprocess.run(
        cmd, shell=shell, capture_output=True, text=True, timeout=timeout
    )
    if result.stdout:
        print(result.stdout.strip()[-1000:])
    if result.stderr:
        print(result.stderr.strip()[-500:])
    return result


def install_nodejs():
    """Install Node.js 20.x LTS using binary tarball if not already at v20+."""
    check = subprocess.run('node --version 2>/dev/null', shell=True, capture_output=True, text=True)
    version = check.stdout.strip()
    if version.startswith('v20') or version.startswith('v22'):
        print(f'Node.js {version} already installed')
        return

    print('Installing Node.js 20.x LTS via binary tarball...')

    # Remove old system nodejs if present
    run_cmd(f'echo {SUDO_PASS} | sudo -S apt-get remove -y nodejs libnode72 2>/dev/null || true')

    # Download and install Node.js 20 binary
    run_cmd(
        'curl -fsSL https://nodejs.org/dist/v20.18.0/node-v20.18.0-linux-x64.tar.xz '
        '-o /tmp/node.tar.xz',
        timeout=120
    )
    run_cmd(f'echo {SUDO_PASS} | sudo -S tar -xf /tmp/node.tar.xz -C /usr/local --strip-components=1')
    run_cmd('rm -f /tmp/node.tar.xz')

    # Verify
    run_cmd('node --version')
    run_cmd('npm --version')
    print('Node.js 20 installed successfully')


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
    # Install Node.js if needed
    install_nodejs()

    # Create the empty project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f'Created empty project directory: {PROJECT_DIR}')

    # Verify Node.js and npm are available
    run_cmd('node --version')
    run_cmd('npm --version')

    # Open VSCode with the empty project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
