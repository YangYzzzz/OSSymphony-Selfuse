"""
Initial Setup: Set up environment for numpy project setup task
Task ID: osworld_multi_apps_vscode_env_setup_003
Domain: multi_apps / vscode / os

Initial state:
- /home/user/numpy does NOT exist (agent must clone it)
- Build dependencies (cython, meson-python, build) are NOT installed
- Chrome, Terminal, and VSCode are open for the agent to use
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_env_setup_003'

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


def ensure_clean_state():
    """Ensure /home/user/numpy does NOT exist and build deps are NOT installed."""

    # Remove /home/user/numpy if it somehow exists
    numpy_dir = os.path.join(WORKDIR, 'numpy')
    if os.path.exists(numpy_dir):
        import shutil
        shutil.rmtree(numpy_dir)
        print(f'Removed existing {numpy_dir}')

    # Uninstall build dependencies if they are installed (so initial state is clean)
    packages_to_remove = ['cython', 'meson-python', 'build']
    for pkg in packages_to_remove:
        result = subprocess.run(
            ['pip3', 'show', pkg],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            subprocess.run(
                ['pip3', 'uninstall', '-y', pkg],
                capture_output=True, text=True
            )
            print(f'Uninstalled {pkg} for clean initial state')

    print('Initial state verified: /home/user/numpy absent, build deps not installed')


def create_reference_note():
    """Create a reference note file with instructions visible in the home folder."""
    note_path = os.path.join(WORKDIR, 'README_task.txt')
    content = (
        "Task: Set up the numpy project environment\n"
        "\n"
        "Steps:\n"
        "1. Clone the numpy repo: git clone https://github.com/numpy/numpy /home/user/numpy\n"
        "2. Install build dependencies: pip3 install cython meson-python build\n"
        "3. Verify: python3 -c \"import numpy\"\n"
        "\n"
        "Reference: https://github.com/numpy/numpy\n"
    )
    with open(note_path, 'w') as f:
        f.write(content)
    print(f'Reference note created: {note_path}')


def setup_initial():
    ensure_clean_state()
    create_reference_note()

    # Launch Chrome open to the numpy GitHub page for reference
    launch_gui('google-chrome https://github.com/numpy/numpy', delay_sec=2.0)

    # Launch a terminal for the agent to use
    launch_gui('gnome-terminal', delay_sec=1.5)

    # Launch VSCode in the home directory
    launch_gui(f'code "{WORKDIR}"', delay_sec=2.0)

    print(f'GUI_READY: Chrome (numpy GitHub), Terminal, VSCode launched with DISPLAY=:0')
    print(f'Initial env setup complete for task: {TASK_ID}')


setup_initial()
