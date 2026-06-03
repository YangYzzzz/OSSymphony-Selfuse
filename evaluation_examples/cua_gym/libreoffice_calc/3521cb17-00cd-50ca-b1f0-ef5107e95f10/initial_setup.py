"""
Initial Setup: Set up empty project directory for AWS serverless workflow
Task ID: vscode_wf_073
Domain: vscode (workflow)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'project')

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
    # Create empty project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f'Created project directory: {PROJECT_DIR}')

    # Ensure no leftover .vscode, src, or other project files exist
    for item in ['template.yaml', 'requirements.txt', 'src', '.vscode']:
        path = os.path.join(PROJECT_DIR, item)
        if os.path.isdir(path):
            import shutil
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)

    # Do NOT install any AWS extensions - task requires the agent to do that
    # Uninstall AWS toolkit if somehow present
    subprocess.run(
        ["code", "--uninstall-extension", "amazonwebservices.aws-toolkit-vscode"],
        capture_output=True, text=True
    )

    # Launch VSCode with the empty project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with empty ~/project')

create_initial()
