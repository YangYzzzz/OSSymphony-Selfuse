"""
Initial Setup: Open VSCode with empty ts-express-api project folder
Task ID: vscode_gf4_018
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_018'
PROJECT_DIR = f'{WORKDIR}/projects/ts-express-api'
NODE_BIN = f'{WORKDIR}/.local/bin'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    env["PATH"] = NODE_BIN + ":" + env.get("PATH", "")
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def install_nodejs():
    """Install Node.js 18 LTS to ~/.local if not already installed."""
    node_path = os.path.join(NODE_BIN, 'node')
    if os.path.exists(node_path):
        result = subprocess.run([node_path, '--version'], capture_output=True, text=True)
        print(f'Node.js already installed: {result.stdout.strip()}')
        return

    print('Installing Node.js 18 to ~/.local ...')
    os.makedirs(f'{WORKDIR}/.local', exist_ok=True)
    subprocess.run(
        f'curl -fsSL https://nodejs.org/dist/v18.20.4/node-v18.20.4-linux-x64.tar.xz -o /tmp/node.tar.xz',
        shell=True, check=True, capture_output=True, text=True
    )
    subprocess.run(
        f'tar -xf /tmp/node.tar.xz -C {WORKDIR}/.local --strip-components=1',
        shell=True, check=True, capture_output=True, text=True
    )
    # Add to PATH for this process and bashrc
    os.environ["PATH"] = NODE_BIN + ":" + os.environ.get("PATH", "")

    # Persist PATH in .bashrc so the agent terminal can use node/npm
    bashrc = os.path.join(WORKDIR, '.bashrc')
    path_line = f'\nexport PATH="{NODE_BIN}:$PATH"\n'
    if os.path.exists(bashrc):
        with open(bashrc, 'r') as f:
            content = f.read()
        if NODE_BIN not in content:
            with open(bashrc, 'a') as f:
                f.write(path_line)
    else:
        with open(bashrc, 'w') as f:
            f.write(path_line)

    node_ver = subprocess.run([os.path.join(NODE_BIN, 'node'), '--version'], capture_output=True, text=True)
    npm_ver = subprocess.run([os.path.join(NODE_BIN, 'npm'), '--version'], capture_output=True, text=True)
    print(f'Installed Node.js: {node_ver.stdout.strip()}, npm: {npm_ver.stdout.strip()}')


def create_initial():
    # Install Node.js if needed
    install_nodejs()

    # Create the empty project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f'Created project directory: {PROJECT_DIR}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
