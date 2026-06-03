"""
Initial Setup: Create a Python project with .vscode folder but no extensions.json
Task ID: vscode_file_023
Domain: vs_code
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_023'
PROJECT_DIR = f'{WORKDIR}/data-project'


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
    # Create project directory structure
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    src_dir = os.path.join(PROJECT_DIR, 'src')

    os.makedirs(vscode_dir, exist_ok=True)
    os.makedirs(src_dir, exist_ok=True)

    # Create .vscode/settings.json with realistic settings
    settings = {
        "python.defaultInterpreterPath": "/usr/bin/python3",
        "editor.formatOnSave": True,
        "editor.tabSize": 4,
        "files.exclude": {
            "**/__pycache__": True,
            "**/*.pyc": True
        }
    }
    settings_path = os.path.join(vscode_dir, 'settings.json')
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'Created: {settings_path}')

    # Make sure NO extensions.json exists (pre-task state)
    extensions_path = os.path.join(vscode_dir, 'extensions.json')
    if os.path.exists(extensions_path):
        os.remove(extensions_path)
        print(f'Removed pre-existing: {extensions_path}')

    # Create src/analysis.py with realistic Python code
    analysis_py = '''\
"""
Data analysis module for the data-project.
"""
import pandas as pd
import numpy as np
from pathlib import Path


DATA_DIR = Path(__file__).parent.parent / "data"


def load_dataset(filename: str) -> pd.DataFrame:
    """Load a CSV dataset from the data directory."""
    filepath = DATA_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Dataset not found: {filepath}")
    return pd.read_csv(filepath)


def compute_summary_stats(df: pd.DataFrame) -> dict:
    """Compute summary statistics for numeric columns."""
    stats = {}
    for col in df.select_dtypes(include=[np.number]).columns:
        stats[col] = {
            "mean": df[col].mean(),
            "median": df[col].median(),
            "std": df[col].std(),
            "min": df[col].min(),
            "max": df[col].max(),
        }
    return stats


def filter_outliers(df: pd.DataFrame, column: str, z_threshold: float = 3.0) -> pd.DataFrame:
    """Remove rows where the specified column has outliers beyond z_threshold."""
    mean = df[column].mean()
    std = df[column].std()
    z_scores = (df[column] - mean) / std
    return df[abs(z_scores) <= z_threshold]


if __name__ == "__main__":
    print("Analysis module loaded successfully.")
'''
    analysis_path = os.path.join(src_dir, 'analysis.py')
    with open(analysis_path, 'w') as f:
        f.write(analysis_py)
    print(f'Created: {analysis_path}')

    # Create requirements.txt with realistic dependencies
    requirements = '''\
pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.6.0
scikit-learn>=1.1.0
pytest>=7.2.0
black>=22.10.0
flake8>=6.0.0
'''
    requirements_path = os.path.join(PROJECT_DIR, 'requirements.txt')
    with open(requirements_path, 'w') as f:
        f.write(requirements)
    print(f'Created: {requirements_path}')

    print(f'\nProject structure created at: {PROJECT_DIR}')
    print('  .vscode/settings.json  -> EXISTS')
    print('  .vscode/extensions.json -> DOES NOT EXIST (task: create this)')
    print('  src/analysis.py        -> EXISTS')
    print('  requirements.txt       -> EXISTS')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with data-project folder using DISPLAY=:0')


create_initial()
