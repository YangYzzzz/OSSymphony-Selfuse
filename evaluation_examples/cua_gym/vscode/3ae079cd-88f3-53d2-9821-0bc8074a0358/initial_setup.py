"""
Initial Setup: Emmet form expansion task
Task ID: vscode_code_058
Domain: vs_code

Creates /home/user/web/form.html with a basic HTML structure (no form),
then opens VSCode with the file so the agent can use Emmet to expand the form.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_058'
WEB_DIR = f'{WORKDIR}/web'
OUTPUT = f'{WEB_DIR}/form.html'


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
    # Create the web directory if it doesn't exist
    os.makedirs(WEB_DIR, exist_ok=True)

    # Create the initial HTML file — basic structure WITHOUT a form
    # Cursor position context: after the <h1> tag
    html_content = """<!DOCTYPE html>
<html>
<head><title>Registration</title></head>
<body>
  <h1>Register</h1>

</body>
</html>
"""

    with open(OUTPUT, 'w') as f:
        f.write(html_content)

    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open VSCode with the file
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
