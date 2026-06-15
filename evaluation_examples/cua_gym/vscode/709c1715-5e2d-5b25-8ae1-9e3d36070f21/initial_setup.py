"""
Initial Setup: TypeScript GraphQL Server project scaffolding
Task ID: vscode_gf4_032
Domain: vscode

Creates an empty project folder ~/projects/ts-graphql-server,
installs Node.js 18 if missing, and opens VSCode with that folder.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_032'
PROJECT_DIR = f'{WORKDIR}/projects/ts-graphql-server'


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


def run_cmd(cmd, check=True, shell=True):
    """Run a shell command and print output."""
    result = subprocess.run(cmd, shell=shell, capture_output=True, text=True)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed ({result.returncode}): {cmd}")
    return result


def install_nodejs():
    """Install Node.js 18 via binary download if not already installed."""
    result = subprocess.run("which node", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Node.js already installed: {result.stdout.strip()}")
        return

    print("Installing Node.js 18 via binary tarball...")
    cmds = [
        "curl -fsSL https://nodejs.org/dist/v18.20.4/node-v18.20.4-linux-x64.tar.xz -o /tmp/node.tar.xz",
        "echo 'password' | sudo -S tar -xJf /tmp/node.tar.xz -C /usr/local --strip-components=1",
        "rm -f /tmp/node.tar.xz",
    ]
    for cmd in cmds:
        run_cmd(cmd)
    run_cmd("node --version")
    run_cmd("npm --version")


def create_initial():
    # Step 1: Install Node.js 18
    install_nodejs()

    # Step 2: Create empty project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f"Project directory created: {PROJECT_DIR}")

    # Step 3: Install VSCode extensions (TypeScript, ESLint, Jest)
    extensions = [
        "dbaeumer.vscode-eslint",
        "orta.vscode-jest",
    ]
    for ext in extensions:
        subprocess.run(["code", "--install-extension", ext], capture_output=True, text=True)
        print(f"Installed extension: {ext}")

    # Step 4: Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print(f'GUI_READY: launched VSCode with DISPLAY=:0 on {PROJECT_DIR}')


create_initial()
