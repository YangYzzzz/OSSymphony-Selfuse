"""
Initial Setup: Extract config object literal into DEFAULT_CONFIG constant
Task ID: vscode_rrt_056
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_056'
PROJECT_DIR = f'{WORKDIR}/projects/server'
OUTPUT = f'{PROJECT_DIR}/app.js'


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
    # Create project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Write the initial app.js with inline config object in createMiddleware
    content = """\
const express = require('express');
const app = express();

app.listen(3000, () => {
    console.log('Server running');
});

function createMiddleware() {
    return {
        cors: true,
        maxAge: 86400,
        methods: ['GET', 'POST', 'PUT', 'DELETE'],
        allowedHeaders: ['Content-Type', 'Authorization'],
        credentials: true
    };
}
"""
    with open(OUTPUT, 'w') as f:
        f.write(content)

    print(f'Initial file created: {OUTPUT}')

    # Launch VSCode with the file open
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
