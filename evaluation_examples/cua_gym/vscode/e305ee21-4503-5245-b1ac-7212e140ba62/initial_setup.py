"""
Initial Setup: Set up C++ development environment in ~/project
Task ID: vscode_wf_062
Domain: vscode

Initial state: VSCode open with empty ~/project directory.
No C++ extensions, no source files, no configs.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'project')


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
    # Ensure ~/project exists and is empty
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Verify no C++ extensions are installed (uninstall if present)
    for ext_id in ['ms-vscode.cpptools', 'ms-vscode.cmake-tools']:
        result = subprocess.run(
            ['code', '--list-extensions'],
            capture_output=True, text=True
        )
        if ext_id in result.stdout:
            subprocess.run(['code', '--uninstall-extension', ext_id],
                           capture_output=True, text=True)
            print(f'Uninstalled pre-existing extension: {ext_id}')

    print(f'Empty project directory ready: {PROJECT_DIR}')

    # Launch VSCode with the empty project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
