"""
Initial Setup: Open ~/project/data.csv in VSCode with CSV data
Task ID: vscode_wf_019
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_019'
PROJECT_DIR = f'{WORKDIR}/project'
CSV_PATH = f'{PROJECT_DIR}/data.csv'


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

    # Create data.csv with realistic data (5 rows)
    csv_content = """name,age,city
Alice Morgan,29,Seattle
Carlos Rivera,34,Austin
Priya Patel,27,Chicago
James O'Brien,41,Boston
Mei-Ling Zhang,33,San Francisco"""

    with open(CSV_PATH, 'w') as f:
        f.write(csv_content.strip() + '\n')

    print(f'CSV file created: {CSV_PATH}')

    # Make sure data.json does NOT exist
    json_path = f'{PROJECT_DIR}/data.json'
    if os.path.exists(json_path):
        os.remove(json_path)

    # Make sure Rainbow CSV is NOT installed
    result = subprocess.run(
        ['code', '--list-extensions'],
        capture_output=True, text=True
    )
    if 'mechatroner.rainbow-csv' in result.stdout.lower():
        subprocess.run(
            ['code', '--uninstall-extension', 'mechatroner.rainbow-csv'],
            capture_output=True, text=True
        )
        print('Uninstalled rainbow-csv extension from initial env')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)

    # Open the CSV file specifically
    launch_gui(f'code "{CSV_PATH}"', delay_sec=2.0)

    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
