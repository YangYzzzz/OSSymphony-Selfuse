"""
Initial Setup: Toggle line comments on CSS dark theme rules
Task ID: vscode_code_032
Domain: vs_code

Creates /home/user/web/theme.css with both light and dark theme blocks uncommented,
then opens the file in VSCode so the agent can comment out the dark theme lines.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_032'
WEB_DIR = f'{WORKDIR}/web'
CSS_FILE = f'{WEB_DIR}/theme.css'

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

    # CSS content — dark theme block is fully uncommented (pre-task state)
    css_content = """/* Light theme */
:root {
  --bg-color: #ffffff;
  --text-color: #333333;
  --accent-color: #0066cc;
}

/* Dark theme */
.dark-theme {
  --bg-color: #1a1a2e;
  --text-color: #e0e0e0;
  --accent-color: #4da6ff;
  --border-color: #333355;
  --shadow-color: rgba(0, 0, 0, 0.3);
}
"""

    with open(CSS_FILE, 'w') as f:
        f.write(css_content)

    print(f'Initial file created: {CSS_FILE}')

    # GUI-ready startup: open VSCode with the CSS file
    launch_gui(f'code "{CSS_FILE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with theme.css on DISPLAY=:0')

create_initial()
