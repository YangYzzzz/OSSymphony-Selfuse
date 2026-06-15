"""
Initial Setup: NeurIPS Awards Spreadsheet - Pre-task state
Task ID: osworld_multi_apps_acl_awards_calc_007
Domain: libreoffice_calc

Creates neurips_awards.ods with headers only (Year, Paper Title, Authors, Award Category).
No data rows are present — the agent must research and add NeurIPS 2021/2022 award papers.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_acl_awards_calc_007'
# The task uses .ods format — create via LibreOffice conversion
XLSX_TEMP = f'{WORKDIR}/{TASK_ID}_temp.xlsx'
OUTPUT = f'{WORKDIR}/neurips_awards.ods'


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


def run_cmd(command: str) -> str:
    """Run a shell command and return stdout."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()


def create_initial():
    import openpyxl

    # Create workbook with headers only — no data rows
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'NeurIPS Awards'

    # Headers: Year, Paper Title, Authors, Award Category
    headers = ['Year', 'Paper Title', 'Authors', 'Award Category']
    for col, header in enumerate(headers, 1):
        ws.cell(row=1, column=col, value=header)

    # Column widths for readability
    ws.column_dimensions['A'].width = 8    # Year
    ws.column_dimensions['B'].width = 60   # Paper Title
    ws.column_dimensions['C'].width = 40   # Authors
    ws.column_dimensions['D'].width = 30   # Award Category

    # Save as xlsx temporarily
    wb.save(XLSX_TEMP)
    print(f'Temp XLSX created: {XLSX_TEMP}')

    # Convert xlsx to ods using LibreOffice headless
    convert_cmd = (
        f'libreoffice --headless --convert-to ods --outdir "{WORKDIR}" "{XLSX_TEMP}"'
    )
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    proc = subprocess.run(
        shlex.split(convert_cmd),
        capture_output=True,
        text=True,
        env=env,
        timeout=60,
    )
    print(f'Conversion stdout: {proc.stdout}')
    print(f'Conversion stderr: {proc.stderr}')

    # LibreOffice converts and names output based on input filename
    converted_path = f'{WORKDIR}/{TASK_ID}_temp.ods'
    if os.path.exists(converted_path):
        os.rename(converted_path, OUTPUT)
        print(f'Renamed to: {OUTPUT}')
    else:
        # Fallback: check if it was directly created
        if os.path.exists(OUTPUT):
            print(f'ODS file already at: {OUTPUT}')
        else:
            print(f'ERROR: Conversion failed, converted_path={converted_path}')

    # Clean up temp xlsx
    if os.path.exists(XLSX_TEMP):
        os.remove(XLSX_TEMP)
        print(f'Removed temp file: {XLSX_TEMP}')

    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open Chrome first, then LibreOffice Calc with the ods file
    # The task requires Chrome to be open for looking up NeurIPS award papers
    launch_gui('google-chrome --new-window', delay_sec=2.0)
    launch_gui(f'libreoffice --calc "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Chrome and LibreOffice Calc with DISPLAY=:0')


create_initial()
