"""
Initial Setup: Create finance directory for purchase order task
Task ID: pdf_fin_079
Domain: pdf

The agent must create a purchase order PDF using reportlab.
Initial state: /home/user/finance/ directory exists, no PO file yet.
A terminal is open for the agent to write and run Python code.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_079'
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
    # Create the finance directory
    os.makedirs(FINANCE_DIR, exist_ok=True)
    print(f'Finance directory created: {FINANCE_DIR}')

    # Create a small helper reference file so the directory isn't empty
    # and the agent has context about what POs look like
    ref_path = os.path.join(FINANCE_DIR, 'po_template_notes.txt')
    with open(ref_path, 'w') as f:
        f.write("Purchase Order Template Notes\n")
        f.write("=" * 40 + "\n\n")
        f.write("Standard PO format for MidWest Manufacturing Inc.\n\n")
        f.write("Required fields:\n")
        f.write("  - Company name and address\n")
        f.write("  - PO number and date\n")
        f.write("  - Vendor information\n")
        f.write("  - Ship-to address\n")
        f.write("  - Line items (description, qty, unit price, extended price)\n")
        f.write("  - Subtotal, shipping, tax, total\n")
        f.write("  - Payment terms\n\n")
        f.write("Use reportlab for PDF generation.\n")
    print(f'Reference file created: {ref_path}')

    # Ensure no PO PDF exists (clean state)
    po_path = os.path.join(FINANCE_DIR, 'po_2024_0089.pdf')
    if os.path.exists(po_path):
        os.remove(po_path)
        print(f'Removed existing PO file: {po_path}')

    # Open a terminal for the agent to write code
    launch_gui('bash -c "cd /home/user/finance && xterm -geometry 120x40+50+50 -e bash"', delay_sec=1.5)

    # Also open the file manager to show the finance directory
    launch_gui(f'nautilus "{FINANCE_DIR}"', delay_sec=2.0)

    print('GUI_READY: launched terminal and file manager with DISPLAY=:0')

create_initial()
