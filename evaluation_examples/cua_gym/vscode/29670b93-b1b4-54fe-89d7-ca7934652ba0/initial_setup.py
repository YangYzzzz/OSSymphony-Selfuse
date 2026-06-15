"""
Initial Setup: Scaffold a TypeScript React app and configure VSCode settings
Task ID: vscode_gf4_011
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_011'
PROJECT_DIR = f'{WORKDIR}/projects/react-app'
NVM_DIR = f'{WORKDIR}/.nvm'


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


def install_nodejs_local():
    """Install Node.js 18 locally using prebuilt binary (no root needed)."""
    print("Installing Node.js 18 (user-local)...")
    node_dir = f'{WORKDIR}/.local/node'
    os.makedirs(node_dir, exist_ok=True)

    # Download prebuilt Node.js 18 binary
    node_version = 'v18.20.8'
    tarball = f'node-{node_version}-linux-x64.tar.xz'
    url = f'https://nodejs.org/dist/{node_version}/{tarball}'

    subprocess.run(
        f'curl -fsSL "{url}" -o "/tmp/{tarball}"',
        shell=True, check=True,
    )
    subprocess.run(
        f'tar -xJf "/tmp/{tarball}" -C "{node_dir}" --strip-components=1',
        shell=True, check=True,
    )
    os.remove(f'/tmp/{tarball}')

    # Add to PATH for this process and write to bashrc for future shells
    node_bin = f'{node_dir}/bin'
    os.environ['PATH'] = f'{node_bin}:{os.environ["PATH"]}'

    # Persist PATH for future shells
    bashrc = f'{WORKDIR}/.bashrc'
    export_line = f'\nexport PATH="{node_bin}:$PATH"\n'
    with open(bashrc, 'a') as f:
        f.write(export_line)

    # Verify
    result = subprocess.run(['node', '--version'], capture_output=True, text=True)
    print(f"Node.js installed: {result.stdout.strip()}")
    result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
    print(f"npm installed: {result.stdout.strip()}")


def create_initial():
    # Step 1: Install Node.js if not present
    node_check = subprocess.run(['which', 'node'], capture_output=True)
    if node_check.returncode != 0:
        install_nodejs_local()

    # Step 2: Create the empty project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f"Created project directory: {PROJECT_DIR}")

    # Step 3: Install VSCode extensions (ESLint)
    print("Installing VSCode extensions...")
    for ext_id in ["dbaeumer.vscode-eslint"]:
        subprocess.run(
            ["code", "--install-extension", ext_id, "--force"],
            capture_output=True, text=True,
        )
        print(f"  Installed: {ext_id}")

    # Step 4: Open VSCode with the empty project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print(f'GUI_READY: launched VSCode with DISPLAY=:0 on {PROJECT_DIR}')


create_initial()
