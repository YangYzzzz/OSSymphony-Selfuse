"""
Initial Setup: Open VSCode with empty ts-microservice-framework project folder
Task ID: vscode_gf4_060
Domain: vscode

Creates:
- Empty ~/projects/ts-microservice-framework directory
- Installs Node.js 18 and npm
- Opens VSCode with the project folder
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_060'
PROJECT_DIR = f'{WORKDIR}/projects/ts-microservice-framework'


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


def install_nodejs():
    """Install Node.js 18 LTS via direct binary download."""
    # Check if node is already installed
    result = subprocess.run(["bash", "-c", "which node"], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Node.js already installed at {result.stdout.strip()}")
        return

    print("Installing Node.js 18 via binary tarball...")
    NODE_VERSION = "v18.20.4"
    ARCH = "linux-x64"
    NODE_DIR = f"/home/user/.local/node"
    TARBALL = f"/tmp/node-{NODE_VERSION}-{ARCH}.tar.xz"
    URL = f"https://nodejs.org/dist/{NODE_VERSION}/node-{NODE_VERSION}-{ARCH}.tar.xz"

    # Download first
    subprocess.run(
        ["curl", "-fsSL", "-o", TARBALL, URL],
        check=True,
        timeout=300
    )
    print("Download complete, extracting...")

    # Extract to user-owned directory
    os.makedirs(NODE_DIR, exist_ok=True)
    subprocess.run(
        ["tar", "-xJf", TARBALL, "-C", NODE_DIR, "--strip-components=1"],
        check=True,
        timeout=120
    )
    os.remove(TARBALL)

    # Add to PATH via .bashrc
    bashrc = os.path.expanduser("~/.bashrc")
    path_line = f'\nexport PATH="{NODE_DIR}/bin:$PATH"\n'
    with open(bashrc, "a") as f:
        f.write(path_line)

    # Also create symlinks in /usr/local/bin if we have sudo access
    try:
        subprocess.run(
            ["bash", "-c", f"sudo ln -sf {NODE_DIR}/bin/node /usr/local/bin/node && sudo ln -sf {NODE_DIR}/bin/npm /usr/local/bin/npm && sudo ln -sf {NODE_DIR}/bin/npx /usr/local/bin/npx"],
            check=True, timeout=10
        )
    except Exception:
        pass  # Symlinks are nice-to-have

    # Verify installation using full path
    result = subprocess.run([f"{NODE_DIR}/bin/node", "--version"], capture_output=True, text=True)
    print(f"Node.js installed: {result.stdout.strip()}")
    result = subprocess.run([f"{NODE_DIR}/bin/npm", "--version"], capture_output=True, text=True)
    print(f"npm installed: {result.stdout.strip()}")


def create_initial():
    # Step 1: Install Node.js 18
    install_nodejs()

    # Step 2: Create empty project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f"Created project directory: {PROJECT_DIR}")

    # Step 3: Verify directory is empty (no project files)
    contents = os.listdir(PROJECT_DIR)
    if contents:
        print(f"WARNING: Project directory not empty: {contents}")
    else:
        print("Project directory is empty as expected")

    # Step 4: Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
