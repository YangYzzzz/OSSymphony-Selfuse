"""
Initial Setup: Create empty keybindings.json and open VSCode
Task ID: vscode_rrt_080
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
KEYBINDINGS_PATH = os.path.join(VSCODE_USER, 'keybindings.json')


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
    # Ensure the VSCode user config directory exists
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Write an empty keybindings.json array
    with open(KEYBINDINGS_PATH, 'w') as f:
        json.dump([], f, indent=4)
    print(f'Initial keybindings.json created: {KEYBINDINGS_PATH}')

    # Also create a small workspace folder so VSCode has something to open
    workspace_dir = os.path.join(HOME, 'workspace')
    os.makedirs(workspace_dir, exist_ok=True)

    readme_path = os.path.join(workspace_dir, 'README.md')
    if not os.path.exists(readme_path):
        with open(readme_path, 'w') as f:
            f.write('# Terminal Management Project\n\n'
                    'This workspace is used for terminal management tasks.\n')

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{workspace_dir}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
