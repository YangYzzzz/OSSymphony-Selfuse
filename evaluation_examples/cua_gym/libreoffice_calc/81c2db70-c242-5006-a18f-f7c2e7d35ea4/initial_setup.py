"""
Initial Setup: Prepare environment for ZFS setup script task
Task ID: os_gf2_091
Domain: os
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'os_gf2_091'

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
    # Ensure no leftover zfs_setup.sh exists
    script_path = f'{WORKDIR}/{TASK_ID}_zfs_setup.sh'
    # We don't create the script - that's the agent's job
    # The task says /home/user/zfs_setup.sh, so make sure it doesn't exist
    for p in [f'{WORKDIR}/zfs_setup.sh', script_path]:
        if os.path.exists(p):
            os.remove(p)

    # Open a terminal for the user to work in
    launch_gui('gnome-terminal', delay_sec=2.0)
    print('GUI_READY: launched terminal with DISPLAY=:0')

create_initial()
