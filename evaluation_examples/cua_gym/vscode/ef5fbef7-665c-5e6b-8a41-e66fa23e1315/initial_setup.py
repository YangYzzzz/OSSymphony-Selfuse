"""
Initial Setup: Traffic light state machine project - empty folder
Task ID: vscode_gf4_039
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_039'
PROJECT_DIR = f'{WORKDIR}/projects/ts-state-machine'

def run_cmd(cmd, check=True, timeout=120):
    """Run a shell command and print output."""
    print(f'Running: {cmd}')
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    if result.stdout:
        print(result.stdout[-500:])
    if result.returncode != 0 and result.stderr:
        print(f'STDERR: {result.stderr[-500:]}')
    if check and result.returncode != 0:
        raise RuntimeError(f'Command failed with code {result.returncode}: {cmd}')
    return result

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
    """Install Node.js 18 LTS using nvm (no root required)."""
    # Check if node is already available
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f'Node.js already installed: {result.stdout.strip()}')
            return
    except FileNotFoundError:
        pass

    # Check if nvm node already exists
    nvm_node = os.path.expanduser('~/.nvm/versions/node')
    if os.path.isdir(nvm_node) and os.listdir(nvm_node):
        # nvm node exists, just need to add to PATH
        versions = os.listdir(nvm_node)
        node_dir = os.path.join(nvm_node, versions[0], 'bin')
        os.environ['PATH'] = node_dir + ':' + os.environ['PATH']
        print(f'Added existing nvm node to PATH: {node_dir}')
        return

    print('Installing Node.js 18 via binary download...')
    # Download pre-built Node.js 18 binary
    node_version = 'v18.20.4'
    node_archive = f'node-{node_version}-linux-x64'
    home = os.path.expanduser('~')
    node_install_dir = f'{home}/.local/node'

    run_cmd(f'curl -fsSL https://nodejs.org/dist/{node_version}/{node_archive}.tar.xz -o /tmp/{node_archive}.tar.xz', timeout=120)
    run_cmd(f'mkdir -p {node_install_dir}', timeout=10)
    run_cmd(f'tar -xf /tmp/{node_archive}.tar.xz -C {node_install_dir} --strip-components=1', timeout=60)

    # Add to PATH for this process and persist in bashrc
    node_bin = f'{node_install_dir}/bin'
    os.environ['PATH'] = node_bin + ':' + os.environ['PATH']

    # Persist in bashrc so the agent can use it
    bashrc = f'{home}/.bashrc'
    export_line = f'\nexport PATH="{node_bin}:$PATH"\n'
    with open(bashrc, 'a') as f:
        f.write(export_line)

    # Also add to profile
    profile = f'{home}/.profile'
    with open(profile, 'a') as f:
        f.write(export_line)

    run_cmd('node --version')
    run_cmd('npm --version')
    print('Node.js 18 installed successfully')

def create_initial():
    # Install Node.js first (task says it should be available)
    install_node()

    # Create the empty project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f'Created empty project directory: {PROJECT_DIR}')

    # Open VSCode with the empty project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
