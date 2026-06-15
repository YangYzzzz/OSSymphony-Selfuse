"""
Initial Setup: Rename 'getData' function to 'fetchUserData' using F2 in VSCode
Task ID: vscode_code_035
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_035'
PROJECT_DIR = f'{WORKDIR}/project'
OUTPUT = f'{PROJECT_DIR}/api.js'


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
    # Create the project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Write the initial api.js with 'getData' function (pre-rename state)
    content = """\
async function getData(userId) {
  const response = await fetch(`/api/users/${userId}`);
  return response.json();
}

async function processUser(id) {
  const data = await getData(id);
  if (data.active) {
    console.log('Active user:', data.name);
  }
  return data;
}

// Export the getData function
module.exports = { getData, processUser };
"""
    with open(OUTPUT, 'w') as f:
        f.write(content)

    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open VSCode with the specific file
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
