"""
Initial Setup: Initialize git repository environment for branch topology task
Task ID: vscode_git_076
Domain: vs_code (git)

Creates an empty /home/user/new-project directory (no git repo yet).
The agent must: init the repo, create branches, commits, and visualize with git log.
"""

import os
import shlex
import subprocess
import shutil
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_076'
PROJECT_DIR = f'{WORKDIR}/new-project'


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
    # Remove existing directory if present (idempotent)
    if os.path.exists(PROJECT_DIR):
        shutil.rmtree(PROJECT_DIR)

    # Create the empty project directory (NO git init — agent must do that)
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Add a README placeholder so the directory is not completely empty
    # but has no git repo
    readme_path = os.path.join(PROJECT_DIR, 'README.md')
    with open(readme_path, 'w') as f:
        f.write("# new-project\n\nA new project to demonstrate Git branching workflows.\n")

    # Add a basic project file to give the agent something to commit
    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)

    main_py = os.path.join(src_dir, 'main.py')
    with open(main_py, 'w') as f:
        f.write(
            '"""Main module for new-project."""\n\n'
            'def main():\n'
            '    print("Hello from new-project!")\n\n'
            'if __name__ == "__main__":\n'
            '    main()\n'
        )

    print(f'Initial project directory created: {PROJECT_DIR}')
    print(f'  Contents: README.md, src/main.py')
    print(f'  NOTE: No git repository initialized — agent must do this.')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with project folder (DISPLAY=:0)')


create_initial()
