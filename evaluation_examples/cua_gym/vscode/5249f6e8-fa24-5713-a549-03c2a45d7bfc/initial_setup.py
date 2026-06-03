"""
Initial Setup: Open VSCode with empty ~/projects/ts-virtual-dom folder.
Node.js 18, npm installed. No project files exist yet.
Task ID: vscode_gf4_084
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_084'
PROJECT_DIR = f'{WORKDIR}/projects/ts-virtual-dom'


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
    """Install Node.js 18 LTS via nvm (no root required)."""
    # Check if already available
    check = subprocess.run(
        ["bash", "-c", "source ~/.nvm/nvm.sh 2>/dev/null; node --version 2>/dev/null || echo NOTFOUND"],
        capture_output=True, text=True
    )
    if check.stdout.strip().startswith("v18"):
        print(f"Node.js already installed: {check.stdout.strip()}")
        return

    print("Installing Node.js 18 via nvm...")
    # Install nvm + Node.js 18
    subprocess.run(
        ["bash", "-c",
         'curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash && '
         'export NVM_DIR="$HOME/.nvm" && '
         '[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" && '
         'nvm install 18 && '
         'nvm use 18 && '
         'nvm alias default 18 && '
         'node --version && npm --version'],
        check=True,
        timeout=180
    )

    # Create symlinks so node/npm are available without sourcing nvm
    nvm_node = subprocess.run(
        ["bash", "-c",
         'export NVM_DIR="$HOME/.nvm" && '
         '[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" && '
         'which node'],
        capture_output=True, text=True
    )
    node_path = nvm_node.stdout.strip()
    if node_path:
        node_dir = os.path.dirname(node_path)
        # Add nvm node bin to PATH via .bashrc
        bashrc_path = os.path.expanduser("~/.bashrc")
        with open(bashrc_path, "a") as f:
            f.write(f'\nexport PATH="{node_dir}:$PATH"\n')
        # Also create symlinks in /usr/local/bin if possible, or ~/bin
        bin_dir = os.path.expanduser("~/bin")
        os.makedirs(bin_dir, exist_ok=True)
        for cmd in ["node", "npm", "npx"]:
            src = os.path.join(node_dir, cmd)
            dst = os.path.join(bin_dir, cmd)
            if os.path.exists(src) and not os.path.exists(dst):
                os.symlink(src, dst)
        print(f"Node.js 18 installed. node at: {node_path}")


def create_initial():
    # Step 1: Install Node.js 18
    install_nodejs()

    # Step 2: Create the empty project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f"Created project directory: {PROJECT_DIR}")

    # Step 3: Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
