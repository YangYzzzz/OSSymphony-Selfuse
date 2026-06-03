"""
Initial Setup: Create JavaScript file with duplicated validation logic
Task ID: vscode_rrt_048
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_048'
PROJECT_DIR = f'{WORKDIR}/projects/form'
OUTPUT = f'{PROJECT_DIR}/validation.js'


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

    # Write the initial JavaScript file with duplicated validation logic
    js_content = '''\
function validateForm(data) {
    if (data.age < 0 || data.age > 150) {
        return { valid: false, field: 'age' };
    }
    if (data.score < 0 || data.score > 100) {
        return { valid: false, field: 'score' };
    }
    if (data.temperature < -50 || data.temperature > 60) {
        return { valid: false, field: 'temperature' };
    }
    return { valid: true };
}
'''
    with open(OUTPUT, 'w') as f:
        f.write(js_content)

    print(f'Initial file created: {OUTPUT}')

    # Launch VSCode with the file open
    launch_gui(f'code "{OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
