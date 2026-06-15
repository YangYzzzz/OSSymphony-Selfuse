"""
Initial Setup: Insert a 'switch' statement inside the processCommand function
Task ID: vscode_code_022
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_022'
PROJECT_DIR = f'{WORKDIR}/project'
OUTPUT = f'{PROJECT_DIR}/commands.js'


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
    # Create project directory if it doesn't exist
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create the initial commands.js file with empty processCommand function
    js_content = """function processCommand(command) {
  // Handle different commands

}

module.exports = { processCommand };
"""

    with open(OUTPUT, 'w') as f:
        f.write(js_content)

    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open VSCode with the project folder and the specific file
    launch_gui(f'code "{PROJECT_DIR}" "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
