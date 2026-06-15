"""
Initial Setup: budget_tracker.py incomplete script with transactions.csv
Task ID: osworld_multi_apps_vscode_run_capture_012
Domain: multi_apps (VSCode + file system)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DESKTOP = f'{WORKDIR}/Desktop'
TASK_ID = 'osworld_multi_apps_vscode_run_capture_012'


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
    os.makedirs(DESKTOP, exist_ok=True)

    # --- transactions.csv on Desktop ---
    # Income: 3500.00 + 250.00 + 120.00 = 3870.00
    # Expenses: 1200.00 + 85.50 + 45.00 + 320.00 + 60.00 + 150.00 = 1860.50
    # Net balance: 3870.00 - 1860.50 = 2009.50
    csv_content = """date,description,type,amount
2025-03-01,Monthly Salary,income,3500.00
2025-03-03,Freelance Web Design,income,250.00
2025-03-05,Stock Dividends,income,120.00
2025-03-02,Apartment Rent,expense,1200.00
2025-03-04,Electricity Bill,expense,85.50
2025-03-06,Internet Service,expense,45.00
2025-03-08,Weekly Groceries,expense,320.00
2025-03-10,Public Transport,expense,60.00
2025-03-12,Health Insurance,expense,150.00
"""
    csv_path = f'{DESKTOP}/transactions.csv'
    with open(csv_path, 'w') as f:
        f.write(csv_content.lstrip())
    print(f'Created: {csv_path}')

    # --- budget_tracker.py on Desktop (INCOMPLETE) ---
    # The script has the CSV reading done but balance computation and summary printing are stubs
    py_content = '''import csv
import os

DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")
CSV_FILE = os.path.join(DESKTOP, "transactions.csv")
OUTPUT_FILE = os.path.join(DESKTOP, "budget_summary.txt")


def read_transactions(filepath):
    """Read transactions from CSV and return list of dicts."""
    transactions = []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            transactions.append({
                "date": row["date"],
                "description": row["description"],
                "type": row["type"],
                "amount": float(row["amount"]),
            })
    return transactions


def compute_summary(transactions):
    """Compute total income, total expenses, and net balance.

    Returns a dict with keys: total_income, total_expenses, net_balance.
    """
    total_income = 0.0
    total_expenses = 0.0

    # TODO: iterate over transactions and accumulate totals
    # Hint: check transaction["type"] == "income" or "expense"

    net_balance = 0.0  # TODO: compute net_balance from total_income and total_expenses

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_balance": net_balance,
    }


def print_summary(summary):
    """Print the budget summary and save it to OUTPUT_FILE."""
    lines = []

    # TODO: build the summary lines and print them
    # Expected format:
    #   Budget Summary
    #   ==============
    #   Total Income:    $XXXX.XX
    #   Total Expenses:  $XXXX.XX
    #   Net Balance:     $XXXX.XX

    output = "\\n".join(lines)
    # TODO: print output and write it to OUTPUT_FILE


if __name__ == "__main__":
    transactions = read_transactions(CSV_FILE)
    summary = compute_summary(transactions)
    print_summary(summary)
'''
    py_path = f'{DESKTOP}/budget_tracker.py'
    with open(py_path, 'w') as f:
        f.write(py_content)
    print(f'Created: {py_path}')

    # budget_summary.txt MUST NOT exist in initial state (agent creates it by running the script)
    summary_path = f'{DESKTOP}/budget_summary.txt'
    if os.path.exists(summary_path):
        os.remove(summary_path)
        print(f'Removed pre-existing: {summary_path}')

    # GUI-ready startup: open budget_tracker.py in VSCode
    launch_gui(f'code "{DESKTOP}/budget_tracker.py"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with budget_tracker.py and DISPLAY=:0')


create_initial()
