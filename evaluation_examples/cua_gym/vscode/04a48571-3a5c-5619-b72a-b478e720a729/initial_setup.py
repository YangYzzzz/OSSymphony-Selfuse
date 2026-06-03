"""
Initial Setup: Create a Python project with calculator module, open in VSCode.
Task ID: vscode_wf_017
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_017'
PROJECT_DIR = f'{WORKDIR}/project'

VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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

    # Create calculator.py with add and subtract functions
    calculator_content = '''\
"""Calculator module with basic arithmetic operations."""


def add(a, b):
    """Return the sum of two numbers."""
    return a + b


def subtract(a, b):
    """Return the difference of two numbers."""
    return a - b


def multiply(a, b):
    """Return the product of two numbers."""
    return a * b


def divide(a, b):
    """Return the quotient of two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
'''
    with open(os.path.join(PROJECT_DIR, 'calculator.py'), 'w') as f:
        f.write(calculator_content)

    # Ensure NO tests directory exists
    tests_dir = os.path.join(PROJECT_DIR, 'tests')
    if os.path.exists(tests_dir):
        import shutil
        shutil.rmtree(tests_dir)

    # Ensure settings.json does NOT have python.testing settings
    # Load existing settings, remove any testing keys if present
    os.makedirs(VSCODE_USER, exist_ok=True)
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                import re
                content = f.read()
                content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
                settings = json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Remove any python testing settings that might exist
    keys_to_remove = [k for k in settings if k.startswith('python.testing.')]
    for k in keys_to_remove:
        del settings[k]

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'calculator.py created with add() and subtract() functions')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
