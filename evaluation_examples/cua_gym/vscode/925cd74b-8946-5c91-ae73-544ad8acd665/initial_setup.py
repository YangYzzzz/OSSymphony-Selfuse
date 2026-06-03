"""
Initial Setup: Configure empty Go project directory with Go installed
Task ID: vscode_gf5_041
Domain: vscode

Creates ~/projects/go-server/ (empty), installs Go 1.21, opens VSCode.
Go extension is NOT installed. No go.mod, main.go, or launch.json.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_041'
PROJECT_DIR = f'{WORKDIR}/projects/go-server'

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

def run_cmd(cmd, check=True):
    """Run a shell command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Command failed: {cmd}")
        print(f"stderr: {result.stderr}")
    return result

def create_initial():
    # 1. Create empty project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f'Created project directory: {PROJECT_DIR}')

    # 2. Install Go 1.21 in user-writable location if not present
    GO_INSTALL_DIR = f'{WORKDIR}/go-sdk'
    GO_BIN = f'{GO_INSTALL_DIR}/go/bin/go'
    go_check = run_cmd(f'test -f {GO_BIN}', check=False)
    if go_check.returncode != 0:
        print('Installing Go 1.21...')
        os.makedirs(GO_INSTALL_DIR, exist_ok=True)
        run_cmd(f'wget -q https://go.dev/dl/go1.21.13.linux-amd64.tar.gz -O /tmp/go.tar.gz')
        run_cmd(f'tar -C {GO_INSTALL_DIR} -xzf /tmp/go.tar.gz')
        run_cmd('rm /tmp/go.tar.gz')
        print('Go 1.21 installed')

    # Add Go to PATH via .bashrc so the agent can use it
    bashrc_path = f'{WORKDIR}/.bashrc'
    go_path_line = f'export PATH={GO_INSTALL_DIR}/go/bin:$HOME/go/bin:$PATH'
    gopath_line = f'export GOPATH=$HOME/go'
    # Check if already added
    existing = ''
    if os.path.exists(bashrc_path):
        with open(bashrc_path, 'r') as f:
            existing = f.read()
    if 'go-sdk' not in existing:
        with open(bashrc_path, 'a') as f:
            f.write(f'\n# Go SDK\n{go_path_line}\n{gopath_line}\n')

    # Also create a symlink so 'go' is findable
    symlink_dir = f'{WORKDIR}/.local/bin'
    os.makedirs(symlink_dir, exist_ok=True)
    go_symlink = f'{symlink_dir}/go'
    if not os.path.exists(go_symlink):
        os.symlink(GO_BIN, go_symlink)

    # Verify Go is available
    go_ver = run_cmd(f'{GO_BIN} version', check=False)
    print(f'Go version: {go_ver.stdout.strip()}')

    # 3. Ensure Go extension is NOT installed in VSCode
    ext_check = run_cmd('code --list-extensions 2>/dev/null', check=False)
    if 'golang.go' in ext_check.stdout.lower():
        run_cmd('code --uninstall-extension golang.Go', check=False)
        print('Uninstalled Go extension')

    # 4. Open VSCode with the empty project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
