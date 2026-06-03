"""
Initial Setup: Clone scikit-learn, install dependencies, install in editable mode
Task ID: osworld_multi_apps_vscode_env_setup_006
Domain: multi_apps (Chrome + Terminal + VSCode)

Initial state:
  - Chrome is open showing the scikit-learn GitHub page
  - Terminal is available
  - VSCode is available
  - /home/user/scikit-learn does NOT exist yet
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_env_setup_006'
REPO_DIR = f'{WORKDIR}/scikit-learn'


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


def create_initial():
    # Ensure /home/user/scikit-learn does NOT exist (clean state)
    if os.path.isdir(REPO_DIR):
        import shutil
        shutil.rmtree(REPO_DIR)
        print(f'Removed existing {REPO_DIR} to ensure clean initial state')

    print(f'Initial state: {REPO_DIR} does not exist.')

    # Open Chrome with the scikit-learn GitHub page (as described in context)
    launch_gui(
        'google-chrome --new-window "https://github.com/scikit-learn/scikit-learn"',
        delay_sec=2.5
    )
    print('Launched Chrome with scikit-learn GitHub page.')

    # Open a terminal (gnome-terminal) for the agent to use
    launch_gui('gnome-terminal', delay_sec=1.5)
    print('Launched gnome-terminal.')

    # Open VSCode in the home directory
    launch_gui(f'code "{WORKDIR}"', delay_sec=2.0)
    print('Launched VSCode.')

    print('GUI_READY: launched Chrome (GitHub), gnome-terminal, and VSCode with DISPLAY=:0')


create_initial()
