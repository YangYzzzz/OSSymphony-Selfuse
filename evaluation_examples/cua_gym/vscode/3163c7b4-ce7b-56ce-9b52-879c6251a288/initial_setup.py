"""
Initial Setup: Configure Git settings in VSCode
Task ID: vscode_we_036
Domain: vscode

Creates a Git repository workspace and opens VSCode with empty user settings.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_036'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
WORKSPACE_DIR = os.path.join(WORKDIR, 'my-project')


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
    # 1. Create a realistic Git repository workspace
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Initialize git repo
    subprocess.run(['git', 'init'], cwd=WORKSPACE_DIR, check=True,
                   capture_output=True)
    subprocess.run(['git', 'config', 'user.email', 'dev@example.com'],
                   cwd=WORKSPACE_DIR, check=True, capture_output=True)
    subprocess.run(['git', 'config', 'user.name', 'Developer'],
                   cwd=WORKSPACE_DIR, check=True, capture_output=True)

    # Create some realistic project files
    readme_content = """# My Project

A sample Python project for data analysis.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

Run the main script:
```bash
python main.py
```
"""
    with open(os.path.join(WORKSPACE_DIR, 'README.md'), 'w') as f:
        f.write(readme_content)

    main_py = """import csv
import os
from datetime import datetime


def load_data(filepath: str) -> list:
    \"\"\"Load CSV data from the given file path.\"\"\"
    results = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append(row)
    return results


def process_records(records: list) -> dict:
    \"\"\"Process records and return summary statistics.\"\"\"
    total = len(records)
    if total == 0:
        return {"count": 0, "average": 0.0}

    values = [float(r.get("value", 0)) for r in records]
    return {
        "count": total,
        "sum": sum(values),
        "average": sum(values) / total,
        "min": min(values),
        "max": max(values),
    }


if __name__ == "__main__":
    data = load_data("data/sales.csv")
    summary = process_records(data)
    print(f"Processed {summary['count']} records")
    print(f"Total: {summary['sum']:.2f}, Average: {summary['average']:.2f}")
"""
    with open(os.path.join(WORKSPACE_DIR, 'main.py'), 'w') as f:
        f.write(main_py)

    requirements = """pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
"""
    with open(os.path.join(WORKSPACE_DIR, 'requirements.txt'), 'w') as f:
        f.write(requirements)

    # Create data directory with sample CSV
    data_dir = os.path.join(WORKSPACE_DIR, 'data')
    os.makedirs(data_dir, exist_ok=True)

    sales_csv = """date,product,region,value,quantity
2025-01-15,Widget A,North,1250.00,50
2025-01-16,Widget B,South,890.50,35
2025-01-17,Widget A,East,1100.00,44
2025-01-18,Widget C,West,2300.75,92
2025-01-19,Widget B,North,750.25,30
2025-01-20,Widget A,South,1450.00,58
2025-01-21,Widget C,East,1875.50,75
"""
    with open(os.path.join(data_dir, 'sales.csv'), 'w') as f:
        f.write(sales_csv)

    # Make initial git commit
    subprocess.run(['git', 'add', '.'], cwd=WORKSPACE_DIR, check=True,
                   capture_output=True)
    subprocess.run(['git', 'commit', '-m', 'Initial project setup'],
                   cwd=WORKSPACE_DIR, check=True, capture_output=True)

    # 2. Ensure VSCode user settings directory exists with empty settings
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)
    print(f'VSCode settings initialized (empty): {SETTINGS_PATH}')

    # 3. Launch VSCode with the project workspace
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
