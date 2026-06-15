"""
Initial Setup: Clone PyTorch from source and install dependencies
Task ID: osworld_multi_apps_vscode_env_setup_013
Domain: os (multi-app: terminal + chrome)

Initial state: Chrome is open for reference. Terminal is available.
/home/user/pytorch does NOT exist.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_env_setup_013'


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


def ensure_pytorch_not_present():
    """Ensure /home/user/pytorch does not exist (initial state requirement)."""
    pytorch_dir = os.path.join(WORKDIR, 'pytorch')
    if os.path.exists(pytorch_dir):
        import shutil
        shutil.rmtree(pytorch_dir)
        print(f'Removed existing {pytorch_dir}')
    print('Verified: /home/user/pytorch does not exist')


def setup_initial_state():
    """Set up the initial environment state for the task."""
    # Ensure pytorch repo is NOT present (task requires agent to clone it)
    ensure_pytorch_not_present()

    # Create a helpful README on the Desktop to give context
    desktop_dir = os.path.join(WORKDIR, 'Desktop')
    os.makedirs(desktop_dir, exist_ok=True)

    # Create a task hint file (not part of task completion, just context)
    hint_path = os.path.join(desktop_dir, 'task_hint.txt')
    with open(hint_path, 'w') as f:
        f.write(
            "Task: Set up PyTorch from source\n"
            "Steps:\n"
            "1. Clone: git clone https://github.com/pytorch/pytorch /home/user/pytorch\n"
            "2. Install deps: pip install -r /home/user/pytorch/requirements.txt\n"
            "3. Install torch: pip install torch (or python setup.py install)\n"
            "4. Verify: python -c \"import torch\"\n"
        )
    print(f'Created task hint at {hint_path}')

    # Open Chrome (for reference) and a terminal
    # Open Chrome with the PyTorch GitHub page as reference
    launch_gui(
        'google-chrome --new-window "https://github.com/pytorch/pytorch"',
        delay_sec=2.0
    )

    # Open a GNOME terminal for the user to work in
    launch_gui('gnome-terminal', delay_sec=1.5)

    print('GUI_READY: launched Chrome and terminal with DISPLAY=:0')


setup_initial_state()
