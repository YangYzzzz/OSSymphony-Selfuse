"""
Initial Setup: Extract variable refactoring - create app.js with repeated getElementById expression
Task ID: vscode_rrt_033
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_033'
PROJECT_DIR = f'{WORKDIR}/projects/web'
OUTPUT = f'{PROJECT_DIR}/app.js'

INITIAL_CODE = '''\
function updateUI(data) {
    document.getElementById("output").innerHTML = data.title;
    document.getElementById("output").style.color = data.color;
    document.getElementById("output").classList.add("active");
    document.getElementById("output").setAttribute("data-id", data.id);
}
'''

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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Write the initial app.js with repeated getElementById calls
    with open(OUTPUT, 'w') as f:
        f.write(INITIAL_CODE)
    print(f'Initial file created: {OUTPUT}')

    # Open VSCode with the file
    launch_gui(f'code "{OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
