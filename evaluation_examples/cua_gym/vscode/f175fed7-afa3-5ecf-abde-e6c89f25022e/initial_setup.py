"""
Initial Setup: Add JSDoc documentation for two functions in math.js
Task ID: vscode_code_033
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_033'
PROJECT_DIR = f'{WORKDIR}/project'
OUTPUT = f'{PROJECT_DIR}/math.js'


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

    # Write the initial math.js file WITHOUT JSDoc comments
    math_js_content = """\
function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

function factorial(n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1);
}

module.exports = { fibonacci, factorial };
"""

    with open(OUTPUT, 'w') as f:
        f.write(math_js_content)

    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open VSCode with the project folder and the specific file
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    time.sleep(1.0)
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with project and math.js file (DISPLAY=:0)')


create_initial()
