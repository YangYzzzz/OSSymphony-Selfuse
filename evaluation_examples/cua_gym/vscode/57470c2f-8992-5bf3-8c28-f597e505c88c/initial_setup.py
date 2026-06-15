"""
Initial Setup: VSCode Python IntelliSense - DataFrame autocomplete exploration
Task ID: vscode_lp_041
Domain: vscode

Creates analysis.py with pandas DataFrame loaded from data.csv.
Line 10 has df = pd.read_csv("data.csv"), line 11 is empty (cursor position).
Pylance + pandas stubs installed for IntelliSense.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_041'
ANALYSIS_FILE = f'{WORKDIR}/analysis.py'
DATA_FILE = f'{WORKDIR}/data.csv'


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


def create_data_csv():
    """Create a realistic CSV dataset for the analysis script."""
    csv_content = """employee_id,name,department,salary,hire_date,performance_score
1001,Sarah Chen,Engineering,95000,2021-03-15,4.5
1002,Marcus Johnson,Marketing,72000,2020-06-01,3.8
1003,Priya Patel,Engineering,88000,2022-01-10,4.2
1004,David Kim,Finance,81000,2019-11-22,4.0
1005,Elena Rodriguez,Marketing,69000,2023-02-28,3.5
1006,James Wilson,Engineering,102000,2018-07-14,4.7
1007,Aisha Mohammed,HR,67000,2021-09-03,3.9
1008,Robert Taylor,Finance,78000,2020-04-17,4.1
1009,Lisa Wang,Engineering,91000,2022-08-25,4.3
1010,Michael Brown,Marketing,74000,2019-12-05,3.6
1011,Jennifer Lee,HR,71000,2021-05-20,4.0
1012,Carlos Mendez,Finance,85000,2020-10-11,4.4
1013,Amanda Foster,Engineering,97000,2023-01-08,4.6
1014,Kevin O'Brien,Marketing,68000,2022-06-30,3.3
1015,Fatima Al-Rashid,Finance,83000,2021-04-12,4.2
"""
    with open(DATA_FILE, 'w') as f:
        f.write(csv_content.strip() + '\n')
    print(f'Data file created: {DATA_FILE}')


def create_analysis_py():
    """Create analysis.py with pandas import and DataFrame on line 10.

    Line layout:
      1: # Employee Performance Analysis
      2: # Analyze department-level salary and performance metrics
      3: (blank)
      4: import pandas as pd
      5: import numpy as np
      6: (blank)
      7: # Load the employee dataset
      8: DATA_PATH = "data.csv"
      9: (blank)
     10: df = pd.read_csv(DATA_PATH)
     11: (empty - cursor here for agent to type df.)
     12: (blank)
     13: # TODO: Explore DataFrame methods to analyze the data
    """
    lines = [
        '# Employee Performance Analysis',
        '# Analyze department-level salary and performance metrics',
        '',
        'import pandas as pd',
        'import numpy as np',
        '',
        '# Load the employee dataset',
        'DATA_PATH = "data.csv"',
        '',
        'df = pd.read_csv(DATA_PATH)',
        '',
        '',
        '# TODO: Explore DataFrame methods to analyze the data',
    ]
    with open(ANALYSIS_FILE, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    print(f'Analysis file created: {ANALYSIS_FILE}')


def install_python_deps():
    """Install pandas, numpy, and pandas-stubs for IntelliSense."""
    subprocess.run(
        ['pip3', 'install', 'pandas', 'numpy', 'pandas-stubs'],
        capture_output=True, text=True
    )
    print('Python dependencies installed (pandas, numpy, pandas-stubs)')


def setup_vscode_settings():
    """Configure VSCode settings for Python IntelliSense with Pylance."""
    import json

    vscode_user_dir = os.path.join(WORKDIR, '.config', 'Code', 'User')
    settings_path = os.path.join(vscode_user_dir, 'settings.json')

    # Load existing settings
    try:
        with open(settings_path, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Merge Python/Pylance settings
    settings.update({
        "python.languageServer": "Pylance",
        "python.analysis.typeCheckingMode": "basic",
        "editor.quickSuggestions": {
            "other": True,
            "comments": False,
            "strings": False
        },
        "editor.suggestOnTriggerCharacters": True,
        "editor.parameterHints.enabled": True,
    })

    os.makedirs(vscode_user_dir, exist_ok=True)
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'VSCode settings configured: {settings_path}')


def main():
    # 1. Install Python deps for IntelliSense
    install_python_deps()

    # 2. Create data file
    create_data_csv()

    # 3. Create analysis.py
    create_analysis_py()

    # 4. Configure VSCode settings for Pylance
    setup_vscode_settings()

    # 5. Open VSCode with the analysis file
    launch_gui(f'code "{ANALYSIS_FILE}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with analysis.py with DISPLAY=:0')


main()
