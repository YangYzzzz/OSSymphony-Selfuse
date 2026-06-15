"""
Initial Setup: Open VSCode with default keybindings and a workspace with code files.
Task ID: vscode_stu_083
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_083'
WORKSPACE_DIR = f'{WORKDIR}/workspace'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
KEYBINDINGS_PATH = os.path.join(VSCODE_USER, 'keybindings.json')


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


def create_workspace_files():
    """Create a realistic workspace with sample code files."""
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Main Python file
    main_py = """\
import csv
import sys
from datetime import datetime

def load_sales_data(filepath):
    \"\"\"Load quarterly sales data from CSV file.\"\"\"
    records = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                'date': datetime.strptime(row['date'], '%Y-%m-%d'),
                'product': row['product'],
                'quantity': int(row['quantity']),
                'unit_price': float(row['unit_price']),
                'region': row['region'],
            })
    return records

/*
This block comment style is intentionally wrong in Python
to give context for the task about block comments.
*/

def calculate_revenue(records):
    \"\"\"Calculate total revenue grouped by product.\"\"\"
    revenue = {}
    for rec in records:
        product = rec['product']
        total = rec['quantity'] * rec['unit_price']
        revenue[product] = revenue.get(product, 0) + total
    return revenue


def generate_report(revenue_data):
    \"\"\"Print a formatted sales report.\"\"\"
    print("=" * 50)
    print("  Quarterly Sales Report")
    print("=" * 50)
    for product, total in sorted(revenue_data.items(), key=lambda x: -x[1]):
        print(f"  {product:<25} ${total:>10,.2f}")
    print("-" * 50)
    grand_total = sum(revenue_data.values())
    print(f"  {'TOTAL':<25} ${grand_total:>10,.2f}")
    print("=" * 50)


if __name__ == '__main__':
    filepath = sys.argv[1] if len(sys.argv) > 1 else 'sales_q1.csv'
    data = load_sales_data(filepath)
    rev = calculate_revenue(data)
    generate_report(rev)
"""
    with open(os.path.join(WORKSPACE_DIR, 'sales_report.py'), 'w') as f:
        f.write(main_py)

    # A utility module
    utils_py = """\
import os
import logging

logger = logging.getLogger(__name__)

def ensure_directory(path):
    \"\"\"Create directory if it doesn't exist.\"\"\"
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f"Created directory: {path}")

def format_currency(amount, currency='USD'):
    \"\"\"Format a number as currency string.\"\"\"
    symbols = {'USD': '$', 'EUR': '\\u20ac', 'GBP': '\\u00a3'}
    symbol = symbols.get(currency, currency + ' ')
    return f"{symbol}{amount:,.2f}"

def truncate_string(s, max_length=50):
    \"\"\"Truncate a string and add ellipsis if too long.\"\"\"
    if len(s) <= max_length:
        return s
    return s[:max_length - 3] + '...'
"""
    with open(os.path.join(WORKSPACE_DIR, 'utils.py'), 'w') as f:
        f.write(utils_py)

    # Sample CSV data
    csv_data = """\
date,product,quantity,unit_price,region
2025-01-05,Widget Pro,150,29.99,North America
2025-01-12,Widget Pro,85,29.99,Europe
2025-01-19,DataSync Suite,42,199.00,North America
2025-02-03,Widget Pro,200,29.99,Asia Pacific
2025-02-14,CloudBridge,78,149.50,North America
2025-02-21,DataSync Suite,35,199.00,Europe
2025-03-01,Widget Pro,120,29.99,North America
2025-03-10,CloudBridge,95,149.50,Europe
2025-03-18,DataSync Suite,60,199.00,Asia Pacific
2025-03-25,Widget Pro,175,29.99,North America
"""
    with open(os.path.join(WORKSPACE_DIR, 'sales_q1.csv'), 'w') as f:
        f.write(csv_data)


def setup_default_keybindings():
    """Ensure keybindings.json is at default (empty array)."""
    os.makedirs(VSCODE_USER, exist_ok=True)
    # Write empty keybindings - this is the default state
    with open(KEYBINDINGS_PATH, 'w') as f:
        json.dump([], f, indent=4)
    print(f'Keybindings reset to default (empty): {KEYBINDINGS_PATH}')


def main():
    create_workspace_files()
    print(f'Workspace created at: {WORKSPACE_DIR}')

    setup_default_keybindings()

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
