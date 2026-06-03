"""
Initial Setup: Configure Error Lens extension in VSCode
Task ID: vscode_we_066
Domain: vscode

Initial state: VSCode open with errorlens extension installed but default settings.
User settings.json is empty ({}).
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
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
    # Ensure VSCode config directory exists
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Write empty user settings (no errorLens config)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)
    print(f'Initial settings created: {SETTINGS_PATH}')

    # Create a sample workspace with a Python file that has some errors
    # so Error Lens has something to display
    workspace_dir = os.path.join(WORKDIR, 'workspace')
    os.makedirs(workspace_dir, exist_ok=True)

    sample_file = os.path.join(workspace_dir, 'main.py')
    with open(sample_file, 'w') as f:
        f.write('''"""
Sales Report Generator
"""

import os
import sys
from datetime import datetime


def calculate_quarterly_revenue(transactions):
    """Calculate revenue for each quarter from transaction data."""
    quarterly = {"Q1": 0, "Q2": 0, "Q3": 0, "Q4": 0}
    for txn in transactions:
        month = txn["date"].month
        if month <= 3:
            quarterly["Q1"] += txn["amount"]
        elif month <= 6:
            quarterly["Q2"] += txn["amount"]
        elif month <= 9:
            quarterly["Q3"] += txn["amount"]
        else:
            quarterly["Q4"] += txn["amount"]
    return quarterly


def format_currency(amount):
    """Format a number as USD currency string."""
    return f"${amount:,.2f}"


def generate_report(data_path, output_path):
    """Generate a formatted sales report from raw transaction data."""
    if not os.path.exists(data_path):
        print(f"Error: Data file not found at {data_path}")
        sys.exit(1)

    transactions = [
        {"date": datetime(2025, 1, 15), "amount": 45230.00, "region": "West"},
        {"date": datetime(2025, 4, 22), "amount": 38750.50, "region": "East"},
        {"date": datetime(2025, 7, 8), "amount": 52100.75, "region": "Central"},
        {"date": datetime(2025, 10, 3), "amount": 41890.25, "region": "West"},
    ]

    revenue = calculate_quarterly_revenue(transactions)

    with open(output_path, "w") as report:
        report.write("=== Quarterly Sales Report 2025 ===\\n\\n")
        total = 0
        for quarter, amount in revenue.items():
            report.write(f"  {quarter}: {format_currency(amount)}\\n")
            total += amount
        report.write(f"\\n  Total: {format_currency(total)}\\n")

    print(f"Report generated: {output_path}")


if __name__ == "__main__":
    generate_report("sales_data.csv", "report.txt")
''')
    print(f'Sample workspace created: {workspace_dir}')

    # Ensure errorlens extension is installed
    try:
        result = subprocess.run(
            ['code', '--list-extensions'],
            capture_output=True, text=True, timeout=30
        )
        if 'usernamehw.errorlens' not in result.stdout.lower():
            print('Installing errorlens extension...')
            subprocess.run(
                ['code', '--install-extension', 'usernamehw.errorlens'],
                capture_output=True, text=True, timeout=60
            )
            print('Extension installed.')
        else:
            print('errorlens extension already installed.')
    except Exception as e:
        print(f'Extension check/install note: {e}')

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{workspace_dir}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
