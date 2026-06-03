"""
Initial Setup: Network Traffic Analyzer Script
Task ID: os_gf5_027
Domain: os (Python scripting)

Sets up the VM environment: ensures Python3 and Scapy are installed,
opens a terminal window for the user. No traffic_analyzer.py exists yet.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'os_gf5_027'


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
    # Ensure scapy is installed (task says it should be available)
    subprocess.run(
        ["pip3", "install", "scapy"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Make sure no traffic_analyzer.py exists (clean state)
    target = os.path.join(WORKDIR, 'traffic_analyzer.py')
    if os.path.exists(target):
        os.remove(target)

    # Open a terminal for the user to work in
    launch_gui('gnome-terminal', delay_sec=2.0)
    print('Initial setup complete: scapy installed, terminal opened')
    print('GUI_READY: launched terminal with DISPLAY=:0')


create_initial()
