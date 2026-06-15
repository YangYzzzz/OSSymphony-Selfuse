"""
Initial Setup: Open VSCode with flask-api project folder containing only app.py
Task ID: vscode_gf4_001
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_001'
PROJECT_DIR = f'{WORKDIR}/projects/flask-api'

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
    # 1. Create the project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # 2. Create an empty app.py
    app_py_path = os.path.join(PROJECT_DIR, 'app.py')
    with open(app_py_path, 'w') as f:
        f.write('')  # empty file as specified
    print(f'Created empty app.py at {app_py_path}')

    # 3. Ensure NO venv directory exists
    venv_path = os.path.join(PROJECT_DIR, 'venv')
    if os.path.exists(venv_path):
        import shutil
        shutil.rmtree(venv_path)
        print(f'Removed existing venv at {venv_path}')

    # 4. Ensure NO requirements.txt exists
    req_path = os.path.join(PROJECT_DIR, 'requirements.txt')
    if os.path.exists(req_path):
        os.remove(req_path)
        print(f'Removed existing requirements.txt')

    # 5. Ensure VSCode settings do NOT contain python.defaultInterpreterPath
    import json
    settings_dir = os.path.join(WORKDIR, '.config', 'Code', 'User')
    settings_path = os.path.join(settings_dir, 'settings.json')
    os.makedirs(settings_dir, exist_ok=True)
    try:
        with open(settings_path, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Remove the setting if it exists
    if 'python.defaultInterpreterPath' in settings:
        del settings['python.defaultInterpreterPath']
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=4)
        print('Removed python.defaultInterpreterPath from settings.json')
    else:
        # Write settings if file doesn't exist yet
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=4)
        print('VSCode settings.json is clean (no python.defaultInterpreterPath)')

    # 6. Ensure python3-venv is available (needed by the agent to create venv)
    print('Ensuring python3.10-venv is available...')
    subprocess.run(
        'echo "password" | sudo -S apt-get update -qq && echo "password" | sudo -S apt-get install -y -qq python3.10-venv',
        shell=True, capture_output=True, text=True
    )
    print('python3.10-venv installed')

    print(f'Initial project structure created at {PROJECT_DIR}')

    # 7. Launch VSCode with the project folder (GUI-ready)
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
