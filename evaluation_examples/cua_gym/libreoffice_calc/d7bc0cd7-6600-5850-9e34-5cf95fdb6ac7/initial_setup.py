"""
Initial Setup: Prepare environment for bank reconciliation PDF creation task.
Task ID: pdf_fin_055
Domain: pdf (reportlab)

Creates the /home/user/finance/ directory with some context files,
installs reportlab, and opens a terminal + file manager so the agent
can begin work.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
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
    # 1. Create the finance directory
    os.makedirs(FINANCE_DIR, exist_ok=True)

    # 2. Place a reference text file with the reconciliation data
    #    (this gives the agent the raw data to work from)
    reference_data = """BANK RECONCILIATION DATA - MARCH 2025
=====================================

Prepared by: Accounting Department
Date: March 31, 2025

BANK SIDE:
-----------
Bank Statement Balance (per bank statement): $45,230.15

Deposits in Transit (not yet recorded by bank):
  1. Mar 29 - Customer payment (Acme Corp)         $3,200.00
  2. Mar 30 - Online transfer (GlobalTech Inc)      $2,800.00
  3. Mar 31 - Cash deposit (Retail Sales)           $2,500.00
  Total Deposits in Transit:                        $8,500.00

Outstanding Checks (issued but not yet cleared):
  Check #4521 - Mar 15 - Office Supplies Co         $1,245.00
  Check #4523 - Mar 20 - Utility Payment             $890.50
  Check #4525 - Mar 22 - Insurance Premium          $1,500.00
  Check #4527 - Mar 25 - Vendor Payment (DataServ)  $1,235.00
  Check #4529 - Mar 28 - Employee Reimbursement     $1,250.00
  Total Outstanding Checks:                         $6,120.50

Adjusted Bank Balance: $47,609.65

BOOK SIDE:
-----------
Book Balance (per company records): $48,109.65

Less: Bank Fees (monthly service charge):      $50.00
Less: NSF Check (returned - Johnson & Co):    $450.00

Adjusted Book Balance: $47,609.65

RECONCILIATION STATUS: BALANCED
Both adjusted balances equal $47,609.65
"""
    with open(os.path.join(FINANCE_DIR, 'reconciliation_data.txt'), 'w') as f:
        f.write(reference_data)

    # 3. Place a brief instruction note
    instructions = """TASK: Create a bank reconciliation report PDF

Output file: /home/user/finance/bank_recon_march.pdf
Tool to use: reportlab (Python library)

Use the data in reconciliation_data.txt to create a properly
formatted bank reconciliation PDF report.
"""
    with open(os.path.join(FINANCE_DIR, 'instructions.txt'), 'w') as f:
        f.write(instructions)

    # 4. Install reportlab
    subprocess.run(['pip3', 'install', 'reportlab'], capture_output=True)

    print(f'Initial environment created: {FINANCE_DIR}')
    print(f'  - reconciliation_data.txt (raw data)')
    print(f'  - instructions.txt (task brief)')

    # 5. GUI-ready startup: open file manager
    launch_gui(f'nautilus "{FINANCE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched file manager with DISPLAY=:0')

create_initial()
