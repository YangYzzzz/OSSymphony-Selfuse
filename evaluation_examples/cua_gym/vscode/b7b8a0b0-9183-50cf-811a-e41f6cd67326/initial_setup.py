"""
Initial Setup: Emmet Wrap with Abbreviation - wrap <li> items with <ul>
Task ID: vscode_code_057
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_057'
WEB_DIR = f'{WORKDIR}/web'
HTML_FILE = f'{WEB_DIR}/list.html'


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
    # Create the web directory
    os.makedirs(WEB_DIR, exist_ok=True)

    # Create the HTML file with <li> items NOT wrapped in <ul>
    # (The task asks the agent to wrap them using Emmet's Wrap with Abbreviation)
    html_content = """<!DOCTYPE html>
<html>
<body>
  <div class="shopping-list">
    <li>Milk</li>
    <li>Eggs</li>
    <li>Bread</li>
    <li>Butter</li>
  </div>
</body>
</html>
"""
    with open(HTML_FILE, 'w') as f:
        f.write(html_content)

    print(f'Initial file created: {HTML_FILE}')

    # GUI-ready startup: open VSCode with the HTML file
    launch_gui(f'code "{HTML_FILE}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
