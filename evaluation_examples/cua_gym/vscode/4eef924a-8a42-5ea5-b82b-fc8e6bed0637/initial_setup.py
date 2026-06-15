"""
Initial Setup: Git repo with three modified files for staging/commit task
Task ID: vscode_stu_032
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_032'
REPO_DIR = f'{WORKDIR}/{TASK_ID}'


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


def run_cmd(cmd, cwd=None):
    """Run a shell command and return output."""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        print(f"stderr: {result.stderr}")
    return result.stdout.strip()


def create_initial():
    # Create repo directory
    os.makedirs(REPO_DIR, exist_ok=True)

    # Initialize git repo
    run_cmd('git init', cwd=REPO_DIR)
    run_cmd('git config user.email "student@university.edu"', cwd=REPO_DIR)
    run_cmd('git config user.name "Alex Rivera"', cwd=REPO_DIR)

    # --- Create initial versions of files and make first commit ---

    # main.py - a data analysis script
    main_py_v1 = '''\
import os
import sys
from utils import load_dataset, preprocess
from config import SETTINGS

def main():
    """Run the data analysis pipeline."""
    data_path = SETTINGS["data_path"]
    if not os.path.exists(data_path):
        print(f"Error: data file not found at {data_path}")
        sys.exit(1)

    raw_data = load_dataset(data_path)
    cleaned = preprocess(raw_data)
    print(f"Processed {len(cleaned)} records")

if __name__ == "__main__":
    main()
'''

    # utils.py - utility functions
    utils_py_v1 = '''\
import csv

def load_dataset(filepath):
    """Load a CSV dataset and return rows as list of dicts."""
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)

def preprocess(data):
    """Basic preprocessing: remove rows with missing values."""
    cleaned = []
    for row in data:
        if all(v.strip() for v in row.values()):
            cleaned.append(row)
    return cleaned
'''

    # config.py - configuration settings
    config_py_v1 = '''\
SETTINGS = {
    "data_path": "data/sales_2025.csv",
    "output_dir": "results",
    "verbose": False,
}
'''

    # Write initial versions
    with open(os.path.join(REPO_DIR, 'main.py'), 'w') as f:
        f.write(main_py_v1)
    with open(os.path.join(REPO_DIR, 'utils.py'), 'w') as f:
        f.write(utils_py_v1)
    with open(os.path.join(REPO_DIR, 'config.py'), 'w') as f:
        f.write(config_py_v1)

    # Initial commit
    run_cmd('git add .', cwd=REPO_DIR)
    run_cmd('git commit -m "Initial commit: exercise 2 solution"', cwd=REPO_DIR)
    print("Initial commit created")

    # --- Now modify all three files (these become the "unsaved modifications") ---

    # main.py v2 - added summary statistics and error handling
    main_py_v2 = '''\
import os
import sys
from utils import load_dataset, preprocess, compute_summary
from config import SETTINGS

def main():
    """Run the data analysis pipeline."""
    data_path = SETTINGS["data_path"]
    if not os.path.exists(data_path):
        print(f"Error: data file not found at {data_path}")
        sys.exit(1)

    raw_data = load_dataset(data_path)
    cleaned = preprocess(raw_data)
    print(f"Processed {len(cleaned)} records")

    # Exercise 3: compute and display summary statistics
    if SETTINGS["verbose"]:
        summary = compute_summary(cleaned, SETTINGS["target_column"])
        for key, value in summary.items():
            print(f"  {key}: {value}")

    output_path = os.path.join(SETTINGS["output_dir"], "summary.txt")
    os.makedirs(SETTINGS["output_dir"], exist_ok=True)
    with open(output_path, "w") as f:
        f.write(f"Total records: {len(cleaned)}\\n")
    print(f"Summary written to {output_path}")

if __name__ == "__main__":
    main()
'''

    # utils.py v2 - added compute_summary function
    utils_py_v2 = '''\
import csv
from collections import Counter

def load_dataset(filepath):
    """Load a CSV dataset and return rows as list of dicts."""
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)

def preprocess(data):
    """Basic preprocessing: remove rows with missing values."""
    cleaned = []
    for row in data:
        if all(v.strip() for v in row.values()):
            cleaned.append(row)
    return cleaned

def compute_summary(data, column):
    """Compute summary statistics for a given column."""
    values = [row.get(column, "") for row in data]
    numeric = []
    for v in values:
        try:
            numeric.append(float(v))
        except (ValueError, TypeError):
            pass
    if not numeric:
        counts = Counter(values)
        return {"unique_values": len(counts), "most_common": counts.most_common(1)[0][0]}
    return {
        "count": len(numeric),
        "mean": sum(numeric) / len(numeric),
        "min": min(numeric),
        "max": max(numeric),
    }
'''

    # config.py v2 - added new settings for exercise 3
    config_py_v2 = '''\
SETTINGS = {
    "data_path": "data/sales_2025.csv",
    "output_dir": "results",
    "verbose": True,
    "target_column": "revenue",
    "decimal_places": 2,
}
'''

    # Write modified versions
    with open(os.path.join(REPO_DIR, 'main.py'), 'w') as f:
        f.write(main_py_v2)
    with open(os.path.join(REPO_DIR, 'utils.py'), 'w') as f:
        f.write(utils_py_v2)
    with open(os.path.join(REPO_DIR, 'config.py'), 'w') as f:
        f.write(config_py_v2)

    print("Modified three files (main.py, utils.py, config.py)")

    # Verify git status shows modified files
    status = run_cmd('git status --short', cwd=REPO_DIR)
    print(f"Git status:\n{status}")

    # Launch VSCode with the repo folder
    launch_gui(f'code "{REPO_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
