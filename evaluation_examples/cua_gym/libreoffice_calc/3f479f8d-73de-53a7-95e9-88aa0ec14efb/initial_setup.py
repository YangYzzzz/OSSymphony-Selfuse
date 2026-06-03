"""
Initial Setup: Install Terraform CLI - pre-task state
Task ID: osworld_multi_apps_cli_path_fix_011
Domain: os (CLI / PATH configuration)

Sets up the initial state where:
- Terraform binary is NOT installed
- Chrome browser is open
- Terminal (gnome-terminal) is open
- ~/.bashrc does NOT have any terraform PATH entry
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_cli_path_fix_011'


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


def setup_initial():
    # ------------------------------------------------------------------
    # 1. Ensure terraform is NOT installed (remove if present)
    # ------------------------------------------------------------------
    terraform_paths = [
        '/usr/local/bin/terraform',
        '/usr/bin/terraform',
        os.path.join(WORKDIR, 'bin', 'terraform'),
    ]
    for path in terraform_paths:
        if os.path.exists(path):
            os.remove(path)
            print(f'Removed existing terraform binary: {path}')

    # ------------------------------------------------------------------
    # 2. Clean up any terraform PATH lines from ~/.bashrc
    # ------------------------------------------------------------------
    bashrc_path = os.path.join(WORKDIR, '.bashrc')
    if os.path.exists(bashrc_path):
        with open(bashrc_path, 'r') as f:
            lines = f.readlines()
        cleaned = [
            line for line in lines
            if 'terraform' not in line.lower()
        ]
        with open(bashrc_path, 'w') as f:
            f.writelines(cleaned)
        print(f'Cleaned terraform entries from {bashrc_path}')
    else:
        # Create a minimal ~/.bashrc if missing
        with open(bashrc_path, 'w') as f:
            f.write('# ~/.bashrc: executed by bash for non-login shells.\n')
            f.write('export PATH="$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"\n')
        print(f'Created minimal {bashrc_path}')

    # ------------------------------------------------------------------
    # 3. Ensure ~/bin directory does NOT contain terraform
    # ------------------------------------------------------------------
    user_bin = os.path.join(WORKDIR, 'bin')
    os.makedirs(user_bin, exist_ok=True)
    user_terraform = os.path.join(user_bin, 'terraform')
    if os.path.exists(user_terraform):
        os.remove(user_terraform)
        print(f'Removed terraform from ~/bin')

    # ------------------------------------------------------------------
    # 4. Verify terraform is not accessible
    # ------------------------------------------------------------------
    result = subprocess.run(['which', 'terraform'], capture_output=True, text=True)
    if result.returncode == 0:
        print(f'WARNING: terraform still found at {result.stdout.strip()} — check PATH')
    else:
        print('Confirmed: terraform is NOT installed (as required)')

    print(f'\nInitial state configured:')
    print(f'  - No terraform binary installed')
    print(f'  - ~/.bashrc cleared of terraform PATH entries')

    # ------------------------------------------------------------------
    # 5. GUI-ready startup: open Chrome and a Terminal
    # ------------------------------------------------------------------
    # Open Chrome (Google Chrome or Chromium)
    launch_gui('google-chrome --new-window "https://developer.hashicorp.com/terraform/install"', delay_sec=2.0)

    # Open GNOME Terminal
    launch_gui('gnome-terminal', delay_sec=1.5)

    print('GUI_READY: Launched Chrome and Terminal with DISPLAY=:0')


setup_initial()
