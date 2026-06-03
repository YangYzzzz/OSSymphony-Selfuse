"""
Initial Setup: Go REST API project in VSCode
Task ID: vscode_gf4_013
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_013'
PROJECT_DIR = f'{WORKDIR}/projects/go-rest-api'
GO_VERSION = '1.21.13'
GO_TARBALL = f'go{GO_VERSION}.linux-amd64.tar.gz'
GO_URL = f'https://go.dev/dl/{GO_TARBALL}'
GO_SDK_DIR = f'{WORKDIR}/go-sdk'
GO_BIN = f'{GO_SDK_DIR}/go/bin/go'


def run_cmd(cmd, check=True, shell=True, timeout=120):
    """Run a shell command and return output."""
    result = subprocess.run(
        cmd, shell=shell, capture_output=True, text=True, timeout=timeout
    )
    if check and result.returncode != 0:
        print(f'CMD FAILED: {cmd}')
        print(f'STDOUT: {result.stdout}')
        print(f'STDERR: {result.stderr}')
        raise RuntimeError(f'Command failed: {cmd}')
    return result


def install_go():
    """Install Go 1.21 to ~/go-sdk if not already present."""
    result = subprocess.run(
        f'{GO_BIN} version',
        shell=True, capture_output=True, text=True
    )
    if result.returncode == 0 and 'go1.21' in result.stdout:
        print(f'Go already installed: {result.stdout.strip()}')
        return

    print(f'Installing Go {GO_VERSION} to {GO_SDK_DIR}...')
    os.makedirs(GO_SDK_DIR, exist_ok=True)

    # Download Go tarball
    run_cmd(f'wget -q -O /tmp/{GO_TARBALL} {GO_URL}', timeout=300)
    # Remove old installation if present
    run_cmd(f'rm -rf {GO_SDK_DIR}/go', check=False)
    # Extract to ~/go-sdk/
    run_cmd(f'tar -C {GO_SDK_DIR} -xzf /tmp/{GO_TARBALL}')
    # Cleanup
    run_cmd(f'rm -f /tmp/{GO_TARBALL}')

    # Add to PATH in bashrc
    bashrc = os.path.expanduser('~/.bashrc')
    path_line = f'export PATH=$PATH:{GO_SDK_DIR}/go/bin'
    with open(bashrc, 'r') as f:
        content = f.read()
    if f'{GO_SDK_DIR}/go/bin' not in content:
        with open(bashrc, 'a') as f:
            f.write(f'\n{path_line}\n')

    # Verify
    result = run_cmd(f'{GO_BIN} version')
    print(f'Installed: {result.stdout.strip()}')


def setup_project():
    """Create empty project directory."""
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f'Project directory created: {PROJECT_DIR}')


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    env["PATH"] = env.get("PATH", "") + f":{GO_SDK_DIR}/go/bin"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def main():
    install_go()
    setup_project()

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print(f'GUI_READY: VSCode opened with {PROJECT_DIR}')


main()
