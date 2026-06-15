"""
Initial Setup: Create a VSCode project with system-generated files cluttering the explorer
Task ID: vscode_file_051
Domain: vs_code
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_051'
PROJECT_DIR = f'{WORKDIR}/project'


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
    os.makedirs(f'{PROJECT_DIR}/.git/objects', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/.git/refs', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/.vscode', exist_ok=True)

    # Create .git/HEAD (minimal git repository marker)
    with open(f'{PROJECT_DIR}/.git/HEAD', 'w') as f:
        f.write('ref: refs/heads/main\n')

    # Create .git/config (minimal git config)
    with open(f'{PROJECT_DIR}/.git/config', 'w') as f:
        f.write('[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n')

    # Create .DS_Store (macOS metadata file - binary-like placeholder)
    with open(f'{PROJECT_DIR}/.DS_Store', 'wb') as f:
        # Minimal DS_Store magic bytes
        f.write(b'\x00\x00\x00\x01Bud1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

    # Create Thumbs.db (Windows thumbnail cache - binary-like placeholder)
    with open(f'{PROJECT_DIR}/Thumbs.db', 'wb') as f:
        # Minimal OLE compound document header
        f.write(b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1\x00\x00\x00\x00\x00\x00\x00\x00')

    # Create src/main.py with realistic Python content
    with open(f'{PROJECT_DIR}/src/main.py', 'w') as f:
        f.write('''#!/usr/bin/env python3
"""
Main application entry point.
Project: Data Processing Pipeline
Author: Development Team
"""

import os
import sys
import logging
from datetime import datetime


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_data(filepath: str) -> list:
    """Load data records from a CSV file."""
    records = []
    try:
        with open(filepath, 'r') as f:
            headers = f.readline().strip().split(',')
            for line in f:
                values = line.strip().split(',')
                if len(values) == len(headers):
                    records.append(dict(zip(headers, values)))
        logger.info(f"Loaded {len(records)} records from {filepath}")
    except FileNotFoundError:
        logger.error(f"Data file not found: {filepath}")
    return records


def process_records(records: list) -> dict:
    """Process and aggregate data records."""
    summary = {
        'total': len(records),
        'processed_at': datetime.now().isoformat(),
        'status': 'success'
    }
    return summary


def main():
    """Main execution function."""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    input_file = os.path.join(data_dir, 'input.csv')

    logger.info("Starting data processing pipeline")
    records = load_data(input_file)

    if not records:
        logger.warning("No records found to process")
        sys.exit(1)

    summary = process_records(records)
    logger.info(f"Processing complete: {summary}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
''')

    # Create src/.main.py.swp (vim swap file - simulated)
    with open(f'{PROJECT_DIR}/src/.main.py.swp', 'wb') as f:
        # Minimal vim swap file header
        f.write(b'b0VIM 9.0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        f.write(b'\x00' * 48)

    # Create README.md
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write('''# Data Processing Pipeline

A Python-based data processing pipeline for batch operations.

## Requirements

- Python 3.8+
- Standard library only

## Usage

```bash
python src/main.py
```

## Project Structure

```
project/
├── src/
│   └── main.py
├── data/
│   └── input.csv
└── README.md
```
''')

    # Ensure .vscode directory exists but settings.json does NOT exist
    # (The task is to create .vscode/settings.json with files.exclude)
    settings_path = f'{PROJECT_DIR}/.vscode/settings.json'
    if os.path.exists(settings_path):
        os.remove(settings_path)

    print(f'Initial project structure created at: {PROJECT_DIR}')
    print('Files created:')
    print(f'  {PROJECT_DIR}/.git/ (git repository)')
    print(f'  {PROJECT_DIR}/.DS_Store (macOS metadata)')
    print(f'  {PROJECT_DIR}/Thumbs.db (Windows thumbnail cache)')
    print(f'  {PROJECT_DIR}/src/main.py (source code)')
    print(f'  {PROJECT_DIR}/src/.main.py.swp (vim swap file)')
    print(f'  {PROJECT_DIR}/README.md')
    print(f'  {PROJECT_DIR}/.vscode/ (empty, no settings.json)')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project folder, DISPLAY=:0')


create_initial()
