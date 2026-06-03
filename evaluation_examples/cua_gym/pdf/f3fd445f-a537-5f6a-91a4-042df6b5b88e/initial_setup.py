"""
Initial Setup: Create directory structure for financial ratio analysis PDF task.
Task ID: pdf_fin_081
Domain: pdf

The agent's task is to CREATE a financial ratio analysis PDF from scratch.
Initial state: /home/user/finance/ directory exists, empty. A text file with
the raw ratio data is provided so the agent has reference material.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_081'
FINANCE_DIR = f'{WORKDIR}/finance'

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
    # Ensure finance directory exists
    os.makedirs(FINANCE_DIR, exist_ok=True)

    # Create a reference data file with the raw ratios the agent should use
    data_file = f'{FINANCE_DIR}/ratio_data_2023.txt'
    with open(data_file, 'w') as f:
        f.write("Meridian Corp - Financial Ratio Analysis Data (FY 2023)\n")
        f.write("=" * 60 + "\n\n")
        f.write("LIQUIDITY RATIOS\n")
        f.write("-" * 40 + "\n")
        f.write("Current Ratio:        2.10\n")
        f.write("Quick Ratio:          1.50\n")
        f.write("Cash Ratio:           0.80\n\n")
        f.write("PROFITABILITY RATIOS\n")
        f.write("-" * 40 + "\n")
        f.write("Gross Margin:         42%\n")
        f.write("Operating Margin:     18%\n")
        f.write("Net Margin:           12%\n")
        f.write("ROE:                  15%\n")
        f.write("ROA:                  8%\n\n")
        f.write("LEVERAGE RATIOS\n")
        f.write("-" * 40 + "\n")
        f.write("Debt-to-Equity:       0.65\n")
        f.write("Interest Coverage:    8.20\n\n")
        f.write("EFFICIENCY RATIOS\n")
        f.write("-" * 40 + "\n")
        f.write("Inventory Turnover:   6.50\n")
        f.write("AR Turnover:          9.20\n")
        f.write("AP Turnover:          7.80\n\n")
        f.write("Notes: Benchmarks are industry averages for mid-cap manufacturing.\n")
        f.write("Green = above benchmark, Red = below benchmark.\n")

    print(f'Initial directory created: {FINANCE_DIR}')
    print(f'Reference data file created: {data_file}')

    # Open a terminal in the finance directory so the agent can work
    launch_gui('bash -c "cd /home/user/finance && xterm"', delay_sec=1.0)
    # Also open the text file for reference
    launch_gui(f'xdg-open {data_file}', delay_sec=2.0)
    print('GUI_READY: launched required app(s) with DISPLAY=:0')

create_initial()
