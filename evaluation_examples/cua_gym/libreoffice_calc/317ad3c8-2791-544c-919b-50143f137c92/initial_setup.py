"""
Initial Setup: kubectl not installed - open Terminal and Chrome
Task ID: osworld_multi_apps_cli_path_fix_010
Domain: os
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_cli_path_fix_010'


def launch_gui(command: str, delay_sec: float = 1.5):
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


def setup_initial():
    # Ensure kubectl is removed from PATH and not installed
    # Remove kubectl binary if it exists
    kubectl_paths = [
        '/usr/local/bin/kubectl',
        '/usr/bin/kubectl',
        '/snap/bin/kubectl',
        f'{WORKDIR}/.local/bin/kubectl',
        f'{WORKDIR}/bin/kubectl',
    ]
    for kpath in kubectl_paths:
        if os.path.exists(kpath):
            try:
                os.remove(kpath)
                print(f'Removed existing kubectl at {kpath}')
            except Exception as e:
                print(f'Could not remove {kpath}: {e}')

    # Remove any kubectl PATH entries from ~/.bashrc to ensure clean state
    bashrc_path = f'{WORKDIR}/.bashrc'
    if os.path.exists(bashrc_path):
        with open(bashrc_path, 'r') as f:
            lines = f.readlines()
        # Filter out lines that reference kubectl
        cleaned = [l for l in lines if 'kubectl' not in l]
        with open(bashrc_path, 'w') as f:
            f.writelines(cleaned)
        print('Cleaned kubectl entries from ~/.bashrc')

    print(f'Initial state ready: kubectl is not installed')

    # GUI-ready startup: open Terminal and Chrome as required by task context
    launch_gui('gnome-terminal', delay_sec=2.0)
    launch_gui('google-chrome --new-window', delay_sec=2.0)
    print('GUI_READY: launched terminal and chrome with DISPLAY=:0')


setup_initial()
