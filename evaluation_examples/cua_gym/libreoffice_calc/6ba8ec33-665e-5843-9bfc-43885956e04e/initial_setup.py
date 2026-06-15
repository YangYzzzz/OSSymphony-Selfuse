"""
Initial Setup: Blank invoice spreadsheet for freelance consulting business
Task ID: calc_gen_smallbiz_018
Domain: libreoffice_calc

Creates a blank workbook with a single sheet named 'Invoice'.
The agent task is to build the full invoice template from scratch.
"""

import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gen_smallbiz_018'
OUTPUT = f'{WORKDIR}/{TASK_ID}_initial.xlsx'


def create_initial():
    wb = openpyxl.Workbook()

    # Single sheet named 'Invoice' — completely blank
    ws = wb.active
    ws.title = 'Invoice'

    # No data, no formulas, no formatting — pure blank template
    # The agent must build the full invoice structure from scratch

    wb.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')
    print('Sheet: Invoice (blank)')


create_initial()
