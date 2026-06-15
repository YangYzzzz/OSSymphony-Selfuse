"""
Initial Setup: Multi-app task - Chrome + LibreOffice Calc
Task ID: osworld_multi_apps_scholar_to_calc_012
Domain: libreoffice_calc (multi-app)
Description: Create researchers.ods with headers only (no data rows),
             then open Chrome at DBLP and LibreOffice Calc with the file.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_scholar_to_calc_012'
OUTPUT_XLSX = f'{WORKDIR}/researchers.xlsx'
OUTPUT_ODS = f'{WORKDIR}/researchers.ods'


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
    import openpyxl
    from openpyxl.styles import Font

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Sheet1'

    # Row 1: Headers only — NO data rows (agent must look up and fill them from DBLP)
    headers = ['Name', 'Affiliation', 'First Year', 'Total Publications', 'Most Recent Paper', 'Career Length']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)

    # Set column widths for readability
    ws.column_dimensions['A'].width = 25  # Name
    ws.column_dimensions['B'].width = 35  # Affiliation
    ws.column_dimensions['C'].width = 14  # First Year
    ws.column_dimensions['D'].width = 22  # Total Publications
    ws.column_dimensions['E'].width = 60  # Most Recent Paper
    ws.column_dimensions['F'].width = 16  # Career Length

    # IMPORTANT: NO data rows, NO Career Length formulas, NO alternating colors
    # The agent must:
    #   1. Look up DBLP profiles for 4 researchers in Chrome
    #   2. Add 4 data rows to the spreadsheet
    #   3. Sort by First Year ascending
    #   4. Add Career Length formulas (=2024-C2 etc.)
    #   5. Apply alternating row background colors (light blue / white)

    # Save as xlsx first
    wb.save(OUTPUT_XLSX)
    print(f'Intermediate xlsx file created: {OUTPUT_XLSX}')

    # Convert xlsx to ods using LibreOffice headless
    # Kill existing LibreOffice instances first
    subprocess.run(['pkill', '-f', 'soffice'], capture_output=True)
    time.sleep(2.0)

    convert_env = os.environ.copy()
    convert_env['DISPLAY'] = ':0'
    result = subprocess.run(
        ['libreoffice', '--headless', '--convert-to', 'ods', '--outdir', WORKDIR, OUTPUT_XLSX],
        capture_output=True,
        text=True,
        env=convert_env,
        timeout=60
    )
    print(f'Conversion stdout: {result.stdout}')
    print(f'Conversion stderr: {result.stderr}')

    if os.path.exists(OUTPUT_ODS):
        print(f'ODS file created: {OUTPUT_ODS}')
        # Remove the intermediate xlsx
        os.remove(OUTPUT_XLSX)
        print(f'Removed intermediate xlsx: {OUTPUT_XLSX}')
    else:
        # Fallback: just rename xlsx to ods
        os.rename(OUTPUT_XLSX, OUTPUT_ODS)
        print(f'Fallback: renamed xlsx to ods: {OUTPUT_ODS}')

    # GUI-ready startup: open Chrome at DBLP, then LibreOffice Calc with the file
    time.sleep(1.0)

    # Launch Chrome at DBLP
    launch_gui('google-chrome "https://dblp.org"', delay_sec=2.0)

    # Launch LibreOffice Calc with the researchers.ods file
    launch_gui(f'libreoffice --calc "{OUTPUT_ODS}"', delay_sec=3.0)

    print('GUI_READY: launched Chrome (DBLP) and LibreOffice Calc with DISPLAY=:0')


create_initial()
