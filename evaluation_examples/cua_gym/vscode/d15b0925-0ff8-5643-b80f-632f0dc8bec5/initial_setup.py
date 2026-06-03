"""
Initial Setup: Change language mode of data.txt to Python in VSCode
Task ID: vscode_file_024
Domain: vs_code
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_024'
PROJECT_DIR = f'{WORKDIR}/project'
DATA_TXT = f'{PROJECT_DIR}/data.txt'
MAIN_PY = f'{PROJECT_DIR}/main.py'

HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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
    # Create project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create data.txt with realistic Python code content (has .txt extension)
    data_txt_content = '''# Data processing utilities
import csv
import json
from datetime import datetime


def load_sales_data(filepath):
    """Load sales data from CSV file."""
    records = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                'date': datetime.strptime(row['date'], '%Y-%m-%d'),
                'product': row['product'],
                'quantity': int(row['quantity']),
                'price': float(row['price']),
                'region': row['region']
            })
    return records


def calculate_revenue(records):
    """Calculate total revenue per region."""
    revenue = {}
    for record in records:
        region = record['region']
        amount = record['quantity'] * record['price']
        revenue[region] = revenue.get(region, 0.0) + amount
    return revenue


def filter_by_date_range(records, start_date, end_date):
    """Filter records within a date range."""
    return [
        r for r in records
        if start_date <= r['date'] <= end_date
    ]


def export_summary(data, output_path):
    """Export summary statistics to JSON."""
    summary = {
        'total_records': len(data),
        'regions': list(set(r['region'] for r in data)),
        'total_revenue': sum(r['quantity'] * r['price'] for r in data),
        'generated_at': datetime.now().isoformat()
    }
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2)
    return summary


if __name__ == '__main__':
    data = load_sales_data('sales_2024.csv')
    revenue = calculate_revenue(data)
    print('Revenue by region:')
    for region, amount in sorted(revenue.items()):
        print(f'  {region}: ${amount:,.2f}')
'''

    with open(DATA_TXT, 'w') as f:
        f.write(data_txt_content)
    print(f'Created: {DATA_TXT}')

    # Create main.py with complementary Python code
    main_py_content = '''#!/usr/bin/env python3
"""
Main entry point for data analysis pipeline.
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))


def main():
    """Run data analysis pipeline."""
    print("Starting data analysis pipeline...")

    # Configuration
    config = {
        'input_dir': '/home/user/data',
        'output_dir': '/home/user/reports',
        'log_level': 'INFO',
    }

    input_dir = config['input_dir']
    output_dir = config['output_dir']

    os.makedirs(output_dir, exist_ok=True)

    # List available data files
    if os.path.exists(input_dir):
        data_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
        print(f"Found {len(data_files)} CSV files to process")
        for fname in sorted(data_files):
            fpath = os.path.join(input_dir, fname)
            print(f"  Processing: {fname}")
    else:
        print(f"Input directory not found: {input_dir}")

    print("Pipeline complete.")


if __name__ == '__main__':
    main()
'''

    with open(MAIN_PY, 'w') as f:
        f.write(main_py_content)
    print(f'Created: {MAIN_PY}')

    # Configure VSCode settings — ensure no files.associations for data.txt initially
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    try:
        with open(SETTINGS_PATH, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Remove any existing files.associations for data.txt (ensure clean initial state)
    if 'files.associations' in settings:
        assoc = settings['files.associations']
        # Remove any association that would make data.txt be Python
        for key in list(assoc.keys()):
            if 'data.txt' in key or key in ('*.txt',):
                del assoc[key]
        if not assoc:
            del settings['files.associations']

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'VSCode settings configured (no files.associations for data.txt)')

    # GUI-ready startup: open VSCode with project folder and data.txt
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    launch_gui(f'code "{DATA_TXT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with project and data.txt open (DISPLAY=:0)')


create_initial()
