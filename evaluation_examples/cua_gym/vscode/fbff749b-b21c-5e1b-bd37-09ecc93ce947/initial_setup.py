"""
Initial Setup: Set up VSCode with no global snippets file present
Task ID: vscode_code_017
Domain: vs_code

This script prepares the initial state for the task:
- VSCode is open with no global snippets (my-global.code-snippets does not exist)
- The agent must create the global snippet file with prefix 'header'
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_017'

# VSCode config paths (on VM)
HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SNIPPETS_DIR = os.path.join(VSCODE_USER, 'snippets')
GLOBAL_SNIPPETS_FILE = os.path.join(SNIPPETS_DIR, 'my-global.code-snippets')

# Also a sample workspace file for VSCode to open
WORKSPACE_DIR = os.path.join(WORKDIR, 'project')


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


def create_initial():
    # Ensure snippets directory exists
    os.makedirs(SNIPPETS_DIR, exist_ok=True)

    # CRITICAL: Remove any existing global snippets file to ensure clean initial state
    if os.path.exists(GLOBAL_SNIPPETS_FILE):
        os.remove(GLOBAL_SNIPPETS_FILE)
        print(f'Removed existing global snippets file: {GLOBAL_SNIPPETS_FILE}')

    # Ensure VSCode user settings directory exists
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Create a sample workspace/project for VSCode to open
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Create a sample Python file in the workspace
    sample_py = os.path.join(WORKSPACE_DIR, 'main.py')
    if not os.path.exists(sample_py):
        with open(sample_py, 'w') as f:
            f.write(
                "# main.py\n"
                "# This is a sample Python file.\n\n"
                "def greet(name):\n"
                "    \"\"\"Greet a user by name.\"\"\"\n"
                "    return f'Hello, {name}!'\n\n\n"
                "if __name__ == '__main__':\n"
                "    print(greet('World'))\n"
            )
    print(f'Sample workspace created: {WORKSPACE_DIR}')

    # Create a settings.json if not present (basic/clean state)
    settings_path = os.path.join(VSCODE_USER, 'settings.json')
    if not os.path.exists(settings_path):
        with open(settings_path, 'w') as f:
            json.dump({}, f, indent=4)

    print(f'Initial state ready: no global snippets file at {GLOBAL_SNIPPETS_FILE}')

    # GUI-ready startup: open VSCode with the sample workspace
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
