"""
Initial Setup: Open VSCode with an empty Go project folder
Task ID: vscode_gf4_086
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_086'
PROJECT_DIR = f'{WORKDIR}/projects/go-query-language'


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


def setup():
    # Create empty project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Install Go 1.21 in user home directory
    go_root = f'{WORKDIR}/go-sdk'
    go_bin = f'{go_root}/go/bin'
    go_tar = '/tmp/go1.21.13.linux-amd64.tar.gz'
    if not os.path.exists(f'{go_bin}/go'):
        subprocess.run(
            ['wget', '-q', '-O', go_tar,
             'https://go.dev/dl/go1.21.13.linux-amd64.tar.gz'],
            check=True
        )
        os.makedirs(go_root, exist_ok=True)
        subprocess.run(
            ['tar', '-C', go_root, '-xzf', go_tar],
            check=True
        )
        os.remove(go_tar)

    # Ensure Go is in PATH for this script
    os.environ['PATH'] = f'{go_bin}:{os.environ["PATH"]}'
    os.environ['GOROOT'] = f'{go_root}/go'
    os.environ['GOPATH'] = f'{WORKDIR}/go'

    # Add Go to user's profile for persistence
    bashrc = os.path.join(WORKDIR, '.bashrc')
    go_path_line = f'export PATH={go_bin}:$PATH'
    go_root_line = f'export GOROOT={go_root}/go'
    try:
        with open(bashrc, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        content = ''
    if go_path_line not in content:
        with open(bashrc, 'a') as f:
            f.write(f'\n{go_path_line}\n{go_root_line}\nexport GOPATH={WORKDIR}/go\n')

    # Verify Go installation
    result = subprocess.run([f'{go_bin}/go', 'version'],
                            capture_output=True, text=True)
    print(f'Go installed: {result.stdout.strip()}')

    # Install Go VSCode extension
    subprocess.run(['code', '--install-extension', 'golang.go',
                    '--force'], capture_output=True, text=True)
    print('Go extension installed')

    # Open VSCode with the empty project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print(f'GUI_READY: VSCode opened with {PROJECT_DIR}')


setup()
