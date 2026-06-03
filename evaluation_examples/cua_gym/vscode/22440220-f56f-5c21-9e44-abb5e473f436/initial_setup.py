"""
Initial Setup: TypeScript monorepo with npm workspaces in VSCode
Task ID: vscode_gf6_061
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_061'
PROJECT_DIR = f'{WORKDIR}/projects/ts-monorepo'


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


def install_node():
    """Install Node.js 18 and TypeScript if not present, using binary tarball."""
    NODE_DIR = '/home/user/.local/node'
    NODE_BIN = f'{NODE_DIR}/bin'

    # Add to PATH for this process
    os.environ['PATH'] = f'{NODE_BIN}:{os.environ.get("PATH", "")}'

    result = subprocess.run(['which', 'node'], capture_output=True, text=True)
    if result.returncode == 0:
        print(f'Node.js already installed: {result.stdout.strip()}')
        return

    print('Installing Node.js 18 from binary tarball...')
    os.makedirs(NODE_DIR, exist_ok=True)
    subprocess.run(
        f'curl -fsSL https://nodejs.org/dist/v18.20.4/node-v18.20.4-linux-x64.tar.xz | tar -xJ --strip-components=1 -C {NODE_DIR}',
        shell=True, check=True, capture_output=True, text=True
    )

    # Add to PATH in bashrc for future sessions
    bashrc = os.path.expanduser('~/.bashrc')
    path_line = f'\nexport PATH="{NODE_BIN}:$PATH"\n'
    with open(bashrc, 'a') as f:
        f.write(path_line)

    result = subprocess.run([f'{NODE_BIN}/node', '--version'], capture_output=True, text=True)
    print(f'Node.js installed: {result.stdout.strip()}')
    result = subprocess.run([f'{NODE_BIN}/npm', '--version'], capture_output=True, text=True)
    print(f'npm installed: {result.stdout.strip()}')

    # Install TypeScript globally
    subprocess.run(
        [f'{NODE_BIN}/npm', 'install', '-g', 'typescript'],
        check=True, capture_output=True, text=True
    )
    result = subprocess.run([f'{NODE_BIN}/npx', 'tsc', '--version'], capture_output=True, text=True)
    print(f'TypeScript installed: {result.stdout.strip()}')


def create_initial():
    install_node()

    # Create project directory structure
    os.makedirs(f'{PROJECT_DIR}/packages/shared/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/packages/api/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/packages/web/src', exist_ok=True)

    # Root package.json - NO workspaces configured (that's the task)
    root_package = {
        "name": "@myapp/root",
        "version": "1.0.0",
        "private": True,
        "description": "TypeScript monorepo for fullstack application",
        "scripts": {
            "clean": "rm -rf packages/*/dist",
            "dev": "echo 'Configure workspaces first'"
        },
        "devDependencies": {
            "typescript": "^5.3.3"
        }
    }

    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(root_package, f, indent=2)
    print(f'Created root package.json (no workspaces)')

    # Create a basic .gitignore
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write("node_modules/\ndist/\n*.js\n*.d.ts\n*.js.map\n!jest.config.js\n")

    print(f'Initial project structure created at {PROJECT_DIR}')

    # GUI-ready: open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
