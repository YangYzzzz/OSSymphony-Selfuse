"""
Initial Setup: Configure VSCode workspace trust and Data Science profile
Task ID: vscode_gf5_040
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_040'
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
    # Ensure VSCode user config directory exists
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Create a workspace with some sample project files that a developer might have
    project_dir = os.path.join(WORKDIR, 'workspace')
    os.makedirs(project_dir, exist_ok=True)

    # Create some sample files to make the workspace realistic
    # A simple Python data science script
    ds_dir = os.path.join(project_dir, 'data_analysis')
    os.makedirs(ds_dir, exist_ok=True)

    with open(os.path.join(ds_dir, 'analyze.py'), 'w') as f:
        f.write('''"""
Quarterly Sales Analysis Script
Analyzes Q1-Q4 2025 revenue data across regions.
"""
import csv
import statistics

def load_sales_data(filepath):
    """Load sales CSV and return list of dicts."""
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)

def compute_regional_totals(data):
    """Aggregate revenue by region."""
    totals = {}
    for row in data:
        region = row['region']
        revenue = float(row['revenue'])
        totals[region] = totals.get(region, 0) + revenue
    return totals

def main():
    data = load_sales_data('sales_q1_q4_2025.csv')
    totals = compute_regional_totals(data)
    for region, total in sorted(totals.items()):
        print(f"{region}: ${total:,.2f}")

if __name__ == '__main__':
    main()
''')

    with open(os.path.join(ds_dir, 'sales_q1_q4_2025.csv'), 'w') as f:
        f.write('region,quarter,revenue,units_sold\n')
        f.write('North America,Q1,245300.50,1230\n')
        f.write('North America,Q2,312400.75,1567\n')
        f.write('Europe,Q1,189750.25,945\n')
        f.write('Europe,Q2,201300.00,1012\n')
        f.write('Asia Pacific,Q1,156200.80,782\n')
        f.write('Asia Pacific,Q2,178900.60,893\n')

    with open(os.path.join(ds_dir, 'requirements.txt'), 'w') as f:
        f.write('pandas>=2.0.0\nnumpy>=1.24.0\nmatplotlib>=3.7.0\nscikit-learn>=1.3.0\njupyterlab>=4.0.0\n')

    # A Jupyter notebook stub (JSON format)
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["# Sales Data Exploration\n", "Exploring Q1-Q4 2025 regional sales data."]
            },
            {
                "cell_type": "code",
                "metadata": {},
                "source": ["import pandas as pd\nimport matplotlib.pyplot as plt\n"],
                "execution_count": None,
                "outputs": []
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }
    with open(os.path.join(ds_dir, 'exploration.ipynb'), 'w') as f:
        json.dump(notebook, f, indent=2)

    # A web dev project directory (to show why profiles are useful)
    webdev_dir = os.path.join(project_dir, 'webapp_frontend')
    os.makedirs(webdev_dir, exist_ok=True)
    with open(os.path.join(webdev_dir, 'index.html'), 'w') as f:
        f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Acme Corp</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header><h1>Acme Corp Dashboard</h1></header>
    <main id="app"></main>
    <script src="app.js"></script>
</body>
</html>
''')

    with open(os.path.join(webdev_dir, 'app.js'), 'w') as f:
        f.write('// Dashboard application entry point\nconsole.log("Acme Corp Dashboard loaded");\n')

    # A markdown notes file
    with open(os.path.join(project_dir, 'README.md'), 'w') as f:
        f.write('''# Development Workspace

This workspace contains multiple project types:

## Projects
- **data_analysis/** - Python data science scripts and notebooks
- **webapp_frontend/** - Acme Corp dashboard frontend

## Setup Notes
- Each project type benefits from different VSCode extensions and settings
- Consider using VSCode Profiles to manage per-project configurations
''')

    # Write default VSCode settings (minimal, no profile-related settings)
    settings = {
        "workbench.colorTheme": "Default Light Modern",
        "editor.fontSize": 12,
        "editor.tabSize": 4,
        "editor.minimap.enabled": True,
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000
    }
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'Settings written to {SETTINGS_PATH}')

    # Make sure ~/profiles directory does NOT exist (task requires creating it)
    profiles_dir = os.path.join(WORKDIR, 'profiles')
    if os.path.exists(profiles_dir):
        import shutil
        shutil.rmtree(profiles_dir)

    print(f'Initial workspace created at {project_dir}')

    # GUI-ready startup: open VSCode with the workspace
    launch_gui(f'code "{project_dir}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
