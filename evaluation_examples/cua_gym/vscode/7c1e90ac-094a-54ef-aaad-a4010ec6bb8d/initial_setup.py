"""
Initial Setup: Git stash workflow with untracked files
Task ID: vscode_git_046
Domain: vs_code

Creates a git repository at /home/user/project on branch 'feature/dashboard'
with a modified tracked file (dashboard.py) and an untracked file (chart_utils.py).
No stash exists yet.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_046'
PROJECT_DIR = f'{WORKDIR}/project'


def run(cmd, cwd=None, check=True, env=None):
    """Run a shell command, return stdout."""
    result = subprocess.run(
        cmd if isinstance(cmd, list) else shlex.split(cmd),
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f'Command failed: {cmd}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}')
    return result.stdout.strip()


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # Set up git config if needed
    git_env = os.environ.copy()
    git_env['GIT_AUTHOR_NAME'] = 'Dev User'
    git_env['GIT_AUTHOR_EMAIL'] = 'dev@example.com'
    git_env['GIT_COMMITTER_NAME'] = 'Dev User'
    git_env['GIT_COMMITTER_EMAIL'] = 'dev@example.com'

    # Remove existing project dir if present (idempotent)
    if os.path.exists(PROJECT_DIR):
        subprocess.run(['rm', '-rf', PROJECT_DIR], check=True)

    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Initialize git repo
    run('git init', cwd=PROJECT_DIR, env=git_env)
    run('git config user.email "dev@example.com"', cwd=PROJECT_DIR)
    run('git config user.name "Dev User"', cwd=PROJECT_DIR)
    run('git config init.defaultBranch main', cwd=PROJECT_DIR)

    # Create initial project files on main branch
    # README.md
    readme_content = """# Dashboard Project

A data visualization dashboard for sales analytics.

## Features
- Real-time sales tracking
- Revenue charts and graphs
- Customer segmentation analysis
- Export to PDF/CSV

## Requirements
- Python 3.8+
- pandas, matplotlib, plotly
"""
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme_content)

    # main app file
    app_content = """#!/usr/bin/env python3
\"\"\"
Main application entry point for the Dashboard project.
\"\"\"
import os
import sys

def main():
    print("Starting Dashboard Application...")
    from dashboard import DashboardApp
    app = DashboardApp()
    app.run()

if __name__ == '__main__':
    main()
"""
    with open(os.path.join(PROJECT_DIR, 'app.py'), 'w') as f:
        f.write(app_content)

    # requirements.txt
    requirements_content = """pandas==2.0.3
matplotlib==3.7.2
plotly==5.15.0
flask==2.3.2
sqlalchemy==2.0.19
"""
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write(requirements_content)

    # Original dashboard.py (clean version on main)
    dashboard_original = """#!/usr/bin/env python3
\"\"\"
Dashboard module - core visualization logic.
\"\"\"
import pandas as pd
import matplotlib.pyplot as plt


class DashboardApp:
    def __init__(self):
        self.data = None
        self.title = "Sales Dashboard"

    def load_data(self, filepath):
        \"\"\"Load sales data from CSV file.\"\"\"
        self.data = pd.read_csv(filepath)
        print(f"Loaded {len(self.data)} records from {filepath}")

    def generate_report(self):
        \"\"\"Generate a summary report.\"\"\"
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        summary = {
            'total_sales': self.data['sales'].sum(),
            'avg_sales': self.data['sales'].mean(),
            'top_product': self.data.groupby('product')['sales'].sum().idxmax(),
        }
        return summary

    def run(self):
        \"\"\"Start the dashboard application.\"\"\"
        print(f"Running: {self.title}")
        print("Dashboard ready.")
"""
    with open(os.path.join(PROJECT_DIR, 'dashboard.py'), 'w') as f:
        f.write(dashboard_original)

    # Initial commit on main
    run('git add -A', cwd=PROJECT_DIR, env=git_env)
    run(['git', 'commit', '-m', 'Initial commit: project scaffold'], cwd=PROJECT_DIR, env=git_env)
    # Ensure the branch is named 'main' (git may default to 'master' on older git versions)
    run('git branch -M main', cwd=PROJECT_DIR, env=git_env)

    # Create and switch to feature/dashboard branch
    run('git checkout -b feature/dashboard', cwd=PROJECT_DIR, env=git_env)

    # Modify dashboard.py with WIP changes (tracked modified file)
    dashboard_wip = """#!/usr/bin/env python3
