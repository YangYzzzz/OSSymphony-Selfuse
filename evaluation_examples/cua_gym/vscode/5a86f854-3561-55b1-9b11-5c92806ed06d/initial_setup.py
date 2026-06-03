"""
Initial Setup: Set up a multi-cell Jupyter notebook that loads CSV, shows stats, and creates a bar chart
Task ID: vscode_lp_036
Domain: vscode

Creates:
- ~/projects/analysis/data.csv with Product, Sales, Region, Quarter columns
- Opens VSCode with the analysis folder
- Ensures Jupyter extension is installed
- NO notebook file exists (that's the agent's task)
"""

import csv
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_036'
PROJECT_DIR = f'{WORKDIR}/projects/analysis'
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

    # Create data.csv with realistic sales data
    data = [
        ['Product', 'Sales', 'Region', 'Quarter'],
        ['Widget Alpha', 15230, 'North America', 'Q1'],
        ['Widget Alpha', 18450, 'North America', 'Q2'],
        ['Widget Alpha', 12890, 'Europe', 'Q1'],
        ['Widget Alpha', 16720, 'Europe', 'Q2'],
        ['Widget Beta', 22100, 'North America', 'Q1'],
        ['Widget Beta', 19870, 'North America', 'Q2'],
        ['Widget Beta', 24530, 'Europe', 'Q1'],
        ['Widget Beta', 21340, 'Europe', 'Q2'],
        ['Gadget Pro', 31200, 'North America', 'Q1'],
        ['Gadget Pro', 28750, 'North America', 'Q2'],
        ['Gadget Pro', 26890, 'Europe', 'Q1'],
        ['Gadget Pro', 33410, 'Europe', 'Q2'],
        ['Sensor Max', 9870, 'North America', 'Q1'],
        ['Sensor Max', 11230, 'North America', 'Q2'],
        ['Sensor Max', 8540, 'Europe', 'Q1'],
        ['Sensor Max', 10680, 'Europe', 'Q2'],
        ['Power Unit', 45600, 'North America', 'Q1'],
        ['Power Unit', 42310, 'North America', 'Q2'],
        ['Power Unit', 38970, 'Europe', 'Q1'],
        ['Power Unit', 41250, 'Europe', 'Q2'],
    ]

    with open(CSV_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

    print(f'CSV file created: {CSV_PATH}')

    # Ensure no notebook files exist in the directory
    for fname in os.listdir(PROJECT_DIR):
        if fname.endswith('.ipynb'):
            os.remove(os.path.join(PROJECT_DIR, fname))
            print(f'Removed existing notebook: {fname}')

    # Install Jupyter extension for VSCode if not already installed
    subprocess.run(['code', '--install-extension', 'ms-toolsai.jupyter'], check=False)
    time.sleep(2)

    # Open VSCode with the analysis folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with analysis folder on DISPLAY=:0')


create_initial()
