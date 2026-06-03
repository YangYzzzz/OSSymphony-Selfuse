"""
Initial Setup: Configure VSCode with analysis.py for pandas.merge parameter hints exploration
Task ID: vscode_lp_032
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_032'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
WORKSPACE_DIR = os.path.join(WORKDIR, 'workspace')
OUTPUT = os.path.join(WORKSPACE_DIR, 'analysis.py')


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


def load_settings():
    try:
        with open(SETTINGS_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def update_settings(updates: dict):
    settings = load_settings()
    settings.update(updates)
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)


def create_initial():
    # Create workspace directory
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Create analysis.py with realistic data analysis code
    # pd.merge(df1, df2) must be on line 15
    analysis_code = '''import pandas as pd
import numpy as np
from datetime import datetime

# Employee records from HR database
employees = {'employee_id': [101, 102, 103, 104, 105], 'name': ['Sarah Chen', 'Marcus Johnson', 'Priya Patel', 'James Wilson', 'Ana Rodriguez'], 'department': ['Engineering', 'Marketing', 'Engineering', 'Sales', 'Marketing'], 'salary': [95000, 72000, 88000, 68000, 75000]}
df1 = pd.DataFrame(employees)

# Quarterly performance review scores
reviews = {'employee_id': [101, 102, 103, 104, 105], 'review_score': [4.5, 3.8, 4.2, 3.5, 4.0], 'review_date': ['2025-03-15', '2025-03-14', '2025-03-15', '2025-03-13', '2025-03-14']}
df2 = pd.DataFrame(reviews)

# Combine employee info with their performance data
# Parameters: left, right, how, on, left_on, right_on, suffixes, etc.
result = pd.merge(df1, df2)

# Department-level aggregation
dept_summary = result.groupby('department').agg(
    avg_salary=('salary', 'mean'),
    avg_score=('review_score', 'mean')
).round(2)

# Filter top performers with review score >= 4.0
top_performers = result[result['review_score'] >= 4.0].sort_values(
    'review_score', ascending=False
)

# Generate summary report
print("=" * 60)
print("Employee Performance Summary Report")
print("=" * 60)
print(f"\\nTotal employees analyzed: {len(result)}")
print(f"\\nDepartment Averages:\\n{dept_summary}")
print(f"\\nTop Performers:\\n{top_performers[['name', 'department', 'review_score']]}")

# Save merged dataset
result.to_csv('/home/user/workspace/merged_report.csv', index=False)
print("\\nReport exported to merged_report.csv")
'''
    with open(OUTPUT, 'w') as f:
        f.write(analysis_code)
    print(f'Created analysis.py at {OUTPUT}')

    # Verify line 15 contains pd.merge
    with open(OUTPUT, 'r') as f:
        lines = f.readlines()
    print(f'Line 15: {lines[14].strip()}')
    assert 'pd.merge' in lines[14], f'pd.merge not on line 15! Found: {lines[14]}'

    # Configure VSCode settings - disable parameter hints (initial state)
    update_settings({
        "editor.parameterHints.enabled": False,
        "editor.hover.enabled": True,
        "python.analysis.typeCheckingMode": "off",
        "python.languageServer": "Pylance",
        "workbench.colorTheme": "Visual Studio Dark",
        "editor.fontSize": 14,
        "files.autoSave": "afterDelay"
    })
    print(f'VSCode settings configured with parameter hints DISABLED')

    # Ensure pandas is installed
    subprocess.run(['pip3', 'install', 'pandas'], capture_output=True, text=True)
    print('Ensured pandas is installed')

    # Launch VSCode with the workspace and file
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
