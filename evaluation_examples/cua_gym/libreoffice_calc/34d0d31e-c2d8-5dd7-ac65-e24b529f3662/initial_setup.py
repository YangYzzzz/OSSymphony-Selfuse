"""
Initial Setup: VSCode Jupyter notebook data analysis workflow
Task ID: vscode_gf5_014
Domain: vscode (python/jupyter)

Creates:
- ~/projects/python-data/ directory (empty workspace)
- ~/data/sales.csv with realistic monthly sales data
- Opens VSCode with the project folder
"""

import os
import shlex
import subprocess
import time
import csv

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_014'

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
    # 1. Create project directory (empty, no venv, no notebook)
    project_dir = os.path.join(WORKDIR, 'projects', 'python-data')
    os.makedirs(project_dir, exist_ok=True)
    print(f'Created project directory: {project_dir}')

    # 2. Create ~/data/sales.csv with realistic monthly sales data
    data_dir = os.path.join(WORKDIR, 'data')
    os.makedirs(data_dir, exist_ok=True)
    csv_path = os.path.join(data_dir, 'sales.csv')

    sales_data = [
        ['Month', 'Revenue', 'Units'],
        ['January', 45230.50, 312],
        ['February', 38910.75, 267],
        ['March', 52140.00, 389],
        ['April', 41875.25, 295],
        ['May', 63420.80, 442],
        ['June', 58310.60, 401],
        ['July', 71250.00, 498],
        ['August', 67890.45, 463],
        ['September', 54320.90, 378],
        ['October', 49875.30, 341],
        ['November', 82150.00, 567],
        ['December', 91430.25, 634],
    ]

    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(sales_data)
    print(f'Created sales data: {csv_path}')

    # 3. Ensure no venv or notebook exists (clean state)
    venv_path = os.path.join(project_dir, 'venv')
    notebook_path = os.path.join(project_dir, 'data_analysis.ipynb')
    if os.path.exists(venv_path):
        import shutil
        shutil.rmtree(venv_path)
        print('Removed existing venv')
    if os.path.exists(notebook_path):
        os.remove(notebook_path)
        print('Removed existing notebook')

    # 4. Open VSCode with the project folder
    launch_gui(f'code "{project_dir}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
