"""
Initial Setup: Create a student homework project with hello.py for debugging task
Task ID: vscode_td_049
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_049'
PROJECT_DIR = os.path.join(WORKDIR, 'homework', 'week3')


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

    # Create hello.py - a simple Python script suitable for debugging practice
    hello_py = os.path.join(PROJECT_DIR, 'hello.py')
    with open(hello_py, 'w') as f:
        f.write('''"""A simple greeting program for Week 3 homework."""


def greet(name):
    """Return a personalized greeting message."""
    message = f"Hello, {name}! Welcome to Python programming."
    return message


def main():
    names = ["Alice", "Bob", "Charlie"]
    for name in names:
        greeting = greet(name)
        print(greeting)
    print("All greetings complete!")


if __name__ == "__main__":
    main()
''')
    print(f'Created: {hello_py}')

    # Ensure NO .vscode folder exists (task requires user to create it)
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)
        print(f'Removed existing .vscode directory')

    # Verify Python extension is installed
    result = subprocess.run(['code', '--list-extensions'], capture_output=True, text=True)
    if 'ms-python.python' not in result.stdout.lower():
        subprocess.run(['code', '--install-extension', 'ms-python.python'], check=False)
        print('Installed Python extension')
    else:
        print('Python extension already installed')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
