"""
Initial Setup: Install Scheme/Script-Fu VSCode extension and create crop_center.scm
Task ID: osworld_multi_apps_vscode_ext_script_008
Domain: multi_apps (VSCode + OS)

Initial state:
- VSCode is open
- No Scheme or Script-Fu extension is installed
- ~/Desktop/gimp_scripts/ does NOT exist
- No crop_center.scm file exists
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_ext_script_008'
DESKTOP = f'{WORKDIR}/Desktop'
GIMP_SCRIPTS_DIR = f'{DESKTOP}/gimp_scripts'


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


def remove_if_exists(path: str):
    """Remove a file or directory if it exists."""
    import shutil
    if os.path.isfile(path):
        os.remove(path)
        print(f'Removed file: {path}')
    elif os.path.isdir(path):
        shutil.rmtree(path)
        print(f'Removed directory: {path}')


def uninstall_scheme_extensions():
    """Uninstall any Scheme/Script-Fu related VSCode extensions if present."""
    scheme_extension_ids = [
        'stkb.scheme',
        'sorpaas.vscode-scheme',
        'jgehring.scheme-support',
        'gimlixx.scheme-for-vscode',
        'vscode-gimp-script-fu',
        'suketa.vscode-deno',
    ]
    # List currently installed extensions
    try:
        result = subprocess.run(
            ['code', '--list-extensions'],
            capture_output=True,
            text=True,
            timeout=30
        )
        installed = result.stdout.strip().lower()
        for ext_id in scheme_extension_ids:
            if ext_id.lower() in installed:
                subprocess.run(
                    ['code', '--uninstall-extension', ext_id],
                    capture_output=True,
                    timeout=60
                )
                print(f'Uninstalled extension: {ext_id}')
    except Exception as e:
        print(f'Note: Could not check/uninstall extensions: {e}')


def create_initial():
    # 1. Ensure Desktop exists
    os.makedirs(DESKTOP, exist_ok=True)

    # 2. Remove gimp_scripts directory if it exists (should NOT exist in initial state)
    remove_if_exists(GIMP_SCRIPTS_DIR)

    # 3. Uninstall any Scheme/Script-Fu extensions (should NOT be installed in initial state)
    uninstall_scheme_extensions()

    print(f'Initial state prepared:')
    print(f'  - ~/Desktop/gimp_scripts/ does NOT exist')
    print(f'  - No Scheme/Script-Fu VSCode extension installed')

    # 4. GUI-ready startup: open VSCode so the agent can start working
    # Open VSCode with the Desktop folder as workspace context
    launch_gui(f'code "{DESKTOP}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
