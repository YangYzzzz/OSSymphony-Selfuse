"""
Initial Setup: ACL Awards Spreadsheet - Initial State
Task ID: osworld_multi_apps_acl_awards_calc_002
Domain: libreoffice_calc

Creates awards.ods with headers only (Year, Conference, Paper Title, Authors, Award Type).
The agent must add 4 award entries and apply a filter.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_acl_awards_calc_002'
OUTPUT = f'{WORKDIR}/awards.ods'


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
    # Create the ODS file using a Python script with ezodf
    # We build a spreadsheet with only the header row (no data rows)
    # The agent must add the 4 award entries

    create_script = r'''
import ezodf

# Create a new ODS spreadsheet
doc = ezodf.newdoc(doctype='ods', filename='/home/user/awards.ods')
sheet = doc.sheets[0]
sheet.name = 'Awards'

# Resize to accommodate header + potential data rows
sheet.reset(size=(20, 5))

# Set column headers in Row 0 (0-indexed)
headers = ['Year', 'Conference', 'Paper Title', 'Authors', 'Award Type']
for col_idx, header in enumerate(headers):
    sheet[0, col_idx].set_value(header)

# Save the document
doc.save()
print(f'Initial ODS file created: /home/user/awards.ods')
'''

    # Write the inner script to a temp location and run it
    import subprocess
    result = subprocess.run(
        ['python3', '-c', create_script],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f'ezodf script error: {result.stderr}')
        # Fallback: use LibreOffice macro approach via CSV conversion
        import csv
        csv_path = '/tmp/awards_initial.csv'
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Year', 'Conference', 'Paper Title', 'Authors', 'Award Type'])

        # Convert CSV to ODS using LibreOffice headless
        env = os.environ.copy()
        env['DISPLAY'] = ':0'
        conv_result = subprocess.run(
            ['libreoffice', '--headless', '--convert-to', 'ods', '--outdir', WORKDIR, csv_path],
            capture_output=True, text=True, env=env, timeout=30
        )
        print(f'LibreOffice conversion stdout: {conv_result.stdout}')
        print(f'LibreOffice conversion stderr: {conv_result.stderr}')
        # The converted file will be named awards_initial.ods; rename it
        import shutil
        converted = '/home/user/awards_initial.ods'
        if os.path.exists(converted):
            shutil.move(converted, OUTPUT)
            print(f'Renamed {converted} -> {OUTPUT}')
        elif not os.path.exists(OUTPUT):
            print('ERROR: Could not create awards.ods')
            raise RuntimeError('Failed to create awards.ods')
    else:
        print(result.stdout)

    # Verify file exists
    if os.path.exists(OUTPUT):
        print(f'Verified: {OUTPUT} exists (size={os.path.getsize(OUTPUT)} bytes)')
    else:
        raise RuntimeError(f'File not found after creation: {OUTPUT}')

    # GUI-ready startup: open awards.ods in LibreOffice Calc
    launch_gui(f'libreoffice --calc "{OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Calc with awards.ods using DISPLAY=:0')


create_initial()
