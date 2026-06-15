"""
Initial Setup: Professional Invoice Template (blank initial state)
Task ID: calc_fin_invoice_template_016
Domain: libreoffice_calc

Creates a blank Invoice sheet — the initial state before the agent acts.
The sheet has a single 'Invoice' sheet with no content, formulas, or formatting.
"""

import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_fin_invoice_template_016'
OUTPUT = f'{WORKDIR}/{TASK_ID}_initial.xlsx'


def create_initial():
    wb = openpyxl.Workbook()

    # Single blank sheet named 'Invoice'
    ws = wb.active
    ws.title = 'Invoice'

    # Sheet is completely blank — no data, no formatting, no protection

    wb.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')


create_initial()
