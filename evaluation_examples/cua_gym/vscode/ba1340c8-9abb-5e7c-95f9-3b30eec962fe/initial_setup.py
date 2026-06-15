"""
Initial Setup: Format only the calculateTotal function in a JavaScript file
Task ID: vscode_code_005
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_005'
PROJECT_DIR = f'{WORKDIR}/project'
OUTPUT = f'{PROJECT_DIR}/utils.js'


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

    # The initial utils.js file: calculateTotal is minified/unformatted on one line
    # The rest of the file has deliberate odd spacing that must NOT be changed
    initial_content = """\
// Utility functions - DO NOT REFORMAT
const   API_URL =   'https://api.example.com';
const   TIMEOUT =   5000;

function calculateTotal(items){
let total=0;for(let i=0;i<items.length;i++){if(items[i].price>0){total+=items[i].price*items[i].quantity;}}
return total;}

// Legacy code below - DO NOT REFORMAT
var   x =   1;
var   y =   2;
"""

    with open(OUTPUT, 'w') as f:
        f.write(initial_content)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open VSCode with the project folder and the file
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    # Also open the specific file in VSCode
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
