"""
Initial Setup: Create environment for bash string operations script task
Task ID: os_gf2_039
Domain: os
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'os_gf2_039'

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
    # Ensure no pre-existing script at the target path
    target = os.path.join(WORKDIR, 'string_ops.sh')
    if os.path.exists(target):
        os.remove(target)

    # Open a terminal so the agent can start working immediately
    launch_gui('gnome-terminal', delay_sec=2.0)
    print('GUI_READY: launched gnome-terminal with DISPLAY=:0')

create_initial()
