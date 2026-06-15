"""
Initial Setup: Monthly Expense Report Template (blank initial state)
Task ID: calc_gen_template_037
Domain: libreoffice_calc

Creates a blank spreadsheet with a single sheet named 'ExpenseReport'.
The agent task is to build the full template from this blank state.
"""

import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gen_template_037'
OUTPUT = f'{WORKDIR}/{TASK_ID}_initial.xlsx'


def create_initial():
    wb = openpyxl.Workbook()

    # Single sheet named 'ExpenseReport' — blank, ready for the agent to build
    ws = wb.active
    ws.title = 'ExpenseReport'

    # No content — the task is to build the entire template from scratch
    wb.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')
    print('Sheet: ExpenseReport (blank)')


create_initial()
