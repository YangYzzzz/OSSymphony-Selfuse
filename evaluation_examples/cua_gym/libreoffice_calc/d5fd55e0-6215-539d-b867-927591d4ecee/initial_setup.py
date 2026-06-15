"""
Initial Setup: Create llm_jan2024.ods with header row only (no paper data yet).
Task ID: osworld_multi_apps_arxiv_llms_calc_005
Domain: libreoffice_calc (multi-app: Chrome + LibreOffice Calc)

The agent must browse arxiv.org cs.CL January 2024 papers, find 10 LLM/language model
papers, and add them to this spreadsheet.
"""

import os
import shlex
import subprocess
import time
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_arxiv_llms_calc_005'
OUTPUT = f'{WORKDIR}/llm_jan2024.ods'


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
    # Create a new workbook with just a header row
    wb = openpyxl.Workbook()

    ws = wb.active
    ws.title = 'Sheet1'

    # Write the header row exactly as specified in the task
    headers = ['arXiv ID', 'Title', 'Authors']
    for col, header in enumerate(headers, 1):
        ws.cell(row=1, column=col, value=header)

    # Set column widths for readability
    ws.column_dimensions['A'].width = 18   # arXiv ID like 2401.12345
    ws.column_dimensions['B'].width = 60   # Title (long text)
    ws.column_dimensions['C'].width = 40   # Authors

    # NO data rows — agent must fill them in from arxiv browsing
    # This is the critical constraint: row 2 onwards must be empty

    # Save as .ods format (LibreOffice native format)
    wb.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup:
    # 1. Open Chrome (for browsing arxiv.org)
    launch_gui('google-chrome "https://arxiv.org/list/cs.CL/2024-01"', delay_sec=3.0)

    # 2. Open LibreOffice Calc with the spreadsheet
    launch_gui(f'libreoffice --calc "{OUTPUT}"', delay_sec=2.0)

    print('GUI_READY: launched Chrome and LibreOffice Calc with DISPLAY=:0')


create_initial()
