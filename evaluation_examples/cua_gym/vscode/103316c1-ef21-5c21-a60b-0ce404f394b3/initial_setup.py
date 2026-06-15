"""
Initial Setup: Configure VSCode with ~/projects/data-viz folder for polyglot notebook task
Task ID: vscode_gf5_024
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_024'
PROJECT_DIR = f'{WORKDIR}/projects/data-viz'


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
    # 1. Create project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create some realistic sample data files for the data-viz project
    # A CSV dataset the researcher might want to explore
    csv_content = """date,category,revenue,units_sold,region
2024-01-15,Electronics,45230.50,312,North America
2024-01-15,Clothing,28750.00,587,Europe
2024-01-15,Electronics,31200.75,198,Europe
2024-01-15,Food & Beverage,15430.25,1043,North America
2024-02-15,Electronics,52100.00,356,North America
2024-02-15,Clothing,33420.50,621,Europe
2024-02-15,Electronics,29870.30,187,Asia Pacific
2024-02-15,Food & Beverage,18200.75,1187,North America
2024-03-15,Electronics,48900.25,334,North America
2024-03-15,Clothing,36100.00,698,Europe
2024-03-15,Electronics,34500.50,223,Asia Pacific
2024-03-15,Food & Beverage,21350.00,1302,North America
2024-04-15,Electronics,55700.75,389,North America
2024-04-15,Clothing,31800.25,572,Europe
2024-04-15,Electronics,37200.00,245,Asia Pacific
2024-04-15,Food & Beverage,19800.50,1156,North America
"""
    with open(os.path.join(PROJECT_DIR, 'sales_data.csv'), 'w') as f:
        f.write(csv_content.strip() + '\n')

    # A README for the project
    readme_content = """# Data Visualization Project

## Overview
This project explores quarterly sales data across multiple regions and product categories.
The goal is to build interactive visualizations combining C# data processing with JavaScript
charting using Vega-Lite in a polyglot notebook environment.

## Data Sources
- `sales_data.csv` - Quarterly sales records (Jan-Apr 2024)

## Setup
1. Open this folder in VSCode
2. Install the Polyglot Notebooks extension
3. Create a new .ipynb notebook to begin analysis
"""
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme_content)

    print(f'Project directory created: {PROJECT_DIR}')
    print(f'Files: sales_data.csv, README.md')

    # 2. Ensure Polyglot Notebooks extension is NOT installed
    #    (Uninstall if present, to guarantee clean initial state)
    try:
        subprocess.run(
            ['code', '--uninstall-extension', 'ms-dotnettools.dotnet-interactive-vscode'],
            capture_output=True, text=True, timeout=30
        )
    except Exception:
        pass

    # 3. Make sure exploration.ipynb does NOT exist
    notebook_path = os.path.join(PROJECT_DIR, 'exploration.ipynb')
    if os.path.exists(notebook_path):
        os.remove(notebook_path)

    # 4. Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
