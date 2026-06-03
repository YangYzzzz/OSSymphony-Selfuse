"""
Initial Setup: Set up a TypeScript project from scratch in ~/project
Task ID: vscode_wf_040
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'project')

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

def install_node_if_missing():
    """Install Node.js and npm via user-space binary if not already present."""
    result = subprocess.run(['which', 'node'], capture_output=True, text=True)
    if result.returncode != 0:
        print('Node.js not found, installing user-space binary...')
        node_dir = os.path.expanduser('~/.local/node')
        os.makedirs(node_dir, exist_ok=True)
        tarball = '/tmp/node.tar.xz'
        url = 'https://nodejs.org/dist/v20.11.1/node-v20.11.1-linux-x64.tar.xz'
        subprocess.run(['wget', '-q', '-O', tarball, url], check=True)
        subprocess.run(['tar', '-xf', tarball, '-C', node_dir, '--strip-components=1'],
                       check=True)
        os.remove(tarball)
        # Add to PATH for this process and future commands
        node_bin = os.path.join(node_dir, 'bin')
        os.environ['PATH'] = node_bin + ':' + os.environ.get('PATH', '')
        # Also add to bashrc for the GUI agent session
        bashrc = os.path.expanduser('~/.bashrc')
        with open(bashrc, 'a') as f:
            f.write(f'\nexport PATH="{node_bin}:$PATH"\n')
        print('Node.js installed to ~/.local/node')
    node_ver = subprocess.run(['node', '--version'], capture_output=True, text=True)
    npm_ver = subprocess.run(['npm', '--version'], capture_output=True, text=True)
    print(f'Node: {node_ver.stdout.strip()}, npm: {npm_ver.stdout.strip()}')

def create_initial():
    # Install Node.js if needed
    install_node_if_missing()

    # Create the empty project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f'Created project directory: {PROJECT_DIR}')

    # Open VSCode with the empty project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0 on ~/project')

create_initial()
