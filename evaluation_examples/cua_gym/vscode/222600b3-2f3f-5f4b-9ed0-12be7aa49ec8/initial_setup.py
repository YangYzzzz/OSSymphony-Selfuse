"""
Initial Setup: VSCode Format Selection task - config.js with compact settings object
Task ID: vscode_code_006
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'  # VM path — all scripts run on the VM
TASK_ID = 'vscode_code_006'
PROJECT_DIR = f'{WORKDIR}/project'
OUTPUT = f'{PROJECT_DIR}/config.js'


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

    # The initial file: settings object is all on one compact line (unformatted)
    # The agent's task is to select the settings block and use Format Selection (Ctrl+K Ctrl+F)
    content = (
        "module.exports = {\n"
        "  name: 'MyApp',\n"
        "  version: '1.0.0',\n"
        "  settings: {debug:true,logging:{level:'info',format:'json',output:{file:'/var/log/app.log',console:true,rotation:{maxSize:'10mb',maxFiles:5}}},cache:{enabled:true,ttl:3600}},\n"
        "  description: 'A sample application'\n"
        "};\n"
    )

    with open(OUTPUT, 'w') as f:
        f.write(content)

    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open VSCode with the specific file open in editor
    launch_gui(f'code "{OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
