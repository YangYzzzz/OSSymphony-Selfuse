"""
Initial Setup: Extract inline type annotation into a separate named interface
Task ID: vscode_rrt_038
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_038'
PROJECT_DIR = f'{WORKDIR}/projects/app'
OUTPUT = f'{PROJECT_DIR}/user.ts'


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
    # Create directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # TypeScript file with inline type annotations (NO separate interface)
    content = """\
function displayUser(user: { name: string; email: string; age: number; role: 'admin' | 'user' }) {
    console.log(`${user.name} (${user.email}) - ${user.role}`);
}

function updateUser(user: { name: string; email: string; age: number; role: 'admin' | 'user' }, data: Partial<{ name: string; email: string; age: number; role: 'admin' | 'user' }>) {
    return { ...user, ...data };
}
"""

    with open(OUTPUT, 'w') as f:
        f.write(content)

    print(f'Initial file created: {OUTPUT}')

    # Launch VSCode with the file open
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
