"""
Initial Setup: Configure VSCode for Terraform infrastructure-as-code editing
Task ID: osworld_multi_apps_vscode_ext_script_010
Domain: multi_apps (VSCode + OS filesystem)

Initial state:
  - VSCode is open
  - No Terraform extension installed
  - ~/Desktop/infra/ does NOT exist
  - No main.tf file
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_ext_script_010'
DESKTOP_DIR = f'{WORKDIR}/Desktop'
INFRA_DIR = f'{DESKTOP_DIR}/infra'


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
    # Ensure Desktop directory exists
    os.makedirs(DESKTOP_DIR, exist_ok=True)

    # Ensure infra directory does NOT exist (task asks agent to set it up)
    if os.path.exists(INFRA_DIR):
        import shutil
        shutil.rmtree(INFRA_DIR)
        print(f'Removed pre-existing infra directory: {INFRA_DIR}')

    # Ensure hashicorp.terraform extension is NOT installed
    result = subprocess.run(
        ['code', '--list-extensions'],
        capture_output=True, text=True
    )
    installed_extensions = result.stdout.strip().splitlines()
    terraform_ext_id = 'hashicorp.terraform'
    if any(ext.lower() == terraform_ext_id.lower() for ext in installed_extensions):
        subprocess.run(
            ['code', '--uninstall-extension', terraform_ext_id],
            capture_output=True, text=True
        )
        print(f'Uninstalled extension: {terraform_ext_id}')
        time.sleep(2.0)
    else:
        print(f'Extension {terraform_ext_id} is not installed (as expected).')

    print('Initial state created: VSCode open, no Terraform extension, no infra/ directory.')

    # GUI-ready: Open VSCode pointing to Desktop directory
    launch_gui(f'code "{DESKTOP_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
