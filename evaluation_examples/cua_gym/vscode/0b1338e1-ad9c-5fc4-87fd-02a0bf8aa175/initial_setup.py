"""
Initial Setup: Copy function from lines 3-8 and paste at line 20
Task ID: vscode_stu_011
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_011'
OUTPUT = f'{WORKDIR}/{TASK_ID}.py'

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
    content = '''\
import os
import sys
def calculate_tax(income, rate=0.25):
    """Calculate tax amount based on income and rate."""
    if income < 0:
        raise ValueError("Income cannot be negative")
    tax = income * rate
    return round(tax, 2)

# Tax brackets for reference
BRACKETS = {
    "low": 0.10,
    "medium": 0.20,
    "high": 0.30,
    "premium": 0.35,
}

def get_bracket(income):
    """Return the tax bracket name for a given income."""
    if income < 25000:
        return "low"
    elif income < 50000:
        return "medium"
    elif income < 100000:
        return "high"
    else:
        return "premium"


def compute_net_income(gross_income):
    """Compute net income after tax deduction."""
    bracket = get_bracket(gross_income)
    rate = BRACKETS[bracket]
    tax = calculate_tax(gross_income, rate)
    return gross_income - tax


def format_currency(amount):
    """Format a number as USD currency string."""
    return f"${amount:,.2f}"


if __name__ == "__main__":
    sample_incomes = [18000, 35000, 72000, 150000]
    for inc in sample_incomes:
        net = compute_net_income(inc)
        bracket = get_bracket(inc)
        print(f"Gross: {format_currency(inc)} | Bracket: {bracket} | Net: {format_currency(net)}")
'''

    os.makedirs(WORKDIR, exist_ok=True)
    with open(OUTPUT, 'w') as f:
        f.write(content)
    print(f'Initial file created: {OUTPUT}')

    # Verify line counts
    with open(OUTPUT, 'r') as f:
        lines = f.readlines()
    print(f'Total lines: {len(lines)}')
    print(f'Lines 3-8:')
    for i in range(2, 8):
        print(f'  {i+1}: {lines[i].rstrip()}')
    print(f'Line 20: {lines[19].rstrip()}')

    # Open VSCode with the file
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
