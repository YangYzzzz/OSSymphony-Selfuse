"""
Initial Setup: Clone Hugging Face Transformers and install with torch
Task ID: osworld_multi_apps_vscode_env_setup_004
Domain: os / vscode (terminal + package installation task)

Initial state:
  - Chrome is open for reference
  - Terminal is available
  - /home/user/transformers does NOT exist
  - transformers package may or may not be installed (we uninstall to clean state)
"""

import os
import shlex
import shutil
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_env_setup_004'
REPO_DIR = f'{WORKDIR}/transformers'


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


def setup_initial():
    # 1. Ensure /home/user/transformers does NOT exist (clean pre-task state)
    if os.path.exists(REPO_DIR):
        shutil.rmtree(REPO_DIR)
        print(f'Removed existing {REPO_DIR} to ensure clean initial state')

    # 2. Uninstall transformers if installed, to ensure pre-task state
    #    (the task requires the agent to install it themselves)
    subprocess.run(
        ['pip3', 'uninstall', '-y', 'transformers'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print('Uninstalled transformers package (if present) to ensure clean state')

    # 3. Open Chrome for reference (context says "Chrome is open for reference")
    launch_gui('google-chrome --no-first-run', delay_sec=2.0)

    # 4. Open a GNOME Terminal so the agent can run commands
    launch_gui('gnome-terminal', delay_sec=1.5)

    print(f'Initial state ready:')
    print(f'  - {REPO_DIR} does not exist: {not os.path.exists(REPO_DIR)}')
    print(f'  - Chrome launched for reference')
    print(f'  - Terminal launched for agent use')
    print('GUI_READY: launched Chrome and terminal with DISPLAY=:0')


setup_initial()
