"""
Initial Setup: Configure VSCode with default terminal settings
Task ID: vscode_we_035
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_035'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
WORKSPACE_DIR = os.path.join(WORKDIR, 'workspace')


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
    # Create workspace directory with a sample project
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Create a simple project file so VSCode has something to show
    main_py = os.path.join(WORKSPACE_DIR, 'main.py')
    with open(main_py, 'w') as f:
        f.write('''#!/usr/bin/env python3
"""
Sales Report Generator
Generates quarterly sales reports from transaction data.
"""

import csv
import os
from datetime import datetime


def load_transactions(filepath):
    """Load transaction records from CSV file."""
    transactions = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            transactions.append({
                'date': datetime.strptime(row['date'], '%Y-%m-%d'),
                'product': row['product'],
                'quantity': int(row['quantity']),
                'unit_price': float(row['unit_price']),
                'region': row['region'],
            })
    return transactions


def calculate_quarterly_totals(transactions):
    """Aggregate sales by quarter and region."""
    totals = {}
    for txn in transactions:
        quarter = f"Q{(txn['date'].month - 1) // 3 + 1}"
        key = (quarter, txn['region'])
        if key not in totals:
            totals[key] = 0.0
        totals[key] += txn['quantity'] * txn['unit_price']
    return totals


def generate_report(totals, output_path):
    """Write quarterly summary report."""
    with open(output_path, 'w') as f:
        f.write("Quarterly Sales Report\\n")
        f.write("=" * 40 + "\\n\\n")
        for (quarter, region), amount in sorted(totals.items()):
            f.write(f"  {quarter} | {region:>12} | ${amount:>10,.2f}\\n")
        f.write("\\n" + "=" * 40 + "\\n")


if __name__ == '__main__':
    data_file = os.path.join(os.path.dirname(__file__), 'transactions.csv')
    report_file = os.path.join(os.path.dirname(__file__), 'report.txt')
    txns = load_transactions(data_file)
    totals = calculate_quarterly_totals(txns)
    generate_report(totals, report_file)
    print("Report generated successfully.")
''')

    # Create sample data file
    csv_path = os.path.join(WORKSPACE_DIR, 'transactions.csv')
    with open(csv_path, 'w') as f:
        f.write('date,product,quantity,unit_price,region\n')
        f.write('2025-01-15,Widget A,120,24.99,North\n')
        f.write('2025-01-22,Widget B,85,39.50,South\n')
        f.write('2025-02-10,Widget A,200,24.99,East\n')
        f.write('2025-03-05,Widget C,45,89.00,North\n')
        f.write('2025-04-18,Widget B,150,39.50,West\n')
        f.write('2025-05-02,Widget A,95,24.99,South\n')

    # Ensure VSCode user config directory exists with empty settings
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)
    print(f'Empty settings.json created at: {SETTINGS_PATH}')

    # Launch VSCode with workspace
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