\"\"\"
Dashboard module - core visualization logic with chart support.
\"\"\"
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


class DashboardApp:
    def __init__(self):
        self.data = None
        self.title = "Sales Dashboard v2"
        self.chart_config = {
            'style': 'seaborn-v0_8',
            'dpi': 150,
            'figsize': (12, 8),
        }

    def load_data(self, filepath):
        \"\"\"Load sales data from CSV file.\"\"\"
        self.data = pd.read_csv(filepath)
        print(f"Loaded {len(self.data)} records from {filepath}")

    def generate_report(self):
        \"\"\"Generate a summary report.\"\"\"
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        summary = {
            'total_sales': self.data['sales'].sum(),
            'avg_sales': self.data['sales'].mean(),
            'top_product': self.data.groupby('product')['sales'].sum().idxmax(),
            'monthly_growth': self._calculate_growth(),
        }
        return summary

    def _calculate_growth(self):
        \"\"\"Calculate month-over-month growth rate.\"\"\"
        # TODO: implement growth calculation using chart_utils
        return 0.0

    def create_charts(self):
        \"\"\"Create dashboard charts layout.\"\"\"
        fig = plt.figure(figsize=self.chart_config['figsize'])
        gs = gridspec.GridSpec(2, 2, figure=fig)
        # TODO: populate chart panels
        return fig

    def run(self):
        \"\"\"Start the dashboard application.\"\"\"
        print(f"Running: {self.title}")
        print("Dashboard with charts ready.")
"""
    with open(os.path.join(PROJECT_DIR, 'dashboard.py'), 'w') as f:
        f.write(dashboard_wip)

    # Create untracked new file chart_utils.py (NOT added to git)
    chart_utils_content = """#!/usr/bin/env python3
\"\"\"
Chart utilities for the Dashboard project.
Provides helper functions for creating and styling charts.
\"\"\"
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np


CHART_COLORS = [
    '#2196F3',  # Blue
    '#4CAF50',  # Green
    '#FF9800',  # Orange
    '#E91E63',  # Pink
    '#9C27B0',  # Purple
]


def create_bar_chart(ax, labels, values, title='', color_index=0):
    \"\"\"Create a styled bar chart on the given axes.\"\"\"
    color = CHART_COLORS[color_index % len(CHART_COLORS)]
    bars = ax.bar(labels, values, color=color, edgecolor='white', linewidth=0.8)
    ax.set_title(title, fontsize=12, fontweight='bold', pad=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3)
    # Add value labels on bars
    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(values) * 0.01,
            f'{val:,.0f}',
            ha='center', va='bottom', fontsize=9
        )
    return bars


def create_line_chart(ax, x_data, y_data, title='', label='', color_index=1):
    \"\"\"Create a styled line chart on the given axes.\"\"\"
    color = CHART_COLORS[color_index % len(CHART_COLORS)]
    line = ax.plot(x_data, y_data, color=color, linewidth=2, marker='o',
                   markersize=5, label=label)
    ax.set_title(title, fontsize=12, fontweight='bold', pad=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(alpha=0.3)
    if label:
        ax.legend()
    return line


def format_currency(value):
    \"\"\"Format a number as currency string.\"\"\"
    return f'${value:,.2f}'


def calculate_percentage_change(old_val, new_val):
    \"\"\"Calculate percentage change between two values.\"\"\"
    if old_val == 0:
        return float('inf') if new_val != 0 else 0.0
    return ((new_val - old_val) / abs(old_val)) * 100
"""
    with open(os.path.join(PROJECT_DIR, 'chart_utils.py'), 'w') as f:
        f.write(chart_utils_content)

    # Verify state: dashboard.py is modified, chart_utils.py is untracked
    status = run('git status --short', cwd=PROJECT_DIR)
    print(f'Git status:\n{status}')

    # Verify there are no stashes
    stash_list = run('git stash list', cwd=PROJECT_DIR, check=False)
    print(f'Stash list (should be empty): "{stash_list}"')

    # Verify current branch
    branch = run('git branch --show-current', cwd=PROJECT_DIR)
    print(f'Current branch: {branch}')

    print(f'Initial project created at: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project folder, DISPLAY=:0')


create_initial()
