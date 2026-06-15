"""
Initial Setup: VSCode open, no Docker extension installed, ~/Desktop/myapp/ does not exist.
Task ID: osworld_multi_apps_vscode_ext_script_013
Domain: vscode / os
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_ext_script_013'
DESKTOP = f'{WORKDIR}/Desktop'
MYAPP_DIR = f'{DESKTOP}/myapp'


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
    # --- Ensure Desktop directory exists ---
    os.makedirs(DESKTOP, exist_ok=True)

    # --- Ensure ~/Desktop/myapp does NOT exist (remove if present from a previous run) ---
    if os.path.exists(MYAPP_DIR):
        import shutil
        shutil.rmtree(MYAPP_DIR)
    print(f'Confirmed ~/Desktop/myapp does not exist.')

    # --- Uninstall Docker extension if it happens to be installed (idempotent reset) ---
    try:
        result = subprocess.run(
            ['code', '--list-extensions'],
            capture_output=True, text=True, timeout=30
        )
        if 'ms-azuretools.vscode-docker' in result.stdout.lower():
            subprocess.run(
                ['code', '--uninstall-extension', 'ms-azuretools.vscode-docker'],
                capture_output=True, text=True, timeout=60
            )
            print('Uninstalled ms-azuretools.vscode-docker to reset state.')
        else:
            print('Docker extension not installed — initial state confirmed.')
    except Exception as e:
        print(f'Extension check skipped: {e}')

    # --- Open VSCode (no folder, just the editor) ---
    launch_gui('code', delay_sec=3.0)
    print('GUI_READY: VSCode launched with DISPLAY=:0')


create_initial()
